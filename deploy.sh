#!/bin/bash

# Deployment script for PythonAnywhere
# Run this script after uploading your code to PythonAnywhere

echo "🚀 Starting Django deployment on PythonAnywhere..."

# Activate virtual environment
echo "📦 Activating virtual environment..."
source .venv/bin/activate

# Install/update requirements
echo "📦 Installing requirements..."
pip install -r requirements.txt

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --settings=webbuilder.settings_production

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate --settings=webbuilder.settings_production

# Create cache table (if using database caching)
# python manage.py createcachetable --settings=webbuilder.settings_production

echo "✅ Deployment complete!"
echo "🌐 Don't forget to:"
echo "   1. Update ALLOWED_HOSTS in settings_production.py with your domain"
echo "   2. Configure static file mappings in PythonAnywhere Web tab"
echo "   3. Reload your web app in PythonAnywhere Web tab"
echo "   4. Create a superuser: python manage.py createsuperuser --settings=webbuilder.settings_production"
