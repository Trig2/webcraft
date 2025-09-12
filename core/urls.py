from django.urls import path,include
from . import views
from .views import custom_logout
from . import views
from .blog_views import BlogListView, BlogDetailView, blog_home, blog_tags
from . import profile_views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("faq/", views.faq, name="faq"),
    path("pricing/", views.pricing, name="pricing"),
    path("page/<slug:slug>/", views.PageDetailView.as_view(), name="page"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", custom_logout, name="logout"),
    # path('dashboard/', views.dashboard, name='dashboard'),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    
    # New enhanced features
    path("lead-capture/", views.lead_capture, name="lead_capture"),
    path("quick-quote/", views.quick_quote, name="quick_quote"),
    path("api/newsletter/", views.api_newsletter_signup, name="api_newsletter"),
    path("newsletter/subscribe/", views.newsletter_subscribe, name="newsletter_subscribe"),
    
    # Blog URLs
    path("blog/", BlogListView.as_view(), name="blog_list"),
    path("blog/home/", blog_home, name="blog_home"),
    path("blog/tags/", blog_tags, name="blog_tags"),
    path("blog/<slug:slug>/", BlogDetailView.as_view(), name="blog_detail"),
    
    # Portfolio with tech filtering
    path("portfolio/", views.portfolio_list, name="portfolio_list"),
    
    # Legal pages
    path("terms-of-service/", views.terms_of_service, name="terms_of_service"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    # Admin dashboard core section routes
    path("admin-dashboard/activity-logs/", views.activity_logs, name="activity_logs"),
    path("admin-dashboard/announcements/", views.announcements, name="announcements"),
    path(
        "admin-dashboard/contact-messages/",
        views.contact_messages,
        name="contact_messages",
    ),
    path("admin-dashboard/leads/", views.leads, name="leads"),
    path("admin-dashboard/faqs/", views.faqs, name="faqs"),
    path(
        "admin-dashboard/newsletter-subscribers/",
        views.newsletter_subscribers,
        name="newsletter_subscribers",
    ),
    path("admin-dashboard/pages/", views.pages, name="pages"),
    path("admin-dashboard/pricing-plans/", views.pricing_plans, name="pricing_plans"),
    path("admin-dashboard/site-settings/", views.site_settings, name="site_settings"),
    path("admin-dashboard/team-members/", views.team_members, name="team_members"),
    path("admin-dashboard/testimonials/", views.testimonials, name="testimonials"),

    path("team/<slug:slug>/profile", views.team_member_details,name="team_profile"),

    path("developer/<slug:slug>/", views.profile, name="developer_profile"),
    
    # User Profile URLs
    path("profile/", profile_views.profile_view, name="profile"),
    path("profile/edit/", profile_views.profile_edit, name="profile_edit"),
    path("profile/activity/", profile_views.profile_activity, name="profile_activity"),
    path("profile/projects/", profile_views.profile_projects, name="profile_projects"),
    path("profile/settings/", profile_views.profile_settings, name="profile_settings"),
    path("profiles/", profile_views.public_profiles, name="public_profiles"),

]
