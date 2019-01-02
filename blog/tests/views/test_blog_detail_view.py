from mock import patch
from django.test import TestCase
from django.core.urlresolvers import reverse


class BlogDetailViewTestCase(TestCase):

    def setUp(self):
        super(BlogDetailViewTestCase, self).setUp()
        self.article_filename = "2000-01-01-00-00-Hello-World!.md"
        self.article = {
            "year": "2000", "month": "01", "day": "01", "body": "# This is a test document",
            "creation_date": "2000-01-01", "hour": "00h00", "title": "Hello World!",
        }

    @patch("blog.handlers.articles_handler.ArticlesHandler.get_article_from_title")
    def test_get_request(self, mock_get_article_from_title):
        """
        Ensure that simple GET request to blog detail view returns expected response
        """
        mock_get_article_from_title.return_value = {"post": self.article}

        # TODO: This should be a service
        slug = self.article.get('title').replace(" ", "-") + ".md"
        args = ("{year} {month} {day}".format(**self.article).split(" ")) + [slug]

        res = self.client.get(reverse('blog:detail', args=args))
        self.assertEqual(res.status_code, 200)
