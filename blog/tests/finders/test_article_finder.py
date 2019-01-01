from mock import patch
from django.test import TestCase

from blog.finders.article_finder import ArticleFinder


class ArticleFinderTestCase(TestCase):

    @patch("blog.services.get_articles_list_service.GetArticlesListService.call")
    def test_by_title_returns_none(self, mock_get_articles):
        """
        Ensure that using "by_title()" is returning None when given article title doesn't exist
        """
        mock_get_articles.return_value = ["2000-01-01-00-00-Hello-World!.md"]
        self.assertIsNone(ArticleFinder.by_title("No title"))

    @patch("blog.services.get_articles_list_service.GetArticlesListService.call")
    def test_by_title_raise_value_error(self, mock_get_articles):
        """
        Ensure that using "by_title()" is raising ValueError if multiple articles were found with the same title
        """
        mock_get_articles.return_value = ["2000-01-01-00-00-Hello-World!.md", "2000-01-01-00-00-Hello-World!.md"]
        self.assertRaises(ValueError, ArticleFinder.by_title("Hello-World!.md"))

    @patch("blog.services.get_articles_list_service.GetArticlesListService.call")
    def test_by_title_success(self, mock_get_articles):
        """
        Ensure that using "by_title()" is returning expected article
        """
        mock_get_articles.return_value = ["2000-01-01-00-00-Hello-World!.md"]
        self.assertEqual(ArticleFinder.by_title("Hello-World!.md"), "2000-01-01-00-00-Hello-World!.md")
