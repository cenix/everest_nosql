"""
This file is part of the everest project.
See LICENSE.txt for licensing, CONTRIBUTORS.txt for contributor information.

Created on Nov 27, 2013.
"""
from everest.querying.specifications import desc
from everest.querying.specifications import eq
from everest.querying.specifications import gt
from everest.tests.complete_app.testing import create_entity
from everest.tests.test_aggregates import RootAggregateTestCaseBase
from everest_nosql.aggregate import NoSqlAggregate
from everest_nosql.testing import NoSqlTestCaseMixin

__docformat__ = 'reStructuredText en'
__all__ = ['NosSqlRootAggregateTestCase',
           ]


class NosSqlRootAggregateTestCase(NoSqlTestCaseMixin,
                                  RootAggregateTestCaseBase):
    config_file_name = 'everest_nosql.tests:configure.zcml'
    agg_class = NoSqlAggregate

    def test_nested_attribute(self):
        agg = self._aggregate
        ent0 = create_entity(entity_id=0)
        ent0.parent.text_ent = '222'
        ent1 = create_entity(entity_id=1)
        ent1.parent.text_ent = '111'
        ent2 = create_entity(entity_id=2)
        ent2.parent.text_ent = '000'
        agg.add(ent0)
        agg.add(ent1)
        agg.add(ent2)
        self.assert_equal(len(list(agg.iterator())), 3)
        agg.filter = eq(**{'parent.text_ent':'222'})
        self.assert_equal(len(list(agg.iterator())), 1)
        agg.filter = None
        self.assert_equal(len(list(agg.iterator())), 3)
        # TODO: Nested attribute ordering does not work with NoSQL.
        agg.order = desc('id')
        self.assert_true(next(agg.iterator()) is ent2)
        # With nested filter and order.
        agg.filter = gt(**{'parent.text_ent':'000'})
        self.assert_true(next(agg.iterator()) is ent1)
        # With nested filter, order, and slice.
        agg.slice = slice(1, 2)
        self.assert_true(next(agg.iterator()) is ent0)

