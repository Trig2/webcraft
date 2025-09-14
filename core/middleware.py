from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.conf import settings
from .models import SiteSetting
from django.core.cache import cache


class MaintenanceModeMiddleware:
    """
    Middleware to check if the site is in maintenance mode.
    Only allows admin users to access the site when maintenance mode is enabled.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if we should skip maintenance mode
        if self.should_skip_maintenance(request):
            response = self.get_response(request)
            return response

        # Check if maintenance mode is enabled
        if self.is_maintenance_mode_enabled():
            # Allow admin users to access the site
            if request.user.is_authenticated and request.user.is_staff:
                response = self.get_response(request)
                return response
            else:
                # Show maintenance page to regular users
                return self.render_maintenance_page(request)

        response = self.get_response(request)
        return response

    def should_skip_maintenance(self, request):
        """
        Determine if maintenance mode should be skipped for this request.
        """
        # Skip for admin URLs
        if request.path.startswith('/admin/'):
            return True
        
        # Skip for login/logout URLs
        if request.path in ['/login/', '/logout/', '/accounts/login/', '/accounts/logout/']:
            return True
            
        # Skip for static/media files
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return True
            
        # Skip for API endpoints (if any)
        if request.path.startswith('/api/'):
            return True
            
        return False

    def is_maintenance_mode_enabled(self):
        """
        Check if maintenance mode is enabled from site settings.
        Uses caching to avoid database hits on every request.
        """
        # Try to get from cache first
        maintenance_mode = cache.get('maintenance_mode')
        
        if maintenance_mode is None:
            try:
                site_setting = SiteSetting.objects.first()
                maintenance_mode = site_setting.maintenance_mode if site_setting else False
                # Cache for 5 minutes
                cache.set('maintenance_mode', maintenance_mode, 300)
            except Exception:
                # If there's any database error, assume maintenance mode is off
                maintenance_mode = False
                
        return maintenance_mode

    def render_maintenance_page(self, request):
        """
        Render the maintenance page with site branding.
        """
        try:
            # Get site settings for branding
            site_setting = SiteSetting.objects.first()
            context = {
                'site_name': site_setting.site_name if site_setting else 'WebBuilder',
                'logo': site_setting.logo if site_setting else None,
                'contact_email': site_setting.contact_email if site_setting else None,
                'contact_phone': site_setting.contact_phone if site_setting else None,
            }
        except Exception:
            # Fallback context if database is unavailable
            context = {
                'site_name': 'WebBuilder',
                'logo': None,
                'contact_email': None,
                'contact_phone': None,
            }
        
        return render(request, 'maintenance.html', context, status=503)
