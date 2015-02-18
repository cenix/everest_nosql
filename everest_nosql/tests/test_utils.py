"""
This file is part of the everest project.
See LICENSE.txt for licensing, CONTRIBUTORS.txt for contributor information.

Created on Nov 27, 2013.
"""
from everest_nosql.utils import MongoClassRegistry
from everest_nosql.utils import MongoInstrumentedAttribute
from everest_nosql.utils import NoSqlAttributeInspector

import pytest

from everest.constants import RESOURCE_ATTRIBUTE_KINDS
from everest.tests.complete_app.entities import MyEntity
from everest.tests.complete_app.entities import MyEntityChild
from everest.tests.complete_app.entities import MyEntityGrandchild


__docformat__ = 'reStructuredText en'
__all__ = ['TestNoSqlRepositoryUtils',
           ]


@pytest.mark.usefixtures('nosql')
class TestNoSqlRepositoryUtils(object):
    package_name = 'everest.tests.complete_app'
    config_file_name = 'everest_nosql.tests:configure.zcml'

    def test_nosql_attribute_inspector(self):
        infos = NoSqlAttributeInspector.inspect(MyEntity,
                                                'children.children.id')
        assert len(infos) == 3
        assert infos[0][0] == RESOURCE_ATTRIBUTE_KINDS.COLLECTION
        assert infos[0][1] == MyEntityChild
        assert infos[0][2] == 'children'
        assert infos[1][0] == RESOURCE_ATTRIBUTE_KINDS.COLLECTION
        assert infos[1][1] == MyEntityGrandchild
        assert infos[1][2] == 'children'
        assert infos[2][0] == RESOURCE_ATTRIBUTE_KINDS.TERMINAL
        assert infos[2][1] == int
        assert infos[2][2] == 'id'

    def test_nosql_attribute_inspector_embedded_attribute(self):
        infos = NoSqlAttributeInspector.inspect(MyEntity,
                                                'children.id.foo')
        assert len(infos) == 2
        assert infos[1][0] == RESOURCE_ATTRIBUTE_KINDS.TERMINAL
        assert infos[1][1] == None
        assert infos[1][2] == 'id.foo'

    def test_register_unregister(self):
        class Foo(object):
            pass
        assert isinstance(MyEntity.parent, MongoInstrumentedAttribute)
        with pytest.raises(ValueError):
            MongoClassRegistry.unregister(Foo)
        assert MongoClassRegistry.is_registered(MyEntity)
        # Registering a registered class raises a ValueError.
        with pytest.raises(ValueError):
            MongoClassRegistry.register(MyEntity, None)
        MongoClassRegistry.unregister(MyEntity)
        assert not MongoClassRegistry.is_registered(MyEntity)
