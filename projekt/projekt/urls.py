"""projekt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.home),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('home/', views.home, name='home'),
    path('subjects/', views.subjects, name='subjects'),
    path('subjects/<int:subject_id>', views.students_by_subject, name='students_by_subject'),
    path('create_subject/', views.create_subject, name='create_subject'),
    path('create_user/', views.create_user, name='create_user'),
    path('subjects/<int:subject_id>/update_subject', views.update_subject, name='update_subject'),
    path('subjects/<int:subject_id>/delete_confirmation', views.delete_confirmation, name='confirm_deletion'),
    path('subjects/<int:subject_id>/delete_subject', views.delete_subject, name='delete_subject'),
    path('students/', views.students, name='students'),
    path('students/<int:user_id>/update_user', views.update_user, name='update_user'),
    path('students/<int:user_id>/delete_user', views.delete_user, name='delete_user'),
    path('students/<int:user_id>/delete_confirmation_user', views.delete_confirmation_user, name='delete_confirmation_user'),
    path('professors/', views.professors, name='professors'),
    path('professors/<int:user_id>/update_user', views.update_user, name='update_user'),
    path('professors/<int:user_id>/delete_user', views.delete_user, name='delete_user'),
    path('professors/<int:user_id>/delete_confirmation_user', views.delete_confirmation_user, name='delete_confirmation_user'),
    path('home/enrollment_form/<int:student_id>', views.enrollment_form, name='enrollment_form'),
    path('home/enrollment_form/<int:student_id>/<int:subject_id>', views.enroll_subject, name='enroll_subject'),
    path('home/enrollment_form/remove_subject/<int:student_id>/<int:subject_id>', views.remove_subject, name='remove_subject'),
    path('home/enrollment_form/remove_confirmation_subject/<int:student_id>/<int:subject_id>', views.remove_confirmation_subject, name='remove_confirmation_subject'),
    path('subjects/<int:subject_id>/<int:enrollment_id>', views.pass_subject, name='pass_subject'),
    path('subjects/<int:subject_id>/<int:enrollment_id>/fail_subject', views.fail_subject, name='fail_subject'),
    path('home/all_subjects/', views.all_subjects, name='all_subjects'),
    #path('home/all_subjects/<int:student_id>', views.subject_students, name='subject_students'),

    ]
