"""
This file is part of the everest project.
See LICENSE.txt for licensing, CONTRIBUTORS.txt for contributor information.

Created on Nov 27, 2013.
"""
import pytest

from everest.tests.test_url import BaseTestUrl


__docformat__ = 'reStructuredText en'
__all__ = ['TestUrlNoSql',
           ]


@pytest.mark.usefixtures('nosql')
class TestUrlNoSql(BaseTestUrl):
    config_file_name = 'everest_nosql.tests:configure.zcml'
