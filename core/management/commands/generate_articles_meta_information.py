# !/usr/bin/python
# -*- coding: utf-8 -*-
import os
import json
import logging

from django.core.management.base import BaseCommand

logger = logging.getLogger()


class Command(BaseCommand):
    help = 'Generates _meta.md on blog/articles folder to optimize pagination'

    BLACKLIST = ['.DS_Store']

    def _get_all_articles(self, filepath):
        articles = []
        for f in os.listdir(filepath):
            if not os.path.isfile(os.path.join(filepath, f)):
                continue
            if f in self.BLACKLIST:
                continue
            if not f.endswith(".md"):
                continue
            articles.append(f)

        return articles

    def _build_meta_data(self, articles):
        return {
            'articles': articles,
            'total': len(articles)
        }

    def _save_meta_data(self, meta_data):
        with open(os.path.join(os.getcwd(), "blog/articles/meta.json"), "w+") as meta_json:
            meta_json.write(json.dumps(meta_data))

    def handle(self, *args, **options):
        articles = self._get_all_articles(os.path.join(os.getcwd(), "blog/articles"))

        meta_data = self._build_meta_data(articles)

        self._save_meta_data(meta_data)