from brownie import FundMe, network, accounts, exceptions
import pytest

from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRENMENTS  
from scripts.deploy_dca_v3_factory import deploy_dca_v3_factory
from scripts.deploy_assets_white_list import deploy_assets_white_list
from scripts.deploy_dca_v3 import deploy_dca_v3


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
    # TBD
   


def test_can_create_dca():
    account = get_account()
    dca_v3_factory = deploy_dca_v3_factory()
