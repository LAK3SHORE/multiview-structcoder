#!/usr/bin/env python
"""Test script to verify the preprocessing pipeline works correctly."""

import sys
import os

# Ensure parser directory is accessible
sys.path.insert(0, os.path.dirname(__file__))

# Clean tree_sitter module to avoid version conflicts
if 'tree_sitter' in sys.modules:
    del sys.modules['tree_sitter']

from datasets import load_dataset
import pandas as pd
from transformers import RobertaTokenizer
from tree_sitter import Language, Parser
from parser import DFG_java, DFG_csharp

print("=" * 60)
print("Testing StructCoder Preprocessing Pipeline")
print("=" * 60)

# Test 1: Load a small sample dataset
print("\n[1/4] Testing dataset loading...")
try:
    dataset = load_dataset('code_x_glue_cc_code_to_code_trans', split='train[:10]')
    print(f"✅ Loaded {len(dataset)} examples successfully")
except Exception as e:
    print(f"❌ Failed to load dataset: {e}")
    sys.exit(1)

# Test 2: Test parsers
print("\n[2/4] Testing tree-sitter parsers...")
try:
    for lang in ['java', 'c_sharp']:
        LANGUAGE = Language('parser/my-languages2.so', 'c_sharp' if lang == 'c_sharp' else lang)
        parser = Parser()
        parser.set_language(LANGUAGE)
        print(f"✅ {lang} parser loaded successfully")
except Exception as e:
    print(f"❌ Failed to load parser: {e}")
    sys.exit(1)

# Test 3: Test tokenizer
print("\n[3/4] Testing CodeT5 tokenizer...")
try:
    tokenizer = RobertaTokenizer.from_pretrained('Salesforce/codet5-base')
    test_code = "public class Test { }"
    tokens = tokenizer(test_code).input_ids
    print(f"✅ Tokenizer loaded successfully (tokenized to {len(tokens)} tokens)")
except Exception as e:
    print(f"❌ Failed to load tokenizer: {e}")
    sys.exit(1)

# Test 4: Test parsing a simple Java code
print("\n[4/4] Testing code parsing...")
try:
    LANGUAGE = Language('parser/my-languages2.so', 'java')
    parser = Parser()
    parser.set_language(LANGUAGE)

    test_code = "public class HelloWorld { public static void main(String[] args) { System.out.println(\"Hello\"); } }"
    tree = parser.parse(bytes(test_code, 'utf8'))
    root = tree.root_node
    print(f"✅ Successfully parsed Java code (AST has {root.child_count} top-level nodes)")
except Exception as e:
    print(f"❌ Failed to parse code: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ All preprocessing components are working correctly!")
print("=" * 60)
print("\nYou can now run the finetune_preprocess.ipynb notebook.")
print("Note: Processing the full dataset will take some time.")
