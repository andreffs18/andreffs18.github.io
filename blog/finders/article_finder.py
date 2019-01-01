import logging
from blog.services.get_articles_list_service import GetArticlesListService

logger = logging.getLogger(__name__)


class ArticleFinder:

    @classmethod
    def by_title(cls, title):
        article = list(filter(lambda article: article.endswith(title), GetArticlesListService().call()))

        if len(article) == 0:
            logger.error(u'Article "{}" does not exist.'.format(title))
            return None
        if len(article) > 1:
            raise ValueError(u'Two articles with same title "{}"'.format(title))

        return article[0]
