import os
import json


class GetArticlesListService:

    def __init__(self, filepath=None):
        self.filepath = filepath or os.path.join(os.getcwd(), "blog/articles/meta.json")

    def call(self):
        return json.load(open(self.filepath))['articles']

