from brownie import AssetsWhitelist, config, network

from scripts.helpful_scripts import get_account

core_assets_to_spend = [
    "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1", # DAI
    "0x2058A9D7613eEE744279e3856Ef0eAda5FCbaA7e", # USDC # Mubmai
    "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9" # USDT
]

core_assets_to_buy = [
    "0xFa7F8980b0f1E64A2062791cc3b0871572f1F7f0",  # UNI
    "0x326C977E6efc84E512bB9C30f76E30c160eD06FB", # CHAIN LINK # Mumbai
    "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1" # WETH
]

def deploy_assets_whitelist():
    account = get_account()
    assets_white_list = AssetsWhitelist.deploy(
        core_assets_to_spend,
        core_assets_to_buy,
        {'from': account},
        publish_source=config['networks'][network.show_active()].get('verify')
    )

    print(f'Contract deployed to: {assets_white_list.address}')
    return assets_white_list

def main():
    deploy_assets_whitelist()