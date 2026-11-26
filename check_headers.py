#!/usr/bin/env python3
"""Check the headers of the corpus for the errors a copied file leaves behind.

Reports only; it changes nothing. Run from the root of the repository:

    python3 check_headers.py

What it checks:

  1. <idno type="tm">, <idno type="edr">, <idno type="uel"> are unique across the
     corpus - the same number in two files means one was not updated
  2. <idno type="filename"> matches the actual file name
  3. the <title> names the inscription this file is about
  4. <idno type="inventory"> is unique
  5. every @ana, @ref and @corresp that should be a fragment pointer begins with #
"""

import os
import re
import sys
from collections import defaultdict

from saxonche import PySaxonProcessor

XML_DIR = "inscriptions"

# Words in a file name that say nothing about which person it is.
STOPWORDS = {"fl", "flavius", "flavia", "aurelius", "aurelia", "inscription", "et", "the", "of"}

UNIQUE_IDNO = ("tm", "edr", "uel", "inventory")


def tokens(stem):
    parts = re.split(r"[^a-z0-9]+", stem.lower())
    return [p for p in parts if len(p) >= 4 and p not in STOPWORDS]


def value(xp, expression):
    result = xp.evaluate(expression)
    if result is None or result.size == 0:
        return ""
    return result.item_at(0).string_value.strip()


def values(xp, expression):
    result = xp.evaluate(expression)
    if result is None:
        return []
    return [result.item_at(i).string_value.strip() for i in range(result.size)]


def main():
    if not os.path.isdir(XML_DIR):
        sys.exit("'%s' not found - run this from the root of the repository" % XML_DIR)

    problems = defaultdict(list)
    seen = {kind: defaultdict(list) for kind in UNIQUE_IDNO}
    checked = 0

    with PySaxonProcessor(license=False) as proc:
        xp = proc.new_xpath_processor()
        for name in sorted(os.listdir(XML_DIR)):
            if not name.lower().endswith(".xml"):
                continue
            path = os.path.join(XML_DIR, name)
            stem = os.path.splitext(name)[0]
            checked += 1
            try:
                xp.set_context(xdm_item=proc.parse_xml(xml_file_name=path))
            except Exception as error:
                problems[name].append("could not be read: %s" % error)
                continue

            # 2. the declared file name
            declared = value(xp, "//*[local-name()='publicationStmt']"
                                 "/*[local-name()='idno'][@type='filename']")
            if declared and declared != name:
                problems[name].append("<idno type='filename'> says '%s'" % declared)

            # 3. the title
            title = value(xp, "//*[local-name()='titleStmt']/*[local-name()='title'][1]")
            wanted = tokens(stem)
            if title and wanted and not any(w in title.lower() for w in wanted):
                problems[name].append("the title is '%s' but the file is '%s'" % (title, name))

            # 1 and 4. identifiers that must be unique
            for kind in UNIQUE_IDNO:
                for found in values(xp, "//*[local-name()='idno'][@type='%s']" % kind):
                    if found:
                        seen[kind][found].append(name)

            # 5. fragment pointers written without the hash
            for attr in ("ana", "corresp"):
                for found in values(xp, "//@*[local-name()='%s']" % attr):
                    for token in found.split():
                        if token and not token.startswith("#") and "#" not in token \
                           and not token.startswith(("http", "../", "./")):
                            problems[name].append(
                                "@%s='%s' has no '#': it points to a file, not to an id"
                                % (attr, token))

    # the uniqueness report
    for kind in UNIQUE_IDNO:
        for found, files in sorted(seen[kind].items()):
            if len(files) > 1:
                for name in files:
                    others = [f for f in files if f != name]
                    problems[name].append(
                        "<idno type='%s'>%s</idno> is also in %s"
                        % (kind, found, ", ".join(others)))

    print("%d file(s) checked, %d with something to look at\n" % (checked, len(problems)))
    for name in sorted(problems):
        print(name)
        for problem in problems[name]:
            print("    %s" % problem)
        print()


if __name__ == "__main__":
    main()
