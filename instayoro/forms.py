from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import fields
from django.forms import widgets
from django.forms.widgets import Input, TextInput, Widget

from instayoro.models import Album, Image

class NewUserForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit = True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class NewAlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ("name", "hashtags", "publish")

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(NewAlbumForm, self).__init__(*args, **kwargs)

    def save(self):
        album = super(NewAlbumForm, self).save(commit= False)
        album.created_by = self.user
        album.save()
        return album

class NewImageForm(forms.ModelForm):

    color = forms.CharField(widget = forms.TextInput(attrs={'type':'color'}))

    class Meta:
        model = Image
        fields = ("image", "title", "color", "position", "hashtags", "album", "publish")
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(NewImageForm, self).__init__(*args, **kwargs)
        self.fields['album'] = forms.ModelChoiceField(queryset=Album.objects.filter(created_by=self.user))

    def save(self):
        image = super(NewImageForm, self).save(commit= False)
        image.created_by = self.user
        image.save()
        return image
