from mock import patch
from django.test import TestCase

from blog.handlers.articles_handler import ArticlesHandler


class ArticleFinderTestCase(TestCase):

    def setUp(self):
        super(ArticleFinderTestCase, self).setUp()
        self.article_filename = "2000-01-01-00-00-Hello-World!.md"
        self.article = {
            "year": "2000", "month": "01", "day": "01", "body": "# This is a test document",
            "creation_date": "2000-01-01", "hour": "00h00", "title": "Hello World!",
        }

    @patch("blog.services.get_article_service.GetArticleService.call")
    @patch("blog.services.get_articles_list_service.GetArticlesListService.call")
    def test_get_articles(self, mock_get_articles_list, mock_get_article):
        """
        Ensure that get_articles() is returning the expected response
        """
        mock_get_articles_list.return_value = [self.article_filename]
        mock_get_article.return_value = [self.article]
        expected_response = {"posts": [self.article]}

        self.assertEqual(expected_response, ArticlesHandler.get_articles())
        mock_get_articles_list.assert_called_with()
        self.assertTrue(mock_get_articles_list.called)
        self.assertEqual(mock_get_articles_list.call_count, 1)

        mock_get_article.assert_called_with(self.article_filename)
        self.assertTrue(mock_get_article.called)
        self.assertEqual(mock_get_article.call_count, 1)

    @patch("blog.services.get_article_service.GetArticleService.call")
    def test_get_article_from_title(self, mock_get_article):
        """
        Ensure that get_article_from_title() is retuning the expected article response
        """
        mock_get_article.return_value = [self.article]
        expected_response = {"post": self.article}
        self.assertEqual(expected_response, ArticlesHandler.get_article_from_title(self.article.get('title')))

        mock_get_article.assert_called_with(self.article_filename)
        self.assertTrue(mock_get_article.called)
        self.assertEqual(mock_get_article.call_count, 1)
