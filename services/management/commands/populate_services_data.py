from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from services.models import *
from faker import Faker
import random
from decimal import Decimal

fake = Faker()

class Command(BaseCommand):
    help = 'Populate services models with sample data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reviews',
            type=int,
            default=50,
            help='Number of service reviews to create'
        )
        parser.add_argument(
            '--faqs',
            type=int,
            default=30,
            help='Number of FAQs to create'
        )
        parser.add_argument(
            '--requests',
            type=int,
            default=40,
            help='Number of service requests to create'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Starting Services Data Population...'))
        
        # Create service reviews
        self.create_service_reviews(options['reviews'])
        
        # Create service FAQs
        self.create_service_faqs(options['faqs'])
        
        # Create service requests
        self.create_service_requests(options['requests'])
        
        # Create service packages
        self.create_service_packages()
        
        self.stdout.write(self.style.SUCCESS('✅ Services data population completed!'))

    def create_service_reviews(self, count):
        self.stdout.write(f'Creating {count} service reviews...')
        
        services = list(Service.objects.all())
        users = list(User.objects.all())
        
        positive_comments = [
            "Excellent service! Very professional and delivered on time.",
            "Great experience working with the team. Highly recommended!",
            "Outstanding quality and attention to detail.",
            "Perfect communication throughout the project.",
            "Exceeded our expectations in every way.",
            "Fast delivery and excellent support.",
            "Very satisfied with the final result.",
            "Professional, reliable, and creative team.",
            "Great value for money and quality work.",
            "Will definitely work with them again!"
        ]
        
        neutral_comments = [
            "Good service overall, minor delays but acceptable quality.",
            "Decent work, met most of our requirements.",
            "Average experience, nothing exceptional but satisfactory.",
            "Good communication but could be faster.",
            "Quality work but took longer than expected."
        ]
        
        negative_comments = [
            "Service was below expectations, needed multiple revisions.",
            "Communication could be better, delayed responses.",
            "Final product didn't match initial requirements.",
            "Too many delays in the project timeline."
        ]
        
        for i in range(count):
            rating = random.choices([1, 2, 3, 4, 5], weights=[5, 10, 15, 35, 35])[0]
            
            if rating >= 4:
                comment = random.choice(positive_comments)
            elif rating == 3:
                comment = random.choice(neutral_comments)
            else:
                comment = random.choice(negative_comments)
            
            ServiceReview.objects.create(
                service=random.choice(services),
                user=random.choice(users) if random.choice([True, False]) else None,
                rating=rating,
                comment=comment,
                is_approved=random.choice([True, True, True, False])  # 75% approved
            )
            
        self.stdout.write(self.style.SUCCESS(f'✓ Created {count} service reviews'))

    def create_service_faqs(self, count):
        self.stdout.write(f'Creating {count} service FAQs...')
        
        services = list(Service.objects.all())
        
        faq_templates = [
            {
                'question': 'How long does this service take to complete?',
                'answer': 'The timeline varies depending on the project scope and complexity. Typically, we complete projects within 2-4 weeks for standard requirements.'
            },
            {
                'question': 'What is included in this service?',
                'answer': 'Our service includes comprehensive planning, design, development, testing, and deployment. We also provide post-launch support and maintenance.'
            },
            {
                'question': 'Do you provide ongoing support?',
                'answer': 'Yes, we offer various support packages ranging from basic maintenance to comprehensive ongoing development and optimization.'
            },
            {
                'question': 'Can you work with our existing team?',
                'answer': 'Absolutely! We collaborate seamlessly with in-house teams and can adapt to your existing workflows and processes.'
            },
            {
                'question': 'What technologies do you use?',
                'answer': 'We use modern, industry-standard technologies including React, Django, Node.js, and cloud platforms like AWS and Azure.'
            },
            {
                'question': 'How do you handle project communication?',
                'answer': 'We maintain regular communication through project management tools, weekly updates, and scheduled check-ins to ensure transparency.'
            },
            {
                'question': 'What is your revision policy?',
                'answer': 'We include up to 3 rounds of revisions in our standard pricing. Additional revisions are available at competitive rates.'
            },
            {
                'question': 'Do you offer payment plans?',
                'answer': 'Yes, we offer flexible payment options including milestone-based payments and installment plans for larger projects.'
            },
            {
                'question': 'What happens if we need changes after launch?',
                'answer': 'We provide post-launch support and can implement changes as needed. Minor updates are often covered under our support packages.'
            },
            {
                'question': 'How do you ensure project security?',
                'answer': 'We follow industry best practices for security, including secure coding standards, regular testing, and compliance with relevant regulations.'
            }
        ]
        
        for i in range(count):
            template = random.choice(faq_templates)
            service = random.choice(services)
            
            ServiceFAQ.objects.create(
                service=service,
                question=template['question'],
                answer=template['answer'],
                display_order=i,
                is_active=random.choice([True, True, True, False])  # 75% active
            )
            
        self.stdout.write(self.style.SUCCESS(f'✓ Created {count} service FAQs'))

    def create_service_requests(self, count):
        self.stdout.write(f'Creating {count} service requests...')
        
        services = list(Service.objects.all())
        
        request_messages = [
            "I'm interested in this service for my business. Can you provide more details about the process?",
            "Looking to upgrade our current solution. Would like to discuss requirements and timeline.",
            "Need a quote for this service. Our project has specific requirements that I'd like to discuss.",
            "Impressed with your portfolio! Would like to explore how you can help our company.",
            "Ready to get started with this service. Please contact me to schedule a consultation.",
            "Have some questions about your approach and would like to discuss our project needs.",
            "Looking for a reliable partner for this type of work. Can we set up a call?",
            "Interested in learning more about your process and getting a custom quote.",
            "Need this service urgently. What's your availability for immediate projects?",
            "Would like to discuss a long-term partnership for multiple projects."
        ]
        
        for i in range(count):
            ServiceRequest.objects.create(
                service=random.choice(services),
                name=fake.name(),
                email=fake.email(),
                phone=fake.phone_number()[:15],
                message=random.choice(request_messages),
                status=random.choice(['new', 'in_progress', 'completed']),
            )
            
        self.stdout.write(self.style.SUCCESS(f'✓ Created {count} service requests'))

    def create_service_packages(self):
        self.stdout.write('Creating service packages...')
        
        packages_data = [
            {
                'name': 'Startup Web Package',
                'description': 'Perfect for new businesses looking to establish their online presence with a professional website.',
                'price': Decimal('2499.00'),
                'services': ['web_development', 'web_design', 'seo']
            },
            {
                'name': 'Business Growth Package',
                'description': 'Comprehensive solution for growing businesses that need a robust online platform.',
                'price': Decimal('4999.00'),
                'services': ['web_development', 'ecommerce', 'cms', 'seo']
            },
            {
                'name': 'Enterprise Solution',
                'description': 'Full-scale digital transformation package for large organizations.',
                'price': Decimal('9999.00'),
                'services': ['web_development', 'ecommerce', 'cms', 'seo', 'maintenance', 'consultation']
            },
            {
                'name': 'E-commerce Starter',
                'description': 'Everything you need to start selling online with a professional e-commerce platform.',
                'price': Decimal('3499.00'),
                'services': ['ecommerce', 'web_design', 'seo']
            },
            {
                'name': 'Maintenance & Support',
                'description': 'Ongoing support package to keep your website running smoothly and up-to-date.',
                'price': Decimal('199.00'),
                'services': ['maintenance', 'hosting']
            }
        ]
        
        for package_data in packages_data:
            package, created = ServicePackage.objects.get_or_create(
                name=package_data['name'],
                defaults={
                    'description': package_data['description'],
                    'price': package_data['price'],
                    'is_featured': random.choice([True, False]),
                    'is_active': True
                }
            )
            
            if created:
                # Add services to the package
                for service_category in package_data['services']:
                    services = Service.objects.filter(category=service_category)[:2]
                    for service in services:
                        PackageService.objects.get_or_create(
                            package=package,
                            service=service
                        )
                        
        self.stdout.write(self.style.SUCCESS('✓ Created service packages'))
