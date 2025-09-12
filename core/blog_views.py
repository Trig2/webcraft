# Blog views
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import BlogPost, BlogTag
from django.views.generic import ListView, DetailView
from core.models import SiteSetting


class BlogListView(ListView):
    model = BlogPost
    template_name = "core/blog_list.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site_setting = SiteSetting.objects.first()
        if site_setting:
          context.update({
              "site_name":site_setting.site_name
          })
        return context

        print(context)

    def get_queryset(self):
        queryset = BlogPost.objects.filter(status="published").prefetch_related("tags")

        # Search functionality
        search_query = self.request.GET.get("search")
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query)
                | Q(content__icontains=search_query)
                | Q(excerpt__icontains=search_query)
            )

        # Tag filtering
        tag_slug = self.request.GET.get("tag")
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)

        return queryset.order_by("-publish_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_posts"] = BlogPost.objects.filter(
            status="published", is_featured=True
        )[:3]
        context["all_tags"] = BlogTag.objects.all()
        context["search_query"] = self.request.GET.get("search", "")
        context["current_tag"] = self.request.GET.get("tag", "")

        # Add selected_tag object for enhanced tags component
        tag_slug = self.request.GET.get("tag")
        if tag_slug:
            try:
                context["selected_tag"] = BlogTag.objects.get(slug=tag_slug)
            except BlogTag.DoesNotExist:
                context["selected_tag"] = None
        else:
            context["selected_tag"] = None

        return context


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = "core/blog_detail.html"
    context_object_name = "post"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return BlogPost.objects.filter(status="published")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get related posts by tags
        post = self.get_object()
        related_posts = (
            BlogPost.objects.filter(status="published", tags__in=post.tags.all())
            .exclude(id=post.id)
            .distinct()[:3]
        )

        context["related_posts"] = related_posts
        context["all_tags"] = BlogTag.objects.all()
        return context


def blog_home(request):
    """Blog home page with featured posts and recent posts"""
    featured_posts = BlogPost.objects.filter(
        status="published", is_featured=True
    ).order_by("-publish_date")[:3]

    recent_posts = BlogPost.objects.filter(status="published").order_by(
        "-publish_date"
    )[:6]

    popular_tags = BlogTag.objects.all()[:8]

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
            about = setting.about

    context = {
        "featured_posts": featured_posts,
        "recent_posts": recent_posts,
        "popular_tags": popular_tags,
        "setting": setting,
    }

    return render(request, "core/blog_home.html", context)


def blog_tags(request):
    """Blog tags page showing all tags organized by category"""

    # Get all tags ordered by category and post count
    all_tags = BlogTag.objects.all().order_by("category", "-post_count")

    # Get popular tags (top 10 by post count)
    popular_tags = all_tags.filter(post_count__gt=0)[:10]

    # Get featured tags
    featured_tags = BlogTag.objects.filter(is_featured=True)

    # Statistics
    total_tags = all_tags.count()
    total_posts = BlogPost.objects.filter(status="published").count()
    categories_count = all_tags.values("category").distinct().count()

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
            about = setting.about

    context = {
        "all_tags": all_tags,
        "popular_tags": popular_tags,
        "featured_tags": featured_tags,
        "total_tags": total_tags,
        "total_posts": total_posts,
        "categories_count": categories_count,
        "setting": setting,
    }

    return render(request, "core/tags.html", context)
