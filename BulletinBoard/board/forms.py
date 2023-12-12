from django import forms
from django.core.exceptions import ValidationError
from board.models import Post, Comment, Category
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.translation import gettext_lazy as _


class PostForm(forms.ModelForm):
    header = forms.CharField(label='Header')
    content = forms.CharField(widget=CKEditorUploadingWidget,
                                label='Content')
    # categories = forms.ModelChoiceField(queryset=Category.objects.all(),
    #                                        label='Category',
    #                                        empty_label='Not selected')
    def __init__(self, *args, **kwargs):
        category_choices = kwargs.pop('category_choices', None)
        super().__init__(*args, **kwargs)
        if category_choices:
            self.fields['categories'].queryset = category_choices

    class Meta:
        model = Post
        fields = ['categories', 'header', 'content'] #'image', 'video_url']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'text',
        ]
