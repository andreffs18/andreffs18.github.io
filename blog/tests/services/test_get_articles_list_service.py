import os
from mock import patch
from django.test import TestCase

from blog.services.get_articles_list_service import GetArticlesListService


class GetArticlesListServiceTestCase(TestCase):

    def setUp(self):
        super(GetArticlesListServiceTestCase, self).setUp()
        self.article_filename = "2000-01-01-00-00-Hello-World!.md"

    def test_service_initialization(self):
        """
        Ensure that service __init__ is initializing correct values, no matter the input
        """
        service = GetArticlesListService()
        self.assertEqual(service.filepath, os.path.join(os.getcwd(), "blog/articles/meta.json"))

    @patch("open.read")
    def test_call_success(self, mock_meta_json):
        """
        Ensure that service call is working properly and returning expected article value
        """
        mock_meta_json.return_value = [{"articles": ["2000-01-01-00-00-Hello-World!.md"]}]

        self.assertEqual(["2000-01-01-00-00-Hello-World!.md"], GetArticlesListService(self.article_filename).call())
        mock_meta_json.assert_called_with(self.article_filename)
        self.assertTrue(mock_meta_json.called)
        self.assertEqual(mock_meta_json.call_count, 1)
