from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.db import models
from django.test import SimpleTestCase

from model_utils.managers import (
    InheritanceManager,
    QueryManager,
    SoftDeletableManager,
)

if not TYPE_CHECKING:
    from model_utils.managers import JoinManager


class ManagerClassAssignmentTests(SimpleTestCase):
    """
    Tests for manager __class__ assignment compatibility.

    This is a regression test for GitHub issue #636 where manager mixins
    inheriting from Generic[T] at runtime were incompatible with
    django-modeltranslation due to Python's __class__ assignment restrictions.

    The fix moves Generic[T] inheritance behind TYPE_CHECKING so it's only
    used for static type checking, not at runtime.

    See: https://github.com/jazzband/django-model-utils/issues/636
    """

    def test_softdeletable_manager_class_can_be_reassigned(self) -> None:
        """SoftDeletableManager instances support __class__ reassignment."""
        manager: Any = SoftDeletableManager()

        class PatchedManager(SoftDeletableManager):
            pass

        manager.__class__ = PatchedManager
        self.assertIsInstance(manager, PatchedManager)

    def test_inheritance_manager_class_can_be_reassigned(self) -> None:
        """InheritanceManager instances support __class__ reassignment."""
        manager: Any = InheritanceManager()

        class PatchedManager(InheritanceManager):
            pass

        manager.__class__ = PatchedManager
        self.assertIsInstance(manager, PatchedManager)

    def test_query_manager_class_can_be_reassigned(self) -> None:
        """QueryManager instances support __class__ reassignment."""
        manager: Any = QueryManager(is_active=True)

        class PatchedManager(models.Manager):
            pass

        manager.__class__ = PatchedManager
        self.assertIsInstance(manager, PatchedManager)

    def test_join_manager_class_can_be_reassigned(self) -> None:
        """JoinManager instances support __class__ reassignment."""
        manager: Any = JoinManager()  # type: ignore[name-defined]

        class PatchedManager(models.Manager):
            pass

        manager.__class__ = PatchedManager
        self.assertIsInstance(manager, PatchedManager)
