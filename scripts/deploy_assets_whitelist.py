from brownie import AssetsWhitelist, config, network

from scripts.helpful_scripts import get_account

core_assets_to_spend = [
    "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1", # DAI
    "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8", # USDC
    "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9" # USDT
]

core_assets_to_buy = [
    "0xFa7F8980b0f1E64A2062791cc3b0871572f1F7f0",  # UNI
    "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f", # WBTC
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