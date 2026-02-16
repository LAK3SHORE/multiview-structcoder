#!/usr/bin/env python3
"""
StructCoder Setup Progress Tracker
===================================
Check your setup progress and what remains to be done.

Usage:
    python check_setup.py
"""

import os
import sys
from pathlib import Path


def print_header(text):
    """Print section header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def check_item(name, condition, details=""):
    """Check and print item status"""
    status = "✅" if condition else "❌"
    print(f"{status} {name}")
    if details and condition:
        print(f"   {details}")
    return condition


def check_uv():
    """Check if UV is installed"""
    try:
        import subprocess
        result = subprocess.run(['uv', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            return True, version
    except FileNotFoundError:
        pass
    return False, None


def check_venv():
    """Check if virtual environment exists and is activated"""
    venv_path = Path('.venv')
    exists = venv_path.exists()
    activated = sys.prefix != sys.base_prefix
    return exists, activated


def check_packages():
    """Check if required packages are installed"""
    packages = {
        'torch': 'PyTorch',
        'transformers': 'Transformers',
        'datasets': 'Datasets',
        'tree_sitter': 'Tree-sitter',
        'numpy': 'NumPy',
        'scipy': 'SciPy',
        'sklearn': 'Scikit-learn',
        'tqdm': 'TQDM',
    }
    
    installed = {}
    for pkg, name in packages.items():
        try:
            __import__(pkg)
            installed[name] = True
        except ImportError:
            installed[name] = False
    
    return installed


def check_parser():
    """Check parser files"""
    parser_dir = Path('parser')
    files_needed = {
        'my-languages.so': 'Compiled parser (primary)',
        'my-languages2.so': 'Compiled parser (alternate)',
        'DFG.py': 'Data flow graph extraction',
        'utils.py': 'Parser utilities',
    }
    
    found = {}
    for file, desc in files_needed.items():
        path = parser_dir / file
        found[file] = (path.exists(), desc)
    
    return found


def check_directories():
    """Check project directories"""
    dirs_needed = {
        'saved_models/pretrain': 'Pretrained model storage',
        'data': 'Preprocessed data',
        'results': 'Experiment results',
    }
    
    exists = {}
    for dir_path, desc in dirs_needed.items():
        exists[dir_path] = (Path(dir_path).exists(), desc)
    
    return exists


def check_model():
    """Check if pretrained model exists"""
    model_path = Path('saved_models/pretrain/checkpoint_best_at_175000.bin')
    if model_path.exists():
        size_mb = model_path.stat().st_size / (1024 * 1024)
        return True, f"{size_mb:.1f} MB"
    return False, None


def check_data():
    """Check if preprocessed data exists"""
    data_dir = Path('data')
    datasets = {
        'codexglue_translation': 'Java↔C# translation',
        'codexglue_generation': 'Text-to-code (Concode)',
        'apps_generation': 'APPS dataset',
    }
    
    found = {}
    for dataset, desc in datasets.items():
        dataset_path = data_dir / dataset
        has_files = False
        if dataset_path.exists():
            pkl_files = list(dataset_path.glob('*.pkl'))
            has_files = len(pkl_files) > 0
        found[dataset] = (has_files, desc)
    
    return found


def calculate_progress():
    """Calculate overall progress percentage"""
    total_steps = 8
    completed = 0
    
    # Check each component
    uv_ok, _ = check_uv()
    if uv_ok:
        completed += 1
    
    venv_exists, _ = check_venv()
    if venv_exists:
        completed += 1
    
    packages = check_packages()
    if all(packages.values()):
        completed += 1
    
    parser_files = check_parser()
    if all(found for found, _ in parser_files.values()):
        completed += 1
    
    dirs = check_directories()
    if all(exists for exists, _ in dirs.values()):
        completed += 1
    
    model_ok, _ = check_model()
    if model_ok:
        completed += 1
    
    data = check_data()
    if any(found for found, _ in data.values()):
        completed += 1
    
    # Test script exists
    if Path('test_dfg_extraction.py').exists():
        completed += 1
    
    return (completed / total_steps) * 100


def main():
    """Main check function"""
    print_header("🔍 StructCoder Setup Progress Check")
    
    # Calculate progress
    progress = calculate_progress()
    print(f"\n📊 Overall Progress: {progress:.0f}%")
    
    # Progress bar
    filled = int(progress / 5)
    bar = "█" * filled + "░" * (20 - filled)
    print(f"[{bar}] {progress:.0f}%")
    
    # Component 1: UV
    print_header("1. UV Package Manager")
    uv_ok, uv_version = check_uv()
    check_item("UV installed", uv_ok, uv_version if uv_ok else "")
    if not uv_ok:
        print("   Install: curl -LsSf https://astral.sh/uv/install.sh | sh")
    
    # Component 2: Virtual Environment
    print_header("2. Virtual Environment")
    venv_exists, venv_activated = check_venv()
    check_item("Virtual environment exists", venv_exists, ".venv directory found")
    check_item("Environment activated", venv_activated, f"Using: {sys.prefix}")
    if not venv_activated and venv_exists:
        print("   Activate: source .venv/bin/activate")
    elif not venv_exists:
        print("   Create: uv venv --python 3.10")
    
    # Component 3: Python Packages
    print_header("3. Python Packages")
    packages = check_packages()
    all_installed = all(packages.values())
    
    for name, installed in packages.items():
        check_item(name, installed)
    
    if not all_installed:
        print("\n   Install missing packages:")
        print("   uv pip install -r requirements.txt")
    else:
        # Show versions
        try:
            import torch
            import transformers
            print(f"\n   PyTorch: {torch.__version__}")
            print(f"   Transformers: {transformers.__version__}")
            print(f"   CUDA available: {torch.cuda.is_available()}")
        except:
            pass
    
    # Component 4: Parser Files
    print_header("4. Parser Files")
    parser_files = check_parser()
    all_parser = all(found for found, _ in parser_files.values())
    
    for file, (found, desc) in parser_files.items():
        check_item(f"{file} ({desc})", found)
    
    if all_parser:
        print("\n   ✨ Parser fully configured!")
    
    # Component 5: Directories
    print_header("5. Project Directories")
    dirs = check_directories()
    all_dirs = all(exists for exists, _ in dirs.values())
    
    for dir_path, (exists, desc) in dirs.items():
        check_item(f"{dir_path}/ ({desc})", exists)
    
    if not all_dirs:
        print("\n   Create directories:")
        print("   mkdir -p saved_models/pretrain data results")
    
    # Component 6: Pretrained Model
    print_header("6. Pretrained Model")
    model_ok, model_size = check_model()
    check_item("Checkpoint file", model_ok, model_size if model_ok else "")
    
    if not model_ok:
        print("\n   Download from:")
        print("   https://drive.google.com/file/d/10Jee9uv4-XuqecWTlKvo1CeNQh1hOXEs/view")
        print("   Save to: saved_models/pretrain/checkpoint_best_at_175000.bin")
    
    # Component 7: Preprocessed Data
    print_header("7. Preprocessed Data")
    data = check_data()
    any_data = any(found for found, _ in data.values())
    
    for dataset, (found, desc) in data.items():
        check_item(f"{dataset} ({desc})", found)
    
    if not any_data:
        print("\n   Run preprocessing:")
        print("   jupyter notebook finetune_preprocess.ipynb")
    
    # Component 8: Test Scripts
    print_header("8. Test Scripts")
    test_scripts = {
        'test_dfg_extraction.py': 'DFG extraction test',
        'setup.sh': 'Setup script (Linux/Mac)',
        'setup.bat': 'Setup script (Windows)',
    }
    
    for script, desc in test_scripts.items():
        exists = Path(script).exists()
        check_item(f"{script} ({desc})", exists)
    
    # Summary
    print_header("📋 Summary & Next Steps")
    
    if progress == 100:
        print("\n🎉 Setup is 100% complete!")
        print("\nYou can now:")
        print("  1. Test DFG extraction: python test_dfg_extraction.py")
        print("  2. Run experiments: python finetune_translation_main.py")
        print("  3. Analyze results: check results/ directory")
    elif progress >= 75:
        print(f"\n✨ You're {progress:.0f}% there!")
        print("\nRemaining tasks:")
        if not model_ok:
            print("  ⬜ Download pretrained model")
        if not any_data:
            print("  ⬜ Run preprocessing")
        print("\nEstimated time: 30-90 minutes")
    elif progress >= 50:
        print(f"\n🔄 You're {progress:.0f}% complete")
        print("\nNext steps:")
        if not all_installed:
            print("  ⬜ Install Python packages")
        if not model_ok:
            print("  ⬜ Download pretrained model")
        if not any_data:
            print("  ⬜ Run preprocessing")
        print("\nEstimated time: 1-2 hours")
    else:
        print(f"\n🚀 Let's get started! ({progress:.0f}% complete)")
        print("\nFollow the setup guide:")
        print("  cat UV_SETUP_GUIDE.md")
        print("\nOr run automated setup:")
        print("  ./setup.sh  (Linux/Mac)")
        print("  setup.bat   (Windows)")
    
    print("\n" + "=" * 70 + "\n")
    
    return int(progress)


if __name__ == '__main__':
    progress = main()
    sys.exit(0 if progress >= 75 else 1)
