from django.contrib import admin

from django import forms
from .models import Comment, Post
from ckeditor_uploader.widgets import CKEditorUploadingWidget
# импортируем модель амдинки
# Register your models here.

admin.site.register(Comment)
admin.site.register(Post)




# class PostAdminForm(forms.ModelForm):
#     content = forms.CharField(widget=CKEditorUploadingWidget())
#     class Meta:
#         model = Post
#         fields = '__all__'