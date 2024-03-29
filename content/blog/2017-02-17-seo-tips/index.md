---
title: "SEO Tips"
slug: seo-tips
subtitle: ""
date: 2017-02-17T00:45:32+00:00
draft: false
tags: ["seo", "automation", "git-hooks"]
toc: false
plotly: false
---

My key takeaways from making this website "SEO friendly":

1. Use link "tree structure" from homepage. This way, bots and crawlers can find every page on the website
2. Good **titles**, under 65 characters
3. Meta tags with good keywords under 100 characters
4. Use canonical urls on every page

```html
<link rel="canonical" href="http://localhost:1313/blog/seo-tips/">
<!-- instead of -->
<link rel="canonical" href="/blog/seo-tips">
```

5. Add "alt" tag to images

```html
<img alt="About me picture" src="/images/about.jpeg">
```

## Pre-commit hooks

Having this checklist is nice but it would be better if I didn't have to check this by myself every time I do a side project.

In that spirit, we can create something, like a CI/CD stage or a pre-commit hook that checks all of these rules!

So I've built a simple pre-commit hook that checks for all those rules:

```python
# .git/hooks/seo-pre-commit.py
import re
import sys


def check_title_length(html, max_length=65):
    """
    Search on given `html` file for any <title> tags and check if the title length is greater
    than `max_length`.
    """
    titles = re.findall(r"<title>(.*?)</title>", html)
    for title in titles:
        if len(title) > max_length:
            _warning(u"{}: ⚠️ No title {} length more than {}!".format(filepath, title, max_length))


def check_alt_prop(html):
    """
    Search on given `html` file for all <img> tags and alert if:
    - img tag has "alt=" attribute but without content (eg: alt="")
    - img tag does not have "atl=" attribute
    """
    alt_texts = re.findall(r"<img.*?alt=[\'\"](.*?)[\'\"][^>]*>", html)
    for alt in alt_texts:
        if not alt:
            _warning(u"{}: ⚠️  No alt text!".format(filepath))

    missing_alt_texts = re.findall(r"<img(?!.*?alt=([\'\"]).*?)[^>]*>", html)
    for missing in missing_alt_texts:
        _warning(u"{}: ⚠️  No alt attribute!".format(filepath))


def check_canonical_urls(html):
    """
    Search on given `html` file for all <a> tags and check if configured href is canonical. (absolute url)
    This also accepts urls when href starts with "mailto:" or expected characters: "#", "{", "%", ""
    """
    urls = re.findall(r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"', html)
    for url in urls:
        if any([
            url == "",  # empty url is accepted
            map(lambda rule: url.startswith(rule), ["http", "mailto:", "#", "{", "%"],),
        ]):
            continue
        _warning(u"({}) ⚠️ Relative URL {}!".format(filepath, url))


if __name__ == "__main__":
    for filepath in sys.argv[1:]:
        with open(filepath, "r+") as html:
            html = html.read()
        check_alt_prop(html)
        check_canonical_urls(html)
        check_title_length(html)

    if ERROR:
        sys.exit(1)
```

> If you want to add this to your project, you can download and install it by running the one liner on the companion repository: https://github.com/andreffs18/seo-git-hooks


# External Resources

Below is a list of free tools that helped me analyze my website and see what could be improved:

* [SEO for beginners - Free course](https://www.youtube.com/watch?v=_M7rAjznXFM&list=PLdN82lhRV2eJzgOrTTTmBhHrqR6kTEo07)
* "put your url and we tell you what to do"
    * https://developers.google.com/speed/pagespeed/insights/ & https://web.dev/measure/ (mandatory)
    * http://varvy.com
    * http://websiteoptimization.com/services/analyze/
    * https://gtmetrix.com/
* https://www.xml-sitemaps.com/ - scrapes your website and builds a sitemap
* https://backlinko.com/seo-tools - great "form-like" website to find tools for all of your SEO needs
* https://www.sideprojectchecklist.com/marketing-checklist - complete thorough checklist for all your side projects
* https://web.dev/vitals/ - good blog post about web vitals
* https://www.fastorslow.com/app - lets you know how much time around the globe does it take to open your website.

👋
