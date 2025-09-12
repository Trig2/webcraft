from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
import random

from core.models import (
    BlogTag,
    BlogPost,
    Lead,
    Quote,
    Client,
    WebsiteAnalytics,
    ConversionTracking,
    FAQ,
    Testimonial,
)
from projects.models import (
    Project,
    ProjectTechnology,
    ProjectImage,
    ProjectMetrics,
    Technology,
)
from services.models import Service


class Command(BaseCommand):
    help = "Create sample data for WebBuilder website"

    def handle(self, *args, **options):
        self.stdout.write("Creating sample data...")

        # Create sample blog tags
        self.create_blog_tags()

        # Create sample blog posts
        self.create_blog_posts()

        # Create sample technologies
        self.create_technologies()

        # Create sample leads
        self.create_leads()

        # Create sample analytics data
        self.create_analytics()

        # Create sample FAQs
        self.create_faqs()

        # Create sample testimonials
        self.create_testimonials()

        self.stdout.write(self.style.SUCCESS("Successfully created sample data!"))

    def create_blog_tags(self):
        tags_data = [
            ("Web Development", "#3B82F6"),
            ("Django", "#092E20"),
            ("React", "#61DAFB"),
            ("SEO", "#10B981"),
            ("UI/UX Design", "#8B5CF6"),
            ("E-commerce", "#F59E0B"),
            ("WordPress", "#21759B"),
            ("Performance", "#EF4444"),
            ("Security", "#6B7280"),
            ("Mobile", "#06B6D4"),
        ]

        for name, color in tags_data:
            tag, created = BlogTag.objects.get_or_create(
                name=name, defaults={"color": color}
            )
            if created:
                self.stdout.write(f"Created blog tag: {name}")

    def create_blog_posts(self):
        # Get admin user or create one
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.create_superuser(
                "admin", "admin@webbuilder.com", "admin123"
            )

        posts_data = [
            {
                "title": "10 Essential Web Development Trends for 2025",
                "excerpt": "Discover the latest trends shaping the future of web development, from AI integration to progressive web apps.",
                "content": """
<h2>The Future is Here</h2>
<p>Web development is evolving rapidly, and staying ahead of the curve is crucial for success. Here are the top 10 trends that will dominate 2025:</p>

<h3>1. AI-Powered Development</h3>
<p>Artificial Intelligence is revolutionizing how we build websites. From automated code generation to intelligent testing, AI tools are becoming indispensable.</p>

<h3>2. Progressive Web Apps (PWAs)</h3>
<p>PWAs continue to bridge the gap between web and mobile apps, offering native-like experiences with web technologies.</p>

<h3>3. Serverless Architecture</h3>
<p>Serverless computing is gaining traction for its scalability and cost-effectiveness, allowing developers to focus on code rather than infrastructure.</p>

<h3>4. WebAssembly Integration</h3>
<p>WebAssembly enables high-performance applications in the browser, opening new possibilities for complex web applications.</p>

<h3>5. Advanced CSS Features</h3>
<p>CSS Grid, Flexbox, and new properties like Container Queries are making responsive design more powerful and intuitive.</p>
                """,
                "tags": ["Web Development", "SEO", "Performance"],
                "is_featured": True,
            },
            {
                "title": "Building Scalable E-commerce Solutions with Django",
                "excerpt": "Learn how to create robust e-commerce platforms using Django framework with best practices and optimization techniques.",
                "content": """
<h2>Why Django for E-commerce?</h2>
<p>Django provides a solid foundation for building scalable e-commerce solutions. Its batteries-included approach and robust security features make it ideal for handling sensitive customer data and transactions.</p>

<h3>Key Features to Implement</h3>
<ul>
    <li>User authentication and profiles</li>
    <li>Product catalog management</li>
    <li>Shopping cart functionality</li>
    <li>Payment gateway integration</li>
    <li>Order management system</li>
    <li>Inventory tracking</li>
</ul>

<h3>Performance Optimization</h3>
<p>Optimize your Django e-commerce site with caching strategies, database indexing, and CDN integration for faster load times.</p>
                """,
                "tags": ["Django", "E-commerce", "Web Development"],
                "is_featured": False,
            },
            {
                "title": "The Complete Guide to React Performance Optimization",
                "excerpt": "Master React performance optimization techniques to build lightning-fast user interfaces that scale.",
                "content": """
<h2>React Performance Fundamentals</h2>
<p>Building performant React applications requires understanding the framework's rendering behavior and implementing optimization strategies.</p>

<h3>Key Optimization Techniques</h3>
<h4>1. Memoization</h4>
<p>Use React.memo, useMemo, and useCallback to prevent unnecessary re-renders.</p>

<h4>2. Code Splitting</h4>
<p>Implement lazy loading and dynamic imports to reduce initial bundle size.</p>

<h4>3. Virtual Scrolling</h4>
<p>Handle large lists efficiently with windowing techniques.</p>

<h4>4. State Management</h4>
<p>Optimize state structure and avoid unnecessary global state.</p>
                """,
                "tags": ["React", "Performance", "Web Development"],
                "is_featured": True,
            },
        ]

        for post_data in posts_data:
            # Create blog post
            post, created = BlogPost.objects.get_or_create(
                title=post_data["title"],
                defaults={
                    "excerpt": post_data["excerpt"],
                    "content": post_data["content"],
                    "author": admin_user,
                    "status": "published",
                    "is_featured": post_data["is_featured"],
                    "publish_date": timezone.now()
                    - timedelta(days=random.randint(1, 30)),
                },
            )

            if created:
                # Add tags
                for tag_name in post_data["tags"]:
                    tag = BlogTag.objects.get(name=tag_name)
                    post.tags.add(tag)

                self.stdout.write(f"Created blog post: {post.title}")

    def create_technologies(self):
        tech_data = [
            ("Python", "backend", "fab fa-python", "#3776AB"),
            ("Django", "framework", "fas fa-server", "#092E20"),
            ("JavaScript", "frontend", "fab fa-js-square", "#F7DF1E"),
            ("React", "frontend", "fab fa-react", "#61DAFB"),
            ("HTML5", "frontend", "fab fa-html5", "#E34F26"),
            ("CSS3", "frontend", "fab fa-css3-alt", "#1572B6"),
            ("PostgreSQL", "database", "fas fa-database", "#336791"),
            ("MySQL", "database", "fas fa-database", "#4479A1"),
            ("Docker", "tool", "fab fa-docker", "#2496ED"),
            ("Git", "tool", "fab fa-git-alt", "#F05032"),
            ("AWS", "hosting", "fab fa-aws", "#232F3E"),
            ("Nginx", "hosting", "fas fa-server", "#009639"),
        ]

        for name, category, icon, color in tech_data:
            tech, created = Technology.objects.get_or_create(
                name=name,
                defaults={
                    "category": category,
                    "icon": icon,
                    "color": color,
                    "is_active": True,
                },
            )
            if created:
                self.stdout.write(f"Created technology: {name}")

    def create_leads(self):
        leads_data = [
            {
                "name": "Sarah Johnson",
                "email": "sarah@lincolnhigh.edu",
                "company": "Lincoln High School",
                "budget": 15000,
                "timeline": "3 months",
                "source": "website",
                "status": "qualified",
                "project_type": "School Website",
                "message": "We need a new website for our school with student portal and event management.",
            },
            {
                "name": "Michael Chen",
                "email": "mike@urbanstyles.com",
                "company": "Urban Styles",
                "budget": 25000,
                "timeline": "2 months",
                "source": "referral",
                "status": "proposal",
                "project_type": "E-commerce Website",
                "message": "Looking to revamp our online store with better UX and mobile optimization.",
            },
            {
                "name": "Dr. Emily Rodriguez",
                "email": "emily@cityhospital.org",
                "company": "City General Hospital",
                "budget": 35000,
                "timeline": "4 months",
                "source": "google_ads",
                "status": "closed_won",
                "project_type": "Hospital Website",
                "message": "Need a comprehensive hospital website with patient portal and appointment booking.",
            },
        ]

        for lead_data in leads_data:
            lead, created = Lead.objects.get_or_create(
                email=lead_data["email"], defaults=lead_data
            )
            if created:
                self.stdout.write(f"Created lead: {lead.name}")

    def create_analytics(self):
        # Create analytics data for the last 30 days
        for i in range(30):
            date = timezone.now().date() - timedelta(days=i)
            analytics, created = WebsiteAnalytics.objects.get_or_create(
                date=date,
                defaults={
                    "page_views": random.randint(100, 500),
                    "unique_visitors": random.randint(50, 200),
                    "contact_forms": random.randint(2, 15),
                    "service_requests": random.randint(1, 8),
                    "quote_requests": random.randint(1, 5),
                    "bounce_rate": round(random.uniform(25.0, 65.0), 2),
                },
            )
            if created and i % 10 == 0:  # Log every 10th day to avoid spam
                self.stdout.write(f"Created analytics for: {date}")

    def create_faqs(self):
        faq_data = [
            {
                "question": "How long does it take to build a website?",
                "answer": "The timeline depends on the complexity of your project. A simple website typically takes 2-4 weeks, while complex e-commerce or custom solutions may take 2-4 months.",
                "category": "General",
            },
            {
                "question": "Do you provide website maintenance?",
                "answer": "Yes, we offer comprehensive maintenance packages including security updates, content updates, performance monitoring, and technical support.",
                "category": "Services",
            },
            {
                "question": "Can you help with SEO optimization?",
                "answer": "Absolutely! All our websites are built with SEO best practices, and we offer additional SEO services including keyword research, content optimization, and ongoing SEO management.",
                "category": "SEO",
            },
            {
                "question": "What platforms do you work with?",
                "answer": "We specialize in custom Django applications, but also work with WordPress, React, and other modern web technologies based on your specific needs.",
                "category": "Technical",
            },
        ]

        for i, faq_data in enumerate(faq_data):
            faq, created = FAQ.objects.get_or_create(
                question=faq_data["question"],
                defaults={
                    "answer": faq_data["answer"],
                    "category": faq_data["category"],
                    "display_order": i,
                },
            )
            if created:
                self.stdout.write(f"Created FAQ: {faq.question}")

    def create_testimonials(self):
        testimonials_data = [
            {
                "client_name": "Dr. Sarah Johnson",
                "client_position": "Principal",
                "client_company": "Lincoln High School",
                "content": "WebBuilder completely transformed our school's digital presence. The new website is not only visually stunning but also incredibly functional. Parent engagement has increased by 60%!",
                "rating": 5,
                "is_featured": True,
            },
            {
                "client_name": "Michael Chen",
                "client_position": "CEO",
                "client_company": "Urban Styles",
                "content": "Our e-commerce sales skyrocketed by 40% after WebBuilder redesigned our online store. The new checkout process is seamless, and our customers absolutely love the modern interface.",
                "rating": 5,
                "is_featured": True,
            },
            {
                "client_name": "Dr. Robert Williams",
                "client_position": "Director",
                "client_company": "City General Hospital",
                "content": "The patient portal WebBuilder created has revolutionized our patient communication. Administrative workload decreased by 35%, and patient satisfaction scores are at an all-time high.",
                "rating": 5,
                "is_featured": True,
            },
        ]

        for testimonial_data in testimonials_data:
            testimonial, created = Testimonial.objects.get_or_create(
                client_name=testimonial_data["client_name"],
                client_company=testimonial_data["client_company"],
                defaults=testimonial_data,
            )
            if created:
                self.stdout.write(f"Created testimonial: {testimonial.client_name}")
