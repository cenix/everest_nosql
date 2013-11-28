"""
This file is part of the everest project.
See LICENSE.txt for licensing, CONTRIBUTORS.txt for contributor information.

Created on Nov 27, 2013.
"""
from everest.repositories.constants import REPOSITORY_TYPES
from everest.repositories.interfaces import IRepository
from everest.resources.utils import get_root_collection
from everest.tests.complete_app.entities import MyEntity
from everest.tests.complete_app.entities import MyEntityChild
from everest.tests.complete_app.entities import MyEntityGrandchild
from everest.tests.complete_app.entities import MyEntityParent
from everest.tests.complete_app.interfaces import IMyEntity
from everest.tests.test_repositories import RepositoryTestCaseBase
from everest.utils import get_repository_manager
from everest_nosql.testing import NoSqlTestCaseMixin
from iso8601 import iso8601
import transaction

__docformat__ = 'reStructuredText en'
__all__ = ['NoSqlRepositoryTestCase',
           ]


class NoSqlRepositoryTestCase(NoSqlTestCaseMixin,
                              RepositoryTestCaseBase):
    package_name = 'everest.tests.complete_app'
    config_file_name = 'everest_nosql.tests:configure.zcml'

    def set_up(self):
        RepositoryTestCaseBase.set_up(self)
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

    def tear_down(self):
        transaction.abort()

    def test_init(self):
        repo_mgr = get_repository_manager()
        repo = repo_mgr.get(REPOSITORY_TYPES.NO_SQL)
        self.assert_true(IRepository.providedBy(repo)) # pylint: disable=E1101
        # Test initialization through config.
        tmp_name = 'TMP'
        self.config.add_nosql_repository(tmp_name)
        repo = repo_mgr.get(tmp_name)
        self.assert_true(IRepository.providedBy(repo)) # pylint: disable=E1101

    def test_commit(self):
        coll = get_root_collection(IMyEntity)
        mb = next(iter(coll))
        TEXT = 'Changed.'
        mb.text = TEXT
        transaction.commit()
        self.assert_equal(next(iter(coll)).text, TEXT)

    def test_load_referenced_entities(self):
        coll = get_root_collection(IMyEntity)
        ent = next(iter(coll)).get_entity()
        parent = ent.parent
        self.assert_true(isinstance(parent, MyEntityParent))
        self.assert_equal(len(ent.children), 1)
        self.assert_true(isinstance(ent.children[0], MyEntityChild))
        self.assert_true(len(ent.children[0].children), 1)
        self.assert_true(isinstance(ent.children[0].children[0],
                         MyEntityGrandchild))
