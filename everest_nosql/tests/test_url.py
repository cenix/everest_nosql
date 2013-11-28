"""
This file is part of the everest project.
See LICENSE.txt for licensing, CONTRIBUTORS.txt for contributor information.

Created on Nov 27, 2013.
"""
from everest.tests.test_url import UrlTestCaseBase
from everest_nosql.testing import NoSqlTestCaseMixin

__docformat__ = 'reStructuredText en'
__all__ = ['RepoUrlTestCaseNoSql',
           ]

class RepoUrlTestCaseNoSql(NoSqlTestCaseMixin, UrlTestCaseBase):
    config_file_name = 'everest_nosql.tests:configure.zcml'
