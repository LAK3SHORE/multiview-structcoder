#!/usr/bin/env python
"""Test the Concode preprocessing with a small subset to verify the HuggingFace dataset works."""

import sys
import os

# Clean tree_sitter module
if 'tree_sitter' in sys.modules:
    del sys.modules['tree_sitter']

from datasets import load_dataset
import pandas as pd
from transformers import RobertaTokenizer
from tree_sitter import Language, Parser
from parser import DFG_java, remove_comments_and_docstrings

print("=" * 70)
print("Testing Concode Dataset Loading from HuggingFace")
print("=" * 70)

# Test the updated read_examples function
def read_examples(split, max_examples=None):
    # Map split names to HuggingFace naming convention
    if split in ['valid', 'validation']:
        split='validation'

    # Load from HuggingFace
    if max_examples:
        dataset = load_dataset('google/code_x_glue_tc_text_to_code', split=f'{split}[:{max_examples}]')
    else:
        dataset = load_dataset('google/code_x_glue_tc_text_to_code', split=split)

    examples = []
    for idx, example in enumerate(dataset):
        nl = example['nl'].strip()
        code = example['code'].strip()
        assert (code == remove_comments_and_docstrings(code, 'java'))
        assert ('\n' not in code)
        examples.append([idx, nl, code])

    print(f'Loaded {len(examples)} examples from {split} split')
    return pd.DataFrame(examples, columns=['id', 'nl', 'java'])

# Test with just 10 examples
print("\n[1/3] Testing dataset loading with 10 examples...")
try:
    data = read_examples('train', max_examples=10)
    print(f"✅ Successfully loaded {len(data)} examples")
    print(f"   Columns: {list(data.columns)}")
    print(f"   Sample NL: {data['nl'].iloc[0][:80]}...")
    print(f"   Sample code: {data['java'].iloc[0][:80]}...")
except Exception as e:
    print(f"❌ Failed to load dataset: {e}")
    sys.exit(1)

# Test tokenization
print("\n[2/3] Testing tokenization...")
try:
    tokenizer = RobertaTokenizer.from_pretrained('Salesforce/codet5-base')
    nl_tokens = tokenizer(list(data['nl'])).input_ids
    code_tokens = tokenizer(list(data['java'])).input_ids
    print(f"✅ Tokenization successful")
    print(f"   Avg NL tokens: {sum(len(t) for t in nl_tokens)/len(nl_tokens):.1f}")
    print(f"   Avg code tokens: {sum(len(t) for t in code_tokens)/len(code_tokens):.1f}")
except Exception as e:
    print(f"❌ Tokenization failed: {e}")
    sys.exit(1)

# Test parsing
print("\n[3/3] Testing Java code parsing...")
try:
    LANGUAGE = Language('parser/my-languages2.so', 'java')
    parser = Parser()
    parser.set_language(LANGUAGE)

    test_code = data['java'].iloc[0]
    tree = parser.parse(bytes(test_code, 'utf8'))
    root = tree.root_node
    print(f"✅ Parsing successful")
    print(f"   Sample code parsed with {root.child_count} top-level nodes")
except Exception as e:
    print(f"❌ Parsing failed: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("✅ All tests passed! The Concode section should work now.")
print("=" * 70)
print("\nNext steps:")
print("1. Open finetune_preprocess.ipynb in Jupyter")
print("2. Run the 'CodeXGLUE generation' cell")
print("3. The dataset will be downloaded automatically (~42 MB)")
print("4. Processing 100k examples may take 10-15 minutes")
print("\nOptional: To test with a smaller subset first, modify the cell to use:")
print("  dataset = load_dataset('google/code_x_glue_tc_text_to_code', split='train[:100]')")
