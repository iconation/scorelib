from iconsdk.builder.transaction_builder import DeployTransactionBuilder
from tbears.libs.icon_integrate_test import IconIntegrateTestBase, SCORE_INSTALL_ADDRESS
from iconsdk.libs.in_memory_zip import gen_deploy_data_content
from iconsdk.signed_transaction import SignedTransaction
from .utils import *

import json
import os

DIR_PATH = os.path.abspath(os.path.dirname(__file__))

class ScoreLibTests(IconIntegrateTestBase):

    SCORE_PATH = os.path.abspath(os.path.join(DIR_PATH, '../'))

    def setUp(self):
        super().setUp()

        self.icon_service = None

        # install SCORE
        self._operator = self._test1
        self._user = self._wallet_array[0]
        self._attacker = self._wallet_array[9]

        for wallet in self._wallet_array:
            icx_transfer_call(super(), self._test1, wallet.get_address(), 100 * 10**18, self.icon_service)

        self._operator_icx_balance = get_icx_balance(super(), address=self._operator.get_address(), icon_service=self.icon_service)
        self._score_address = self._deploy_score(self.SCORE_PATH, params={})['scoreAddress']

    def _deploy_score(self, project, to: str = SCORE_INSTALL_ADDRESS, params={}) -> dict:
        # Generates an instance of transaction for deploying SCORE.
        transaction = DeployTransactionBuilder() \
            .from_(self._test1.get_address()) \
            .to(to) \
            .step_limit(100_000_000_000) \
            .nid(3) \
            .nonce(100) \
            .content_type("application/zip") \
            .content(gen_deploy_data_content(project)) \
            .params(params) \
            .build()

        # Returns the signed transaction object having a signature
        signed_transaction = SignedTransaction(transaction, self._test1)

        # process the transaction in local
        result = self.process_transaction(signed_transaction, self.icon_service)

        self.assertTrue('status' in result)

        if result['status'] != 1:
            print(result)

        self.assertEqual(1, result['status'])
        self.assertTrue('scoreAddress' in result)

        return result

    def _deploy_irc2(self, project, to: str = SCORE_INSTALL_ADDRESS) -> dict:
        # Generates an instance of transaction for deploying SCORE.
        transaction = DeployTransactionBuilder() \
            .params({
                "_initialSupply": 0x100000000000,
                "_decimals": 18,
                "_name": 'StandardToken',
                "_symbol": 'ST',
            }) \
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
        result = self.process_transaction(
            signed_transaction, self.icon_service)

        self.assertTrue('status' in result)
        self.assertEqual(1, result['status'])
        self.assertTrue('scoreAddress' in result)

        return result

    def shard_set(self, key: str, value: int, success=True):
        return transaction_call(
            super(),
            from_=self._operator,
            to_=self._score_address,
            method='shard_set',
            params={'key': key, 'value': value},
            icon_service=self.icon_service,
            success=success
        )

    def shard_get(self, key: str, success=True):
        return transaction_call(
            super(),
            from_=self._operator,
            to_=self._score_address,
            method='shard_get',
            params={'key': key},
            icon_service=self.icon_service,
            success=success
        )

    def shard_multiset(self, count: int, success=True):
        return transaction_call(
            super(),
            from_=self._operator,
            to_=self._score_address,
            method='shard_multiset',
            params={'count': count},
            icon_service=self.icon_service,
            success=success
        )
