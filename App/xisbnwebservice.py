#!/usr/bin/env python

import HTMLParser
import re


def method_url(method, isbn):
    return 'http://xisbn.worldcat.org/webservices/xid/isbn/%(isbn)s?method=%(method)s&format=csv' % vars()


class XisbnWebService:
    def __init__(self, opener):
        self.opener = opener

    def get_editions(self, isbn):
        work_data = self.opener(
            "https://www.goodreads.com/book/isbn/" + isbn).content
        editions_url = self._parse_goodreads_work(work_data)

        editions_parser = self.GoodreadsEditionsParser()
        editions_parser.feed(self.opener(editions_url).content.decode("UTF-8"))
        return editions_parser.all_ISBNs

    def _parse_goodreads_work(self, data):
        return re.search('"([^"]+/work/editions/[^"]+)"', data).group(1)

    class GoodreadsEditionsParser(HTMLParser.HTMLParser):
        def __init__(self):
            HTMLParser.HTMLParser.__init__(self)
            self.in_data_row = False
            self.in_data_title = False
            self.saw_ISBN = False

            self.all_ISBNs = set()

        def handle_starttag(self, tag, attrs):
            if tag == 'div':
                for (attr_name, attr_value) in attrs:
                    if self.in_data_row:
                        if attr_name == 'class' and attr_value == 'dataTitle':
                            self.in_data_title = True
                            break
                    elif attr_name == 'class' and attr_value == 'dataRow':
                        self.in_data_row = True
                        break

        def handle_endtag(self, tag):
            if tag == 'div':
                if self.in_data_title:
                    self.in_data_title = False
                elif self.in_data_row:
                    self.in_data_row = False
                    self.saw_ISBN = False

        def handle_data(self, data):
            if self.saw_ISBN:
                data = data.strip()
                if data:
                    self.all_ISBNs.add(data.strip('()').split(' ')[-1])
            elif self.in_data_title and 'ISBN' in data:
                self.saw_ISBN = True
