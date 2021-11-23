from django.contrib.auth.models import User
from django.http.response import Http404
from django.shortcuts import redirect, render
from .forms import NewImageForm, NewUserForm, NewAlbumForm
from django.contrib.auth import login
from .models import Album, Image

def user_profile(request, username_lookup=None):
    if username_lookup:
        try:
            user = User.objects.get(username = username_lookup)
        except User.DoesNotExist:
            raise Http404
    elif request.user.is_authenticated:
        return redirect("profile/{}".format(request.user.username))


    if request.user == user and request.user.is_authenticated:

        profile_username = request.user.username
        
        published_albums = []
        albums  = Album.objects.filter(created_by=request.user).filter(publish=True)
        for album in albums:
            temp = {
                'name': album.name,
                'hashtags': album.hashtags,
                'images': Image.objects.filter(created_by=request.user).filter(album=album).filter(publish=True)
            }
            published_albums.append(temp)

        unpublished_albums = []
        albums  = Album.objects.filter(created_by=request.user).filter(publish=False)
        for album in albums:
            temp = {
                'name': album.name,
                'hashtags': album.hashtags,
                'images': Image.objects.filter(created_by=request.user).filter(album=album).filter(publish=False)
            }
            unpublished_albums.append(temp)

        context = {
            'published_albums':published_albums,
            'unpublished_albums':unpublished_albums,
            'profile_username':profile_username
        }

        return render(request, 'instayoro/private_profile.html', context)

    else:
        profile_username = user.username
        published_albums = []
        albums = list(Album.objects.filter(created_by=user).filter(publish=True))
        if len(albums) > 0:
            for album in albums:
                temp = {
                    'name': album.name,
                    'hashtags': album.hashtags,
                    'images': Image.objects.filter(created_by=user).filter(album=album).filter(publish=True)
                }
                published_albums.append(temp)

        context = {
            'published_albums': published_albums,
            'profile_username':profile_username
        }

        return render(request, 'instayoro/public_profile.html', context)

def index(request):

    albums  = Album.objects.filter(publish=True).order_by('date')
    images = Image.objects.filter(publish=True).order_by('date')
    context = {
        'albums': albums,
        'images': images
    }
    return render(request, 'instayoro/index.html', context)

def users_redirect(request):
    if request.user.is_anonymous:
        return redirect("login")
    elif request.user.is_authenticated:
        return redirect("home")

def new_user_registration(request):

    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print("Registration successful.")
            return redirect("home")
        print("Unsuccessful registration. Invalid information.")
    
    form = NewUserForm()
    context = {
        'form':form
    }

    return render(request, 'instayoro/register.html', context)

def new_album(request):

    if request.method == 'POST':
        form = NewAlbumForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            return redirect("home")
    
    form = NewAlbumForm()
    context = {
        'form': form
    }

    return render(request, 'instayoro/new_album.html', context)

def new_image(request):
    if request.method == 'POST':
        form = NewImageForm(request.user, data = request.POST, files = request.FILES)

        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            print(form)
            print("not successful for saving image")
    
    form = NewImageForm(request.user)
    context = {
        'form': form
    }

    return render(request, 'instayoro/new_image.html', context)

def display_album(request, username_lookup=None, album_name=None):

    if username_lookup:
        try:
            user = User.objects.get(username = username_lookup)
        except User.DoesNotExist:
            raise Http404
        else:
            try:
                album = Album.objects.get(created_by=user, name=album_name)
            except Album.DoesNotExist:
                return Http404
            else:

                images = Image.objects.filter(created_by=user).filter(album=album)

                if request.user == user and request.user.is_authenticated:
                    if request.method == 'POST':
                        form = NewAlbumForm(user, request.POST, instance = album)
                        if form.is_valid():
                            form.save()
                            return redirect("redirect_profile")

                    form = NewAlbumForm(user, instance=album)
                    # form.fields['name'].disabled = True
                    context = {
                        'form':form,
                        'images': images
                    }
                    return render(request, 'instayoro/private_album.html', context)
                else:
                    images = images.filter(publish=True).order_by('date')
                    context = {
                        'album': album,
                        'images': images
                    }
                    return render(request, 'instayoro/public_album.html', context)
    else:
        return Http404


## REST API Views

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from .serializers import *

class AlbumViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin):
    serializer_class = AlbumSerializer
    queryset = Album.objects.all()

class UserViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class ImageViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    