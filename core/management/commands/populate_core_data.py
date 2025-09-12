from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import *
from faker import Faker
import random
from decimal import Decimal

fake = Faker()

class Command(BaseCommand):
    help = 'Populate core models with sample data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clients',
            type=int,
            default=15,
            help='Number of clients to create'
        )
        parser.add_argument(
            '--leads',
            type=int,
            default=25,
            help='Number of leads to create'
        )
        parser.add_argument(
            '--activities',
            type=int,
            default=50,
            help='Number of activity logs to create'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Starting Core Data Population...'))
        
        # Create clients
        self.create_clients(options['clients'])
        
        # Create additional leads
        self.create_leads(options['leads'])
        
        # Create site settings if not exists
        self.create_site_settings()
        
        # Create newsletter subscribers
        self.create_newsletter_subscribers(30)
        
        # Create announcements
        self.create_announcements(8)
        
        # Create activity logs
        self.create_activity_logs(options['activities'])
        
        # Create website analytics
        self.create_website_analytics()
        
        self.stdout.write(self.style.SUCCESS('✅ Core data population completed!'))

    def create_clients(self, count):
        self.stdout.write(f'Creating {count} clients...')
        
        industries = ['technology', 'healthcare', 'education', 'finance', 'ecommerce', 'marketing', 'nonprofit', 'real_estate', 'hospitality', 'other']
        
        for i in range(count):
            # Create a user for the client
            username = f"client_{fake.user_name()}_{i}"
            email = fake.unique.email()
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': fake.first_name(),
                    'last_name': fake.last_name(),
                    'is_active': True
                }
            )
            
            if created:
                company_name = f"{fake.company().replace(',', '').replace('.', '')}"
                
                Client.objects.create(
                    user=user,
                    company_name=company_name,
                    industry=random.choice(industries),
                    phone=fake.phone_number()[:15],
                    address=fake.address(),
                    website=f"https://www.{fake.domain_name()}",
                    notes=fake.paragraph(nb_sentences=3),
                    is_active=random.choice([True, True, True, False])  # 75% active
                )
            
        self.stdout.write(self.style.SUCCESS(f'✓ Created {count} clients'))

    def create_leads(self, count):
        self.stdout.write(f'Creating {count} additional leads...')
        
        project_types = ['Web Development', 'E-commerce', 'Mobile App', 'SEO', 'Digital Marketing', 'CMS', 'Custom Software']
        sources = ['website', 'referral', 'social_media', 'google_ads', 'email_campaign', 'phone_call', 'other']
        statuses = ['new', 'contacted', 'qualified', 'proposal', 'closed_won', 'closed_lost']
        
        for i in range(count):
            Lead.objects.create(
                name=fake.name(),
                email=fake.unique.email(),
                phone=fake.phone_number()[:15],
                company=fake.company(),
                budget=random.choice([None, Decimal(str(random.randint(1000, 50000)))]),
                timeline=random.choice(['ASAP', '1 month', '3 months', '6 months', 'Flexible']),
                source=random.choice(sources),
                status=random.choice(statuses),
                assigned_to=random.choice(User.objects.filter(is_staff=True)),
                project_type=random.choice(project_types),
                message=fake.paragraph(nb_sentences=4),
                notes=fake.paragraph(nb_sentences=2) if random.choice([True, False]) else None
            )
            
        self.stdout.write(self.style.SUCCESS(f'✓ Created {count} leads'))

    def create_site_settings(self):
        if not SiteSetting.objects.exists():
            self.stdout.write('Creating site settings...')
            SiteSetting.objects.create(
                site_name="WebBuilder Pro",
                contact_email="info@webbuilder.com",
                contact_phone="+1 (555) 123-4567",
                address="123 Tech Street, Digital City, DC 12345",
                facebook="https://facebook.com/webbuilder",
                twitter="https://twitter.com/webbuilder",
                linkedin="https://linkedin.com/company/webbuilder",
                instagram="https://instagram.com/webbuilder"
            )
            self.stdout.write(self.style.SUCCESS('✓ Created site settings'))

    def create_newsletter_subscribers(self, count):
        self.stdout.write(f'Creating {count} newsletter subscribers...')
        
        for i in range(count):
            NewsletterSubscriber.objects.get_or_create(
                email=fake.unique.email(),
                defaults={
                    'is_active': random.choice([True, True, True, False])  # 75% active
                }
            )
            
        self.stdout.write(self.style.SUCCESS(f'✓ Created {count} newsletter subscribers'))

    def create_announcements(self, count):
        self.stdout.write(f'Creating {count} announcements...')
        
        announcement_types = [
            'New Service Launch', 'Company Update', 'Holiday Notice', 
            'Maintenance Window', 'Feature Release', 'Event Announcement'
        ]
        
        for i in range(count):
            Announcement.objects.create(
                title=f"{random.choice(announcement_types)}: {fake.catch_phrase()}",
                message=fake.paragraph(nb_sentences=5),
                is_active=random.choice([True, True, True, False]),
                start_date=fake.date_time_between(start_date='-60d', end_date='+30d'),
                end_date=fake.date_time_between(start_date='+1d', end_date='+90d')
            )
            
        self.stdout.write(self.style.SUCCESS(f'✓ Created {count} announcements'))

    def create_activity_logs(self, count):
        self.stdout.write(f'Creating {count} activity logs...')
        
        actions = [
            'project_created', 'project_updated', 'client_added', 'lead_converted',
            'service_purchased', 'payment_received', 'meeting_scheduled', 
            'proposal_sent', 'contract_signed', 'milestone_completed'
        ]
        
        users = list(User.objects.filter(is_staff=True))
        projects = list(Project.objects.all())
        
        for i in range(count):
            ActivityLog.objects.create(
                user=random.choice(users),
                project_logs=random.choice(projects) if random.choice([True, False]) else None,
                action=random.choice(actions),
                details=fake.sentence()
            )
            
        self.stdout.write(self.style.SUCCESS(f'✓ Created {count} activity logs'))

    def create_website_analytics(self):
        self.stdout.write('Creating website analytics data...')
        
        # Create analytics for the last 30 days
        from datetime import datetime, timedelta
        
        for i in range(30):
            date = datetime.now().date() - timedelta(days=i)
            
            WebsiteAnalytics.objects.get_or_create(
                date=date,
                defaults={
                    'page_views': random.randint(100, 500),
                    'unique_visitors': random.randint(50, 300),
                    'bounce_rate': round(random.uniform(30.0, 70.0), 2),
                    'contact_forms': random.randint(2, 15),
                    'service_requests': random.randint(1, 10),
                    'quote_requests': random.randint(3, 20),
                }
            )
            
        self.stdout.write(self.style.SUCCESS('✓ Created website analytics data'))
