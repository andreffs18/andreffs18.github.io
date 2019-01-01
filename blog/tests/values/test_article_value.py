from django.test import TestCase

from blog.values.article_value import ArticleValue


class ArticleValueTestCase(TestCase):
    def setUp(self):
        super(ArticleValueTestCase, self).setUp()
        self.article_filename = "2000-01-01-00-00-Hello-World!.md"
        self.article = {
            "year": "2000", "month": "01", "day": "01", "body": "# This is a test document",
            "creation_date": "2000-01-01", "hour": "00h00", "title": "Hello World!",
        }

    def test_value_to_dict(self):
        """
        Ensure that value is returning expected dictionary
        """
        self.assertEqual(self.article, ArticleValue(self.article_filename, self.article.get('body')).to_dict())
