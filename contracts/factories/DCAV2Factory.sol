// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;
pragma abicoder v2;

import "interfaces/IDCA.sol";
import "interfaces/IAssetsWhitelist.sol";
import "interfaces/ISwapRouterV2.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/proxy/Clones.sol";
import '@uniswap/contracts/libraries/TransferHelper.sol';

contract DCAV2Factory {
    address public assetsWhitelist;
    address public dcaImpl;
    uint256 public price;
    address public treasury;

    address public constant WBTC = 0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f;
    address public constant SWAP_ROUTER = 0xE592427A0AEce92De3Edee1F18E0157C05861564;

    event DcaDeployed(address indexed newDcaAddress, address indexed newOwner);

    constructor(
        address assetsWhitelist_,
        address dcaImpl_,
        uint256 price_,
        address treasury_
    ) {
        require(assetsWhitelist_ != address(0));
        require(dcaImpl_ != address(0));
        require(price_ > 0);
        require(treasury_ != address(0));
        assetsWhitelist = assetsWhitelist_;
        dcaImpl = dcaImpl_;
        price = price_;
        treasury = treasury_;
    }

    function createDCA(
        address newOwner,
        IDCA.Position calldata initialPosition,
        address[] calldata path,
        uint256 amountInMax,
        uint256 deadline
    ) external payable {
        uint256 last = path.length - 1;

        require(path[last] == WBTC, "Not WBTC token");

        uint256[] memory swappedAmounts;

        if (msg.value > 0) {
            swappedAmounts = ISwapRouterV2(SWAP_ROUTER).swapETHForExactTokens(
                price,
                path,
                treasury,
                deadline
            );
        } else {
            TransferHelper.safeTransferFrom(path[last], msg.sender, address(this), amountInMax);
            TransferHelper.safeApprove(path[last], SWAP_ROUTER, amountInMax);

            swappedAmounts = ISwapRouterV2(SWAP_ROUTER).swapTokensForExactTokens(
                price,
                amountInMax,
                path,
                treasury,
                deadline
            );
        }
        _deployDCA(newOwner, initialPosition);
    }

    function createDCAWithRoobee(
        address newOwner,
        IDCA.Position calldata initialPosition
    ) external {
        TransferHelper.safeTransferFrom(WBTC, msg.sender, treasury, price);
        _deployDCA(newOwner, initialPosition);
    }

    function _deployDCA(
        address _newOwner,
        IDCA.Position calldata _initialPosition
    ) internal {
        address proxy = Clones.clone(dcaImpl);

        IDCA(proxy).initialize(
            IAssetsWhitelist(assetsWhitelist),
            SWAP_ROUTER,
            _newOwner,
            _initialPosition
        );

        emit DcaDeployed(proxy, _newOwner);
    }
}
