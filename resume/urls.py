from django.urls import path
from . import views

urlpatterns = [
    path('create-resume/', views.create_resume, name= 'create-resume'),
    path('resume-details/<int:pk>/',views.resume_details, name = 'resume-details' )
]