"""
Testing utilities for the noSQL backend.

This file is part of the everest project.
See LICENSE.txt for licensing, CONTRIBUTORS.txt for contributor information.

Created on Nov 26, 2013.
"""
from everest_nosql.utils import MongoClassRegistry

import pytest


__docformat__ = 'reStructuredText en'
__all__ = []


@pytest.fixture(scope='class')
def nosql(request):
    """
    Fixture for all tests that use the NoSQL backend.
    """
    def tear_down():
        MongoClassRegistry.unregister_all()
    request.addfinalizer(tear_down)
