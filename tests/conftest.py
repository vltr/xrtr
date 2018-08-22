import pytest


class Endpoint:
    def __init__(self, x):
        self.x = x

    def __repr__(self):
        return "<Endpoint {}>".format(self.x)

    __str__ = __repr__


class Middleware:
    def __init__(self, x):
        self.x = x

    def __repr__(self):
        return "<Middleware {}>".format(self.x)

    __str__ = __repr__


@pytest.fixture
def endpoint_factory():
    return Endpoint


@pytest.fixture
def middleware_factory():
    return Middleware
