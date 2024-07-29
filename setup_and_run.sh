#!/bin/bash

# Install pipenv if not already installed
pip install pipenv

# Install dependencies using Pipenv
pipenv install

# Run the Node.js script
node index.js
