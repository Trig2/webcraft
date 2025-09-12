from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count
from .models import TeamMember, ActivityLog
from .forms import ProfileForm, TeamMemberForm
from projects.models import Project, ProjectCollaborator
from services.models import ServiceReview
from django.utils import timezone
from datetime import timedelta


@login_required
def profile_view(request, username=None):
    """View user profile"""
    if username:
        user = get_object_or_404(User, username=username)
        is_own_profile = request.user == user
    else:
        user = request.user
        is_own_profile = True
    
    # Get or create team member profile
    try:
        team_member = user.team_member
    except TeamMember.DoesNotExist:
        team_member = None
    
    # Get user's projects
    collaborated_projects = ProjectCollaborator.objects.filter(
        user=user
    ).select_related('project').order_by('-added_at')[:5]
    
    # Get user's recent activity
    recent_activities = ActivityLog.objects.filter(
        user=user
    ).order_by('-created_at')[:10]
    
    # Get user's service reviews
    user_reviews = ServiceReview.objects.filter(
        user=user
    ).select_related('service').order_by('-created_at')[:5]
    
    # Profile statistics
    stats = {
        'projects_count': ProjectCollaborator.objects.filter(user=user).count(),
        'reviews_count': ServiceReview.objects.filter(user=user).count(),
        'activities_count': ActivityLog.objects.filter(user=user).count(),
        'member_since': user.date_joined,
        'last_active': user.last_login,
    }
    
    context = {
        'profile_user': user,
        'team_member': team_member,
        'is_own_profile': is_own_profile,
        'collaborated_projects': collaborated_projects,
        'recent_activities': recent_activities,
        'user_reviews': user_reviews,
        'stats': stats,
    }
    
    return render(request, 'core/profile/profile_detail.html', context)


@login_required
def profile_edit(request):
    """Edit user profile"""
    user = request.user
    
    # Get or create team member profile
    try:
        team_member = user.team_member
    except TeamMember.DoesNotExist:
        team_member = TeamMember(user=user, name=user.get_full_name() or user.username)
        team_member.save()
    
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=user)
        team_form = TeamMemberForm(request.POST, request.FILES, instance=team_member)
        
        if profile_form.is_valid() and team_form.is_valid():
            profile_form.save()
            team_member = team_form.save(commit=False)
            team_member.user = user
            team_member.save()
            
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('core:profile_view')
    else:
        profile_form = ProfileForm(instance=user)
        team_form = TeamMemberForm(instance=team_member)
    
    context = {
        'profile_form': profile_form,
        'team_form': team_form,
        'team_member': team_member,
    }
    
    return render(request, 'core/profile/profile_edit.html', context)


@login_required
def profile_activity(request):
    """Show user's activity history"""
    activities = ActivityLog.objects.filter(
        user=request.user
    ).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(activities, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'activities': page_obj,
        'page_obj': page_obj,
    }
    
    return render(request, 'core/profile/profile_activity.html', context)


@login_required
def profile_projects(request):
    """Show user's projects"""
    collaborated_projects = ProjectCollaborator.objects.filter(
        user=request.user
    ).select_related('project').order_by('-added_at')
    
    # Group by role
    projects_by_role = {}
    for collab in collaborated_projects:
        role = collab.get_role_display()
        if role not in projects_by_role:
            projects_by_role[role] = []
        projects_by_role[role].append(collab)
    
    # Pagination
    paginator = Paginator(collaborated_projects, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'collaborated_projects': page_obj,
        'projects_by_role': projects_by_role,
        'page_obj': page_obj,
    }
    
    return render(request, 'core/profile/profile_projects.html', context)


@login_required
def profile_settings(request):
    """Profile privacy and account settings"""
    if request.method == 'POST':
        # Handle privacy settings
        show_email = request.POST.get('show_email') == 'on'
        show_projects = request.POST.get('show_projects') == 'on'
        show_activity = request.POST.get('show_activity') == 'on'
        
        # For now, we'll store these in session
        # In a real app, you'd want a UserProfile model
        request.session['profile_show_email'] = show_email
        request.session['profile_show_projects'] = show_projects
        request.session['profile_show_activity'] = show_activity
        
        messages.success(request, 'Privacy settings updated!')
        return redirect('core:profile_settings')
    
    # Get current settings from session
    settings = {
        'show_email': request.session.get('profile_show_email', True),
        'show_projects': request.session.get('profile_show_projects', True),
        'show_activity': request.session.get('profile_show_activity', False),
    }
    
    context = {
        'settings': settings,
    }
    
    return render(request, 'core/profile/profile_settings.html', context)


def public_profiles(request):
    """Public directory of team members"""
    team_members = TeamMember.objects.filter(
        is_active=True,
        user__isnull=False
    ).select_related('user').order_by('display_order', 'name')
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        team_members = team_members.filter(
            Q(name__icontains=search_query) |
            Q(position__icontains=search_query) |
            Q(bio__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(team_members, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'team_members': page_obj,
        'search_query': search_query,
        'page_obj': page_obj,
    }
    
    return render(request, 'core/profile/public_profiles.html', context)
