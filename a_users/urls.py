from django.urls import path
from a_users.views import profile_view, profile_edit, profile_delete_view


urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('<username>/', profile_view, name='userprofile'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('profile/delete/', profile_delete_view, name='profile-delete'),
    path('profile/onboarding/', profile_edit, name='profile-onboarding'),
]
