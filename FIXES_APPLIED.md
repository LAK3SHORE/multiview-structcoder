# StructCoder Preprocessing Fix Summary

## Issues Fixed

### 1. Tree-Sitter Version Incompatibility (FIXED ✅)
**Problem**: The notebook was failing with `ValueError: Incompatible Language version 15. Must be between 13 and 14`

**Root Cause**:
- The tree-sitter Python library (v0.20.4) only supported Language versions 13-14
- The compiled tree-sitter language grammars in `parser/vendor/` had been updated to newer versions that produce Language version 15

**Solution**:
1. Upgraded tree-sitter from v0.20.4 to v0.21.3 (supports Language version 14)
2. Checked out compatible versions of the language grammars:
   - tree-sitter-python: v0.20.4
   - tree-sitter-c-sharp: dd5e597
   - tree-sitter-go: 05900fa
   - tree-sitter-javascript: 4a95461
3. Rebuilt the parser library with `parser/build_tree_sitter.py`

### 2. Testing Infrastructure
**Added**:
- `test_preprocessing.py` - Comprehensive test of all preprocessing components
- `run_preprocessing_small_test.py` - Small-scale test (50 examples) to verify the pipeline works

## Current Status

✅ All preprocessing components working:
- Java parser
- C# parser
- Python parser
- Go parser
- JavaScript parser
- Ruby parser
- CodeT5 tokenizer
- Dataset loading from HuggingFace

⚠️ PHP parser still has version incompatibility (not needed for current tasks)

### 2. Concode Dataset FileNotFoundError (FIXED ✅)
**Problem**: The "CodeXGLUE generation" section was failing with `FileNotFoundError: [Errno 2] No such file or directory: '../datasets/concode/train.json'`

**Root Cause**:
- The notebook expected local Concode JSON files to be downloaded manually
- Files were not present on the system

**Solution**:
- Modified the `read_examples()` function in the Concode section (cell id: `695bf2a3`)
- Changed from reading local JSON files to using HuggingFace datasets
- Now loads from `google/code_x_glue_tc_text_to_code` dataset automatically
- Consistent with the translation section approach

**Changes Made**:
- Replaced file reading with `load_dataset('google/code_x_glue_tc_text_to_code', split=split)`
- Updated split name mapping: 'dev' → 'validation' to match HuggingFace naming
- Kept all data validation and assertions intact

## Current Status - All Preprocessing Sections

| Section | Status | Dataset | Notes |
|---------|--------|---------|-------|
| CodeXGLUE translation (Java↔C#) | ✅ Working | Already preprocessed (634 MB) | Ready to use |
| CodeXGLUE generation (Concode) | ✅ Fixed | Auto-downloads from HuggingFace (~42 MB) | 100k train, 2k val, 2k test |
| APPS generation | ❓ Not tested yet | HuggingFace `codeparrot/apps` | Should work as-is |

## How to Use

### Quick Test
Run the test script to verify everything works:
```bash
cd /Users/cris/Desktop/StructCoder
.venv/bin/python test_preprocessing.py
```

### Small Scale Test
Test the full pipeline on 50 examples:
```bash
cd /Users/cris/Desktop/StructCoder
.venv/bin/python run_preprocessing_small_test.py
```

### Test Concode Dataset
Test the Concode (text-to-code) dataset loading:
```bash
cd /Users/cris/Desktop/StructCoder
.venv/bin/python test_concode_small.py
```

### Run Full Preprocessing
Open [finetune_preprocess.ipynb](finetune_preprocess.ipynb) in Jupyter and run the cells.

**For the Concode section:**
- First run will download ~42 MB from HuggingFace (automatic)
- Processing 100k training examples may take 10-15 minutes
- Optional: Test with a smaller subset first by modifying the cell:
  ```python
  dataset = load_dataset('google/code_x_glue_tc_text_to_code', split='train[:100]')
  ```

**Note**: The full preprocessing for each task will:

**Translation (Java↔C#):**
- Already complete! Data ready in `data/codexglue_translation/`

**Generation (Concode):**
- Process 100,000 training examples
- Process 2,000 validation examples
- Process 2,000 test examples
- Save preprocessed data to `data/codexglue_generation/`

**APPS:**
- Process training examples with solutions
- Process test examples
- Save preprocessed data to `data/apps_generation/`

## Technical Details

### Dependencies
- Python 3.10.17 (in .venv)
- tree-sitter 0.21.3
- transformers (for CodeT5 tokenizer)
- datasets (for HuggingFace dataset loading)

### Data Directory Structure
```
data/
└── codexglue_translation/
    ├── preprocessed_data_by_split.pkl
    └── all_node_types.pkl
```

### Parser Files
- `parser/my-languages2.so` - Compiled tree-sitter language library
- Compatible with tree-sitter 0.21.3
- Includes: Java, C#, Python, Go, JavaScript, Ruby, PHP

## Warnings (Expected)
You may see these warnings when running - they are normal:
- `FutureWarning: Language(path, name) is deprecated` - Tree-sitter API deprecation notice
- `FutureWarning: resume_download is deprecated` - HuggingFace Hub deprecation notice

These warnings don't affect functionality.

## Next Steps

You can now proceed with:
1. Running the full preprocessing notebook
2. Training the model with the preprocessed data
3. Testing the model on the evaluation sets

For training commands, see the main [README.md](README.md).
