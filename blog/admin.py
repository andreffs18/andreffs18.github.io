from django.contrib import admin
from django import forms
from .models import Post


class PostModelForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Post
        fields = "__all__"


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "body", "creation_date",
                    "last_update_at", "tags")

    fields = ("title", "body", "tags")
    exclude = ("creation_date", "last_update_at")
    form = PostModelForm

    def save_model(self, request, obj, form, change):
        return super(PostAdmin, self).save_model(request, obj, form, change)

admin.site.register(Post, PostAdmin)


