from django.core.management.base import BaseCommand
from django.utils import timezone
from projects.models import Project
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Create sample projects for production'

    def handle(self, *args, **options):
        sample_projects = [
            {
                'client_name': 'John Smith',
                'client_email': 'john@example.com',
                'organization_name': 'Smith Enterprises',
                'title': 'Corporate Website Redesign',
                'description': 'Modern responsive website for corporate business',
                'project_type': 'marketing',
                'status': 'completed',
                'budget': 5000.00,
                'completed_date': date.today() - timedelta(days=30)
            },
            {
                'client_name': 'Sarah Johnson',
                'client_email': 'sarah@example.com',
                'organization_name': 'Johnson School',
                'title': 'Educational Platform',
                'description': 'Online learning management system for school',
                'project_type': 'school',
                'status': 'completed',
                'budget': 8000.00,
                'completed_date': date.today() - timedelta(days=45)
            },
            {
                'client_name': 'Mike Davis',
                'client_email': 'mike@example.com',
                'organization_name': 'Davis Health Clinic',
                'title': 'Medical Practice Website',
                'description': 'Professional medical practice website with appointment booking',
                'project_type': 'hospital',
                'status': 'completed',
                'budget': 6500.00,
                'completed_date': date.today() - timedelta(days=60)
            },
            {
                'client_name': 'Emily Wilson',
                'client_email': 'emily@example.com',
                'organization_name': 'Wilson Boutique',
                'title': 'E-Commerce Store',
                'description': 'Online boutique store with payment integration',
                'project_type': 'ecommerce',
                'status': 'completed',
                'budget': 7500.00,
                'completed_date': date.today() - timedelta(days=20)
            },
            {
                'client_name': 'David Brown',
                'client_email': 'david@example.com',
                'organization_name': 'Brown Photography',
                'title': 'Portfolio Website',
                'description': 'Professional photography portfolio with gallery',
                'project_type': 'portfolio',
                'status': 'completed',
                'budget': 3500.00,
                'completed_date': date.today() - timedelta(days=15)
            },
            {
                'client_name': 'Lisa Garcia',
                'client_email': 'lisa@example.com',
                'organization_name': 'Garcia Blog',
                'title': 'Personal Blog Platform',
                'description': 'Custom blog platform with social media integration',
                'project_type': 'blog',
                'status': 'completed',
                'budget': 4000.00,
                'completed_date': date.today() - timedelta(days=10)
            },
            {
                'client_name': 'Robert Taylor',
                'client_email': 'robert@example.com',
                'organization_name': 'Taylor Tech Solutions',
                'title': 'Custom Web Application',
                'description': 'Custom business management web application',
                'project_type': 'custom',
                'status': 'completed',
                'budget': 12000.00,
                'completed_date': date.today() - timedelta(days=90)
            },
            {
                'client_name': 'Amanda White',
                'client_email': 'amanda@example.com',
                'organization_name': 'White Consulting',
                'title': 'Consulting Firm Website',
                'description': 'Professional consulting firm website with client portal',
                'project_type': 'marketing',
                'status': 'completed',
                'budget': 5500.00,
                'completed_date': date.today() - timedelta(days=25)
            },
            {
                'client_name': 'Chris Anderson',
                'client_email': 'chris@example.com',
                'organization_name': 'Anderson Elementary',
                'title': 'School Website Redesign',
                'description': 'Modern school website with parent portal',
                'project_type': 'school',
                'status': 'completed',
                'budget': 6000.00,
                'completed_date': date.today() - timedelta(days=35)
            },
            {
                'client_name': 'Jennifer Martinez',
                'client_email': 'jennifer@example.com',
                'organization_name': 'Martinez Medical Center',
                'title': 'Healthcare Portal',
                'description': 'Patient portal and medical center website',
                'project_type': 'hospital',
                'status': 'completed',
                'budget': 9000.00,
                'completed_date': date.today() - timedelta(days=50)
            },
            {
                'client_name': 'Kevin Thompson',
                'client_email': 'kevin@example.com',
                'organization_name': 'Thompson Sports',
                'title': 'Sports Equipment Store',
                'description': 'E-commerce store for sports equipment',
                'project_type': 'ecommerce',
                'status': 'completed',
                'budget': 8500.00,
                'completed_date': date.today() - timedelta(days=40)
            },
            {
                'client_name': 'Michelle Lee',
                'client_email': 'michelle@example.com',
                'organization_name': 'Lee Creative Studio',
                'title': 'Creative Agency Portfolio',
                'description': 'Creative agency portfolio with project showcase',
                'project_type': 'portfolio',
                'status': 'completed',
                'budget': 4500.00,
                'completed_date': date.today() - timedelta(days=18)
            },
            {
                'client_name': 'James Wilson',
                'client_email': 'james@example.com',
                'organization_name': 'Wilson Travel Blog',
                'title': 'Travel Blog Website',
                'description': 'Travel blog with photo galleries and trip reviews',
                'project_type': 'blog',
                'status': 'completed',
                'budget': 3800.00,
                'completed_date': date.today() - timedelta(days=12)
            },
            {
                'client_name': 'Rachel Green',
                'client_email': 'rachel@example.com',
                'organization_name': 'Green Tech Solutions',
                'title': 'Tech Startup Website',
                'description': 'Modern tech startup website with investor portal',
                'project_type': 'custom',
                'status': 'completed',
                'budget': 7800.00,
                'completed_date': date.today() - timedelta(days=28)
            },
            {
                'client_name': 'Mark Rodriguez',
                'client_email': 'mark@example.com',
                'organization_name': 'Rodriguez Enterprises',
                'title': 'Enterprise Business Platform',
                'description': 'Large-scale enterprise business platform',
                'project_type': 'custom',
                'status': 'completed',
                'budget': 15000.00,
                'completed_date': date.today() - timedelta(days=75)
            }
        ]

        # Add 20 more projects to ensure we have enough for production
        additional_projects = []
        client_names = [
            'Alex Turner', 'Maria Gonzalez', 'Tom Wilson', 'Anna Schmidt', 'Carlos Mendez',
            'Sofia Petrova', 'Jake Miller', 'Isabella Costa', 'Ryan O\'Connor', 'Priya Sharma',
            'Omar Hassan', 'Elena Rossi', 'Nathan Kim', 'Zara Al-Ahmad', 'Lucas Silva',
            'Fatima Kone', 'Daniel Larsson', 'Aisha Patel', 'Max Weber', 'Lina Andersson'
        ]
        
        organizations = [
            'Tech Solutions Inc', 'Digital Innovations', 'Creative Minds Agency', 'Global Ventures',
            'Smart Systems Ltd', 'Future Designs', 'Innovative Works', 'Professional Services',
            'Modern Solutions', 'Elite Consulting', 'Prime Technologies', 'Advanced Systems',
            'Dynamic Enterprises', 'Strategic Partners', 'Excellence Group', 'Progressive Tech',
            'Superior Solutions', 'Leading Edge Co', 'Premium Services', 'Quality Systems'
        ]
        
        project_titles = [
            'Advanced E-learning Platform', 'Medical Records System', 'Real Estate Portal',
            'Fitness Tracking App', 'Restaurant Management System', 'Event Planning Platform',
            'Inventory Management Tool', 'Customer Support Portal', 'Social Media Dashboard',
            'Financial Planning App', 'HR Management System', 'Project Tracking Tool',
            'Booking Management System', 'Content Management Platform', 'Analytics Dashboard',
            'Communication Portal', 'Workflow Automation Tool', 'Document Management System',
            'Customer Relationship Platform', 'Business Intelligence Dashboard'
        ]
        
        project_types = ['marketing', 'school', 'hospital', 'ecommerce', 'portfolio', 'blog', 'custom']
        
        for i in range(20):
            additional_projects.append({
                'client_name': client_names[i],
                'client_email': f'{client_names[i].lower().replace(" ", "").replace("\'", "")}@example.com',
                'organization_name': organizations[i],
                'title': project_titles[i],
                'description': f'Professional {project_titles[i].lower()} with modern features and responsive design',
                'project_type': project_types[i % len(project_types)],
                'status': 'completed',
                'budget': random.uniform(3000, 15000),
                'completed_date': date.today() - timedelta(days=random.randint(5, 100))
            })
        
        # Combine original and additional projects
        all_projects = sample_projects + additional_projects

        created_count = 0
        for project_data in all_projects:
            project, created = Project.objects.get_or_create(
                title=project_data['title'],
                client_email=project_data['client_email'],
                defaults=project_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created project: {project.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Project already exists: {project.title}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new projects!')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Total projects in database: {Project.objects.count()}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Completed projects: {Project.objects.filter(status="completed").count()}')
        )
