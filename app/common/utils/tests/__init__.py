from django.test import RequestFactory


class RequestFactoryMixin():

    def generate_request(self):
        factory = RequestFactory()
        request = factory.get("/")
        return request
