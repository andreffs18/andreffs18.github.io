from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from blog.services.get_article_service import GetArticleService
from blog.services.get_articles_list_service import GetArticlesListService
from blog.finders.article_finder import ArticleFinder


class ArticlesHandler:

    @classmethod
    def get_articles(cls, page=1, limit=10):
        articles = GetArticlesListService().call()
        paginator = Paginator(articles, limit)
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            articles = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page.
            articles = paginator.page(paginator.num_pages)

        return {"posts": list(map(lambda slug: GetArticleService(slug).call(), articles))}

    @classmethod
    def get_article_from_title(cls, title):
        slug = ArticleFinder.by_title(title)
        return {"post": GetArticleService(slug).call()}
