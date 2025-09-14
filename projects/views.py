from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Project
from core.models import ActivityLog
from core.models import SiteSetting


# Create your views here.
def project_list(request):
    """View for listing completed projects (portfolio)"""
    # Get completed projects for the portfolio
    completed_projects = Project.objects.filter(status="completed").order_by(
        "-completed_date"
    )

    # Pagination
    paginator = Paginator(completed_projects, 8)  # 8 projects per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Group projects by type (optional, can be removed if not needed)
    project_types = {}
    for project in page_obj:
        project_type = project.get_project_type_display()
        if project_type not in project_types:
            project_types[project_type] = []
        project_types[project_type].append(project)

    site_setting = SiteSetting.objects.all()

    if site_setting:
        for setting in site_setting:
            site_name = setting.site_name
            facebook = setting.facebook
            twitter = setting.twitter
            instagram = setting.instagram
            linkedin = setting.linkedin
            mail = setting.contact_email
            tel = setting.contact_phone
            address = setting.address
            logo = setting.logo

    context = {
        "projects": page_obj,
        "project_types": project_types,
        "page_obj": page_obj,
        "setting":setting
    }

    return render(request, "projects/project_list.html", context)


def project_detail(request, project_id):
    """View for displaying project details with graceful error handling"""
    try:
        project = get_object_or_404(Project, id=project_id, status="completed")
    except:
        # If project doesn't exist, redirect to portfolio with a friendly message
        messages.info(request, f"The project you're looking for (#{project_id}) is not available. Please browse our other projects below.")
        return redirect('projects:list')

    # Get all collaborators for this project using the new helper method
    collaborators_data = []
    for collab in project.get_collaborators():
        user = collab.user
        collaborators_data.append({
            'name': user.get_full_name() or user.username,
            'role': collab.get_role_display(),
            'email': user.email,
            'is_lead': collab.is_lead,
            'added_at': collab.added_at,
        })

    similar_projects = Project.objects.filter(
        project_type=project.project_type
    ).exclude(id=project.id)[:3]

    site_setting = SiteSetting.objects.all()

    if site_setting:
        for setting in site_setting:
            site_name = setting.site_name
            facebook = setting.facebook
            twitter = setting.twitter
            instagram = setting.instagram
            linkedin = setting.linkedin
            mail = setting.contact_email
            tel = setting.contact_phone
            address = setting.address
            logo = setting.logo

    context = {
        "project": project,
        "collaborators": collaborators_data,
        "similar_projects": similar_projects,
        "setting":setting
    }

    return render(request, "projects/project_detail.html", context)
