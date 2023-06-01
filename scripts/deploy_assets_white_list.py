from brownie import AssetsWhitelist, config, network

from scripts.chain_addresses import core_assets_to_buy, core_assets_to_spend
from scripts.helpful_scripts import get_account


def deploy_assets_white_list():
    account = get_account()
    assets_white_list = AssetsWhitelist.deploy(
        core_assets_to_spend,
        core_assets_to_buy,
        {'from': account},
        publish_source=config['networks'][network.show_active()].get('verify')
    )

    print(f'Contract {assets_white_list._name} deployed to: {assets_white_list.address}')
    return assets_white_list

def main():
    deploy_assets_white_list()