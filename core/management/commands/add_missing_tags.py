from django.core.management.base import BaseCommand
from core.models import BlogTag


class Command(BaseCommand):
    help = "Add missing blog tags"

    def handle(self, *args, **options):
        self.stdout.write("Adding missing blog tags...")

        # Missing tags data
        missing_tags = [
            ("JavaScript", "#F7DF1E"),
            ("Python", "#3776AB"),
            ("CSS3", "#1572B6"),
            ("PWA", "#5A0FC8"),
            ("Docker", "#0DB7ED"),
            ("PostgreSQL", "#336791"),
            ("AWS", "#FF9900"),
            ("ES6+", "#F7DF1E"),
            ("TDD", "#25C2A0"),
            ("Quality Assurance", "#FF6B6B"),
            ("GraphQL", "#E10098"),
            ("REST", "#61DAFB"),
            ("Responsive Design", "#E91E63"),
            ("Web3", "#8B5CF6"),
            ("Cryptocurrency", "#F59E0B"),
            ("AI", "#FF6B6B"),
            ("Developer Tools", "#9333EA"),
            ("Productivity", "#10B981"),
            ("Accessibility", "#059669"),
            ("Inclusive Design", "#7C3AED"),
            ("UX", "#F59E0B"),
            ("Web Vitals", "#EF4444"),
            ("Optimization", "#22C55E"),
            ("CI/CD", "#3B82F6"),
            ("Automation", "#8B5CF6"),
            ("Future Tech", "#EC4899"),
            ("Web Trends", "#06B6D4"),
            ("Innovation", "#F97316"),
            ("WebSockets", "#10B981"),
            ("Real-time", "#EF4444"),
        ]

        for name, color in missing_tags:
            tag, created = BlogTag.objects.get_or_create(
                name=name, defaults={"color": color}
            )
            if created:
                self.stdout.write(f"Created tag: {name}")
            else:
                self.stdout.write(f"Tag already exists: {name}")

        self.stdout.write(self.style.SUCCESS("Successfully added missing tags!"))
