"""
This file is part of the everest project.
See LICENSE.txt for licensing, CONTRIBUTORS.txt for contributor information.

Package initialization file.

Created on Nov 3, 2011.
"""
from everest.querying.base import EXPRESSION_KINDS
from everest.querying.interfaces import IFilterSpecificationVisitor
from everest.querying.interfaces import IOrderSpecificationVisitor
from everest.repositories.constants import REPOSITORY_TYPES
from everest_nosql.querying import NoSqlOrderSpecificationVisitor
from everest_nosql.querying import NoSqlFilterSpecificationVisitor


def includeme(config):
    """
    Registers the No SQL backend for everest.
    """
    # Register filter and order specification visitors.
    flt_vst = config.query_registered_utilities(IFilterSpecificationVisitor,
                                                name=EXPRESSION_KINDS.NOSQL)
    if flt_vst is None:
        config.registry.registerUtility(NoSqlFilterSpecificationVisitor,
                                        IFilterSpecificationVisitor,
                                        name=EXPRESSION_KINDS.NOSQL)

    ord_vst = config.query_registered_utilities(IOrderSpecificationVisitor,
                                                name=EXPRESSION_KINDS.NOSQL)
    if ord_vst is None:
        config.registry.registerUtility(NoSqlOrderSpecificationVisitor,
                                        IOrderSpecificationVisitor,
                                        name=EXPRESSION_KINDS.NOSQL)
    # Set up configuration directive to add a No SQL repository.
    config.add_directive('add_nosql_repository', add_nosql_repository,
                         action_wrap=False)
    #
    REPOSITORY_TYPES.NO_SQL = 'NO_SQL'


def add_nosql_repository(self, name=None, repository_class=None,
                         aggregate_class=None,
                         make_default=False, configuration=None,
                         _info=u''):
    # Update configuration from settings.
    if configuration is None:
        configuration = {}
    setting_info = [('db_host', 'db_host'),
                    ('db_port', 'db_port')]
    configuration.update(
                    self.get_configuration_from_settings(setting_info))
    self.add_repository(name, REPOSITORY_TYPES.NO_SQL,
                        repository_class, aggregate_class,
                        make_default, configuration)
