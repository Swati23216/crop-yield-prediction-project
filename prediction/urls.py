from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', LogoutView.as_view(http_method_names=['get', 'post'], next_page='login'), name='logout'),
    path('signup/', views.signup, name='signup'),
    
    # User URLs
    path('', views.user_dashboard, name='user_dashboard'),
    path('crop-review/', views.crop_review, name='crop_review'),
    path('crop-details/<int:crop_id>/', views.crop_details, name='crop_details'),
    path('crop-prediction/', views.crop_prediction, name='crop_prediction'),
    
    # Admin URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-crop/', views.add_crop, name='add_crop'),
    path('update-crop/<int:crop_id>/', views.update_crop, name='update_crop'),
    path('delete-crop/<int:crop_id>/', views.delete_crop, name='delete_crop'),
]