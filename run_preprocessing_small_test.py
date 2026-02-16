#!/usr/bin/env python
"""Small test to verify the preprocessing pipeline works on a subset of data."""

import sys
import os
import pickle

# Clean tree_sitter module to avoid version conflicts
if 'tree_sitter' in sys.modules:
    del sys.modules['tree_sitter']

from datasets import load_dataset
import pandas as pd
from tqdm import tqdm
from transformers import RobertaTokenizer
import numpy as np
from parser import DFG_java, DFG_csharp, DFG_python
from parser import (remove_comments_and_docstrings,
                   tree_to_token_index,
                   index_to_code_token,
                   tree_to_variable_index,
                   detokenize_code, tree_to_token_nodes)
from tree_sitter import Language, Parser

# Import all the functions from the notebook
def read_examples(split='train', max_examples=None):
    if (split=='valid') or (split=='dev'):
        split='validation'

    dataset = load_dataset('code_x_glue_cc_code_to_code_trans', split=split)
    if max_examples:
        dataset = dataset.select(range(min(max_examples, len(dataset))))

    examples = []
    for example in dataset:
        examples.append({
            'id': example['id'],
            'java': example['java'],
            'cs': example['cs']
        })

    print(f'Loaded {len(examples)} examples from {split} split')
    return pd.DataFrame(examples)

def get_tokenizer_chars(tokenizer):
    tokenizer_chars = []
    for i in range(tokenizer.vocab_size):
        token = tokenizer.decode(i)
        if len(token)==1:
            tokenizer_chars.append(token)
    tokenizer_chars = [c for c in tokenizer_chars if c!='�']
    return tokenizer_chars

def tokenize_codes_texts(texts, batch_size=1024):
    tokenizer = RobertaTokenizer.from_pretrained('Salesforce/codet5-base')
    tokenizer_chars = get_tokenizer_chars(tokenizer)
    texts = [''.join(filter(lambda c:c in tokenizer_chars, text)) for text in texts]
    N = len(texts)
    tokenized_texts = []
    for start in range(0, len(texts), batch_size):
        tokenized_texts += tokenizer(texts[start:start+batch_size]).input_ids
    return tokenized_texts

def extract_structure(code, parser):
    tree = parser[0].parse(bytes(code,'utf8'))
    root_node = tree.root_node
    ast_token_nodes = tree_to_token_nodes(root_node)

    tokens_index = [(node.start_point, node.end_point) for node in ast_token_nodes]
    code=code.split('\n')
    code_tokens=[index_to_code_token(x,code) for x in tokens_index]
    index_to_code={index:(idx,code_) for idx,(index,code_) in enumerate(zip(tokens_index,code_tokens))}
    try:
        DFG,_ = parser[1](root_node,index_to_code,{})
    except:
        DFG = []
    for d in DFG:
        assert (d[2]=='comesFrom' or d[2]=='computedFrom')
    DFG = [(d[1], d[4]) for d in DFG if (len(d[4])>0)]
    return code_tokens, ast_token_nodes, DFG

def add_structure(data, lang):
    LANGUAGE = Language('parser/my-languages2.so', 'c_sharp' if lang=='cs' else lang)
    parser = Parser()
    parser.set_language(LANGUAGE)
    dfg_function={'python':DFG_python, 'java':DFG_java, 'cs':DFG_csharp, 'c_sharp':DFG_csharp}
    parser = [parser, dfg_function[lang]]

    ast_leaf_tokens, ast_leaves, dfg_edges = [], [], []
    for code in tqdm(data[lang], desc=f"Processing {lang}"):
        curr_code_tokens, curr_ast_leaves, curr_dfg_edges = extract_structure(code, parser)
        ast_leaf_tokens.append(curr_code_tokens)
        ast_leaves.append(curr_ast_leaves)
        dfg_edges.append(curr_dfg_edges)

    data[lang+'_ast_leaves'] = ast_leaves
    data[lang+'_dfg_edges'] = dfg_edges
    data[lang+'_ast_leaf_tokens'] = ast_leaf_tokens

    print(f'✅ Processed {len(data)} {lang} examples')
    print(f'   # samples with failed/empty DFG: {(data[lang+"_dfg_edges"].apply(len)==0).sum()}')

if __name__ == "__main__":
    print("=" * 70)
    print("Running Small Preprocessing Test (50 examples)")
    print("=" * 70)

    # Test with just 50 examples from train
    data = read_examples('train', max_examples=50)

    print("\nProcessing Java code...")
    add_structure(data, 'java')
    data['java_tokens'] = tokenize_codes_texts(list(data['java']))
    print(f"Java tokenization complete: avg {data['java_tokens'].apply(len).mean():.1f} tokens")

    print("\nProcessing C# code...")
    add_structure(data, 'cs')
    data['cs_tokens'] = tokenize_codes_texts(list(data['cs']))
    print(f"C# tokenization complete: avg {data['cs_tokens'].apply(len).mean():.1f} tokens")

    print("\n" + "=" * 70)
    print("✅ Small test completed successfully!")
    print("=" * 70)
    print("\nThe preprocessing pipeline is working correctly.")
    print("You can now run the full preprocessing in the notebook.")
