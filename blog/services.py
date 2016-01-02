# !/usr/bin/python
# """ Created by andresilva on 12/9/15"""
__author__ = 'andresilva'
__version__ = "1.0.0"
__email__ = "andre@unbabel.com"

from os import listdir, getcwd, rename
from os.path import isfile, join
from slugify import slugify

articles_folder = getcwd() + "/blog/articles/saved"


def _wp(filename):
    """returns filename full path length"""
    return articles_folder + "/" + filename


def get_articles_titles():
    """get all posts from <articles folder>"""
    array_of_titles = [f for f in listdir(articles_folder)
                       if isfile(join(articles_folder, f))]
    return array_of_titles


def script__slugify_files():
    """ this will slugify all files under <articles folder>
    from "This is A Test Name.md" to "this_is_a_test_name.md"
    """
    # get all articles titles
    files = get_articles_titles()
    t = len(files)
    for i, f in enumerate(files, 1):
        print("({}/{}) \"{}\" -> \"{}\"".format(i, t, f, slugify(f)))
        rename(_wp(f), _wp(slugify(f)))
    print("Done!")

