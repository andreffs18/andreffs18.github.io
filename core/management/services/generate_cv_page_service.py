import logging
logger = logging.getLogger(__name__)


class GenerateCVPageService:

    CV_SECTION_TEMPLATE = """
<div class="row section">
    <div class="col-md-2">
        <h3 class="text-uppercase">{category}</h3>
    </div>
    <div class="col-md-10">
        {row}
    </div>
</div>
"""
    CV_ROW_TEMPLATE = """
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
        rows = [self.CV_ROW_TEMPLATE.format(title=row.get('title'),
                                            date=row.get('date'),
                                            description="\n".join(filter(None, row.get('description'))))
                for row in kwargs.get('row')]

        section = self.CV_SECTION_TEMPLATE.format(category=kwargs.get('category'), row="\n".join(rows))
        return section

    def __init__(self, source_filepath="cv.md", target_filepath="cv.html"):
        self.source_filepath = source_filepath
        self.target_filepath = target_filepath

    def call(self):
        logger.info(u'Updating page "{}".'.format(self.target_filepath))

        new_cv_page = []
        with open(self.source_filepath, 'r') as cv_file:
            lines = cv_file.readlines()

            section = None
            for l in lines:
                # first get lead text and strip out all the hashtags
                if l.startswith("## "):
                    if section is not None:
                        new_cv_page.append(self._generate_cv_section(**section))

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
                    l = l.strip()

                    rows = section.get('row', [])
                    if len(rows) == 0:
                        continue
                    if len(rows[-1].get('description', [])) == 0:
                        section['row'][-1]['description'] = [l]
                    else:
                        section['row'][-1]['description'].append(l)

            if section is not None:
                new_cv_page.append(self._generate_cv_section(**section))

        # update cv html file located in "_dynamic_content" templates
        with open('core/templates/_dynamic_content/{}'.format(self.target_filepath), 'w+') as cv_file:
            cv_file.seek(0)
            cv_file.writelines(new_cv_page)

        logger.info("Home page was successfully updated with {} new entries.".format(len(new_cv_page)))
