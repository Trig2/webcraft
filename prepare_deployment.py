#!/usr/bin/env python
"""
PythonAnywhere deployment helper script
Run this on your local machine to prepare for deployment
"""

import os
import subprocess
import sys

def run_command(cmd, description):
    """Run a command and print the result"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {description} failed")
            if result.stderr:
                print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False

def main():
    print("🚀 PythonAnywhere Deployment Preparation")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ manage.py not found. Please run this script from your Django project root.")
        sys.exit(1)
    
    print("✅ Django project detected")
    
    # Check current settings
    print("\n📋 Pre-deployment checks:")
    
    # Test with production settings
    success = run_command(
        'python manage.py check --settings=webbuilder.settings_production',
        'Testing production settings'
    )
    
    if not success:
        print("⚠️  Production settings check failed. Please review settings_production.py")
    
    # Collect static files for testing
    run_command(
        'python manage.py collectstatic --noinput --settings=webbuilder.settings_production',
        'Collecting static files (test)'
    )
    
    # Check migrations
    run_command(
        'python manage.py showmigrations --settings=webbuilder.settings_production',
        'Checking migrations status'
    )
    
    print("\n📋 Deployment files created:")
    files_to_check = [
        'requirements_production.txt',
        'settings_production.py',
        'wsgi_pythonanywhere.py',
        'deploy.sh',
        'DEPLOYMENT_GUIDE.md',
        'DEPLOYMENT_CHECKLIST.md'
    ]
    
    for file in files_to_check:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} missing")
    
    print("\n🎯 Next Steps:")
    print("1. Upload your project to PythonAnywhere (use Git or file upload)")
    print("2. Follow the DEPLOYMENT_CHECKLIST.md step by step")
    print("3. Update 'yourusername' in all configuration files")
    print("4. Configure your web app in PythonAnywhere dashboard")
    print("5. Set up static file mappings")
    print("6. Reload your web app")
    
    print("\n🌐 Your site will be available at:")
    print("https://yourusername.pythonanywhere.com")
    print("(Replace 'yourusername' with your actual PythonAnywhere username)")
    
    print("\n📚 Documentation:")
    print("- Quick start: DEPLOYMENT_CHECKLIST.md")
    print("- Detailed guide: DEPLOYMENT_GUIDE.md")

if __name__ == "__main__":
    main()
