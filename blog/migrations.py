# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Created by andresilva on 8/30/16"""

import os
from slugify import slugify
from blog.models import Post
# list of files to publish

def publish_articles():
    """"""
    # Get all articles
    publish_url = os.getcwd() + '/blog/articles/publish'
    files = [os.path.join(publish_url, f)
             for f in os.listdir(publish_url)
             if os.path.isfile(os.path.join(publish_url, f))]
    # Delete existing articles
    Post.objects.delete()
    # create all articles
    for filepath in files:
        with open(filepath, 'r+') as f:
            body = "\n".join(f.readlines())

        # check if this title already exists and if so,
        # skip it from being created
        title = os.path.basename(filepath)
        slug = slugify(title)
        post = Post.objects.filter(slug=slug)
        if post.count() != 0:
            post = post.first()
        else:
            post = Post.create(title, body)
        print("\"{}\" was just created".format(post))


__author__ = "andresilva"
__email__ = "andre@unbabel.com"
