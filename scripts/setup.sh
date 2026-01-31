#!/bin/bash

# Setup script for AI Resume Parser & Job Recommender

echo "=========================================="
echo "Setting up AI Resume Parser & Job Recommender"
echo "=========================================="

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip --quiet
echo "Installing packages (this may take a few minutes)..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p data/jobs data/resumes data/chroma_db logs

# Copy .env.example to .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
    else
        cat > .env << EOF
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
VECTOR_DB_PROVIDER=chroma
CHROMA_PERSIST_DIR=./data/chroma_db
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
JOB_SOURCES=arbeitnow,remoteok,indeed
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
EOF
    fi
    echo "✓ Created .env file"
fi

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Fetch jobs: python scripts/fetch_jobs.py"
echo "3. Run tests: python tests/test_complete.py"
echo "4. Start API: python run.py"
echo ""
echo "Optional:"
echo "- If using Ollama: ollama serve && ollama pull llama3.1:8b"
echo "- Or use Docker: docker-compose up"
echo ""
