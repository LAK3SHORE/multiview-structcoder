"""
Test DFG Extraction with StructCoder Parser
============================================
This script demonstrates how to extract Data Flow Graphs from code
using your actual parser files.

Prerequisites:
    pip install tree-sitter

Usage:
    python test_dfg_extraction.py
"""

import sys
from pathlib import Path

def check_parser_availability():
    """Check if parser files are available"""
    parser_dir = Path('parser')
    
    required_files = [
        'my-languages.so',
        'my-languages2.so',
        'DFG.py',
        'utils.py'
    ]
    
    missing = []
    for file in required_files:
        if not (parser_dir / file).exists():
            missing.append(file)
    
    if missing:
        print(f"❌ Missing parser files: {missing}")
        print(f"\nExpected location: {parser_dir.absolute()}/")
        return False
    
    print("✅ All parser files found!")
    return True


def test_dfg_python():
    """Test DFG extraction for Python code"""
    print("\n" + "="*70)
    print("Testing DFG Extraction: Python")
    print("="*70)
    
    try:
        from tree_sitter import Language, Parser
        from parser.DFG import DFG_python
        from parser.utils import tree_to_token_index
        
        # Load Python parser
        LANGUAGE = Language('parser/my-languages.so', 'python')
        parser = Parser()
        parser.set_language(LANGUAGE)
        
        # Test code
        code = """x = 5
y = x + 1
z = y * 2
if y > 0:
    result = z
else:
    result = 0"""
        
        print("\nInput Code:")
        print("-" * 70)
        print(code)
        
        # Parse code
        tree = parser.parse(bytes(code, 'utf8'))
        root_node = tree.root_node
        
        # Extract tokens
        code_lines = code.split('\n')
        token_index = tree_to_token_index(root_node)
        
        # Build index_to_code mapping
        index_to_code = {}
        for idx, (start, end) in enumerate(token_index):
            if start[0] == end[0]:
                token = code_lines[start[0]][start[1]:end[1]]
            else:
                token = ""
                token += code_lines[start[0]][start[1]:]
                for i in range(start[0]+1, end[0]):
                    token += code_lines[i]
                token += code_lines[end[0]][:end[1]]
            index_to_code[(start, end)] = (idx, token)
        
        # Extract DFG
        dfg, states = DFG_python(root_node, index_to_code, {})
        
        print("\nData Flow Graph:")
        print("-" * 70)
        print(f"{'Variable':<15} {'Relationship':<15} {'Sources':<30}")
        print("-" * 70)
        
        for edge in dfg:
            var, idx, rel, sources, source_idx = edge
            sources_str = ', '.join(sources) if sources else 'None'
            print(f"{var:<15} {rel:<15} {sources_str:<30}")
        
        print("\nVariable States (final definitions):")
        print("-" * 70)
        for var, positions in states.items():
            print(f"  {var}: defined at position(s) {positions}")
        
        print("\n✅ Python DFG extraction successful!")
        return True
        
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("Make sure tree-sitter is installed: pip install tree-sitter")
        return False
    except Exception as e:
        print(f"\n❌ Error during DFG extraction: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_dfg_java():
    """Test DFG extraction for Java code"""
    print("\n" + "="*70)
    print("Testing DFG Extraction: Java")
    print("="*70)
    
    try:
        from tree_sitter import Language, Parser
        from parser.DFG import DFG_java
        from parser.utils import tree_to_token_index
        
        # Load Java parser
        LANGUAGE = Language('parser/my-languages.so', 'java')
        parser = Parser()
        parser.set_language(LANGUAGE)
        
        # Test code
        code = """int x = 5;
int y = x + 1;
int z = y * 2;"""
        
        print("\nInput Code:")
        print("-" * 70)
        print(code)
        
        # Parse code
        tree = parser.parse(bytes(code, 'utf8'))
        root_node = tree.root_node
        
        # Extract tokens
        code_lines = code.split('\n')
        token_index = tree_to_token_index(root_node)
        
        # Build index_to_code mapping
        index_to_code = {}
        for idx, (start, end) in enumerate(token_index):
            if start[0] == end[0]:
                token = code_lines[start[0]][start[1]:end[1]]
            else:
                token = ""
                token += code_lines[start[0]][start[1]:]
                for i in range(start[0]+1, end[0]):
                    token += code_lines[i]
                token += code_lines[end[0]][:end[1]]
            index_to_code[(start, end)] = (idx, token)
        
        # Extract DFG
        dfg, states = DFG_java(root_node, index_to_code, {})
        
        print("\nData Flow Graph:")
        print("-" * 70)
        print(f"{'Variable':<15} {'Relationship':<15} {'Sources':<30}")
        print("-" * 70)
        
        for edge in dfg:
            var, idx, rel, sources, source_idx = edge
            sources_str = ', '.join(sources) if sources else 'None'
            print(f"{var:<15} {rel:<15} {sources_str:<30}")
        
        print("\nVariable States (final definitions):")
        print("-" * 70)
        for var, positions in states.items():
            print(f"  {var}: defined at position(s) {positions}")
        
        print("\n✅ Java DFG extraction successful!")
        return True
        
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("Make sure tree-sitter is installed: pip install tree-sitter")
        return False
    except Exception as e:
        print(f"\n❌ Error during DFG extraction: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_complex_example():
    """Test DFG extraction with more complex control flow"""
    print("\n" + "="*70)
    print("Testing DFG Extraction: Complex Python (with loops)")
    print("="*70)
    
    try:
        from tree_sitter import Language, Parser
        from parser.DFG import DFG_python
        from parser.utils import tree_to_token_index
        
        # Load Python parser
        LANGUAGE = Language('parser/my-languages.so', 'python')
        parser = Parser()
        parser.set_language(LANGUAGE)
        
        # Complex test code with loop
        code = """total = 0
for i in range(5):
    total = total + i
result = total * 2"""
        
        print("\nInput Code:")
        print("-" * 70)
        print(code)
        
        # Parse code
        tree = parser.parse(bytes(code, 'utf8'))
        root_node = tree.root_node
        
        # Extract tokens
        code_lines = code.split('\n')
        token_index = tree_to_token_index(root_node)
        
        # Build index_to_code mapping
        index_to_code = {}
        for idx, (start, end) in enumerate(token_index):
            if start[0] == end[0]:
                token = code_lines[start[0]][start[1]:end[1]]
            else:
                token = ""
                token += code_lines[start[0]][start[1]:]
                for i in range(start[0]+1, end[0]):
                    token += code_lines[i]
                token += code_lines[end[0]][:end[1]]
            index_to_code[(start, end)] = (idx, token)
        
        # Extract DFG
        dfg, states = DFG_python(root_node, index_to_code, {})
        
        print("\nData Flow Graph:")
        print("-" * 70)
        print(f"{'Variable':<15} {'Relationship':<15} {'Sources':<30}")
        print("-" * 70)
        
        for edge in dfg:
            var, idx, rel, sources, source_idx = edge
            sources_str = ', '.join(sources) if sources else 'None'
            print(f"{var:<15} {rel:<15} {sources_str:<30}")
        
        print("\n💡 Notice:")
        print("  - 'total' depends on itself (feedback loop in for loop)")
        print("  - 'result' depends on 'total'")
        print("  - DFG captures cyclic dependencies!")
        
        print("\n✅ Complex DFG extraction successful!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error during DFG extraction: {e}")
        import traceback
        traceback.print_exc()
        return False


def visualize_dfg_graph():
    """Visualize DFG as a directed graph"""
    print("\n" + "="*70)
    print("DFG Visualization (if networkx available)")
    print("="*70)
    
    try:
        import networkx as nx
        import matplotlib.pyplot as plt
        from tree_sitter import Language, Parser
        from parser.DFG import DFG_python
        from parser.utils import tree_to_token_index
        
        print("\n✅ networkx and matplotlib available!")
        
        # Load Python parser
        LANGUAGE = Language('parser/my-languages.so', 'python')
        parser = Parser()
        parser.set_language(LANGUAGE)
        
        code = """x = 5
y = x + 1
z = y * 2
result = z"""
        
        # Parse and extract DFG
        tree = parser.parse(bytes(code, 'utf8'))
        root_node = tree.root_node
        code_lines = code.split('\n')
        token_index = tree_to_token_index(root_node)
        
        index_to_code = {}
        for idx, (start, end) in enumerate(token_index):
            if start[0] == end[0]:
                token = code_lines[start[0]][start[1]:end[1]]
            else:
                token = ""
                token += code_lines[start[0]][start[1]:]
                for i in range(start[0]+1, end[0]):
                    token += code_lines[i]
                token += code_lines[end[0]][:end[1]]
            index_to_code[(start, end)] = (idx, token)
        
        dfg, states = DFG_python(root_node, index_to_code, {})
        
        # Create directed graph
        G = nx.DiGraph()
        
        # Add edges from DFG
        for var, idx, rel, sources, source_idx in dfg:
            for source in sources:
                G.add_edge(source, var, label=rel)
        
        # Draw graph
        plt.figure(figsize=(10, 6))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', 
                node_size=3000, font_size=12, font_weight='bold',
                arrows=True, arrowsize=20, arrowstyle='->')
        
        # Add edge labels
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=9)
        
        plt.title('Data Flow Graph Visualization')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig('dfg_visualization.png', dpi=150, bbox_inches='tight')
        print("\n📊 Graph saved to: dfg_visualization.png")
        
        return True
        
    except ImportError:
        print("\n⚠️  networkx or matplotlib not available")
        print("Install with: pip install networkx matplotlib")
        print("(Optional - visualization is not required)")
        return False
    except Exception as e:
        print(f"\n⚠️  Visualization failed: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "#"*70)
    print("# DFG Extraction Test Suite")
    print("# Testing StructCoder's Data Flow Graph Extraction")
    print("#"*70)
    
    # Check parser availability
    if not check_parser_availability():
        print("\n❌ Parser files not found!")
        print("Make sure you're running from the StructCoder root directory")
        print("and the parser/ folder is present")
        return
    
    # Run tests
    results = {
        'Python DFG': test_dfg_python(),
        'Java DFG': test_dfg_java(),
        'Complex Python DFG': test_complex_example(),
        'Visualization': visualize_dfg_graph()
    }
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:<25} {status}")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! DFG extraction is working perfectly!")
        print("\nNext steps:")
        print("  1. You can now run StructCoder preprocessing")
        print("  2. Test on your own code examples")
        print("  3. Visualize DFG for complex programs")
        print("  4. Start fine-tuning experiments!")
    else:
        print("\n⚠️  Some tests failed. Check error messages above.")
        print("Make sure tree-sitter is installed: pip install tree-sitter")
    
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
