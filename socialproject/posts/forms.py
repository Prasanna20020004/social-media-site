from .models import Posts, Comment
from django import forms

class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'caption', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)