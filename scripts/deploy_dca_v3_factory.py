from brownie import DCAV3Factory, config, network

from scripts.helpful_scripts import get_account


def deploy_dca_v3_factory(assets_whitelist_address: str , dca_implementation_address: str):

    account = get_account(account_label='main')

    dca_v3_factory = DCAV3Factory.deploy(
        assets_whitelist_address,
        dca_implementation_address,
        {'from': account},
        publish_source=config['networks'][network.show_active()].get('verify')
    )

    print(f'Contract {dca_v3_factory._name} deployed to: {dca_v3_factory.address}')
    return dca_v3_factory


def main():
    assets_whitelist_address = '0x59698022f08FF0d0B6EDbC956Fd9c0596543A983'
    dca_implementation_address = '0xf52Aea45dFDE4669C73010D4C47E9e0c75E5c8ca'
    deploy_dca_v3_factory(assets_whitelist_address, dca_implementation_address)