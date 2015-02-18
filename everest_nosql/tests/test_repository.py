"""
This file is part of the everest project.
See LICENSE.txt for licensing, CONTRIBUTORS.txt for contributor information.

Created on Nov 27, 2013.
"""
from iso8601 import iso8601
import pytest
import transaction

from everest.repositories.constants import REPOSITORY_TYPES
from everest.repositories.interfaces import IRepository
from everest.resources.utils import get_root_collection
from everest.tests.complete_app.entities import MyEntity
from everest.tests.complete_app.entities import MyEntityChild
from everest.tests.complete_app.entities import MyEntityGrandchild
from everest.tests.complete_app.entities import MyEntityParent
from everest.tests.complete_app.interfaces import IMyEntity
from everest.tests.test_repositories import BaseTestRepository
from everest.utils import get_repository_manager


__docformat__ = 'reStructuredText en'
__all__ = ['TestNoSqlRepository',
           ]


@pytest.fixture
def collection():
    # FIXME: This uses a lot of the machinery we are trying to test
    #        here. We should have some sort of pre-loading facility
    #        like the cache loader for the entity repo.
    ent = MyEntity(id=0, number=1, text_ent='TEST',
                   date_time=
                   iso8601.parse_date('2012-06-13 11:06:47+02:00'))
    parent = MyEntityParent(id=0, text_ent='TEXT')
    ent.parent = parent
    child = MyEntityChild(id=0, text_ent='TEXT')
    ent.children.append(child)
    grandchild = MyEntityGrandchild(id=0, text='TEXT')
    child.children.append(grandchild)
    coll = get_root_collection(IMyEntity)
    coll.create_member(ent)
    transaction.commit()
    return coll


@pytest.mark.usefixtures('nosql')
class TestNoSqlRepository(BaseTestRepository):
    package_name = 'everest.tests.complete_app'
    config_file_name = 'everest_nosql.tests:configure.zcml'

    def test_init(self, config):
        repo_mgr = get_repository_manager()
        repo = repo_mgr.get(REPOSITORY_TYPES.NO_SQL)
        self.assert_true(IRepository.providedBy(repo)) # pylint: disable=E1101
        # Test initialization through config.
        tmp_name = 'TMP'
        config.add_nosql_repository(tmp_name)
        repo = repo_mgr.get(tmp_name)
        assert IRepository.providedBy(repo) # pylint: disable=E1101

    def test_commit(self, collection): # pylint:disable=W0221,W0621
        mb = next(iter(collection))
        TEXT = 'Changed.'
        mb.text = TEXT
        transaction.commit()
        assert next(iter(collection)).text == TEXT

    def test_load_referenced_entities(self):
        coll = get_root_collection(IMyEntity)
        ent = next(iter(coll)).get_entity()
        parent = ent.parent
        assert isinstance(parent, MyEntityParent)
        assert len(ent.children) == 1
        assert isinstance(ent.children[0], MyEntityChild)
        assert len(ent.children[0].children) == 1
        assert isinstance(ent.children[0].children[0], MyEntityGrandchild)
