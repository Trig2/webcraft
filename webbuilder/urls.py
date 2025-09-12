"""
URL configuration for webbuilder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import home

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Homepage
    path('', home, name='home'),

    # App URLs
    path('', include('core.urls', namespace='core')),

    path('projects/', include('projects.urls', namespace='projects')),
    path('services/', include('services.urls', namespace='services')),
    path('chat/', include('chat.urls', namespace='chat')),

    # Django Auth URLs
    # path('accounts/', include('django.contrib.auth.urls')),

    # Tailwind (development only)
    path("__reload__/", include("django_browser_reload.urls")),
]

# Error handlers
handler404 = 'core.views.custom_404'
handler500 = 'core.views.custom_500'
handler403 = 'core.views.custom_403'
handler400 = 'core.views.custom_400'

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Test error pages in development
    from django.views.generic import TemplateView
    urlpatterns += [
        path('test-404/', TemplateView.as_view(template_name='404.html'), name='test_404'),
        path('test-500/', TemplateView.as_view(template_name='500.html'), name='test_500'),
        path('test-403/', TemplateView.as_view(template_name='403.html'), name='test_403'),
        path('test-400/', TemplateView.as_view(template_name='400.html'), name='test_400'),
    ]
