class MyResponse:
    def __init__(self, content, status_code=200, headers={}, final_url='http://www.google.ca/'):
        self.content = content
        self.content_was_truncated = False
        self.status_code = 200
        self.headers = headers
        self.final_url = final_url


class MyOpener:
    def __init__(self, *responses):
        self.responses = []
        for response in responses:
            if not isinstance(response, MyResponse):
                response = MyResponse(response)
            self.responses.append(response)

    def __call__(self, url):
        self.last_request = {'url': url}
        response = self.responses.pop(0)
        return response


class MyXisbnWebService:
    def __init__(self):
        self.edition_map = {}

    def __setitem__(self, isbn, editions):
        saved_editions = [isbn] + editions
        self.edition_map[isbn] = saved_editions

    def get_editions(self, isbn):
        if isbn in self.edition_map:
            return self.edition_map[isbn]
        return [isbn]

    def to13(self, isbn10):
        return isbn10 + '147'

    def to10(self, isbn13):
        return isbn13[3:]


class MyCache:
    def __init__(self):
        self.cache = {}

    def get(self, key):
        return self.cache.get(key, None)

    def set(self, key, value, *args):
        self.cache[key] = value
