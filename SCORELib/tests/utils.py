# -*- coding: utf-8 -*-
# Copyright 2020 ICON Foundation
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

from os import path

from iconsdk.builder.call_builder import CallBuilder
from iconsdk.builder.transaction_builder import (CallTransactionBuilder,
                                                 DeployTransactionBuilder,
                                                 TransactionBuilder)
from iconsdk.exception import IconServiceBaseException
from iconsdk.icon_service import IconService
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.wallet.wallet import KeyWallet
from iconservice.base.address import GOVERNANCE_SCORE_ADDRESS, Address
from tbears.libs.icon_integrate_test import (SCORE_INSTALL_ADDRESS,
                                             IconIntegrateTestBase)


def get_icx_balance(icon_integrate_test_base: IconIntegrateTestBase,
                    address: str,
                    icon_service: IconService = None) -> str:
    """Gets ICX coin balance of address

    :param icon_integrate_test_base: IconIntegrateTestBase
    :param address: target address
    :param icon_service: IconService
    :return: ICX coin balance of target address
    """
    try:
        if icon_service is not None:
            response = icon_service.get_balance(address)
        else:
            request = {
                "address": Address.from_string(address)
            }
            response = icon_integrate_test_base._query(request=request, method="icx_getBalance")
    except IconServiceBaseException as e:
        response = e.message

    # Sends the call request
    return response


def irc2_transfer(icon_integrate_test_base: IconIntegrateTestBase,
                  from_: Address, token: str, to_: str, value: int, icon_service: IconService = None):
    return transaction_call_success(
        icon_integrate_test_base,
        from_=from_,
        to_=token,
        method="transfer",
        params={
            '_to': to_,
            '_value': value
        },
        icon_service=icon_service
    )


def get_irc2_balance(icon_integrate_test_base: IconIntegrateTestBase,
                     address: str, token: str,
                     icon_service: IconService = None) -> str:
    return icx_call(
        icon_integrate_test_base,
        from_=address,
        to_=token,
        method="balanceOf",
        params={'_owner': address},
        icon_service=icon_service
    )


def deploy_score(icon_integrate_test_base: IconIntegrateTestBase,
                 content_as_bytes: bytes,
                 from_: KeyWallet,
                 to_: str = SCORE_INSTALL_ADDRESS,
                 params: dict = None,
                 icon_service: IconService = None) -> dict:
    """Deploys the SCORE by using SDK and checks if it succeeded

    :param icon_integrate_test_base: IconIntegrateTestBase
    :param content_as_bytes:  SCORE content as bytes
    :param from_: Message sender's key-wallet instance
    :param to_: SCORE installing address or updating address
    :param params: parameters for the method `on_install` or `on_update` (optional)
    :param icon_service: IconService
    :return: transaction result as dict
    """
    # Generates an instance of transaction for deploying SCORE.
    transaction = DeployTransactionBuilder() \
        .from_(from_.get_address()) \
        .to(to_) \
        .step_limit(100_000_000_000) \
        .nid(3) \
        .nonce(100) \
        .content_type("application/zip") \
        .content(content_as_bytes) \
        .params(params) \
        .build()

    # Returns the signed transaction object having a signature
    signed_transaction = SignedTransaction(transaction, from_)

    # Processes the transaction
    tx_result = icon_integrate_test_base.process_transaction(signed_transaction, icon_service)

    assert 'status', 'scoreAddress' in tx_result
    assert 1 == tx_result['status']
    return tx_result


def icx_call(icon_integrate_test_base: IconIntegrateTestBase,
             from_: str,
             to_: str,
             method: str,
             params: dict = None,
             icon_service: IconService = None) -> any:
    """Calls SCORE's external function which is read-only by using SDK and returns the response

    :param icon_integrate_test_base: IconIntegrateTestBase
    :param from_: Message sender's address
    :param to_: SCORE address that will handle the message
    :param method: name of an external function
    :param params: parameters as dict to be passed to the function (optional)
    :param icon_service: IconService
    :return: response as dict returned by the executed SCORE function
    """
    # Generates a call instance using the CallBuilder
    call = CallBuilder().from_(from_) \
        .to(to_) \
        .method(method) \
        .params(params) \
        .build()

    # Sends the call request
    response = icon_integrate_test_base.process_call(call, icon_service)
    return response


def transaction_call_success(icon_integrate_test_base: IconIntegrateTestBase,
                             from_: KeyWallet,
                             to_: str,
                             method: str,
                             params: dict = None,
                             value: int = 0,
                             icon_service: IconService = None) -> dict:
    """Sends the call transaction by using SDK

    :param icon_integrate_test_base: IconIntegrateTestBase
    :param from_: wallet address making a transaction
    :param to_: wallet address to receive coin or SCORE address to receive a transaction
    :param method: name of an external function
    :param params: parameters as dict passed on the SCORE methods (optional)
    :param value: amount of ICX to be sent (Optional)
    :param icon_service: IconService
    :return: transaction result as dict
    """
    # Generates an instance of transaction for calling method in SCORE.
    tx_result = transaction_call_error(icon_integrate_test_base, from_, to_, method, params, value, icon_service)

    try:
        assert 'status' in tx_result
        assert 1 == tx_result['status']
    except AssertionError:
        raise AssertionError(tx_result)

    return tx_result


def transaction_call_error(icon_integrate_test_base: IconIntegrateTestBase,
                           from_: KeyWallet,
                           to_: str,
                           method: str,
                           params: dict = None,
                           value: int = 0,
                           icon_service: IconService = None) -> dict:
    """Sends the call transaction by using SDK

    :param icon_integrate_test_base: IconIntegrateTestBase
    :param from_: wallet address making a transaction
    :param to_: wallet address to receive coin or SCORE address to receive a transaction
    :param method: name of an external function
    :param params: parameters as dict passed on the SCORE methods (optional)
    :param value: amount of ICX to be sent (Optional)
    :param icon_service: IconService
    :return: transaction result as dict
    """
    # Generates an instance of transaction for calling method in SCORE.
    transaction = CallTransactionBuilder() \
        .from_(from_.get_address()) \
        .to(to_) \
        .step_limit(100_000_000_000) \
        .nid(3) \
        .nonce(100) \
        .method(method) \
        .params(params) \
        .value(value) \
        .build()

    # Returns the signed transaction object having a signature
    signed_transaction = SignedTransaction(transaction, from_)

    # Sends the transaction to the network
    tx_result = icon_integrate_test_base.process_transaction(signed_transaction, icon_service)

    return tx_result

def transaction_call(icon_integrate_test_base: IconIntegrateTestBase,
                    from_: KeyWallet,
                    to_: str,
                    method: str,
                    params: dict = None,
                    value: int = 0,
                    icon_service: IconService = None,
                    success: bool = True) -> dict:
    if success:
        return transaction_call_success(icon_integrate_test_base, from_, to_, method, params, value, icon_service)
    else:
        return transaction_call_error(icon_integrate_test_base, from_, to_, method, params, value, icon_service)

def icx_transfer_call(icon_integrate_test_base: IconIntegrateTestBase,
                      from_: KeyWallet,
                      to_: str,
                      value: int = 0,
                      icon_service: IconService = None) -> dict:
    """Sends the transaction sending ICX by using SDK

    :param icon_integrate_test_base: IconIntegrateTestBase
    :param from_: wallet address making a transaction
    :param to_: wallet address to receive coin or SCORE address to receive a transaction
    :param value: amount of ICX to be sent (Optional)
    :param icon_service: IconService
    :return: transaction result as dict
    """
    # Generates an instance of transaction for calling method in SCORE.
    transaction = TransactionBuilder() \
        .from_(from_.get_address()) \
        .to(to_) \
        .step_limit(100_000_000_000) \
        .nid(3) \
        .nonce(100) \
        .value(value) \
        .build()

    # Returns the signed transaction object having a signature
    signed_transaction = SignedTransaction(transaction, from_)

    # Sends the transaction to the network
    tx_result = icon_integrate_test_base.process_transaction(signed_transaction, icon_service)

    assert 'status' in tx_result
    assert 1 == tx_result['status']

    return tx_result
