from django import forms
from .models import Post

class PostCreateForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title','content','slug']
    class Media:
        js=('tinyinject.js',)