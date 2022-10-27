from django.urls import path
from . import views


app_name = "works"

urlpatterns = [
        path('login/', views.Login.as_view(), name='login'),
        path("logout/", views.Logout.as_view(), name="logout"),
        path('index/', views.index, name='index'),
        path('pulldown-access/', views.pulldown_access, name='pulldown-access'),
        path('admin-login/', views.AdminLogin.as_view(), name='admin-login'),
        path('admin-login/user-list/', views.user_list, name='user-list'),
        path('admin-login/user-result/<int:user_id>/', views.user_result, name='user-result'),
]
