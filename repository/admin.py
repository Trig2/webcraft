from django.contrib import admin
from .models import Repository


# Register your models here.
class RepositoryInline(admin.TabularInline):
    model = Repository
    extra = 1
    fields = ("Project", "Repository Link")


@admin.register(Repository)
class AdminRepository(admin.ModelAdmin):
    list_display = (
        "repository_name",
        "project",
        "repository_link",
        "created_at",
        "updated_at",
    )
    list_filter = ("repository_name", "project")
    search_fields = ("repository_name",)
