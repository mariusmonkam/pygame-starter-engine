#!/bin/bash

# Set up a Python virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate  # Use `venv\Scripts\activate` on Windows

# Install Python packages
pip install -r requirements.txt

# Run the Node.js script
node index.js
