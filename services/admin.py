
from django.contrib import admin
from .models import Service, ServicePackage, PackageService, ServiceReview, ServiceFAQ, ServiceGallery, ServiceRequest
@admin.register(ServiceReview)
class ServiceReviewAdmin(admin.ModelAdmin):
	list_display = ("service", "user", "rating", "is_approved", "created_at")
	list_filter = ("is_approved", "rating", "created_at")
	search_fields = ("service__name", "user__username", "comment")

@admin.register(ServiceFAQ)
class ServiceFAQAdmin(admin.ModelAdmin):
	list_display = ("service", "question", "is_active", "display_order")
	list_filter = ("is_active",)
	search_fields = ("service__name", "question", "answer")
	ordering = ("service", "display_order")

@admin.register(ServiceGallery)
class ServiceGalleryAdmin(admin.ModelAdmin):
	list_display = ("service", "image", "caption", "display_order")
	search_fields = ("service__name", "caption")
	ordering = ("service", "display_order")

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
	list_display = ("service", "name", "email", "phone", "status", "created_at")
	list_filter = ("status", "created_at")
	search_fields = ("service__name", "name", "email", "phone", "message")

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
	list_display = ("name", "category", "base_price", "is_featured", "is_active", "display_order")
	list_filter = ("category", "is_featured", "is_active")
	search_fields = ("name", "short_description", "description")
	ordering = ("display_order", "name")

@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
	list_display = ("name", "price", "is_featured", "is_active", "display_order")
	list_filter = ("is_featured", "is_active")
	search_fields = ("name", "description")
	ordering = ("display_order", "name")

@admin.register(PackageService)
class PackageServiceAdmin(admin.ModelAdmin):
	list_display = ("package", "service", "custom_description")
	search_fields = ("package__name", "service__name", "custom_description")
