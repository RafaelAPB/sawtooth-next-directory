# Copyright 2019 Contributors to Hyperledger Sawtooth
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------
"""Test Role Owner Addresser"""

import pytest

from rbac.common import addresser
from rbac.common.logs import get_default_logger
from tests.rbac.common.assertions import TestAssertions

LOGGER = get_default_logger(__name__)


@pytest.mark.addressing
@pytest.mark.library
class TestRoleOwnerAddresser(TestAssertions):
    """Test Role Owner Addresser"""

    def test_address(self):
        """Tests address makes an address that identifies as the correct AddressSpace"""
        role_id = addresser.role.owner.unique_id()
        next_id = addresser.user.unique_id()
        rel_address = addresser.role.owner.address(
            object_id=role_id, related_id=next_id
        )
        self.assertIsAddress(rel_address)
        self.assertEqual(
            addresser.get_address_type(rel_address), addresser.AddressSpace.ROLES_OWNERS
        )

    def test_address_deterministic(self):
        """Tests address makes an address that identifies as the correct AddressSpace"""
        role_id = addresser.role.owner.unique_id()
        next_id = addresser.user.unique_id()
        rel_address1 = addresser.role.owner.address(
            object_id=role_id, related_id=next_id
        )
        rel_address2 = addresser.role.owner.address(
            object_id=role_id, related_id=next_id
        )
        self.assertIsAddress(rel_address1)
        self.assertIsAddress(rel_address2)
        self.assertEqual(rel_address1, rel_address2)
        self.assertEqual(
            addresser.get_address_type(rel_address1),
            addresser.AddressSpace.ROLES_OWNERS,
        )

    def test_address_random(self):
        """Tests address makes a unique address given different inputs"""
        role_id1 = addresser.role.owner.unique_id()
        user_id1 = addresser.user.unique_id()
        role_id2 = addresser.role.owner.unique_id()
        user_id2 = addresser.user.unique_id()
        rel_address1 = addresser.role.owner.address(
            object_id=role_id1, related_id=user_id1
        )
        rel_address2 = addresser.role.owner.address(
            object_id=role_id2, related_id=user_id2
        )
        self.assertIsAddress(rel_address1)
        self.assertIsAddress(rel_address2)
        self.assertNotEqual(rel_address1, rel_address2)
        self.assertEqual(
            addresser.get_address_type(rel_address1),
            addresser.AddressSpace.ROLES_OWNERS,
        )
        self.assertEqual(
            addresser.get_address_type(rel_address2),
            addresser.AddressSpace.ROLES_OWNERS,
        )

    def test_addresser_parse(self):
        """Test addresser.parse returns a parsed address"""
        role_id = addresser.role.unique_id()
        next_id = addresser.user.unique_id()
        rel_address = addresser.role.owner.address(role_id, next_id)

        parsed = addresser.parse(rel_address)

        self.assertEqual(parsed.object_type, addresser.ObjectType.ROLE)
        self.assertEqual(parsed.related_type, addresser.ObjectType.USER)
        self.assertEqual(parsed.relationship_type, addresser.RelationshipType.OWNER)
        self.assertEqual(parsed.address_type, addresser.AddressSpace.ROLES_OWNERS)
        self.assertEqual(parsed.object_id, role_id)
        self.assertEqual(parsed.related_id, next_id)
