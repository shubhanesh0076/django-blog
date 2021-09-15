#from typing_extensions import Required
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.db.models import fields
from django.db.models.fields import files
from django.forms import widgets
from . models  import Post, Userprofile
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField



class Edit_blog(forms.ModelForm):
    class Meta:
        model=Post
        fields=('title','category','bannerimage', 'thumbnailimg', 'content',)
        widgets = {
         'title': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Type topic here.', 'required':'true' }),
         'category': forms.Select(attrs = {'class': 'form-control', 'required':'true' }),
         #'title_tag': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Give the title tag', 'require':'true' }),
         #'content':   RichTextField(attrs = {'class': 'form-control', 'placeholder': 'Give the title tag' }),
         #'snippets': forms.Textarea(attrs = {'class': 'form-control', 'placeholder': 'Short intro about topic.' }),
         }
        labels ={'category': 'Choose A Category'}
        
      

class post_blog(forms.ModelForm):
    #content = forms.CharField(widget=CKEditorWidget(), required=True)
    #content=forms.CharField(widget=RichTextUploadingField(), required=True)
    bannerimage=forms.ImageField(required=True)
    thumbnailimg=forms.ImageField(required=True)

    class Meta:
        model=Post
        fields=('title','category','bannerimage', 'thumbnailimg', 'content',)
        

        widgets = {
         'title': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Type topic here.'}),
         #'title_tag': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Give a title tag', 'required':'true'}),
         'category': forms.Select(attrs = {'class': 'form-control', 'required':'true'}),
         #'content': forms.CharField('name':'RichTextUploadingField', )
         #'snippets': forms.Textarea(attrs = {'class': 'form-control', 'placeholder': 'Short description about topic.', 'required': 'true'}),
         }
        labels ={'category': 'Choose A Category'}
        

class Userprofileimageform(forms.ModelForm):
    class Meta:
        model=Userprofile
        fields=('userprofileimg',)

class Userprofilebannerform(forms.ModelForm):
    class Meta:
        model=Userprofile
        fields=('userbannerimage',)




