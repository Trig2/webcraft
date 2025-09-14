from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list, name='list'),
    # Keep the old ID-based URL for backward compatibility
    path('<int:project_id>/', views.project_detail_by_id, name='detail_by_id'),
    # New slug-based URL (preferred)
    path('<slug:slug>/', views.project_detail, name='detail'),
]
