from django.core.management.base import BaseCommand
from django.utils.text import slugify
from projects.models import Project


class Command(BaseCommand):
    help = 'Generate slugs for existing projects'

    def handle(self, *args, **options):
        projects_without_slugs = Project.objects.filter(slug__isnull=True)
        
        updated_count = 0
        for project in projects_without_slugs:
            base_slug = slugify(project.title)
            slug = base_slug
            counter = 1
            
            # Ensure unique slug
            while Project.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            project.slug = slug
            project.save()
            updated_count += 1
            
            self.stdout.write(
                self.style.SUCCESS(f'Generated slug "{slug}" for project: {project.title}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully generated slugs for {updated_count} projects!')
        )
