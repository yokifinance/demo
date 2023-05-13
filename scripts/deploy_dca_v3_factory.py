from brownie import DCAV3Factory, config, network

from scripts.deploy_assets_white_list import deploy_assets_white_list
from scripts.deploy_dca_v3 import deploy_dca_v3
from scripts.helpful_scripts import get_account


def deploy_dca_v3_factory():

    account = get_account()
    assets_whitelist_address: str = deploy_assets_white_list().address
    dca_implementation_address: str = deploy_dca_v3().address

    dca_v3_factory = DCAV3Factory.deploy(
        assets_whitelist_address,
        dca_implementation_address,
        {'from': account},
        publish_source=config['networks'][network.show_active()].get('verify')
    )

    print(f'Contract {dca_v3_factory._name} deployed to: {dca_v3_factory.address}')
    return dca_v3_factory


def main():
    deploy_dca_v3_factory()