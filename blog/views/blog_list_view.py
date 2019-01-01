from django.views.generic.base import TemplateView

from blog.handlers import ArticlesHandler


class BlogListView(TemplateView):
    template_name = "blog/list.html"

    def get_context_data(self, page=1, **kwargs):
        context = super(BlogListView, self).get_context_data(**kwargs)
        context.update(ArticlesHandler.get_articles(page))
        return context
