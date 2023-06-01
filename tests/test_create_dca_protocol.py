import pytest
from brownie import accounts, exceptions, network

from scripts.deploy_assets_white_list import deploy_assets_white_list
from scripts.deploy_dca_v3 import deploy_dca_v3
from scripts.deploy_dca_v3_factory import deploy_dca_v3_factory
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRENMENTS, get_account
from scripts.price_convertor import get_amount_wei


def test_can_deploy_assets_white_list():
    account = get_account()
    assets_whitelist = deploy_assets_white_list()
    # TBD


def test_can_deploy_dca_v3():
    account = get_account()
    dca_v3 = deploy_dca_v3()
    # TBD


def test_can_deploy_dca_v3_factory():
    account = get_account()
    dca_v3_factory = deploy_dca_v3_factory()


def test_can_create_dca():
    account = get_account()
    worker = accounts.add()
    dca_v3_factory = deploy_dca_v3_factory()

    position = (
        account.address,
        worker.address,
        get_amount_wei(2, 6),
        "0xc2132D05D31c914a87C6611C10748AEb04B58e8F", # USDT
        "0xb33EaAd8d922B1083446DC23f610c2567fB5180f", # UNI
        0
    )
    tx = dca_v3_factory.createDCA(account, position, {'from': account})
    tx.wait(1)


