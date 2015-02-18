"""
This file is part of the everest project.
See LICENSE.txt for licensing, CONTRIBUTORS.txt for contributor information.

Created on Nov 27, 2013.
"""
from everest_nosql.aggregate import NoSqlAggregate

import pytest

from everest.querying.specifications import desc
from everest.querying.specifications import eq
from everest.querying.specifications import gt
from everest.tests.complete_app.interfaces import IMyEntity
from everest.tests.test_aggregates import BaseTestRootAggregate


__docformat__ = 'reStructuredText en'
__all__ = ['TestNosSqlRootAggregate',
           ]


class Fixtures(object):
    ent0 = lambda entity_tree_fac: entity_tree_fac(id=0, text='222')
    ent1 = lambda entity_tree_fac: entity_tree_fac(id=1, text='111')
    ent2 = lambda entity_tree_fac: entity_tree_fac(id=2, text='000')


@pytest.mark.usefixtures('nosql')
class TestNosSqlRootAggregate(BaseTestRootAggregate):
    config_file_name = 'everest_nosql.tests:configure.zcml'
    agg_class = NoSqlAggregate

    def test_nested_attribute(self, class_entity_repo, ent0, ent1, ent2):
        agg = class_entity_repo.get_aggregate(IMyEntity)
        agg.add(ent0)
        agg.add(ent1)
        agg.add(ent2)
        assert len(list(agg.iterator())) == 3
        agg.filter = eq(**{'parent.text_ent':'222'})
        assert len(list(agg.iterator())) == 1
        agg.filter = None
        assert len(list(agg.iterator())) == 3
        # TODO: Nested attribute ordering does not work with NoSQL.
        agg.order = desc('id')
        assert next(agg.iterator()) is ent2
        # With nested filter and order.
        agg.filter = gt(**{'parent.text_ent':'000'})
        assert next(agg.iterator()) is ent1
        # With nested filter, order, and slice.
        agg.slice = slice(1, 2)
        assert next(agg.iterator()) is ent0

