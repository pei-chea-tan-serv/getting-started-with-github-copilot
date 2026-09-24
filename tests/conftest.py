import copy

import pytest

from src.app import activities


@pytest.fixture(autouse=True)
def reset_activities():
    # Ensures per-test mutations to the in-memory store don't leak across tests.
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(original))
