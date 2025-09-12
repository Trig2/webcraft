from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from projects.models import *
from faker import Faker
import random
from decimal import Decimal
from datetime import datetime, timedelta

fake = Faker()

class Command(BaseCommand):
    help = 'Populate projects models with sample data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--technologies',
            type=int,
            default=20,
            help='Number of additional technologies to create'
        )
        parser.add_argument(
            '--images',
            type=int,
            default=60,
            help='Number of project images to create'
        )
        parser.add_argument(
            '--testimonials',
            type=int,
            default=15,
            help='Number of project testimonials to create'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Starting Projects Data Population...'))
        
        # Create technologies
        self.create_technologies(options['technologies'])
        
        # Create project images
        self.create_project_images(options['images'])
        
        # Create project testimonials
        self.create_project_testimonials(options['testimonials'])
        
        # Create project metrics
        self.create_project_metrics()
        
        # Assign technologies to projects
        self.assign_technologies_to_projects()
        
        self.stdout.write(self.style.SUCCESS('✅ Projects data population completed!'))

    def create_technologies(self, count):
        self.stdout.write(f'Creating {count} additional technologies...')
        
        tech_data = [
            # Frontend Technologies
            {'name': 'Vue.js', 'category': 'frontend', 'icon': 'fab fa-vuejs', 'color': '#4FC08D'},
            {'name': 'Angular', 'category': 'frontend', 'icon': 'fab fa-angular', 'color': '#DD0031'},
            {'name': 'Svelte', 'category': 'frontend', 'icon': 'fas fa-code', 'color': '#FF3E00'},
            {'name': 'Next.js', 'category': 'frontend', 'icon': 'fab fa-react', 'color': '#000000'},
            {'name': 'Nuxt.js', 'category': 'frontend', 'icon': 'fab fa-vuejs', 'color': '#00DC82'},
            {'name': 'TypeScript', 'category': 'frontend', 'icon': 'fab fa-js-square', 'color': '#3178C6'},
            {'name': 'Tailwind CSS', 'category': 'frontend', 'icon': 'fas fa-palette', 'color': '#06B6D4'},
            {'name': 'Material-UI', 'category': 'frontend', 'icon': 'fas fa-layer-group', 'color': '#0081CB'},
            
            # Backend Technologies
            {'name': 'Express.js', 'category': 'backend', 'icon': 'fab fa-node-js', 'color': '#339933'},
            {'name': 'FastAPI', 'category': 'backend', 'icon': 'fas fa-rocket', 'color': '#009688'},
            {'name': 'Laravel', 'category': 'backend', 'icon': 'fab fa-laravel', 'color': '#FF2D20'},
            {'name': 'Ruby on Rails', 'category': 'backend', 'icon': 'fas fa-gem', 'color': '#CC0000'},
            {'name': 'Spring Boot', 'category': 'backend', 'icon': 'fab fa-java', 'color': '#6DB33F'},
            {'name': 'ASP.NET Core', 'category': 'backend', 'icon': 'fab fa-microsoft', 'color': '#512BD4'},
            
            # Databases
            {'name': 'Redis', 'category': 'database', 'icon': 'fas fa-database', 'color': '#DC382D'},
            {'name': 'Elasticsearch', 'category': 'database', 'icon': 'fas fa-search', 'color': '#005571'},
            {'name': 'Firebase', 'category': 'database', 'icon': 'fas fa-fire', 'color': '#FFCA28'},
            {'name': 'Supabase', 'category': 'database', 'icon': 'fas fa-database', 'color': '#3ECF8E'},
            
            # Tools & Others
            {'name': 'Figma', 'category': 'tool', 'icon': 'fab fa-figma', 'color': '#F24E1E'},
            {'name': 'Adobe XD', 'category': 'tool', 'icon': 'fab fa-adobe', 'color': '#FF61F6'},
            {'name': 'Sketch', 'category': 'tool', 'icon': 'fas fa-pencil-alt', 'color': '#F7B500'},
            {'name': 'Webpack', 'category': 'tool', 'icon': 'fas fa-cube', 'color': '#8DD6F9'},
            {'name': 'Vite', 'category': 'tool', 'icon': 'fas fa-bolt', 'color': '#646CFF'},
            {'name': 'GraphQL', 'category': 'backend', 'icon': 'fas fa-project-diagram', 'color': '#E10098'},
            
            # Hosting/Deployment
            {'name': 'Vercel', 'category': 'hosting', 'icon': 'fas fa-cloud', 'color': '#000000'},
            {'name': 'Netlify', 'category': 'hosting', 'icon': 'fas fa-cloud-upload-alt', 'color': '#00C7B7'},
            {'name': 'Heroku', 'category': 'hosting', 'icon': 'fas fa-server', 'color': '#430098'},
            {'name': 'DigitalOcean', 'category': 'hosting', 'icon': 'fab fa-digital-ocean', 'color': '#0080FF'},
        ]
        
        created_count = 0
        for tech in tech_data[:count]:
            technology, created = Technology.objects.get_or_create(
                name=tech['name'],
                defaults={
                    'category': tech['category'],
                    'icon': tech['icon'],
                    'color': tech['color'],
                    'description': f"Modern {tech['category']} technology used in web development.",
                    'is_active': True,
                    'display_order': created_count
                }
            )
            if created:
                created_count += 1
                
        self.stdout.write(self.style.SUCCESS(f'✓ Created {created_count} technologies'))

    def create_project_images(self, count):
        self.stdout.write(f'Creating {count} project image records...')
        
        projects = list(Project.objects.all())
        image_types = ['screenshot', 'mockup', 'process', 'before_after', 'feature']
        
        captions = [
            "Homepage design with modern layout",
            "Mobile responsive interface",
            "User dashboard with analytics",
            "E-commerce product catalog",
            "Contact form and integration",
            "Admin panel interface",
            "Search functionality",
            "User profile management",
            "Payment gateway integration",
            "Blog section design",
            "Portfolio showcase",
            "Team members page",
            "Services overview",
            "About us section"
        ]
        
        descriptions = [
            "Clean and modern design focusing on user experience",
            "Responsive layout that works across all devices",
            "Intuitive interface with easy navigation",
            "Professional design with brand consistency",
            "Optimized for performance and SEO",
            "User-friendly interface with modern aesthetics",
            "Feature-rich implementation with smooth interactions"
        ]
        
        for i in range(count):
            project = random.choice(projects)
            
            ProjectImage.objects.create(
                project=project,
                # Note: Using placeholder since we don't have actual image files
                image=f"project_gallery/placeholder_{i}.jpg",
                image_type=random.choice(image_types),
                caption=random.choice(captions),
                description=random.choice(descriptions),
                is_featured=random.choice([True, False, False, False]),  # 25% featured
                display_order=i
            )
            
        self.stdout.write(self.style.SUCCESS(f'✓ Created {count} project images'))

    def create_project_testimonials(self, count):
        self.stdout.write(f'Creating {count} project testimonials...')
        
        projects = list(Project.objects.filter(status='completed'))
        
        testimonials_data = [
            {
                'feedback': "Working with this team was an absolute pleasure. They delivered a stunning website that exceeded our expectations. The attention to detail and professional approach made all the difference.",
                'client_name': "Sarah Johnson",
                'client_position': "Marketing Director"
            },
            {
                'feedback': "The project was completed on time and within budget. The team was responsive, creative, and really understood our vision. Our new website has significantly improved our online presence.",
                'client_name': "Michael Chen",
                'client_position': "CEO"
            },
            {
                'feedback': "Exceptional work! The development team created exactly what we needed. The website is fast, beautiful, and our customers love the new user experience.",
                'client_name': "Emily Rodriguez",
                'client_position': "Product Manager"
            },
            {
                'feedback': "Professional service from start to finish. The team kept us informed throughout the process and delivered a high-quality solution that has boosted our business.",
                'client_name': "David Williams",
                'client_position': "Business Owner"
            },
            {
                'feedback': "Outstanding results! The website not only looks great but also performs excellently. We've seen a significant increase in conversions since the launch.",
                'client_name': "Lisa Thompson",
                'client_position': "Operations Manager"
            },
            {
                'feedback': "The team's expertise and dedication really showed in the final product. They transformed our outdated website into a modern, efficient platform.",
                'client_name': "James Anderson",
                'client_position': "Founder"
            },
            {
                'feedback': "Highly recommend their services. The project was managed professionally, and the end result perfectly aligned with our brand and business goals.",
                'client_name': "Maria Garcia",
                'client_position': "Brand Manager"
            },
            {
                'feedback': "Excellent communication and technical skills. The team delivered a robust solution that has streamlined our operations and improved customer satisfaction.",
                'client_name': "Robert Taylor",
                'client_position': "CTO"
            }
        ]
        
        for i in range(count):
            if i < len(projects):
                project = projects[i]
                testimonial_data = testimonials_data[i % len(testimonials_data)]
                
                ProjectTestimonial.objects.get_or_create(
                    project=project,
                    defaults={
                        'client_feedback': testimonial_data['feedback'],
                        'rating': random.choices([4, 5], weights=[30, 70])[0],
                        'client_name': testimonial_data['client_name'],
                        'client_position': testimonial_data['client_position'],
                        'is_approved': True,
                        'featured_quote': testimonial_data['feedback'][:100] + "..."
                    }
                )
                
        self.stdout.write(self.style.SUCCESS(f'✓ Created testimonials for {min(count, len(projects))} projects'))

    def create_project_metrics(self):
        self.stdout.write('Creating project metrics...')
        
        projects = list(Project.objects.filter(status='completed'))
        
        for project in projects:
            ProjectMetrics.objects.get_or_create(
                project=project,
                defaults={
                    'page_load_time': round(random.uniform(1.2, 3.5), 2),
                    'lighthouse_score': random.randint(85, 100),
                    'mobile_friendly': True,
                    'traffic_increase': round(random.uniform(25.0, 300.0), 2),
                    'conversion_rate': round(random.uniform(2.5, 8.5), 2),
                    'bounce_rate': round(random.uniform(25.0, 55.0), 2),
                    'development_hours': random.randint(40, 500),
                    'lines_of_code': random.randint(5000, 50000),
                    'seo_score': random.randint(75, 95),
                    'keywords_ranking': random.randint(5, 50)
                }
            )
            
        self.stdout.write(self.style.SUCCESS(f'✓ Created metrics for {len(projects)} projects'))

    def assign_technologies_to_projects(self):
        self.stdout.write('Assigning technologies to projects...')
        
        projects = list(Project.objects.all())
        technologies = list(Technology.objects.all())
        
        for project in projects:
            # Assign 3-8 technologies per project
            num_techs = random.randint(3, 8)
            selected_techs = random.sample(technologies, min(num_techs, len(technologies)))
            
            for tech in selected_techs:
                ProjectTechnology.objects.get_or_create(
                    project=project,
                    technology=tech,
                    defaults={
                        'importance': random.choice(['primary', 'secondary', 'tool'])
                    }
                )
                
        self.stdout.write(self.style.SUCCESS('✓ Assigned technologies to projects'))
