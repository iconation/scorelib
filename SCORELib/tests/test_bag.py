# -*- coding: utf-8 -*-

# Copyright 2020 ICONation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import json

from iconsdk.builder.transaction_builder import DeployTransactionBuilder
from iconsdk.builder.call_builder import CallBuilder
from iconsdk.icon_service import IconService
from iconsdk.libs.in_memory_zip import gen_deploy_data_content
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.signed_transaction import SignedTransaction

from tbears.libs.icon_integrate_test import IconIntegrateTestBase, SCORE_INSTALL_ADDRESS
from .utils import *

DIR_PATH = os.path.abspath(os.path.dirname(__file__))


class Test(IconIntegrateTestBase):
    TEST_HTTP_ENDPOINT_URI_V3 = "http://127.0.0.1:9000/api/v3"
    SCORE_PROJECT = os.path.abspath(os.path.join(DIR_PATH, '..'))

    def setUp(self):
        super().setUp()

        self.icon_service = None
        # if you want to send request to network, uncomment next line and set self.TEST_HTTP_ENDPOINT_URI_V3
        # self.icon_service = IconService(HTTPProvider(self.TEST_HTTP_ENDPOINT_URI_V3))

        # install SCORE
        self._operator = self._test1
        self._score_address = self._deploy_score(self.SCORE_PROJECT)['scoreAddress']
        self._user = self._wallet_array[0]
        self._attacker = self._wallet_array[1]

        for wallet in self._wallet_array:
            icx_transfer_call(super(), self._test1, wallet.get_address(), 100 * 10**18, self.icon_service)

        self._operator_icx_balance = get_icx_balance(super(), address=self._operator.get_address(), icon_service=self.icon_service)
        self._user_icx_balance = get_icx_balance(super(), address=self._user.get_address(), icon_service=self.icon_service)

    def _deploy_score(self, project, to: str = SCORE_INSTALL_ADDRESS) -> dict:
        # Generates an instance of transaction for deploying SCORE.
        transaction = DeployTransactionBuilder() \
            .from_(self._operator.get_address()) \
            .to(to) \
            .step_limit(100_000_000_000) \
            .nid(3) \
            .nonce(100) \
            .content_type("application/zip") \
            .content(gen_deploy_data_content(project)) \
            .build()

        # Returns the signed transaction object having a signature
        signed_transaction = SignedTransaction(transaction, self._operator)

        # process the transaction in local
        result = self.process_transaction(signed_transaction, self.icon_service)

        self.assertTrue('status' in result)
        self.assertEqual(1, result['status'])
        self.assertTrue('scoreAddress' in result)

        return result

    # ===============================================================
    def test_length(self):
        length = icx_call(
            super(),
            from_=self._operator.get_address(),
            to_=self._score_address,
            method='bagdb_length',
            icon_service=self.icon_service
        )
        self.assertTrue(int(length, 16) == 0)

        result = transaction_call_success(
            super(),
            from_=self._operator,
            to_=self._score_address,
            method='bagdb_add',
            params={'item': 1},
            icon_service=self.icon_service
        )
        length = icx_call(
            super(),
            from_=self._operator.get_address(),
            to_=self._score_address,
            method='bagdb_length',
            icon_service=self.icon_service
        )
        self.assertTrue(int(length, 16) == 1)

    def test_add_1(self):
        result = transaction_call_success(
            super(),
            from_=self._operator,
            to_=self._score_address,
            method='bagdb_add',
            params={'item': 1},
            icon_service=self.icon_service
        )
        length = icx_call(
            super(),
            from_=self._operator.get_address(),
            to_=self._score_address,
            method='bagdb_length',
            icon_service=self.icon_service
        )
        self.assertTrue(int(length, 16) == 1)

    def test_add_2(self):
        result = transaction_call_success(
            super(),
            from_=self._operator,
            to_=self._score_address,
            method='bagdb_add',
            params={'item': 1},
            icon_service=self.icon_service
        )
        result = transaction_call_success(
            super(),
            from_=self._operator,
            to_=self._score_address,
            method='bagdb_add',
            params={'item': 1},
            icon_service=self.icon_service
        )
        length = icx_call(
            super(),
            from_=self._operator.get_address(),
            to_=self._score_address,
            method='bagdb_length',
            icon_service=self.icon_service
        )
        self.assertTrue(int(length, 16) == 2)

    def test_add_3(self):
        result = transaction_call_success(
            super(),
            from_=self._operator,
            to_=self._score_address,
            method='bagdb_add',
            params={'item': 1},
            icon_service=self.icon_service
        )
        result = transaction_call_success(
            super(),
            from_=self._operator,
            to_=self._score_address,
            method='bagdb_add',
            params={'item': 1},
            icon_service=self.icon_service
        )
        result = transaction_call_success(
            super(),
            from_=self._operator,
            to_=self._score_address,
            method='bagdb_add',
            params={'item': 2},
            icon_service=self.icon_service
        )
        length = icx_call(
            super(),
            from_=self._operator.get_address(),
            to_=self._score_address,
            method='bagdb_length',
            icon_service=self.icon_service
        )
        self.assertTrue(int(length, 16) == 3)

    def test_count_1(self):
        result = transaction_call_success(
            super(),
            from_=self._operator,
            to_=self._score_address,
            method='bagdb_add',
            params={'item': 1},
            icon_service=self.icon_service
        )
        count = icx_call(
            super(),
            from_=self._operator.get_address(),
            to_=self._score_address,
            method='bagdb_count',
            params={'item': 1},
            icon_service=self.icon_service
        )
        self.assertTrue(int(count, 16) == 1)

    def test_count_2(self):
        result = transaction_call_success(
            super(),
            from_=self._operator,
            to_=self._score_address,
            method='bagdb_add',
            params={'item': 1},
            icon_service=self.icon_service
        )
        result = transaction_call_success(
            super(),
            from_=self._operator,
            to_=self._score_address,
            method='bagdb_add',
            params={'item': 1},
            icon_service=self.icon_service
        )
        count = icx_call(
            super(),
            from_=self._operator.get_address(),
            to_=self._score_address,
            method='bagdb_count',
            params={'item': 1},
            icon_service=self.icon_service
        )
        self.assertTrue(int(count, 16) == 2)

    def test_count_3(self):
        result = transaction_call_success(
            super(),
            from_=self._operator,
            to_=self._score_address,
            method='bagdb_add',
            params={'item': 1},
            icon_service=self.icon_service
        )
        result = transaction_call_success(
            super(),
            from_=self._operator,
            to_=self._score_address,
            method='bagdb_add',
            params={'item': 1},
            icon_service=self.icon_service
        )
        result = transaction_call_success(
            super(),
            from_=self._operator,
            to_=self._score_address,
            method='bagdb_add',
            params={'item': 2},
            icon_service=self.icon_service
        )
        count = icx_call(
            super(),
            from_=self._operator.get_address(),
            to_=self._score_address,
            method='bagdb_count',
            params={'item': 1},
            icon_service=self.icon_service
        )
        self.assertTrue(int(count, 16) == 2)

    def test_clear(self):
        result = transaction_call_success(
            super(),
            from_=self._operator,
            to_=self._score_address,
            method='bagdb_add',
            params={'item': 1},
            icon_service=self.icon_service
        )
        result = transaction_call_success(
            super(),
            from_=self._operator,
            to_=self._score_address,
            method='bagdb_add',
            params={'item': 1},
            icon_service=self.icon_service
        )
        result = transaction_call_success(
            super(),
            from_=self._operator,
            to_=self._score_address,
            method='bagdb_add',
            params={'item': 2},
            icon_service=self.icon_service
        )
        result = transaction_call_success(
            super(),
            from_=self._operator,
            to_=self._score_address,
            method='bagdb_clear',
            icon_service=self.icon_service
        )
        length = icx_call(
            super(),
            from_=self._operator.get_address(),
            to_=self._score_address,
            method='bagdb_length',
            icon_service=self.icon_service
        )
        self.assertTrue(int(length, 16) == 0)

    def test_remove_1(self):
        result = transaction_call_success(
            super(),
            from_=self._operator,
            to_=self._score_address,
            method='bagdb_add',
            params={'item': 1},
            icon_service=self.icon_service
        )
        result = transaction_call_success(
            super(),
            from_=self._operator,
            to_=self._score_address,
            method='bagdb_add',
            params={'item': 1},
            icon_service=self.icon_service
        )
        result = transaction_call_success(
            super(),
            from_=self._operator,
            to_=self._score_address,
            method='bagdb_remove',
            params={'item': 1},
            icon_service=self.icon_service
        )
        count = icx_call(
            super(),
            from_=self._operator.get_address(),
            to_=self._score_address,
            method='bagdb_count',
            params={'item': 1},
            icon_service=self.icon_service
        )
        self.assertTrue(int(count, 16) == 1)

    def test_remove_2(self):
        result = transaction_call_success(
            super(),
            from_=self._operator,
            to_=self._score_address,
            method='bagdb_add',
            params={'item': 1},
            icon_service=self.icon_service
        )
        result = transaction_call_success(
            super(),
            from_=self._operator,
            to_=self._score_address,
            method='bagdb_remove',
            params={'item': 1},
            icon_service=self.icon_service
        )
        count = icx_call(
            super(),
            from_=self._operator.get_address(),
            to_=self._score_address,
            method='bagdb_count',
            params={'item': 1},
            icon_service=self.icon_service
        )
        self.assertTrue(int(count, 16) == 0)

    def test_remove_3(self):
        result = transaction_call_success(
            super(),
            from_=self._operator,
            to_=self._score_address,
            method='bagdb_add',
            params={'item': 1},
            icon_service=self.icon_service
        )
        result = transaction_call_success(
            super(),
            from_=self._operator,
            to_=self._score_address,
            method='bagdb_remove',
            params={'item': 2},
            icon_service=self.icon_service
        )
        count = icx_call(
            super(),
            from_=self._operator.get_address(),
            to_=self._score_address,
            method='bagdb_count',
            params={'item': 1},
            icon_service=self.icon_service
        )
        self.assertTrue(int(count, 16) == 1)

    def test_select_1(self):
        result = transaction_call_success(
            super(),
            from_=self._operator,
            to_=self._score_address,
            method='bagdb_add',
            params={'item': 1},
            icon_service=self.icon_service
        )
        result = transaction_call_success(
            super(),
            from_=self._operator,
            to_=self._score_address,
            method='bagdb_add',
            params={'item': 2},
            icon_service=self.icon_service
        )

        bagdb = icx_call(
            super(),
            from_=self._operator.get_address(),
            to_=self._score_address,
            method='bagdb_select',
            params={'offset': 0, 'match': 1},
            icon_service=self.icon_service
        )

        self.assertTrue(len(bagdb) == 1)
