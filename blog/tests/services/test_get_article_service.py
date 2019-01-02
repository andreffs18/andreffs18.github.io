import os
from mock import patch
from django.test import TestCase

from blog.services.get_article_service import GetArticleService


class GetArticleServiceTestCase(TestCase):

    def setUp(self):
        super(GetArticleServiceTestCase, self).setUp()
        self.article_filename = "2000-01-01-00-00-Hello-World!.md"
        self.article = {
            "year": "2000", "month": "01", "day": "01", "body": "# This is a test document",
            "creation_date": "2000-01-01", "hour": "00h00", "title": "Hello World!",
        }

    def test_service_initialization(self):
        """
        Ensure that service __init__ is initializing correct values, no matter the input
        """
        service = GetArticleService(self.article_filename)
        self.assertEqual(service.slug, self.article_filename)
        self.assertEqual(service.articles_filepath, os.path.join(os.getcwd(), 'blog/articles'))

    def test_call_raises_value_error(self):
        """
        Ensure that service call is raising ValueError if file doesn't exist
        """
        self.assertRaises(ValueError, GetArticleService("Non Existing File.md").call)

    @patch("blog.values.article_value.ArticleValue.to_dict")
    # @patch("blog.services.get_article_service.os")
    def test_call_success(self, mock_article_value):
        """
        Ensure that service call is working properly and returning expected article value
        """
        # mock_os.is_file.return_value = True
        mock_article_value.return_value = [self.article]
        #
        #self.assertEqual(self.article, GetArticleService(self.article_filename).call())
        #mock_article_value.assert_called_with(self.article_filename, "# This is a test document")
        #self.assertTrue(mock_article_value.called)
        #self.assertEqual(mock_article_value.call_count, 1)
