from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import *
from services.models import *
from projects.models import *
from chat.models import *


class Command(BaseCommand):
    help = 'Show comprehensive database statistics after population'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('📊 COMPREHENSIVE DATABASE REPORT'))
        self.stdout.write('=' * 60)
        
        # Core Statistics
        self.stdout.write(self.style.HTTP_INFO('\n👥 USER & AUTHENTICATION:'))
        self.stdout.write(f'  Users (Total): {User.objects.count()}')
        self.stdout.write(f'  Staff Users: {User.objects.filter(is_staff=True).count()}')
        self.stdout.write(f'  Active Users: {User.objects.filter(is_active=True).count()}')
        
        # Core Business Data
        self.stdout.write(self.style.HTTP_INFO('\n🏢 CORE BUSINESS DATA:'))
        self.stdout.write(f'  Clients: {Client.objects.count()}')
        self.stdout.write(f'  Leads: {Lead.objects.count()}')
        self.stdout.write(f'  Team Members: {TeamMember.objects.count()}')
        self.stdout.write(f'  Pricing Plans: {PricingPlan.objects.count()}')
        self.stdout.write(f'  Newsletter Subscribers: {NewsletterSubscriber.objects.count()}')
        self.stdout.write(f'  Announcements: {Announcement.objects.count()}')
        self.stdout.write(f'  Activity Logs: {ActivityLog.objects.count()}')
        self.stdout.write(f'  Website Analytics Records: {WebsiteAnalytics.objects.count()}')
        
        # Projects Data
        self.stdout.write(self.style.HTTP_INFO('\n🏗️ PROJECTS & PORTFOLIO:'))
        self.stdout.write(f'  Projects: {Project.objects.count()}')
        self.stdout.write(f'  Project Collaborators: {ProjectCollaborator.objects.count()}')
        self.stdout.write(f'  Technologies: {Technology.objects.count()}')
        self.stdout.write(f'  Project-Technology Assignments: {ProjectTechnology.objects.count()}')
        self.stdout.write(f'  Project Images: {ProjectImage.objects.count()}')
        self.stdout.write(f'  Project Testimonials: {ProjectTestimonial.objects.count()}')
        self.stdout.write(f'  Project Metrics: {ProjectMetrics.objects.count()}')
        
        # Services Data
        self.stdout.write(self.style.HTTP_INFO('\n🛠️ SERVICES & OFFERINGS:'))
        self.stdout.write(f'  Services: {Service.objects.count()}')
        self.stdout.write(f'  Service Packages: {ServicePackage.objects.count()}')
        self.stdout.write(f'  Service Reviews: {ServiceReview.objects.count()}')
        self.stdout.write(f'  Service FAQs: {ServiceFAQ.objects.count()}')
        self.stdout.write(f'  Service Requests: {ServiceRequest.objects.count()}')
        
        # Blog & Content
        self.stdout.write(self.style.HTTP_INFO('\n📝 BLOG & CONTENT:'))
        self.stdout.write(f'  Blog Posts: {BlogPost.objects.count()}')
        self.stdout.write(f'  Blog Tags: {BlogTag.objects.count()}')
        self.stdout.write(f'  Published Posts: {BlogPost.objects.filter(status="published").count()}')
        self.stdout.write(f'  Featured Posts: {BlogPost.objects.filter(is_featured=True).count()}')
        
        # Communication
        self.stdout.write(self.style.HTTP_INFO('\n💬 COMMUNICATION:'))
        self.stdout.write(f'  Chat Messages: {ChatMessage.objects.count()}')
        
        # Summary
        total_records = sum([
            User.objects.count(),
            Client.objects.count(),
            Lead.objects.count(),
            TeamMember.objects.count(),
            PricingPlan.objects.count(),
            NewsletterSubscriber.objects.count(),
            Announcement.objects.count(),
            ActivityLog.objects.count(),
            WebsiteAnalytics.objects.count(),
            Project.objects.count(),
            ProjectCollaborator.objects.count(),
            Technology.objects.count(),
            ProjectTechnology.objects.count(),
            ProjectImage.objects.count(),
            ProjectTestimonial.objects.count(),
            ProjectMetrics.objects.count(),
            Service.objects.count(),
            ServicePackage.objects.count(),
            ServiceReview.objects.count(),
            ServiceFAQ.objects.count(),
            ServiceRequest.objects.count(),
            BlogPost.objects.count(),
            BlogTag.objects.count(),
            ChatMessage.objects.count(),
        ])
        
        self.stdout.write(self.style.SUCCESS(f'\n🎯 TOTAL DATABASE RECORDS: {total_records}'))
        
        # Quick Insights
        self.stdout.write(self.style.HTTP_INFO('\n📈 QUICK INSIGHTS:'))
        avg_rating = ServiceReview.objects.aggregate(models.Avg('rating'))['rating__avg']
        if avg_rating:
            self.stdout.write(f'  Average Service Rating: {avg_rating:.1f}/5.0')
        
        completed_projects = Project.objects.filter(status='completed').count()
        self.stdout.write(f'  Completed Projects: {completed_projects}')
        
        active_clients = Client.objects.filter(is_active=True).count()
        self.stdout.write(f'  Active Clients: {active_clients}')
        
        recent_leads = Lead.objects.filter(status='new').count()
        self.stdout.write(f'  New Leads: {recent_leads}')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Database population completed successfully!'))
