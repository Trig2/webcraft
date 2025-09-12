from django.shortcuts import render, get_object_or_404
from .models import Service, ServicePackage

# Create your views here.
def service_list(request):
    """View for listing all services"""
    services = Service.objects.filter(is_active=True).order_by('display_order', 'name')

    # Group services by category
    categories = {}
    for service in services:
        category = service.get_category_display()
        if category not in categories:
            categories[category] = []
        categories[category].append(service)

    context = {
        'categories': categories,
        'services': services,
    }

    return render(request, 'services/service_list.html', context)

def service_detail(request, slug):
    """View for displaying service details"""
    service = get_object_or_404(Service, slug=slug, is_active=True)

    # Get packages that include this service
    packages = ServicePackage.objects.filter(services=service, is_active=True)

    # Parse features if they exist
    features = []
    if service.features:
        features = [f.strip() for f in service.features.split('\n') if f.strip()]

    context = {
        'service': service,
        'packages': packages,
        'features': features,
    }

    return render(request, 'services/service_detail.html', context)

def package_list(request):
    """View for listing all service packages"""
    packages = ServicePackage.objects.filter(is_active=True).order_by('display_order', 'name')

    context = {
        'packages': packages,
    }

    return render(request, 'services/package_list.html', context)

def package_detail(request, slug):
    """View for displaying package details"""
    package = get_object_or_404(ServicePackage, slug=slug, is_active=True)

    # Get all services in this package with their custom descriptions
    package_services = package.packageservice_set.all().select_related('service')

    context = {
        'package': package,
        'package_services': package_services,
    }

    return render(request, 'services/package_detail.html', context)
