import pytest


def _fn(r, n):
    raise pytest.skip.Exception("XXX_filename fixtures are unknown")


@pytest.fixture(scope="function")
def canonical_filename(request):
    return _fn(request, "canonical")


@pytest.fixture(scope="function")
def data_filename(request):
    return _fn(request, "data")


@pytest.fixture(scope="function")
def detect_filename(request):
    return _fn(request, "detect")


@pytest.fixture(scope="function")
def events_filename(request):
    return _fn(request, "events")
