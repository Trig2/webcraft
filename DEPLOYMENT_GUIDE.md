# PythonAnywhere Deployment Guide

## Prerequisites

1. Sign up for a PythonAnywhere account at <https://www.pythonanywhere.com/>
2. Choose a plan (Beginner plan works for most Django projects)

## Step 1: Upload Your Project

### Method 1: Using Git (Recommended)

1. Create a repository on GitHub/GitLab with your project
2. Push your code to the repository
3. In PythonAnywhere, open a Bash console
4. Clone your repository:

   ```bash
   cd ~
   git clone https://github.com/yourusername/your-repo-name.git DjangoProject
   cd DjangoProject
   ```

### Method 2: Upload Files

1. Use the Files tab in PythonAnywhere dashboard
2. Upload your project files to `/home/yourusername/DjangoProject/`

## Step 2: Set Up Virtual Environment

1. Open a Bash console in PythonAnywhere
2. Create and activate virtual environment:

   ```bash
   cd ~/DjangoProject
   python3.10 -m venv .venv
   source .venv/bin/activate
   ```

3. Install requirements:

   ```bash
   pip install -r requirements.txt
   ```

## Step 3: Configure Django Settings

1. Update ALLOWED_HOSTS in settings_production.py:
   - Replace 'yourusername' with your actual PythonAnywhere username

2. Update database paths if using SQLite:
   - Replace '/home/yourusername/' with your actual path

## Step 4: Collect Static Files

```bash
cd ~/DjangoProject
source .venv/bin/activate
python manage.py collectstatic --settings=webbuilder.settings_production
```

## Step 5: Run Migrations

```bash
python manage.py migrate --settings=webbuilder.settings_production
```

## Step 6: Create Superuser

```bash
python manage.py createsuperuser --settings=webbuilder.settings_production
```

## Step 7: Configure Web App

1. Go to Web tab in PythonAnywhere dashboard
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Choose Python 3.10
5. Set the following configurations:

### Source code

```
/home/yourusername/DjangoProject
```

### Working directory

```
/home/yourusername/DjangoProject
```

### WSGI configuration file

Edit the auto-generated WSGI file and replace its contents with the WSGI content provided below.

## Step 8: Configure Static Files

In the Web tab, add these static file mappings:

| URL        | Directory                                    |
|------------|----------------------------------------------|
| /static/   | /home/yourusername/DjangoProject/staticfiles |
| /media/    | /home/yourusername/DjangoProject/media      |

## Step 9: Environment Variables (Optional)

If you want to use environment variables:

1. Go to Files tab
2. Edit `.bashrc` file
3. Add: `export SECRET_KEY="your-secret-key-here"`

## Step 10: Reload and Test

1. Click "Reload" button in Web tab
2. Visit your site at <https://yourusername.pythonanywhere.com>

## Troubleshooting

### Common Issues

1. **Static files not loading:**
   - Make sure you've run `collectstatic`
   - Check static file mappings in Web tab

2. **500 Internal Server Error:**
   - Check error logs in Web tab
   - Verify ALLOWED_HOSTS setting
   - Check file permissions

3. **Database errors:**
   - Ensure migrations are run
   - Check database file permissions (for SQLite)

4. **Import errors:**
   - Verify all requirements are installed
   - Check Python version compatibility

### Checking Logs

- Error logs: Available in Web tab
- Access logs: Available in Web tab
- Django logs: Check the file specified in logging configuration

## Production Optimizations

1. **Use MySQL instead of SQLite** (for better performance):
   - Create MySQL database in Databases tab
   - Update settings_production.py with MySQL credentials

2. **Enable HTTPS** (automatic on PythonAnywhere)

3. **Set up proper logging** (already configured in settings_production.py)

4. **Configure caching** if needed

5. **Optimize static files** with compression

## Updating Your Deployment

When you make changes:

1. Update your code (git pull if using Git)
2. Activate virtual environment: `source .venv/bin/activate`
3. Install new requirements if any: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate --settings=webbuilder.settings_production`
5. Collect static files: `python manage.py collectstatic --settings=webbuilder.settings_production`
6. Reload web app in Web tab

## Security Notes

- Never commit sensitive information to version control
- Use environment variables for secrets in production
- Regularly update dependencies
- Monitor error logs for security issues
