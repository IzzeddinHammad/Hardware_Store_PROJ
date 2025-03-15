from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView , ProfileEditView , ProfilePageView , ProfileCreateView

urlpatterns = [
    path('signup/',SignUpView.as_view(),name='signup'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('edit_profile/<int:pk>/' ,ProfileEditView.as_view() , name= 'edit_profile' ),
    path('profile/<int:pk>/',ProfilePageView.as_view(), name='show_profile'),
    path('create_profile/', ProfileCreateView.as_view(), name='create_profile'),
]