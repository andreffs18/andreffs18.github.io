from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name'}), required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'E-mail'}), required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Message'}), required=True)