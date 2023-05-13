// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;
pragma abicoder v2;

import "interfaces/IDCA.sol";
import "interfaces/IAssetsWhitelist.sol";
import "../libraries/Path.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/proxy/Clones.sol";
import "@uniswap/contracts/interfaces/ISwapRouter.sol";
import "@uniswap/contracts/libraries/TransferHelper.sol";

contract DCAV3Factory {
    using Path for bytes;

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
        address treasury_,
        uint256 price_
    ) {
        require(assetsWhitelist_ != address(0));
        require(dcaImpl_ != address(0));
        require(treasury_ != address(0));
        require(price_ > 0);
        assetsWhitelist = assetsWhitelist_;
        dcaImpl = dcaImpl_;
        price = price_;
        treasury = treasury_;
    }

    // function createDCA(
    //     address newOwner,
    //     IDCA.Position calldata initialPosition,
    //     ISwapRouter.ExactOutputParams calldata params
    // ) external returns (address newDcaProxy) {
    //     bool hasMultiplePools = params.path.hasMultiplePools();
    //     (address tokenIn, address tokenOut) = params.path.decodeFirstPool();

    //     require(tokenIn == WBTC, 'DCAFactory: Should get WBTC token');
    //     require(params.recipient == treasury, 'DCAFactory: Treasury should be recipient');
    //     require(params.amountOut == price, 'DCAFactory: Wrong amount of WBTC');

    //     bytes memory tempPath;

    //     if (hasMultiplePools) {
    //         tempPath = params.path.skipToken();
    //         while (true) {
    //             hasMultiplePools = tempPath.hasMultiplePools();
    //             (tokenIn, tokenOut) = tempPath.decodeFirstPool();

    //             if (hasMultiplePools) {
    //                 tempPath = tempPath.skipToken();
    //             } else {
    //                 break;
    //             }
    //         }
    //     }

    //     TransferHelper.safeApprove(tokenOut, SWAP_ROUTER, params.amountInMaximum);

    //     uint256 amountIn = ISwapRouter(SWAP_ROUTER).exactOutput(params);

    //     if (amountIn < params.amountInMaximum) {
            // TransferHelper.safeApprove(tokenOut, SWAP_ROUTER, 0);
    //         TransferHelper.safeTransferFrom(tokenOut, address(this), msg.sender, params.amountInMaximum - amountIn);
    //     }

    //     newDcaProxy = _deployDCA(newOwner, initialPosition);
    //     return newDcaProxy;
    // }

    function createDCA(
        address newOwner,
        IDCA.Position calldata initialPosition
    ) external returns (address newDcaProxy) {

        (address tokenIn, address tokenOut) = params.path.decodeFirstPool();

        newDcaProxy = _deployDCA(newOwner, initialPosition);
        TransferHelper.safeApprove(tokenOut, SWAP_ROUTER, 0);

        return newDcaProxy;
    }

    function _deployDCA(
        address _newOwner,
        IDCA.Position calldata _initialPosition
    ) internal returns (address) {
        address proxy = Clones.clone(dcaImpl);

        IDCA(proxy).initialize(
            IAssetsWhitelist(assetsWhitelist),
            SWAP_ROUTER,
            _newOwner,
            _initialPosition
        );

        emit DcaDeployed(proxy, _newOwner);

        return proxy;
    }
}
