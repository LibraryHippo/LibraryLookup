#!/usr/bin/env python

import logging

class Catalogue:
    def __init__(self, xisbn):
        self.xisbn = xisbn

    def find_item(self, isbn, libraries):
        items = []
        for library in libraries:
            logging.debug('looking for ' + isbn)
            item = library.find_item(isbn)
            if item:
                items.append(item)
            else:
                other_editions = self.xisbn.get_editions(isbn)
                for edition in other_editions:
                    if edition == isbn:
                        continue
                    logging.debug('looking for ' + edition)
                    item = library.find_item(edition)
                    if item:
                        items.append(item)
                        break
        return items
