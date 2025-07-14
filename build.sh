#!/bin/bash
set -e  # Stop script if any command fails

# Install dependencies
pip install -r requirements.txt

# Run migrations
python3.9 manage.py migrate

# Collect static files without prompts
python3.9 manage.py collectstatic --noinput

