#!/usr/bin/env python

class Catalogue:
    def __init__(self, xisbn):
        self.xisbn = xisbn

    def find_item(self, isbn, libraries):
        item = libraries[0].find_item(isbn)
        if item:
            return item

        other_editions = self.xisbn.get_editions(isbn)
        for edition in other_editions:
            if edition == isbn:
                continue
            item = libraries[0].find_item(edition)
            if item:
                return item

        return None


        
