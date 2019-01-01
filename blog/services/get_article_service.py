import os

from blog.values.article_value import ArticleValue


class GetArticleService:

    def __init__(self, slug, articles_filepath=None):
        self.slug = slug
        self.articles_filepath = articles_filepath or os.getcwd() + '/blog/articles'

    def call(self):
        if not os.path.isfile(os.path.join(self.articles_filepath, self.slug)):
            raise ValueError(u'Article "{}" doesn\'t exist'.format(self.slug))

        article_path = os.path.join(self.articles_filepath, self.slug)
        with open(article_path, 'r+') as article:
            body = article.read()

        return ArticleValue(self.slug, body).to_dict()
