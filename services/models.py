# --- Professional Service Models ---
from django.db import models
from django.conf import settings


class ServiceReview(models.Model):
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.PositiveSmallIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return f"Review for {self.service.name} by {self.user or 'Anonymous'}"


class ServiceFAQ(models.Model):
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=255)
    answer = models.TextField()
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"FAQ: {self.question} ({self.service.name})"

    class Meta:
        ordering = ['display_order']


class ServiceGallery(models.Model):
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='service_gallery/')
    caption = models.CharField(max_length=255, blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Image for {self.service.name}"

    class Meta:
        ordering = ['display_order']


class ServiceRequest(models.Model):
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='requests')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('new', 'New'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='new')

    def __str__(self):
        return f"Request for {self.service.name} by {self.name}"
from django.db import models
from django.utils.text import slugify

# Create your models here.
class Service(models.Model):
    SERVICE_CATEGORY_CHOICES = [
        ('web_development', 'Web Development'),
        ('web_design', 'Web Design'),
        ('ecommerce', 'E-Commerce Solutions'),
        ('cms', 'Content Management Systems'),
        ('seo', 'Search Engine Optimization'),
        ('maintenance', 'Website Maintenance'),
        ('hosting', 'Web Hosting'),
        ('consultation', 'IT Consultation'),
    ]

    # Basic Information
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=50, choices=SERVICE_CATEGORY_CHOICES)
    short_description = models.CharField(max_length=255)
    description = models.TextField()

    # Pricing
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_recurring = models.BooleanField(default=False)
    recurring_period = models.CharField(max_length=20, blank=True, null=True, 
                                       choices=[('monthly', 'Monthly'), ('yearly', 'Yearly')])

    # Display
    icon = models.CharField(max_length=50, blank=True, null=True, help_text="Font Awesome icon name")
    image = models.ImageField(upload_to='services/', blank=True, null=True)

    # Features
    features = models.TextField(blank=True, null=True, help_text="Enter features separated by new lines")

    # Meta
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['display_order', 'name']

class ServicePackage(models.Model):
    # Basic Information
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()

    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Services included
    services = models.ManyToManyField(Service, through='PackageService')

    # Display
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['display_order', 'name']

class PackageService(models.Model):
    package = models.ForeignKey(ServicePackage, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    # Additional details specific to this service in this package
    custom_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.package.name} - {self.service.name}"
