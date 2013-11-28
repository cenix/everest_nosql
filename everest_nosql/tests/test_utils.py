"""
This file is part of the everest project.
See LICENSE.txt for licensing, CONTRIBUTORS.txt for contributor information.

Created on Nov 27, 2013.
"""
from everest.constants import RESOURCE_ATTRIBUTE_KINDS
from everest.testing import ResourceTestCase
from everest.tests.complete_app.entities import MyEntity
from everest.tests.complete_app.entities import MyEntityChild
from everest.tests.complete_app.entities import MyEntityGrandchild
from everest_nosql.utils import MongoClassRegistry
from everest_nosql.utils import MongoInstrumentedAttribute
from everest_nosql.utils import NoSqlAttributeInspector
from everest_nosql.testing import NoSqlTestCaseMixin

__docformat__ = 'reStructuredText en'
__all__ = ['NoSqlRepositoryUtilsTestCase',
           ]


class NoSqlRepositoryUtilsTestCase(NoSqlTestCaseMixin, ResourceTestCase):
    package_name = 'everest.tests.complete_app'
    config_file_name = 'everest_nosql.tests:configure.zcml'

    def test_nosql_attribute_inspector(self):
        infos = NoSqlAttributeInspector.inspect(MyEntity,
                                                'children.children.id')
        self.assert_equal(len(infos), 3)
        self.assert_equal(infos[0][0],
                          RESOURCE_ATTRIBUTE_KINDS.COLLECTION)
        self.assert_equal(infos[0][1], MyEntityChild)
        self.assert_equal(infos[0][2], 'children')
        self.assert_equal(infos[1][0],
                          RESOURCE_ATTRIBUTE_KINDS.COLLECTION)
        self.assert_equal(infos[1][1], MyEntityGrandchild)
        self.assert_equal(infos[1][2], 'children')
        self.assert_equal(infos[2][0],
                          RESOURCE_ATTRIBUTE_KINDS.TERMINAL)
        self.assert_equal(infos[2][1], int)
        self.assert_equal(infos[2][2], 'id')

    def test_nosql_attribute_inspector_embedded_attribute(self):
        infos = NoSqlAttributeInspector.inspect(MyEntity,
                                                'children.id.foo')
        self.assert_equal(len(infos), 2)
        self.assert_equal(infos[1][0], RESOURCE_ATTRIBUTE_KINDS.TERMINAL)
        self.assert_equal(infos[1][1], None)
        self.assert_equal(infos[1][2], 'id.foo')

    def test_register_unregister(self):
        class Foo(object):
            pass
        self.assert_true(isinstance(MyEntity.parent,
                                    MongoInstrumentedAttribute))
        self.assert_raises(ValueError, MongoClassRegistry.unregister, Foo)
        self.assert_true(MongoClassRegistry.is_registered(MyEntity))
        # Registering a registered class raises a ValueError.
        self.assert_raises(ValueError, MongoClassRegistry.register,
                           MyEntity, None)
        MongoClassRegistry.unregister(MyEntity)
        self.assert_false(MongoClassRegistry.is_registered(MyEntity))
