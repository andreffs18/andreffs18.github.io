from mock import patch
from django.test import TestCase
from django.core.urlresolvers import reverse

from blog.handlers.articles_handler import ArticlesHandler

from django.views.generic.base import TemplateView

from blog.handlers import ArticlesHandler


class BlogDetailView(TemplateView):
    template_name = "blog/detail.html"

    def get_context_data(self, year, month, day, title, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        context.update(ArticlesHandler.get_article_from_title(title))
        return context



class BlogDetailViewTestCase(TestCase):

    def setUp(self):
        super(BlogDetailViewTestCase, self).setUp()
        self.article_filename = "2000-01-01-00-00-Hello-World!.md"
        self.article = {
            "year": "2000", "month": "01", "day": "01", "body": "# This is a test document",
            "creation_date": "2000-01-01", "hour": "00h00", "title": "Hello World!",
        }

    def test_get_request(self):
        """
        Ensure that simple GET request to blog detail view returns expected response
        """
        res = self.client.get(reverse('blog:detail', slug=self.article_filename))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Paid Editor Evaluations")
