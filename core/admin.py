from django.contrib import admin
from .models import (
    Page,
    TeamMember,
    Testimonial,
    ContactMessage,
    FAQ,
    SiteSetting,
    NewsletterSubscriber,
    ActivityLog,
    Announcement,
    PricingPlan,
    # New models
    BlogTag,
    BlogPost,
    Lead,
    Quote,
    QuoteService,
    Client,
    WebsiteAnalytics,
    ConversionTracking,
)


from django.utils.html import format_html
from django.conf import settings


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "billing_type",
        "is_featured",
        "is_active",
        "display_order",
    )
    list_filter = ("billing_type", "is_featured", "is_active")
    search_fields = ("name", "features")
    ordering = ("display_order", "price")


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ("site_name", "contact_email", "contact_phone", "updated_at")
    search_fields = ("site_name", "contact_email", "contact_phone")


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "subscribed_at", "is_active")
    search_fields = ("email",)
    list_filter = ("is_active", "subscribed_at")


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("user", "action", "project_logs", "created_at")
    search_fields = ("user__username", "action", "details")
    list_filter = ("created_at",)


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "start_date", "end_date", "created_at")
    search_fields = ("title", "message")
    list_filter = ("is_active", "start_date", "end_date")


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_published", "created_at")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "content")
    list_filter = ("is_published",)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "position", "is_active", "display_order")
    list_filter = ("is_active",)
    search_fields = ("name", "position")
    ordering = ("display_order", "name")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = (
        "client_name",
        "client_company",
        "rating",
        "is_featured",
        "is_active",
    )
    list_filter = ("is_featured", "is_active", "rating")
    search_fields = ("client_name", "client_company", "content")
    ordering = ("-is_featured", "display_order")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "subject",
        "status",
        "created_at",
        "attachment_link",
    )
    list_filter = ("status", "created_at")
    search_fields = ("name", "email", "subject", "message")
    ordering = ("-created_at",)

    def attachment_link(self, obj):
        if obj.notes and obj.notes.startswith("Attachment: "):
            rel_path = obj.notes.replace("Attachment: ", "").strip()
            url = f"{settings.MEDIA_URL}{rel_path}"
            return format_html('<a href="{}" target="_blank">Download</a>', url)
        return "-"

    attachment_link.short_description = "Attachment"


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "category", "is_active", "display_order")
    list_filter = ("is_active", "category")
    search_fields = ("question", "answer")
    ordering = ("display_order",)


# --- New Model Admin Classes ---

@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "color")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "is_featured", "publish_date", "created_at")
    list_filter = ("status", "is_featured", "tags", "publish_date", "author")
    search_fields = ("title", "content", "excerpt")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    ordering = ("-created_at",)
    date_hierarchy = "publish_date"


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "email", "status", "source", "assigned_to", "created_at")
    list_filter = ("status", "source", "assigned_to", "created_at")
    search_fields = ("name", "email", "company", "message")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    
    fieldsets = (
        ("Contact Information", {
            "fields": ("name", "email", "phone", "company")
        }),
        ("Lead Details", {
            "fields": ("budget", "timeline", "project_type", "source", "message")
        }),
        ("Management", {
            "fields": ("status", "assigned_to", "notes")
        }),
    )


class QuoteServiceInline(admin.TabularInline):
    model = QuoteService
    extra = 1
    fields = ("service", "quantity", "unit_price", "discount_percentage", "total_price")
    readonly_fields = ("total_price",)


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("quote_number", "client_name", "client_company", "total_amount", "status", "created_at")
    list_filter = ("status", "created_at", "created_by")
    search_fields = ("quote_number", "client_name", "client_email", "client_company")
    ordering = ("-created_at",)
    readonly_fields = ("quote_number",)
    inlines = [QuoteServiceInline]
    
    fieldsets = (
        ("Client Information", {
            "fields": ("client_name", "client_email", "client_phone", "client_company")
        }),
        ("Quote Details", {
            "fields": ("quote_number", "status", "valid_until", "lead")
        }),
        ("Pricing", {
            "fields": ("subtotal", "tax_rate", "tax_amount", "total_amount")
        }),
        ("Additional Information", {
            "fields": ("notes", "terms_conditions", "created_by")
        }),
    )


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("company_name", "user", "industry", "phone", "is_active", "created_at")
    list_filter = ("industry", "is_active", "created_at")
    search_fields = ("company_name", "user__username", "user__email", "phone")
    ordering = ("company_name",)


@admin.register(WebsiteAnalytics)
class WebsiteAnalyticsAdmin(admin.ModelAdmin):
    list_display = ("date", "page_views", "unique_visitors", "contact_forms", "service_requests", "bounce_rate")
    list_filter = ("date",)
    ordering = ("-date",)
    date_hierarchy = "date"


@admin.register(ConversionTracking)
class ConversionTrackingAdmin(admin.ModelAdmin):
    list_display = ("action", "source", "value", "lead", "timestamp")
    list_filter = ("action", "source", "timestamp")
    search_fields = ("source", "page_url")
    ordering = ("-timestamp",)
    date_hierarchy = "timestamp"
