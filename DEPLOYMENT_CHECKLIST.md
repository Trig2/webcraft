# PythonAnywhere Quick Deployment Checklist

## Pre-Deployment Checklist ✅

- [ ] Sign up for PythonAnywhere account
- [ ] Choose appropriate plan (Beginner/Hacker/Web Developer)
- [ ] Have your domain name ready (optional)

## Upload Your Code 📁

### Option A: Git (Recommended)

```bash
# In PythonAnywhere Bash console:
cd ~
git clone https://github.com/yourusername/your-repo.git DjangoProject
cd DjangoProject
```

### Option B: File Upload

- Use Files tab to upload your project folder

## Environment Setup 🔧

```bash
# Create virtual environment
cd ~/DjangoProject
python3.10 -m venv .venv
source .venv/bin/activate

# Install packages
pip install -r requirements_production.txt
```

## Configuration Updates 📝

1. **Edit settings_production.py:**
   - Replace `yourusername` with your PythonAnywhere username
   - Update ALLOWED_HOSTS with your domain

2. **Check your paths are correct**

## Django Setup 🐍

```bash
# Collect static files
python manage.py collectstatic --settings=webbuilder.settings_production

# Run migrations
python manage.py migrate --settings=webbuilder.settings_production

# Create superuser
python manage.py createsuperuser --settings=webbuilder.settings_production

# Check deployment status
python manage.py check_deployment --settings=webbuilder.settings_production
```

## Web App Configuration 🌐

1. **Go to Web tab** in PythonAnywhere dashboard
2. **Click "Add a new web app"**
3. **Choose "Manual configuration"**
4. **Select Python 3.10**

### Configure paths

- **Source code:** `/home/yourusername/DjangoProject`
- **Working directory:** `/home/yourusername/DjangoProject`

### WSGI Configuration

- Edit the WSGI file and replace content with `wsgi_pythonanywhere.py` content
- Update `yourusername` in the WSGI file

### Static Files Mapping

| URL      | Directory                                    |
|----------|----------------------------------------------|
| /static/ | /home/yourusername/DjangoProject/staticfiles |
| /media/  | /home/yourusername/DjangoProject/media      |

## Final Steps 🚀

- [ ] Click **"Reload"** in Web tab
- [ ] Visit your site: `https://yourusername.pythonanywhere.com`
- [ ] Test admin panel: `https://yourusername.pythonanywhere.com/admin/`
- [ ] Check all pages work correctly

## Troubleshooting 🔧

### Site not loading?

1. Check error logs in Web tab
2. Verify ALLOWED_HOSTS setting
3. Ensure WSGI file is correct

### Static files not working?

1. Run `collectstatic` again
2. Check static files mapping
3. Verify paths are correct

### 500 errors?

1. Check error logs
2. Run deployment check: `python manage.py check_deployment`
3. Verify database migrations

## Updating Your Site 🔄

When you make changes:

```bash
cd ~/DjangoProject
git pull  # if using Git
source .venv/bin/activate
pip install -r requirements_production.txt  # if new packages
python manage.py migrate --settings=webbuilder.settings_production
python manage.py collectstatic --settings=webbuilder.settings_production
```

Then click **Reload** in Web tab.

## Your Site URLs 🌍

- **Main site:** <https://yourusername.pythonanywhere.com>
- **Admin panel:** <https://yourusername.pythonanywhere.com/admin/>
- **API (if applicable):** <https://yourusername.pythonanywhere.com/api/>

---

**Need help?** Check the full DEPLOYMENT_GUIDE.md for detailed instructions!
