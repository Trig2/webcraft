from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.management import call_command
import os
import sys

class Command(BaseCommand):
    help = 'Check deployment readiness and system status'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔍 Django Deployment Status Check\n'))
        
        # Check DEBUG status
        if settings.DEBUG:
            self.stdout.write(self.style.WARNING('⚠️  DEBUG is True - should be False in production'))
        else:
            self.stdout.write(self.style.SUCCESS('✅ DEBUG is properly set to False'))
        
        # Check ALLOWED_HOSTS
        if not settings.ALLOWED_HOSTS or settings.ALLOWED_HOSTS == []:
            self.stdout.write(self.style.ERROR('❌ ALLOWED_HOSTS is empty - must be configured for production'))
        else:
            self.stdout.write(self.style.SUCCESS(f'✅ ALLOWED_HOSTS configured: {settings.ALLOWED_HOSTS}'))
        
        # Check SECRET_KEY
        if settings.SECRET_KEY.startswith('django-insecure'):
            self.stdout.write(self.style.WARNING('⚠️  Using default SECRET_KEY - consider using environment variable'))
        else:
            self.stdout.write(self.style.SUCCESS('✅ SECRET_KEY appears to be properly configured'))
        
        # Check static files
        try:
            if os.path.exists(settings.STATIC_ROOT):
                static_files = len([f for f in os.listdir(settings.STATIC_ROOT) if os.path.isfile(os.path.join(settings.STATIC_ROOT, f))])
                self.stdout.write(self.style.SUCCESS(f'✅ Static files collected: {static_files} files in {settings.STATIC_ROOT}'))
            else:
                self.stdout.write(self.style.WARNING('⚠️  Static files not collected - run collectstatic'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'⚠️  Could not check static files: {e}'))
        
        # Check database connection
        try:
            from django.db import connection
            cursor = connection.cursor()
            self.stdout.write(self.style.SUCCESS('✅ Database connection successful'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Database connection failed: {e}'))
        
        # Check migrations
        try:
            call_command('showmigrations', '--plan', verbosity=0)
            self.stdout.write(self.style.SUCCESS('✅ Migrations status checked'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'⚠️  Could not check migrations: {e}'))
        
        # Python version
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        self.stdout.write(self.style.SUCCESS(f'✅ Python version: {python_version}'))
        
        # Django version
        import django
        self.stdout.write(self.style.SUCCESS(f'✅ Django version: {django.get_version()}'))
        
        self.stdout.write(self.style.SUCCESS('\n🚀 Deployment check complete!'))
