#!/bin/bash
# Quick Fix for Tokenizers on Apple Silicon
# =========================================

echo "🔧 Fixing tokenizers installation for Apple Silicon..."
echo ""

# Activate environment if not already activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

echo "Installing with compatible tokenizers version..."
echo ""

# Install everything except tokenizers first
uv pip install \
    torch==1.13.1 \
    transformers==4.25.1 \
    datasets==2.8.0 \
    tree-sitter==0.20.1 \
    numpy==1.21.5 \
    scipy==1.9.3 \
    scikit-learn==1.1.3 \
    pandas==1.5.2 \
    tqdm==4.64.1 \
    matplotlib==3.6.2 \
    requests==2.28.1 \
    pyyaml==6.0 \
    regex==2022.7.9 \
    jupyter \
    ipykernel \
    ipython \
    filelock \
    packaging \
    huggingface-hub

echo ""
echo "Installing tokenizers (compatible version for ARM64)..."

# Install newer tokenizers with prebuilt wheel
uv pip install 'tokenizers>=0.13.0'

echo ""
echo "✅ Installation complete!"
echo ""

# Verify
python -c "
import torch
import transformers
import tokenizers
import tree_sitter
print('✅ All packages verified!')
print(f'PyTorch: {torch.__version__}')
print(f'Transformers: {transformers.__version__}')
print(f'Tokenizers: {tokenizers.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')
"
