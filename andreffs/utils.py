__author__ = 'andresilva'

import logging
logger = logging.getLogger('andreffs' + __name__)


def generate_cv(filepath='.md/cv.md'):
    """
    Generates CV dictionary from cv.md file existing in .md folder.
    """
    with open(filepath, 'r') as cv_file:
        cv = {}
        sections = []
        lines = filter(None, map(lambda x: x.rstrip(), cv_file.readlines()))
        for line in lines:

            # h2 header (cv block)
            if line.startswith("## "):
                current_key = line.replace("## ", "").rstrip().lower()
                sections.append(current_key)
                cv[current_key] = []
                continue

            # h3 header (place)
            elif line.startswith("### "):
                place = line.replace("### ", "").rstrip()

                block = {}
                cv[current_key].append(block)
                block['place'] = place
                continue

            # h4 header (period of time)
            elif line.startswith("#### "):
                period = line.replace("#### ", "").rstrip()
                block['period'] = period
                continue

            else:
                line = line.rstrip()
                if 'description' not in block:
                    block['description'] = []
                block['description'].append(line)
                continue

        output = []
        for section in sections:
            for sec in cv[section]:
                sec['description'] = "".join(sec['description'])
            output.append({section : cv[section]})

    return output


def generate_about(filepath=".md/about.md"):
    """
    Generates about page form file about.md in .md folder
    """
    about = []

    with open(filepath, 'r') as about_file:
        lines = filter(None, map(lambda x: x.rstrip(), about_file.readlines()))
        for line in lines:
            if line.startswith("## "):
                continue

            elif line.startswith("### "):
                title = line.replace("### ", "").rstrip()
                about.append(title)
                continue

            else:
                line = line.rstrip()
                about.append(line)
                continue

    return "".join(about)