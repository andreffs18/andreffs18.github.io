from django.views.generic.base import TemplateView

from blog.handlers import ArticlesHandler


class BlogDetailView(TemplateView):
    template_name = "blog/detail.html"

    def get_context_data(self, year, month, day, title, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        context.update(ArticlesHandler.get_article_from_title(title))
        return context
