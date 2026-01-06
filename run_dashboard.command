#!/bin/zsh
cd "$(dirname "$0")"

# Activate the venv
source venv/bin/activate

# Run your dashboard
python -m streamlit run src/ui/dashboard.py
