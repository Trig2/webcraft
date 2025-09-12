
from django.contrib import admin
from .models import (
    Project,
    ProjectAttachment, 
    ProjectNote, 
    ProjectMilestone, 
    ProjectCollaborator,
    # New models
    Technology,
    ProjectTechnology,
    ProjectImage,
    ProjectTestimonial,
    ProjectMetrics,
    ClientProject,
)


class ProjectCollaboratorInline(admin.TabularInline):
    model = ProjectCollaborator
    extra = 1
    fields = ('user', 'role', 'is_lead')
    autocomplete_fields = ['user']


class ProjectTechnologyInline(admin.TabularInline):
    model = ProjectTechnology
    extra = 1


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ("image", "image_type", "caption", "is_featured", "display_order")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "client_name", "organization_name", "project_type", "status", "created_at")
    list_filter = ("project_type", "status", "created_at")
    search_fields = ("title", "client_name", "organization_name", "description")
    ordering = ("-created_at",)
    inlines = [ProjectCollaboratorInline, ProjectTechnologyInline, ProjectImageInline]


@admin.register(ProjectAttachment)
class ProjectAttachmentAdmin(admin.ModelAdmin):
    list_display = ("project", "file", "uploaded_by", "uploaded_at")
    search_fields = ("project__title", "file")
    list_filter = ("uploaded_at",)


@admin.register(ProjectNote)
class ProjectNoteAdmin(admin.ModelAdmin):
    list_display = ("project", "created_by", "created_at")
    search_fields = ("project__title", "note", "created_by__username")
    list_filter = ("created_at",)


@admin.register(ProjectMilestone)
class ProjectMilestoneAdmin(admin.ModelAdmin):
    list_display = ("project", "name", "due_date", "completed", "completed_at")
    search_fields = ("project__title", "name", "description")
    list_filter = ("completed", "due_date")


@admin.register(ProjectCollaborator)
class ProjectCollaboratorAdmin(admin.ModelAdmin):
    list_display = ("project", "user", "role", "is_lead", "added_at")
    list_filter = ("role", "is_lead", "added_at")
    search_fields = ("project__title", "user__username", "user__first_name", "user__last_name")
    autocomplete_fields = ['project', 'user']
    ordering = ('-added_at',)


# --- New Model Admin Classes ---

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "color", "is_active", "display_order")
    list_filter = ("category", "is_active")
    search_fields = ("name", "description")
    ordering = ("category", "display_order", "name")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ProjectTechnology)
class ProjectTechnologyAdmin(admin.ModelAdmin):
    list_display = ("project", "technology", "importance")
    list_filter = ("importance", "technology__category")
    search_fields = ("project__title", "technology__name")


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ("project", "image_type", "caption", "is_featured", "display_order", "uploaded_at")
    list_filter = ("image_type", "is_featured", "uploaded_at")
    search_fields = ("project__title", "caption", "description")
    ordering = ("project", "display_order", "uploaded_at")


@admin.register(ProjectTestimonial)
class ProjectTestimonialAdmin(admin.ModelAdmin):
    list_display = ("project", "client_name", "rating", "is_approved", "created_at")
    list_filter = ("rating", "is_approved", "created_at")
    search_fields = ("project__title", "client_name", "client_feedback")
    ordering = ("-created_at",)


@admin.register(ProjectMetrics)
class ProjectMetricsAdmin(admin.ModelAdmin):
    list_display = ("project", "lighthouse_score", "seo_score", "traffic_increase", "updated_at")
    list_filter = ("mobile_friendly", "updated_at")
    search_fields = ("project__title",)
    ordering = ("-updated_at",)
    
    fieldsets = (
        ("Performance Metrics", {
            "fields": ("page_load_time", "lighthouse_score", "mobile_friendly")
        }),
        ("Business Metrics", {
            "fields": ("traffic_increase", "conversion_rate", "bounce_rate")
        }),
        ("Development Metrics", {
            "fields": ("development_hours", "lines_of_code")
        }),
        ("SEO Metrics", {
            "fields": ("seo_score", "keywords_ranking")
        }),
    )


@admin.register(ClientProject)
class ClientProjectAdmin(admin.ModelAdmin):
    list_display = ("client", "project", "access_level", "client_access_enabled", "last_accessed")
    list_filter = ("access_level", "client_access_enabled", "access_granted_at")
    search_fields = ("client__company_name", "project__title")
    ordering = ("-access_granted_at",)
