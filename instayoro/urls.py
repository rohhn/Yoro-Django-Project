from django.urls import path, re_path
from django.urls.conf import include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'images', views.ImageViewSet)
router.register(r'albums', views.AlbumViewSet)

urlpatterns = [
    path('', views.users_redirect, name='init'),
    path('home', views.index, name='home'),
    path('register',views.new_user_registration, name='new_user_registration'),
    path('new_album', views.new_album, name= 'new_album'),
    path('new_image', views.new_image, name= 'new_image'),
    path('profile', views.user_profile, name="redirect_profile"),
    path('profile/<str:username_lookup>', views.user_profile, name="user_profile"),
    path('profile/<str:username_lookup>/album/<str:album_name>', views.display_album, name="display_album"),
    re_path('^api/', include(router.urls))
]