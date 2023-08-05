from django.urls import path, include
from django.contrib.auth.views import (LoginView, LogoutView, 
                                       PasswordChangeDoneView, 
                                       PasswordChangeView,
                                       PasswordResetDoneView,
                                       PasswordResetView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView)
from .views import user_follow, register, edit, user_detail, user_list



urlpatterns = [
     path('login/', LoginView.as_view(), name='login'),
     path('logout/', LogoutView.as_view(), name='logout'),
     path('password-change/', PasswordChangeView.as_view(),
          name='password_change'),
     path('password-change/done/', PasswordChangeDoneView.as_view(),
          name='password_change_done'),
     path('password-reset/', PasswordResetView.as_view(),
          name='password_reset'),
     path('password-reset/done/', PasswordResetDoneView.as_view(),
          name='password_reset_done'),
     path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
          name='password_reset_confirm'),
     path('password-reset/complete/', PasswordResetCompleteView.as_view(),
          name='password_reset_complete'),
     path('', include('django.contrib.auth.urls')),
     path('registration/', register, name='register'),
     path('edit/', edit, name='edit' ),
     path('users/', user_list, name='user_list'),
     path('users/follow/', user_follow, name='user_follow'),
     path('users/<username>/', user_detail, name='user_detail'),
]