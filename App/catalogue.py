#!/usr/bin/env python

class Catalogue:
    def __init__(self, xisbn):
        self.xisbn = xisbn

    def find_item(self, isbn, libraries):
        items = []
        for library in libraries:
            item = library.find_item(isbn)
            if item:
                items.append(item)

            other_editions = self.xisbn.get_editions(isbn)
            for edition in other_editions:
                if edition == isbn:
                    continue
                item = library.find_item(edition)
                if item:
                    items.append(item)
        return items


        
