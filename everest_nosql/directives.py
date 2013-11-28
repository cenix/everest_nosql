"""
Directives for the No SQL backend.

This file is part of the everest project.
See LICENSE.txt for licensing, CONTRIBUTORS.txt for contributor information.

Created on Nov 27, 2013.
"""
from everest.configuration import Configurator
from everest.directives import IRepositoryDirective
from everest.repositories.constants import REPOSITORY_TYPES
from pyramid.threadlocal import get_current_registry
from zope.schema import Int # pylint: disable=E0611,F0401
from zope.schema import TextLine # pylint: disable=E0611,F0401

__docformat__ = 'reStructuredText en'
__all__ = ['INoSqlRepositoryDirective',
           'nosql_repository',
           ]

# interfaces to not have an __init__ # pylint: disable=W0232
class INoSqlRepositoryDirective(IRepositoryDirective):
    db_host = \
        TextLine(title=u"Host name for the MongoDB server.",
                 required=False)
    db_port = \
        Int(title=u"Port for the MongoDB server.",
            required=False)
    db_name = \
        TextLine(title=u"Database name for the MongoDB server.",
                 required=False)
# pylint: enable=W0232


def nosql_repository(_context, name=None, make_default=False,
                     aggregate_class=None, repository_class=None,
                     db_host='localhost', db_port=27017, db_name='test'):
    repo_type = REPOSITORY_TYPES.NO_SQL
    # Apply eagerly so custom configuration can assume the repo is there.
    discriminator = (repo_type, name)
    _context.action(discriminator=discriminator)
    reg = get_current_registry()
    cnf = dict(db_host=db_host, db_port=db_port, db_name=db_name)
    config = Configurator(reg, package=_context.package)
    config.add_repository(name, repo_type, repository_class,
                          aggregate_class, make_default, cnf)
