#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Set production environment
export DJANGO_ENVIRONMENT=production

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Create sample projects if needed
python manage.py create_sample_projects

# Generate slugs for projects
python manage.py generate_project_slugs
