#!/bin/bash
# StructCoder Quick Setup with UV
# ================================
# This script sets up everything you need in minutes!

set -e  # Exit on error

echo "=========================================="
echo "  StructCoder Environment Setup (UV)"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Check/Install UV
echo "Step 1/5: Installing UV..."
echo "------------------------------------"
if command -v uv &> /dev/null; then
    echo -e "${GREEN}✓ UV is already installed${NC}"
    uv --version
else
    echo "Installing UV..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
    echo -e "${GREEN}✓ UV installed successfully${NC}"
fi
echo ""

# Step 2: Create Python 3.10 environment
echo "Step 2/5: Creating Python 3.10 virtual environment..."
echo "------------------------------------"
if [ -d ".venv" ]; then
    echo -e "${YELLOW}⚠ .venv already exists${NC}"
    read -p "Delete and recreate? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf .venv
        echo "Removed existing .venv"
    fi
fi

if [ ! -d ".venv" ]; then
    uv venv --python 3.10
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Using existing virtual environment${NC}"
fi
echo ""

# Step 3: Activate environment and install dependencies
echo "Step 3/5: Installing dependencies..."
echo "------------------------------------"
echo "⏳ This may take 5-10 minutes (installing PyTorch, etc.)..."
echo ""

source .venv/bin/activate

# Install with UV (super fast!)
uv pip install -r requirements.txt

echo ""
echo -e "${GREEN}✓ All dependencies installed${NC}"
echo ""

# Step 4: Verify installation
echo "Step 4/5: Verifying installation..."
echo "------------------------------------"

python -c "
import sys
packages = {
    'torch': 'PyTorch',
    'transformers': 'Transformers',
    'datasets': 'Datasets',
    'tree_sitter': 'Tree-sitter',
    'numpy': 'NumPy',
    'tqdm': 'TQDM'
}

all_ok = True
for pkg, name in packages.items():
    try:
        __import__(pkg)
        print(f'✓ {name}')
    except ImportError:
        print(f'✗ {name} - MISSING')
        all_ok = False
        
if all_ok:
    print()
    import torch
    import transformers
    print(f'PyTorch version: {torch.__version__}')
    print(f'Transformers version: {transformers.__version__}')
    print(f'CUDA available: {torch.cuda.is_available()}')
    sys.exit(0)
else:
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ Installation verified successfully${NC}"
else
    echo ""
    echo -e "${RED}✗ Some packages failed to install${NC}"
    exit 1
fi
echo ""

# Step 5: Create directories
echo "Step 5/5: Creating project directories..."
echo "------------------------------------"
mkdir -p saved_models/pretrain
mkdir -p data
mkdir -p results
echo -e "${GREEN}✓ Directories created${NC}"
echo ""

# Summary
echo "=========================================="
echo "  🎉 Setup Complete!"
echo "=========================================="
echo ""
echo -e "${GREEN}✅ Environment ready!${NC}"
echo ""
echo "Next steps:"
echo ""
echo "1. Activate environment:"
echo "   ${YELLOW}source .venv/bin/activate${NC}"
echo ""
echo "2. Test DFG extraction:"
echo "   ${YELLOW}python test_dfg_extraction.py${NC}"
echo ""
echo "3. Download pretrained model:"
echo "   Visit: https://drive.google.com/file/d/10Jee9uv4-XuqecWTlKvo1CeNQh1hOXEs/view"
echo "   Save to: saved_models/pretrain/checkpoint_best_at_175000.bin"
echo ""
echo "4. Run preprocessing:"
echo "   ${YELLOW}jupyter notebook finetune_preprocess.ipynb${NC}"
echo ""
echo "5. Start testing:"
echo "   ${YELLOW}python finetune_translation_main.py --source_lang java --target_lang cs --do_test 1${NC}"
echo ""
echo "=========================================="
