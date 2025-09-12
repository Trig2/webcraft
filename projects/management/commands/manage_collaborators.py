from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from projects.models import Project, ProjectCollaborator


class Command(BaseCommand):
    help = 'Manage project collaborators - add, remove, or list collaborators'

    def add_arguments(self, parser):
        parser.add_argument(
            'action',
            choices=['add', 'remove', 'list', 'show'],
            help='Action to perform: add, remove, list, or show'
        )
        parser.add_argument(
            '--project',
            type=int,
            help='Project ID'
        )
        parser.add_argument(
            '--user',
            type=str,
            help='Username of the collaborator'
        )
        parser.add_argument(
            '--role',
            type=str,
            choices=[choice[0] for choice in ProjectCollaborator.ROLE_CHOICES],
            default='collaborator',
            help='Role for the collaborator'
        )
        parser.add_argument(
            '--lead',
            action='store_true',
            help='Mark collaborator as project lead'
        )

    def handle(self, *args, **options):
        action = options['action']

        if action == 'list':
            self.list_all_collaborations()
        elif action == 'show':
            if not options['project']:
                self.stdout.write(self.style.ERROR('Project ID is required for show action'))
                return
            self.show_project_collaborators(options['project'])
        elif action in ['add', 'remove']:
            if not all([options['project'], options['user']]):
                self.stdout.write(self.style.ERROR('Project ID and username are required'))
                return
            
            if action == 'add':
                self.add_collaborator(
                    options['project'], 
                    options['user'], 
                    options['role'],
                    options['lead']
                )
            else:
                self.remove_collaborator(options['project'], options['user'])

    def list_all_collaborations(self):
        """List all project collaborations"""
        self.stdout.write(self.style.SUCCESS('All Project Collaborations:'))
        self.stdout.write('=' * 60)
        
        projects = Project.objects.prefetch_related('projectcollaborator_set__user').all()
        
        for project in projects:
            collaborators = project.get_collaborators()
            if collaborators:
                self.stdout.write(f'\n📁 {project.title} ({project.get_collaborator_count()} collaborators)')
                for collab in collaborators:
                    lead_indicator = ' 👑' if collab.is_lead else ''
                    self.stdout.write(
                        f'   • {collab.user.get_full_name() or collab.user.username} '
                        f'- {collab.get_role_display()}{lead_indicator}'
                    )

    def show_project_collaborators(self, project_id):
        """Show collaborators for a specific project"""
        try:
            project = Project.objects.get(id=project_id)
            collaborators = project.get_collaborators()
            
            self.stdout.write(self.style.SUCCESS(f'Collaborators for: {project.title}'))
            self.stdout.write('=' * 50)
            
            if collaborators:
                for collab in collaborators:
                    lead_status = ' (LEAD)' if collab.is_lead else ''
                    self.stdout.write(
                        f'• {collab.user.get_full_name() or collab.user.username} '
                        f'- {collab.get_role_display()}{lead_status}'
                    )
                    self.stdout.write(f'  Email: {collab.user.email}')
                    self.stdout.write(f'  Added: {collab.added_at.strftime("%Y-%m-%d")}')
                    self.stdout.write('')
            else:
                self.stdout.write('No collaborators assigned to this project.')
                
        except Project.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Project with ID {project_id} not found'))

    def add_collaborator(self, project_id, username, role, is_lead):
        """Add a collaborator to a project"""
        try:
            project = Project.objects.get(id=project_id)
            user = User.objects.get(username=username, is_staff=True)
            
            collaborator, created = project.add_collaborator(user, role)
            
            if created:
                if is_lead:
                    collaborator.is_lead = True
                    collaborator.save()
                
                lead_text = ' as project lead' if is_lead else ''
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Added {user.username} to "{project.title}" '
                        f'as {collaborator.get_role_display()}{lead_text}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'⚠ {user.username} is already a collaborator on "{project.title}"'
                    )
                )
                
        except Project.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Project with ID {project_id} not found'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Staff user "{username}" not found'))

    def remove_collaborator(self, project_id, username):
        """Remove a collaborator from a project"""
        try:
            project = Project.objects.get(id=project_id)
            user = User.objects.get(username=username)
            
            deleted_count, _ = project.remove_collaborator(user)
            
            if deleted_count[0] > 0:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Removed {user.username} from "{project.title}"'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'⚠ {user.username} was not a collaborator on "{project.title}"'
                    )
                )
                
        except Project.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Project with ID {project_id} not found'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User "{username}" not found'))
