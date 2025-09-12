from django.core.management.base import BaseCommand
from core.models import BlogTag


class Command(BaseCommand):
    help = "Update blog tags with enhanced properties for better presentation"

    def handle(self, *args, **options):
        self.stdout.write("Enhancing blog tags with better presentation properties...")

        # Enhanced tag data with icons and categories
        enhanced_tags = {
            "Django": {
                "color": "#092E20",
                "icon": "fab fa-python",
                "category": "backend",
                "description": "Django web framework"
            },
            "JavaScript": {
                "color": "#F7DF1E", 
                "icon": "fab fa-js-square",
                "category": "frontend",
                "description": "JavaScript programming language"
            },
            "Python": {
                "color": "#3776AB",
                "icon": "fab fa-python", 
                "category": "backend",
                "description": "Python programming language"
            },
            "React": {
                "color": "#61DAFB",
                "icon": "fab fa-react",
                "category": "frontend", 
                "description": "React JavaScript library"
            },
            "CSS3": {
                "color": "#1572B6",
                "icon": "fab fa-css3-alt",
                "category": "frontend",
                "description": "CSS3 styling"
            },
            "UI/UX Design": {
                "color": "#FF6B6B",
                "icon": "fas fa-paint-brush",
                "category": "design",
                "description": "User interface and experience design"
            },
            "Web Development": {
                "color": "#4ECDC4",
                "icon": "fas fa-code",
                "category": "general",
                "description": "General web development"
            },
            "Performance": {
                "color": "#45B7D1",
                "icon": "fas fa-tachometer-alt",
                "category": "optimization",
                "description": "Performance optimization"
            },
            "API Development": {
                "color": "#FF6B6B",
                "icon": "fas fa-plug",
                "category": "backend",
                "description": "API development and integration"
            },
            "Cloud Computing": {
                "color": "#4ECDC4",
                "icon": "fas fa-cloud",
                "category": "infrastructure",
                "description": "Cloud computing and services"
            },
            "DevOps": {
                "color": "#45B7D1",
                "icon": "fas fa-tools",
                "category": "infrastructure",
                "description": "DevOps practices and tools"
            },
            "Machine Learning": {
                "color": "#96CEB4",
                "icon": "fas fa-brain",
                "category": "ai",
                "description": "Machine learning and AI"
            },
            "Cybersecurity": {
                "color": "#FFEAA7",
                "icon": "fas fa-shield-alt",
                "category": "security",
                "description": "Cybersecurity practices"
            },
            "Mobile Development": {
                "color": "#DDA0DD",
                "icon": "fas fa-mobile-alt",
                "category": "mobile",
                "description": "Mobile app development"
            },
            "Database Design": {
                "color": "#98D8C8",
                "icon": "fas fa-database",
                "category": "backend",
                "description": "Database design and management"
            },
            "Testing": {
                "color": "#F7DC6F",
                "icon": "fas fa-check-circle",
                "category": "quality",
                "description": "Software testing practices"
            },
            "Microservices": {
                "color": "#BB8FCE",
                "icon": "fas fa-cubes",
                "category": "architecture",
                "description": "Microservices architecture"
            },
            "Blockchain": {
                "color": "#85C1E9",
                "icon": "fas fa-link",
                "category": "crypto",
                "description": "Blockchain technology"
            },
            "PWA": {
                "color": "#5A0FC8",
                "icon": "fas fa-mobile-alt",
                "category": "mobile",
                "description": "Progressive Web Apps"
            },
            "Docker": {
                "color": "#0DB7ED",
                "icon": "fab fa-docker",
                "category": "infrastructure",
                "description": "Docker containerization"
            },
            "PostgreSQL": {
                "color": "#336791",
                "icon": "fas fa-database",
                "category": "backend",
                "description": "PostgreSQL database"
            },
            "AWS": {
                "color": "#FF9900",
                "icon": "fab fa-aws",
                "category": "infrastructure",
                "description": "Amazon Web Services"
            },
            "ES6+": {
                "color": "#F7DF1E",
                "icon": "fab fa-js-square",
                "category": "frontend",
                "description": "Modern JavaScript features"
            },
            "TDD": {
                "color": "#25C2A0",
                "icon": "fas fa-check-double",
                "category": "quality",
                "description": "Test-Driven Development"
            },
            "GraphQL": {
                "color": "#E10098",
                "icon": "fas fa-project-diagram",
                "category": "backend",
                "description": "GraphQL query language"
            },
            "REST": {
                "color": "#61DAFB",
                "icon": "fas fa-exchange-alt",
                "category": "backend",
                "description": "REST API architecture"
            },
            "Responsive Design": {
                "color": "#E91E63",
                "icon": "fas fa-mobile-alt",
                "category": "design",
                "description": "Responsive web design"
            },
            "Web3": {
                "color": "#8B5CF6",
                "icon": "fas fa-globe",
                "category": "crypto",
                "description": "Web3 and decentralized web"
            },
            "AI": {
                "color": "#FF6B6B",
                "icon": "fas fa-robot",
                "category": "ai",
                "description": "Artificial Intelligence"
            },
            "Accessibility": {
                "color": "#059669",
                "icon": "fas fa-universal-access",
                "category": "quality",
                "description": "Web accessibility"
            },
            "WebSockets": {
                "color": "#10B981",
                "icon": "fas fa-broadcast-tower",
                "category": "backend",
                "description": "Real-time communication"
            }
        }

        for tag_name, properties in enhanced_tags.items():
            try:
                tag = BlogTag.objects.get(name=tag_name)
                tag.color = properties["color"]
                tag.save()
                self.stdout.write(f"Updated tag: {tag_name}")
            except BlogTag.DoesNotExist:
                self.stdout.write(f"Tag not found: {tag_name}")

        self.stdout.write(self.style.SUCCESS("Successfully enhanced blog tags!"))
