from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse


# Create your models here.
class Project(models.Model):
    PROJECT_STATUS_CHOICES = [
        ("inquiry", "Inquiry"),
        ("proposal", "Proposal"),
        ("in_progress", "In Progress"),
        ("review", "Review"),
        ("completed", "Completed"),
        ("maintenance", "Maintenance"),
    ]

    PROJECT_TYPE_CHOICES = [
        ("school", "School Website"),
        ("hospital", "Hospital Website"),
        ("ecommerce", "E-Commerce Website"),
        ("marketing", "Marketing Website"),
        ("portfolio", "Portfolio Website"),
        ("blog", "Blog Website"),
        ("custom", "Custom Solution"),
    ]

    # Client Information
    client_name = models.CharField(max_length=255)
    client_email = models.EmailField()
    client_phone = models.CharField(max_length=20, blank=True, null=True)
    organization_name = models.CharField(max_length=255)

    # Project Details
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    description = models.TextField()
    project_type = models.CharField(
        max_length=20, choices=PROJECT_TYPE_CHOICES, default="custom"
    )
    requirements = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to="projects",
        height_field=None,
        width_field=None,
        max_length=None,
        null=True,
    )

    # Dates
    start_date = models.DateField(default=timezone.now)
    deadline = models.DateField(blank=True, null=True)
    completed_date = models.DateField(blank=True, null=True)

    # Status and Management
    status = models.CharField(
        max_length=20, choices=PROJECT_STATUS_CHOICES, default="inquiry"
    )
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Website Information
    domain_name = models.CharField(max_length=255, blank=True, null=True)
    hosting_provider = models.CharField(max_length=255, blank=True, null=True)
    is_featured = models.BooleanField(default=False)


    # Collaborators (ManyToMany for easier assignment, through ProjectCollaborator)
    collaborators = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='ProjectCollaborator',
        related_name='collaborating_projects',
        blank=True
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.client_name} - {self.project_type}"

    def save(self, *args, **kwargs):
        """Auto-generate slug from title if not provided"""
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return the URL for this project"""
        return reverse('projects:detail', kwargs={'slug': self.slug})

    def add_collaborator(self, user, role=None):
        """Add a collaborator to this project"""
        collaborator, created = ProjectCollaborator.objects.get_or_create(
            project=self,
            user=user,
            defaults={'role': role or 'Collaborator'}
        )
        return collaborator, created

    def remove_collaborator(self, user):
        """Remove a collaborator from this project"""
        return ProjectCollaborator.objects.filter(project=self, user=user).delete()

    def get_collaborators(self):
        """Get all collaborators for this project"""
        return self.projectcollaborator_set.select_related('user').all()

    def get_collaborator_count(self):
        """Get the number of collaborators for this project"""
        return self.projectcollaborator_set.count()

    class Meta:
        ordering = ["-created_at"]


# --- Additional Professional Models ---
class ProjectAttachment(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="attachments"
    )
    file = models.FileField(upload_to="project_attachments/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"Attachment for {self.project.title} ({self.file.name})"


class ProjectNote(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="notes")
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"Note for {self.project.title} by {self.created_by}"


class ProjectMilestone(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="milestones"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({'Completed' if self.completed else 'Pending'})"


class ProjectCollaborator(models.Model):
    ROLE_CHOICES = [
        ('project_manager', 'Project Manager'),
        ('lead_developer', 'Lead Developer'),
        ('frontend_developer', 'Frontend Developer'),
        ('backend_developer', 'Backend Developer'),
        ('ui_ux_designer', 'UI/UX Designer'),
        ('qa_tester', 'Quality Assurance'),
        ('devops_engineer', 'DevOps Engineer'),
        ('consultant', 'Consultant'),
        ('collaborator', 'Collaborator'),
    ]
    
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"is_staff": True}
    )
    role = models.CharField(
        max_length=100, 
        choices=ROLE_CHOICES,
        default='collaborator',
        blank=True, 
        null=True
    )
    added_at = models.DateTimeField(auto_now_add=True)
    is_lead = models.BooleanField(default=False, help_text="Is this collaborator the project lead?")

    def __str__(self):
        return f"{self.user} on {self.project.title} as {self.get_role_display()}"

    class Meta:
        unique_together = ['project', 'user']  # Prevent duplicate collaborators
        ordering = ['-is_lead', 'added_at']


# --- Portfolio Enhancement Models ---
class Technology(models.Model):
    CATEGORY_CHOICES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('database', 'Database'),
        ('cms', 'CMS'),
        ('framework', 'Framework'),
        ('tool', 'Development Tool'),
        ('hosting', 'Hosting/Deployment'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    icon = models.CharField(max_length=50, help_text="Font Awesome or DevIcon class name")
    color = models.CharField(max_length=7, default="#3B82F6", help_text="Hex color code")
    description = models.TextField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['category', 'display_order', 'name']
        verbose_name_plural = "Technologies"


class ProjectTechnology(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='technologies')
    technology = models.ForeignKey(Technology, on_delete=models.CASCADE)
    importance = models.CharField(max_length=20, choices=[
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('tool', 'Development Tool')
    ], default='secondary')
    
    def __str__(self):
        return f"{self.project.title} - {self.technology.name}"
    
    class Meta:
        unique_together = ['project', 'technology']


class ProjectImage(models.Model):
    IMAGE_TYPE_CHOICES = [
        ('screenshot', 'Screenshot'),
        ('mockup', 'Mockup'),
        ('process', 'Process Image'),
        ('before_after', 'Before/After'),
        ('feature', 'Feature Highlight'),
        ('other', 'Other'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='project_gallery/')
    image_type = models.CharField(max_length=20, choices=IMAGE_TYPE_CHOICES, default='screenshot')
    caption = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.project.title} - {self.image_type}"
    
    class Meta:
        ordering = ['display_order', 'uploaded_at']


class ProjectTestimonial(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='testimonial')
    client_feedback = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    client_name = models.CharField(max_length=255)
    client_position = models.CharField(max_length=255, blank=True, null=True)
    client_image = models.ImageField(upload_to='project_testimonials/', blank=True, null=True)
    is_approved = models.BooleanField(default=True)
    featured_quote = models.CharField(max_length=255, blank=True, null=True, help_text="Short quote for highlights")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Testimonial for {self.project.title} by {self.client_name}"


class ProjectMetrics(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='metrics')
    # Performance metrics
    page_load_time = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Seconds")
    lighthouse_score = models.PositiveSmallIntegerField(null=True, blank=True, help_text="0-100")
    mobile_friendly = models.BooleanField(default=True)
    
    # Business metrics
    traffic_increase = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Percentage")
    conversion_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Percentage")
    bounce_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Percentage")
    
    # Development metrics
    development_hours = models.PositiveIntegerField(null=True, blank=True)
    lines_of_code = models.PositiveIntegerField(null=True, blank=True)
    
    # SEO metrics
    seo_score = models.PositiveSmallIntegerField(null=True, blank=True, help_text="0-100")
    keywords_ranking = models.PositiveIntegerField(null=True, blank=True, help_text="Number of keywords in top 10")
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Metrics for {self.project.title}"


# --- Client Project Access ---
class ClientProject(models.Model):
    ACCESS_LEVEL_CHOICES = [
        ('view', 'View Only'),
        ('comment', 'View & Comment'),
        ('collaborate', 'Full Collaboration'),
    ]
    
    client = models.ForeignKey('core.Client', on_delete=models.CASCADE, related_name='client_projects')
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='client_access')
    access_level = models.CharField(max_length=20, choices=ACCESS_LEVEL_CHOICES, default='view')
    client_access_enabled = models.BooleanField(default=True)
    access_granted_at = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.client.company_name} access to {self.project.title}"
