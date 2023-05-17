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
    assets_whitelist_address = '0x55767e19Dd3Aa623a4A2537cA2DE29bA95E740f7'
    dca_implementation_address = '0x16EbC30aEaEd24a446722aA4A24A5254ED07e950'
    deploy_dca_v3_factory(assets_whitelist_address, dca_implementation_address)