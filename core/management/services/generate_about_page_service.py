import logging
logger = logging.getLogger(__name__)


class GenerateAboutPageService:

    def __init__(self, source_filepath="about.md", target_filepath="about.html"):
        self.source_filepath = source_filepath
        self.target_filepath = target_filepath

    def _get_about_page_content(self):
        logger.debug(u"Reading new content from {}...".format(self.source_filepath))
        about_page_html = []
        with open(self.source_filepath, 'r') as about_file:
            lines = about_file.readlines()
            logger.debug("Found {} lines on {}...".format(len(lines), self.source_filepath))

            for l in lines:
                # first get lead text and strip out all the hashtags
                if l.startswith("##"):
                    l = l[2:]
                about_page_html.append(l.strip())

        logger.debug(u"Removing empty lines...")
        about_page_html = list(filter(None, about_page_html))
        return about_page_html

    def _update_about_page_content(self, new_about_page):
        # update about html file located in "_dynamic_content" templates
        logger.debug(u"Updating {} dynamic_content...".format(self.target_filepath))
        with open('core/templates/_dynamic_content/{}'.format(self.target_filepath), 'w+') as about_file:
            about_file.seek(0)
            about_file.writelines(new_about_page)
        return True

    def call(self):
        logger.info(u'Updating page "{}".'.format(self.target_filepath))
        parsed_about_html = self._get_about_page_content()
        self._update_about_page_content(parsed_about_html)
        logger.info(u"About page was successfully updated with {} new entries.".format(len(parsed_about_html)))
