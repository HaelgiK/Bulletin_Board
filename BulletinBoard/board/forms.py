from django import forms
from django.core.exceptions import ValidationError
from board.models import Post, Comment, Category
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.translation import gettext_lazy as _


# class PostForm(forms.ModelForm):
#    class Meta:
#        model = Post
#        fields = '__all__'
#
#
# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['text']
#
#     def clean(self):
#         cleaned_data = super().clean()
#         header = cleaned_data.get('header')
#         content = cleaned_data.get('content')
#         if header is not None and len(header) > 50:
#             raise ValidationError({'header': 'Название не может быть более 50 символов.'})
#         if header == content:
#             raise ValidationError('The content shall differ from the title')
#         return cleaned_data

# class PostForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         category_choices = kwargs.pop('category_choices', None)
#         super().__init__(*args, **kwargs)
#         if category_choices:
#             self.fields['categories'].queryset = category_choices
#
#     image = forms.ImageField(required=False)
#     video_url = forms.URLField(required=False)

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
