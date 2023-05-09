from brownie import DCAV3Factory, Wei, config, network

from scripts.helpful_scripts import get_account

ASSETS_WHITE_LISTS = '0xAE435424C6ca7990CC0930c3664e47991F381649'
DCA_IMPL = '0xEf8a6dD37908E418b1596dAD00226Bd2A62c3D7f'
TREASURY_ADDRESS = '0xc292a5E92259067de5E6BAE69059463d870F1d29'
WBTC_PRICE = Wei("1 ether")

def deploy_dca_v3_factory():

    account = get_account()
    dca_v3_factory = DCAV3Factory.deploy(
        ASSETS_WHITE_LISTS,
        DCA_IMPL,
        TREASURY_ADDRESS,
        WBTC_PRICE,
        {'from': account},
        publish_source=config['networks'][network.show_active()].get('verify')
    )

    print(f'Contract deployed to: {dca_v3_factory.address}')
    return dca_v3_factory


def main():
    deploy_dca_v3_factory()