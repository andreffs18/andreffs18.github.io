from django import forms



# from django.forms import ModelForm
# from contact.models import Sugestion
# class FormFromModel(ModelForm):
#     class Meta:
#         model = Sugestion



class BlogAddPostForm(forms.Form):
    title = forms.CharField(label="Title")
    subtitle = forms.CharField(label="Subtitle", required=False)
    content = forms.CharField(label="content", widget=forms.Textarea)
