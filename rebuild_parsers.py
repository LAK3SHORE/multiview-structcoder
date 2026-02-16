#!/usr/bin/env python3
"""
Rebuild Tree-sitter Parsers for Apple Silicon
==============================================
Rebuilds the parser libraries for ARM64 architecture (M1/M2/M3/M4 Macs)
"""

import os
import subprocess
import sys
from pathlib import Path
import shutil


def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n{description}")
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False


def main():
    print("=" * 70)
    print("  Rebuilding Tree-sitter Parsers for Apple Silicon")
    print("=" * 70)
    
    # Check we're in the right directory
    if not Path('parser').exists():
        print("\n❌ Error: parser/ directory not found")
        print("   Run this script from StructCoder root directory")
        sys.exit(1)
    
    os.chdir('parser')
    
    # Step 1: Clone language grammars if needed
    print("\n" + "=" * 70)
    print("Step 1: Checking vendor/ language grammars")
    print("=" * 70)
    
    languages = {
        'tree-sitter-python': 'https://github.com/tree-sitter/tree-sitter-python',
        'tree-sitter-java': 'https://github.com/tree-sitter/tree-sitter-java',
        'tree-sitter-c-sharp': 'https://github.com/tree-sitter/tree-sitter-c-sharp',
        'tree-sitter-javascript': 'https://github.com/tree-sitter/tree-sitter-javascript',
        'tree-sitter-go': 'https://github.com/tree-sitter/tree-sitter-go',
        'tree-sitter-php': 'https://github.com/tree-sitter/tree-sitter-php',
        'tree-sitter-ruby': 'https://github.com/tree-sitter/tree-sitter-ruby',
    }
    
    Path('vendor').mkdir(exist_ok=True)
    
    needs_clone = False
    for lang, url in languages.items():
        lang_path = Path('vendor') / lang
        if not lang_path.exists() or not list(lang_path.iterdir()):
            needs_clone = True
            break
    
    if needs_clone:
        print("\n⚠️  Language grammars missing or empty. Cloning...")
        for lang, url in languages.items():
            lang_path = Path('vendor') / lang
            if lang_path.exists():
                shutil.rmtree(lang_path)
            
            print(f"\nCloning {lang}...")
            if not run_command(['git', 'clone', url, str(lang_path)], f"Cloning {lang}"):
                print(f"❌ Failed to clone {lang}")
                sys.exit(1)
        
        print("\n✅ All language grammars cloned")
    else:
        print("✅ Language grammars already exist")
    
    # Step 2: Backup old .so files
    print("\n" + "=" * 70)
    print("Step 2: Backing up old .so files")
    print("=" * 70)
    
    for so_file in ['my-languages.so', 'my-languages2.so']:
        if Path(so_file).exists():
            backup = f"{so_file}.x86_backup"
            if Path(backup).exists():
                Path(backup).unlink()
            Path(so_file).rename(backup)
            print(f"✅ Backed up {so_file} to {backup}")
    
    # Step 3: Build parsers
    print("\n" + "=" * 70)
    print("Step 3: Building parsers for ARM64")
    print("=" * 70)
    print("⏳ This may take 2-5 minutes...")
    
    if not run_command([sys.executable, 'build_tree_sitter.py'], "Building parsers"):
        print("\n❌ Build failed!")
        print("\nTroubleshooting:")
        print("1. Make sure you're in the parser/ directory")
        print("2. Check that build_tree_sitter.py exists")
        print("3. Verify tree-sitter is installed: pip list | grep tree-sitter")
        sys.exit(1)
    
    # Step 4: Verify
    print("\n" + "=" * 70)
    print("Step 4: Verifying new parser")
    print("=" * 70)
    
    so_file = Path('my-languages2.so')
    if so_file.exists():
        size_mb = so_file.stat().st_size / (1024 * 1024)
        print(f"\n✅ New parser built successfully!")
        print(f"   File: my-languages2.so")
        print(f"   Size: {size_mb:.1f} MB")
        
        # Check architecture
        try:
            result = subprocess.run(['file', 'my-languages2.so'], 
                                  capture_output=True, text=True)
            print(f"   Arch: {result.stdout.strip()}")
            
            if 'arm64' in result.stdout.lower():
                print("   ✅ ARM64 architecture confirmed!")
            else:
                print("   ⚠️  Warning: Architecture doesn't show arm64")
        except:
            pass
        
        # Create symlink if needed
        if not Path('my-languages.so').exists():
            os.symlink('my-languages2.so', 'my-languages.so')
            print("✅ Created symlink: my-languages.so -> my-languages2.so")
    else:
        print("\n❌ Build failed - my-languages2.so not found")
        sys.exit(1)
    
    os.chdir('..')
    
    # Final message
    print("\n" + "=" * 70)
    print("  🎉 Parsers Successfully Rebuilt for ARM64!")
    print("=" * 70)
    print("\nNext steps:")
    print("  1. Test the parser:")
    print("     python test_dfg_extraction.py")
    print("")
    print("  2. If test passes, continue to preprocessing:")
    print("     jupyter notebook finetune_preprocess.ipynb")
    print("")
    print("=" * 70)


if __name__ == '__main__':
    main()
