from django.urls import path,include
from django.contrib.auth import views as auth_views
from .views import register,ProfileUpdateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    path('register/',register,name='register'),
    path('profile/<int:pk>/',ProfileUpdateView.as_view(),name='profile'),
]

# This is mandatory if you want to display images
if settings.DEBUG:
	urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

