from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import GuestRegisterView, LoginView, GuestOtpVerifyView, CustomLogoutView, AgentRegisterView, AgentOtpVerifyView, AgentInfoView, AgentInfoAdminView, AgentListView, AgentInfoEditView, AgentsClient, GuestForgotPasswordView, GuestResetPasswordView, GuestChangePasswordView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('guest-register/', GuestRegisterView.as_view(), name='guest_register'),
    path('login/', LoginView.as_view(), name='guest_login'),

    # agent register
    path('agent-register/', AgentRegisterView.as_view(), name='agent_register'),
    path('agent-otp-verify/', AgentOtpVerifyView.as_view(), name='agent_otp_verify'),

    # Agent Dashboard for Agent role
    path('agent-data/', login_required(AgentRegisterView.as_view()), name='agents_data'),  # Not Working

    # path('agents-client/', login_required(AgentOtpVerifyView.as_view()), name='agents_client'),

    path('agents-client/', login_required(AgentsClient.as_view()), name='agents_client'),

    # Agent Dashboard for admin/ hr role
    path('admin-dashboard/agents/', login_required(AgentListView.as_view()), name='agent_list'),
    path('admin-dashboard/agent-info/', login_required(AgentListView.as_view()), name='agent_info_create_admin'),  # For viewing agent details
    path('admin-dashboard/agent-info/<int:pk>/', login_required(AgentListView.as_view()), name='agent_info_edit_admin'),



    path('admin-dashboard/agent-info/edit/<int:pk>/', AgentInfoEditView.as_view(), name='agent_info_edit_admin'),  # Edit agent info
    # path('admin-dashboard/agent-info/', AgentInfoAdminView.as_view(), name='agent_info_create_admin'),  # For creating agent info
    # path('admin-dashboard/agent-info/<int:pk>/', AgentInfoAdminView.as_view(), name='agent_info_edit_admin'),  # For editing agent info


    # Agent dashboard from agent account login
    path('agent-info/', AgentInfoView.as_view(), name='agents_data'),  # For creating agent info
    path('agent-info/<int:pk>/', AgentInfoView.as_view(), name='agent_info_edit'),


    path('logout/', CustomLogoutView.as_view(), name='logout'),


    path('guest-otp-verify/', GuestOtpVerifyView.as_view(), name='guest_otp_verify'),    # OTP verification


    # path('guest-otp-verify/', views.guest_otp_verify, name='guest_otp_verify'),    # OTP verification
    # path('guest-login/', views.guest_login, name='guest_login'),                  # phone+password login
    path('guest-dashboard/', views.guest_dashboard, name='guest_dashboard'),
    path('guest-change-password/', views.guest_change_password, name='guest_change_password'),
    path('guest-cv/', views.view_guest_cv, name='guest_cv'),
    path('guest-cv-table/', views.guest_cv_list_panel, name='guest_cv_panel'),
    # path('guest-cv/<int:pk>/', views.view_guest_cv_by_pk, name='guest_cv_by_pk'),


    path('role-login/', views.role_based_login, name='role_based_login'),

    # role based dashboard
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('guest-cv-list/', views.guest_cv_list, name='admin_guest_cvs_list'),

    path('guest-cv/<int:pk>/', views.guest_cv_detail_by_pk, name='guest_cv_by_pk'),


    # path('admin-dashboard/', views.admin_index, name='admin_index'),
    # # hr role
    # path('hr-dashboard/', views.hr_dashboard, name='hr_dashboard'),
    # path('hr/guest-passports/', views.hr_view_guests_passport, name='hr_guest_passports'),
    # path('hr/guest-cvs/', views.hr_guest_cvs_list, name='hr_guest_cvs_list'),
    # path('hr/guest-cv/<int:pk>/', views.guest_cv_detail, name='guest_cv_detail'),

    # Custom guest forgot password (Frontend View) - Working with vuexy
    # path('guest-forgot-password/', views.guest_forgot_password, name='guest_forgot_password'),
    path('guest-forgot-password/', GuestForgotPasswordView.as_view(), name='guest_forgot_password'),
    path('guest-reset-password/', GuestResetPasswordView.as_view(), name='guest_reset_password'),

    # Dashboard password change view
    path('dashboard/change-password/', GuestChangePasswordView.as_view(), name='guest_change_password_dashboard'),


    # Django built-in password reset views
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]
