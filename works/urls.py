from django.urls import path
from . import views


app_name = "works"

urlpatterns = [
        path('login/', views.Login.as_view(), name='login'),
        path('index/', views.index, name='index'),
        path('admin-login/', views.admin_login, name='admin-login'),
        path('user-list/', views.user_list, name='user-list'),
        path('user-result/', views.user_result, name='user-result'),
]
