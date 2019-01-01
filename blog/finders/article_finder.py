from blog.services.get_articles_list_service import GetArticlesListService


class ArticleFinder:

    @classmethod
    def by_title(cls, title):
        article = list(filter(lambda article: article.endswith(title), GetArticlesListService().call()))
        if len(article) > 1:
            raise ValueError("Two articles with same title")

        return article[0]
