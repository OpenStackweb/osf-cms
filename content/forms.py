from django import forms
from django_select2.forms import Select2TagWidget

from content.models import Post, Tag


# class TagChoices(ModelSelect2TagWidget):
#     queryset = Tag.objects.all()
#     search_fields = ['name__icontains']
#
#     def get_model_field_values(self, value):
#         return {'name': value }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = []
        widgets = {
            'tags': Select2TagWidget,
        }