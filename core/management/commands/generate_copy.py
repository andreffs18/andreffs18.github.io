# !/usr/bin/python
# -*- coding: utf-8 -*-
import logging

from django.core.management.base import BaseCommand

logger = logging.getLogger()


class Command(BaseCommand):
    help = 'Generates content for the About page using the file "about.md" located on this project\'s root folder.'

    cv_section_template = """
<div class="row section">
    <div class="col-md-2">
        <h3 class="text-uppercase">{category}</h3>
    </div>
    <div class="col-md-10">
        {row}
    </div>
</div>
"""
    cv_row_template = """
        <div class="row">
            <div class="col-md-6">
                <h4 class="text-left text-md-right">{title}</h4>
                <h5 class="text-left text-md-right">{date}</h5>
            </div>
            <div class="col-md-6 text-left description">
                {description}
            </div>
        </div>
"""

    def _generate_cv_section(self, **kwargs):
        rows = list()
        for row in kwargs.get('row'):
            rows.append(self.cv_row_template.format(title=row.get('title'), date=row.get('date'),
                                                    description="\n".join(filter(None, row.get('description')))))
        section = self.cv_section_template.format(category=kwargs.get('category'), row="\n".join(rows))
        return section

    def generate_home_html_file(self, source_file_path="cv.md", target_file_path="cv.html"):
        logger.info("Updating {} file.".format(target_file_path))
        parsed_cv_html = []
        # get file 'cv.md'
        logger.debug("Reading new content from {}...".format(source_file_path))
        with open(source_file_path, 'r') as cv_file:
            logger.debug("Parsing content...")
            lines = cv_file.readlines()
            logger.debug("Found {} lines on {}...".format(len(lines), source_file_path))
            section = None
            for l in lines:
                # first get lead text and strip out all the hashtags
                if l.startswith("## "):
                    if section is not None:
                        parsed_cv_html.append(
                            self._generate_cv_section(**section))

                    section = dict()
                    l = l[3:]
                    l = l.rstrip().strip()
                    section['category'] = l
                    continue

                elif l.startswith("### "):
                    l = l[4:]
                    l = l.rstrip().strip()
                    rows = section.get('row', [])
                    if len(rows) == 0:
                        section['row'] = [{'title': l}]
                    else:
                        section['row'].append({'title': l})
                    continue

                elif l.startswith("#### "):
                    l = l[5:]
                    l = l.rstrip().strip()
                    section['row'][-1]['date'] = l
                    continue

                else:
                    l = l.rstrip().strip()

                    rows = section.get('row', [])
                    if len(rows) == 0:
                        continue
                    if len(rows[-1].get('description', [])) == 0:
                        section['row'][-1]['description'] = [l]
                    else:
                        section['row'][-1]['description'].append(l)

            if section is not None:
                parsed_cv_html.append(self._generate_cv_section(**section))

        # update cv html file located in "_dynamic_content" templates
        logger.debug("Updating {} dynamic_content...".format(target_file_path))
        target_file_path = ('core/templates/_dynamic_content/{}'.format(target_file_path))
        with open(target_file_path, 'w+') as cv_file:
            cv_file.seek(0)
            for line in parsed_cv_html:
                cv_file.write(line)

        logger.info("Home page was successfully updated with {} new entries.".format(len(parsed_cv_html)))

    def generate_about_html_file(self, source_file_path="about.md", target_file_path="about.html"):
        logger.info("Updating {} file.".format(target_file_path))
        parsed_about_html = []
        # get file 'about.md'
        logger.debug("Reading new content from {}...".format(source_file_path))
        with open(source_file_path, 'r') as about_file:
            logger.debug("Parsing content...")
            lines = about_file.readlines()
            logger.debug("Found {} lines on {}...".format(len(lines), source_file_path))
            for l in lines:
                # first get lead text and strip out all the hashtags
                if l.startswith("##"):
                    l = l[2:]

                l = l.rstrip().strip()
                parsed_about_html.append(l)
        # remove any empty spaces
        logger.debug("Removing empty lines...")
        parsed_about_html = filter(None, parsed_about_html)

        # update about html file located in "_dynamic_content" templates
        logger.debug("Updating {} dynamic_content...".format(target_file_path))
        target_file_path = ('core/templates/_dynamic_content/{}'.format(target_file_path))
        with open(target_file_path, 'w+') as about_file:
            about_file.seek(0)
            for line in parsed_about_html:
                about_file.write(line)

        logger.info("About page was successfully updated with {} new entries.".format(len(parsed_about_html)))

    def handle(self, *args, **options):
        self.generate_home_html_file()
        self.generate_about_html_file()
