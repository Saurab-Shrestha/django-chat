from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CustomTokenPairView,
    UserDetailsView,
    RegisterView,
    LogoutView,
    LogoutAllView,
    UserListView
)

urlpatterns = [
    path('login/', CustomTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', UserDetailsView.as_view(), name='user_details'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout-all/', LogoutAllView.as_view(), name='logout_all'),
    path('', UserListView.as_view(), name='user_list'),
]
