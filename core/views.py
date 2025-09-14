from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import (
    Page,
    TeamMember,
    Testimonial,
    FAQ,
    ContactMessage,
    PricingPlan,
    BlogPost,
    BlogTag,
    Lead,
    Quote,
    Client,
    WebsiteAnalytics,
    NewsletterSubscriber,
    ActivityLog,
    SiteSetting,
)
from .forms import (
    ContactForm,
    NewsletterForm,
    LeadCaptureForm,
    QuickQuoteForm,
    CustomUserCreationForm,
)
from django.conf import settings
import os
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from services.models import Service, ServiceReview
from projects.models import Project, ProjectCollaborator
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


# Custom Error Handlers
def custom_404(request, exception):
    """Custom 404 error handler"""
    return render(request, "404.html", status=404)


def custom_500(request):
    """Custom 500 error handler"""
    return render(request, "500.html", status=500)


def custom_403(request, exception):
    """Custom 403 error handler"""
    return render(request, "403.html", status=403)


def custom_400(request, exception):
    """Custom 400 error handler"""
    return render(request, "400.html", status=400)


# Terms of Service and Privacy Policy views
def terms_of_service(request):
    return render(request, "core/terms_of_service.html")


def privacy_policy(request):
    return render(request, "core/privacy_policy.html")


# Admin dashboard section views (placeholders for custom pages)


@staff_member_required
def activity_logs(request):
    context = get_admin_base_context()
    return render(request, "admin/sections/activity_logs.html", context)


def get_admin_base_context():
    """Get base context for admin dashboard and its sections"""
    from django.contrib.auth import get_user_model
    from projects.models import Project
    from services.models import Service, ServiceRequest, ServiceReview
    from core.models import ContactMessage, Announcement, TeamMember, Testimonial

    User = get_user_model()

    return {
        "user_count": User.objects.count(),
        "project_count": Project.objects.count(),
        "service_count": Service.objects.count(),
        "message_count": ContactMessage.objects.filter(status="new").count(),
        "announcements_count": Announcement.objects.filter(is_active=True).count(),
        "recent_projects": Project.objects.all().order_by("-created_at")[:5],
        "recent_services": Service.objects.all().order_by("-created_at")[:5],
        "recent_messages": ContactMessage.objects.filter(status="new").order_by(
            "-created_at"
        )[:5],
        "team_members": TeamMember.objects.filter(is_active=True).order_by(
            "display_order"
        )[:8],
        "testimonials": Testimonial.objects.filter(is_featured=True, is_active=True)[
            :3
        ],
        "latest_announcement": Announcement.objects.filter(is_active=True)
        .order_by("-created_at")
        .first(),
        "total_reviews": ServiceReview.objects.count(),
        "active_services": Service.objects.filter(is_active=True).count(),
        "pending_requests": ServiceRequest.objects.filter(status="pending").count(),
    }


@staff_member_required
def announcements(request):
    context = get_admin_base_context()
    return render(request, "admin/sections/announcements.html", context)


@staff_member_required
def contact_messages(request):
    context = get_admin_base_context()
    return render(request, "admin/sections/contact_messages.html", context)


@staff_member_required
def leads(request):
    from django.core.paginator import Paginator
    from django.db.models import Count, Q

    # Get all leads
    leads_list = Lead.objects.all().order_by("-created_at")

    # Calculate statistics
    total_leads = Lead.objects.count()
    new_leads = Lead.objects.filter(status="new").count()
    qualified_leads = Lead.objects.filter(status="qualified").count()
    closed_won_leads = Lead.objects.filter(status="closed_won").count()

    # Calculate conversion rate
    conversion_rate = 0
    if total_leads > 0:
        conversion_rate = round((closed_won_leads / total_leads) * 100, 1)

    # Pagination
    paginator = Paginator(leads_list, 25)  # Show 25 leads per page
    page_number = request.GET.get("page")
    leads = paginator.get_page(page_number)

    context = get_admin_base_context()
    context.update(
        {
            "leads": leads,
            "total_leads": total_leads,
            "new_leads": new_leads,
            "qualified_leads": qualified_leads,
            "conversion_rate": conversion_rate,
        }
    )
    return render(request, "admin/sections/leads.html", context)


@staff_member_required
def faqs(request):
    context = get_admin_base_context()
    return render(request, "admin/sections/faqs.html", context)


@staff_member_required
def newsletter_subscribers(request):
    context = get_admin_base_context()
    return render(request, "admin/sections/newsletter_subscribers.html", context)


@staff_member_required
def pages(request):
    context = get_admin_base_context()
    return render(request, "admin/sections/pages.html", context)


@staff_member_required
def pricing_plans(request):
    context = get_admin_base_context()
    return render(request, "admin/sections/pricing_plans.html", context)


@staff_member_required
def site_settings(request):
    context = get_admin_base_context()
    return render(request, "admin/sections/site_settings.html", context)


@staff_member_required
def team_members(request):
    context = get_admin_base_context()
    return render(request, "admin/sections/team_members.html", context)


@staff_member_required
def testimonials(request):
    context = get_admin_base_context()
    return render(request, "admin/sections/testimonials.html", context)


# User dashboard view


@login_required
def dashboard(request):
    from services.models import Service

    services = Service.objects.filter(is_active=True)
    return render(request, "core/dashboard.html", {"services": services})


from django.contrib.auth.decorators import user_passes_test


# Admin dashboard view
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def admin_dashboard(request):
    context = get_admin_base_context()
    return render(request, "admin/admin_dashboard.html", context)


@require_POST
def custom_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")


def pricing(request):
    """View for the pricing page"""
    plans = PricingPlan.objects.filter(is_active=True).order_by(
        "display_order", "price"
    )
    site_setting = SiteSetting.objects.all()

    if site_setting:
        for setting in site_setting:
            site_name = setting.site_name
            facebook = setting.facebook
            twitter = setting.twitter
            instagram = setting.instagram
            linkedin = setting.linkedin
            mail = setting.contact_email
            tel = setting.contact_phone
            address = setting.address
            logo = setting.logo

    context = {"plans": plans, "setting": setting}
    return render(request, "core/pricing.html", context)


# Create your views here.
def home(request):
    """View for the homepage"""
    # Get featured services
    featured_services = Service.objects.filter(is_featured=True, is_active=True)[:3]

    # Get testimonials
    testimonials = Testimonial.objects.filter(is_active=True)[:6]

    # Get team members
    team_members = TeamMember.objects.filter(is_active=True)[:6]

    featured_projects = Project.objects.filter(is_featured=True, status="completed").exclude(slug__isnull=True)[:6]

    # Get FAQs
    faqs = FAQ.objects.filter(is_active=True)[:6]

    # Get recent blog post
    recent_posts = BlogPost.objects.filter(status="published").order_by(
        "-publish_date"
    )[:6]

    context = {
        "featured_services": featured_services,
        "testimonials": testimonials,
        "team_members": team_members,
        "featured_projects": featured_projects,
        "faqs": faqs,
        "recent_posts": recent_posts,
    }

    return render(request, "core/home.html", context)


def about(request):
    """View for the about page"""
    # Get team members
    team_members = TeamMember.objects.filter(is_active=True)

    context = {
        "team_members": team_members,
    }

    return render(request, "core/about.html", context)


def contact(request):
    """View for the contact page with file upload support"""
    if request.method == "POST":
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            contact_message = form.save(commit=False)
            attachment = request.FILES.get("attachment")
            if attachment:
                # Save file to media/contact_attachments/
                upload_dir = os.path.join(settings.MEDIA_ROOT, "contact_attachments")
                os.makedirs(upload_dir, exist_ok=True)
                file_path = os.path.join("contact_attachments", attachment.name)
                abs_path = os.path.join(settings.MEDIA_ROOT, file_path)
                with open(abs_path, "wb+") as destination:
                    for chunk in attachment.chunks():
                        destination.write(chunk)
                # Store file path in notes field for now
                contact_message.notes = f"Attachment: {file_path}"
            contact_message.save()
            return render(request, "core/contact_success.html")
    else:
        form = ContactForm()

    return render(
        request,
        "core/contact.html",
        {
            "form": form,
        },
    )


def faq(request):
    """View for the FAQ page"""
    # Get FAQs
    faqs = FAQ.objects.filter(is_active=True)


    context = {"faqs": faqs,}

    return render(request, "core/faq.html", context)


class PageDetailView(DetailView):
    """View for displaying a static page"""

    model = Page
    template_name = "core/page.html"
    context_object_name = "page"

    def get_queryset(self):
        return Page.objects.filter(is_published=True)


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("core:home")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("core:home")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect("core:home")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


def team_member_details(request, slug):
    team_member = get_object_or_404(TeamMember, id=slug)

    # Projects where this team member is a collaborator (if TeamMember is linked to a User)
    from projects.models import Project, ProjectCollaborator

    user = getattr(team_member, "user", None)
    if user:
        projects = Project.objects.filter(collaborators=user).distinct()
    else:
        projects = Project.objects.none()

    # Testimonials for this team member (assuming Testimonial has a ForeignKey or similar relation)
    from core.models import Testimonial

    testimonials = Testimonial.objects.filter(client_name__icontains=team_member.name)

    # Services (if any logic, e.g., by position or explicit relation)
    from services.models import Service

    services = Service.objects.filter(
        is_active=True, description__icontains=team_member.position
    )

    context = {
        "team_member": team_member,
        "projects": projects,
        "testimonials": testimonials,
        "services": services,
    }
    return render(request, "team/team_details.html", context)


@staff_member_required
def profile(request, slug):
    team_member = get_object_or_404(TeamMember, id=slug)
    user = team_member.user

    # Handle case where team member has no associated user
    if not user:
        context = {
            "profile_user": None,
            "team_member": team_member,
            "is_own_profile": False,
            "collaborated_projects": [],
            "recent_activities": [],
            "user_reviews": [],
            "stats": {
                "projects_count": 0,
                "reviews_count": 0,
                "activities_count": 0,
                "member_since": (
                    team_member.created_at
                    if hasattr(team_member, "created_at")
                    else None
                ),
                "last_active": None,
            },
        }
        return render(request, "core/profile.html", context)

    # Get user's projects
    collaborated_projects = (
        ProjectCollaborator.objects.filter(user=user)
        .select_related("project")
        .order_by("-added_at")[:5]
    )

    # Get user's recent activity
    recent_activities = ActivityLog.objects.filter(user=user).order_by("-created_at")[
        :10
    ]

    # Get user's service reviews
    user_reviews = (
        ServiceReview.objects.filter(user=user)
        .select_related("service")
        .order_by("-created_at")[:5]
    )

    # Profile statistics
    stats = {
        "projects_count": ProjectCollaborator.objects.filter(user=user).count(),
        "reviews_count": ServiceReview.objects.filter(user=user).count(),
        "activities_count": ActivityLog.objects.filter(user=user).count(),
        "member_since": user.date_joined,
        "last_active": user.last_login,
    }

    context = {
        "profile_user": user,
        "team_member": team_member,
        "is_own_profile": request.user == user,
        "collaborated_projects": collaborated_projects,
        "recent_activities": recent_activities,
        "user_reviews": user_reviews,
        "stats": stats,
    }

    return render(request, "core/profile.html", context)


# --- New Views for Enhanced Features ---


def lead_capture(request):
    """Lead capture form view"""
    if request.method == "POST":
        form = LeadCaptureForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.source = "website"
            lead.save()

            # Track conversion
            from .models import ConversionTracking

            ConversionTracking.objects.create(
                source="website",
                action="contact_form",
                lead=lead,
                page_url=request.build_absolute_uri(),
            )

            messages.success(
                request,
                "Thank you! We've received your inquiry and will contact you soon.",
            )
            return redirect("core:lead_capture")
    else:
        form = LeadCaptureForm()

    return render(request, "core/lead_capture.html", {"form": form})


def quick_quote(request):
    """Quick quote request form"""
    if request.method == "POST":
        form = QuickQuoteForm(request.POST)
        if form.is_valid():
            # Create a lead from the quote form
            lead = Lead.objects.create(
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                phone=form.cleaned_data.get("phone", ""),
                company=form.cleaned_data.get("company", ""),
                timeline=form.cleaned_data["timeline"],
                project_type=form.cleaned_data["project_type"],
                message=form.cleaned_data["message"],
                source="website",
                status="new",
            )

            # Extract budget from budget_range
            budget_range = form.cleaned_data["budget_range"]
            if budget_range == "5000-10000":
                lead.budget = 7500
            elif budget_range == "10000-25000":
                lead.budget = 17500
            elif budget_range == "25000-50000":
                lead.budget = 37500
            elif budget_range == "50000+":
                lead.budget = 75000
            lead.save()

            # Track conversion
            from .models import ConversionTracking

            ConversionTracking.objects.create(
                source="website",
                action="quote_request",
                lead=lead,
                page_url=request.build_absolute_uri(),
            )

            messages.success(
                request,
                "Quote request submitted! We'll prepare a custom quote and send it to you within 24 hours.",
            )
            return redirect("core:quick_quote")
    else:
        form = QuickQuoteForm()

    return render(request, "core/quick_quote.html", {"form": form})


# Blog Views
def blog_home(request):
    """Blog home page with featured posts and recent posts"""
    featured_posts = BlogPost.objects.filter(
        status="published", is_featured=True
    ).order_by("-publish_date")[:3]

    recent_posts = BlogPost.objects.filter(status="published").order_by(
        "-publish_date"
    )[:6]

    popular_tags = BlogTag.objects.all()[:8]

    context = {
        "featured_posts": featured_posts,
        "recent_posts": recent_posts,
        "popular_tags": popular_tags,
    }

    return render(request, "core/blog_home.html", context)


def blog_list(request):
    """Blog list with pagination and filtering"""
    posts = BlogPost.objects.filter(status="published").order_by("-publish_date")

    # Search functionality
    search_query = request.GET.get("search")
    if search_query:
        from django.db.models import Q

        posts = posts.filter(
            Q(title__icontains=search_query)
            | Q(content__icontains=search_query)
            | Q(excerpt__icontains=search_query)
        )

    # Tag filtering
    tag_slug = request.GET.get("tag")
    selected_tag = None
    if tag_slug:
        selected_tag = get_object_or_404(BlogTag, slug=tag_slug)
        posts = posts.filter(tags=selected_tag)

    # Pagination
    from django.core.paginator import Paginator

    paginator = Paginator(posts, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "posts": page_obj,
        "is_paginated": page_obj.has_other_pages(),
        "featured_posts": BlogPost.objects.filter(status="published", is_featured=True)[
            :3
        ],
        "all_tags": BlogTag.objects.all(),
        "tags": BlogTag.objects.all(),  # For backward compatibility
        "selected_tag": selected_tag,
        "search_query": search_query or "",
        "current_tag": tag_slug or "",
    }

    return render(request, "core/blog_list.html", context)


def blog_detail(request, slug):
    """Blog post detail view"""
    post = get_object_or_404(BlogPost, slug=slug, status="published")

    # Get related posts by tags
    related_posts = (
        BlogPost.objects.filter(status="published", tags__in=post.tags.all())
        .exclude(id=post.id)
        .distinct()[:3]
    )

    # Get recent posts for sidebar
    recent_posts = (
        BlogPost.objects.filter(status="published")
        .exclude(id=post.id)
        .order_by("-publish_date")[:5]
    )

    context = {
        "post": post,
        "related_posts": related_posts,
        "recent_posts": recent_posts,
        "all_tags": BlogTag.objects.all(),
    }
    return render(request, "core/blog_detail.html", context)


# Portfolio Views with Technologies
def portfolio_list(request):
    """Enhanced portfolio list with technology filtering"""
    projects = Project.objects.filter(is_featured=True).order_by("-created_at")

    # Technology filtering
    tech_slug = request.GET.get("tech")
    if tech_slug:
        from projects.models import Technology

        projects = projects.filter(technologies__technology__slug=tech_slug)

    # Get all technologies for filter
    from projects.models import Technology

    all_technologies = Technology.objects.filter(is_active=True).order_by(
        "category", "name"
    )

    context = {
        "projects": projects,
        "all_technologies": all_technologies,
        "current_tech": tech_slug or "",
    }

    return render(request, "projects/portfolio_list.html", context)


@csrf_exempt
def api_newsletter_signup(request):
    """API endpoint for newsletter signup"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")

            if email:
                from .models import NewsletterSubscriber

                subscriber, created = NewsletterSubscriber.objects.get_or_create(
                    email=email, defaults={"is_active": True}
                )

                if created:
                    return JsonResponse(
                        {
                            "success": True,
                            "message": "Successfully subscribed to newsletter!",
                        }
                    )
                else:
                    return JsonResponse(
                        {"success": False, "message": "Email already subscribed."}
                    )
            else:
                return JsonResponse({"success": False, "message": "Email is required."})
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid data format."})

    return JsonResponse({"success": False, "message": "Method not allowed."})


def newsletter_subscribe(request):
    """Handle newsletter subscription from forms"""
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            subscriber, created = NewsletterSubscriber.objects.get_or_create(
                email=email, defaults={"is_active": True}
            )
            if created:
                messages.success(request, "Successfully subscribed to our newsletter!")
            else:
                messages.info(request, "You are already subscribed to our newsletter.")
        else:
            messages.error(request, "Please provide a valid email address.")

    # Redirect back to the referring page or blog list
    return redirect(request.META.get("HTTP_REFERER", "blog_list"))
