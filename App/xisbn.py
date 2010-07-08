class Xisbn:
    def __init__(self, source):
        self.xisbn_source = source

    def get_editions(self, isbn):
        editions = self.xisbn_source.get_editions(isbn)
        if len(isbn) == 13:
            isbn10 = self.xisbn_source.to10(isbn)
            editions += self.xisbn_source.get_editions(isbn10)
        elif len(isbn) == 10:
            isbn13 = self.xisbn_source.to13(isbn)
            editions += self.xisbn_source.get_editions(isbn13)
        return editions
