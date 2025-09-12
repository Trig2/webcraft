from django.db import models
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from projects.models import Project
from django.core.cache import cache

# Create your models here.


class PricingPlan(models.Model):
    BILLING_CHOICES = [
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
        ("one_time", "One Time"),
    ]

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    billing_type = models.CharField(
        max_length=20, choices=BILLING_CHOICES, default="monthly"
    )
    features = models.TextField(help_text="Enter one feature per line")
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def feature_list(self):
        return [f.strip() for f in self.features.splitlines() if f.strip()]

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["display_order", "price"]


class SiteSetting(models.Model):
    site_name = models.CharField(max_length=255, default="WebBuilder")
    logo = models.ImageField(upload_to="settings/", blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    about = models.TextField(max_length=1000,blank=True,null=True)

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete("site_settings") 


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email


class ActivityLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    project_logs = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    action = models.CharField(max_length=255)
    details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.project_logs} {self.action} at {self.created_at}"


class Announcement(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Page(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    meta_description = models.CharField(max_length=255, blank=True, null=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class TeamMember(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="team_member",
        limit_choices_to={"is_staff": True},
    )
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    bio = models.TextField()
    image = models.ImageField(upload_to="team/", blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    whatsapp = models.URLField(blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hero = models.ImageField(upload_to="team/hero/", blank=True, null=True)
    skills = models.TextField(blank=True, null=True, help_text="Enter skills separated by commas")

    def skill_list(self):
        """Return skills as a list"""
        if self.skills:
            return [skill.strip() for skill in self.skills.split(',') if skill.strip()]
        return []

    def __str__(self):
        return f"{self.name} - {self.position}"

    class Meta:
        ordering = ["display_order", "name"]


class Testimonial(models.Model):
    client_name = models.CharField(max_length=255)
    client_position = models.CharField(max_length=255, blank=True, null=True)
    client_company = models.CharField(max_length=255, blank=True, null=True)
    client_image = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(
        default=5, choices=[(i, i) for i in range(1, 6)]
    )
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client_name} - {self.client_company}"

    class Meta:
        ordering = ["-is_featured", "display_order"]


class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        ordering = ["-created_at"]


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.CharField(max_length=100, blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ["display_order"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"


# --- Blog/Content Management Models ---
class BlogTag(models.Model):
    CATEGORY_CHOICES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('design', 'Design'),
        ('mobile', 'Mobile'),
        ('infrastructure', 'Infrastructure'),
        ('ai', 'AI & ML'),
        ('security', 'Security'),
        ('quality', 'Quality'),
        ('architecture', 'Architecture'),
        ('crypto', 'Blockchain & Crypto'),
        ('optimization', 'Optimization'),
        ('general', 'General'),
    ]
    
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    color = models.CharField(
        max_length=7, default="#3B82F6", help_text="Hex color code"
    )
    icon = models.CharField(
        max_length=50, blank=True, null=True, 
        help_text="FontAwesome icon class (e.g., 'fas fa-code')"
    )
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default='general'
    )
    description = models.CharField(max_length=255, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    post_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def update_post_count(self):
        """Update the post count for this tag"""
        self.post_count = self.posts.filter(status='published').count()
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["category", "name"]


class BlogPost(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
        ("archived", "Archived"),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    content = models.TextField()
    excerpt = models.CharField(
        max_length=300, help_text="Brief description for previews"
    )
    featured_image = models.ImageField(upload_to="blog/", blank=True, null=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    tags = models.ManyToManyField(BlogTag, blank=True, related_name="posts")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    is_featured = models.BooleanField(default=False)
    publish_date = models.DateTimeField(blank=True, null=True)
    meta_description = models.CharField(max_length=255, blank=True, null=True)
    read_time = models.PositiveIntegerField(default=5, help_text="Estimated reading time in minutes")
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        # Calculate read time based on content (average 200 words per minute)
        if self.content:
            word_count = len(self.content.split())
            self.read_time = max(1, word_count // 200)
        super().save(*args, **kwargs)

    def get_author_image(self):
        """Get the author's profile image from TeamMember or return None"""
        try:
            team_member = self.author.team_member
            if team_member.image:
                return team_member.image.url
        except (TeamMember.DoesNotExist, AttributeError):
            pass
        return None

    def get_author_avatar(self):
        """Get author image or return initials for avatar"""
        image_url = self.get_author_image()
        if image_url:
            return image_url
        # Return author's initials if no image
        name = self.author.get_full_name() or self.author.username
        initials = ''.join([word[0].upper() for word in name.split()[:2]])
        return initials

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-publish_date", "-created_at"]


# --- Lead Management Models ---
class Lead(models.Model):
    LEAD_STATUS = [
        ("new", "New Lead"),
        ("contacted", "Contacted"),
        ("qualified", "Qualified"),
        ("proposal", "Proposal Sent"),
        ("closed_won", "Closed Won"),
        ("closed_lost", "Closed Lost"),
    ]

    LEAD_SOURCE = [
        ("website", "Website"),
        ("referral", "Referral"),
        ("social_media", "Social Media"),
        ("google_ads", "Google Ads"),
        ("email_campaign", "Email Campaign"),
        ("phone_call", "Phone Call"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    timeline = models.CharField(max_length=100, blank=True, null=True)
    source = models.CharField(max_length=20, choices=LEAD_SOURCE, default="website")
    status = models.CharField(max_length=20, choices=LEAD_STATUS, default="new")
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_leads",
    )
    project_type = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.company or 'No Company'} ({self.status})"

    class Meta:
        ordering = ["-created_at"]


# --- Quote Management Models ---
class Quote(models.Model):
    QUOTE_STATUS = [
        ("draft", "Draft"),
        ("sent", "Sent"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("expired", "Expired"),
    ]

    quote_number = models.CharField(max_length=20, unique=True, blank=True)
    client_name = models.CharField(max_length=255)
    client_email = models.EmailField()
    client_phone = models.CharField(max_length=20, blank=True, null=True)
    client_company = models.CharField(max_length=255, blank=True, null=True)
    services = models.ManyToManyField("services.Service", through="QuoteService")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=QUOTE_STATUS, default="draft")
    valid_until = models.DateField()
    notes = models.TextField(blank=True, null=True)
    terms_conditions = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_quotes"
    )
    lead = models.ForeignKey(
        Lead, on_delete=models.SET_NULL, null=True, blank=True, related_name="quotes"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.quote_number:
            # Generate quote number like Q2025001
            from django.utils import timezone

            year = timezone.now().year
            last_quote = (
                Quote.objects.filter(quote_number__startswith=f"Q{year}")
                .order_by("-quote_number")
                .first()
            )
            if last_quote:
                last_num = int(last_quote.quote_number[-3:])
                new_num = last_num + 1
            else:
                new_num = 1
            self.quote_number = f"Q{year}{new_num:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Quote {self.quote_number} - {self.client_name}"

    class Meta:
        ordering = ["-created_at"]


class QuoteService(models.Model):
    quote = models.ForeignKey(
        Quote, on_delete=models.CASCADE, related_name="quote_services"
    )
    service = models.ForeignKey("services.Service", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Calculate total price with discount
        subtotal = self.quantity * self.unit_price
        discount_amount = subtotal * (self.discount_percentage / 100)
        self.total_price = subtotal - discount_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.service.name} x{self.quantity} - {self.quote.quote_number}"


# --- Client Dashboard Models ---
class Client(models.Model):
    INDUSTRY_CHOICES = [
        ("education", "Education"),
        ("healthcare", "Healthcare"),
        ("ecommerce", "E-Commerce"),
        ("marketing", "Marketing & Advertising"),
        ("nonprofit", "Non-Profit"),
        ("technology", "Technology"),
        ("finance", "Finance"),
        ("real_estate", "Real Estate"),
        ("hospitality", "Hospitality"),
        ("other", "Other"),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="client_profile"
    )
    company_name = models.CharField(max_length=255)
    industry = models.CharField(
        max_length=50, choices=INDUSTRY_CHOICES, default="other"
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to="client_logos/", blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"{self.company_name} - {self.user.get_full_name() or self.user.username}"
        )

    class Meta:
        ordering = ["company_name"]


# --- Analytics & Reporting Models ---
class WebsiteAnalytics(models.Model):
    date = models.DateField(unique=True)
    page_views = models.PositiveIntegerField(default=0)
    unique_visitors = models.PositiveIntegerField(default=0)
    contact_forms = models.PositiveIntegerField(default=0)
    service_requests = models.PositiveIntegerField(default=0)
    quote_requests = models.PositiveIntegerField(default=0)
    bounce_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"Analytics for {self.date}"

    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Website Analytics"


class ConversionTracking(models.Model):
    ACTION_CHOICES = [
        ("contact_form", "Contact Form Submission"),
        ("quote_request", "Quote Request"),
        ("phone_call", "Phone Call"),
        ("email_signup", "Email Signup"),
        ("service_inquiry", "Service Inquiry"),
        ("project_start", "Project Started"),
    ]

    source = models.CharField(max_length=100)  # organic, paid, social, etc.
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    page_url = models.URLField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} from {self.source} on {self.timestamp.date()}"

    class Meta:
        ordering = ["-timestamp"]
