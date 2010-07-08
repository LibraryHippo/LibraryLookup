class MyResponse:
    def __init__(self, content, status_code=200, headers={}, final_url='http://www.google.ca/'):
        self.content = content
        self.content_was_truncated = False
        self.status_code=200
        self.headers=headers
        self.final_url=final_url

class MyOpener:
    def __init__(self, *responses):
        self.responses = []
        for response in responses:
            if not isinstance(response, MyResponse):
                response = MyResponse(response)
            self.responses.append(response)

    def __call__(self, url):
        self.last_request = { 'url':url }
        response = self.responses.pop(0)
        return response

