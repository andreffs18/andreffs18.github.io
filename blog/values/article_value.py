import re
from core.values import ValueComposite


class ArticleValue(ValueComposite):

    def __init__(self, slug, body):
        super(ArticleValue, self).initialize({})

        creation_date, hour, title = re.search(r'(\d{4}-\d{2}-\d{2})-(\d{2}-\d{2})-(.*)', slug).groups()
        year, month, day = creation_date.split("-")

        details = re.findall(r'---\n([$&+,:;=?@#|<>.^*()%!-_ \n\w\d!"\']*)---\n', body)
        if details:
            self._serialize_image(details[0])
            self._serialize_tags(details[0])
            self._serialize_author(details[0])

            # remove details from body
            body.replace(details[0], "")

        self.serialize_with(year=year)
        self.serialize_with(month=month)
        self.serialize_with(day=day)
        self.serialize_with(body=body)
        self.serialize_with(creation_date=creation_date)
        self.serialize_with(hour=hour.replace("-", "h"))

        title = title.replace("-", " ")
        if title.endswith(".md"):
            title = title.replace(".md", "")

        self.serialize_with(title=title)

    def _serialize_image(self, details):
        # self.serialize_with(tags=["this", "is", "a", "tag"])
        tags = re.findall(r'tags: (.*)', details)
        if tags:
            self.serialize_with(tags=list(map(lambda tag: tag.strip(), tags[0].split(","))))

    def _serialize_tags(self, details):
        # self.serialize_with(image="/static/img/education.jpg")
        image = re.findall(r'image: (.*)', details)
        if image:
            self.serialize_with(image=image[0].strip())

    def _serialize_author(self, details):
        author = re.findall(r'author: (.*)', details)
        if author:
            self.serialize_with(author=author[0].strip())
