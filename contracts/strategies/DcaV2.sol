// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;
pragma abicoder v2;

import "./DcaCore.sol";
import "interfaces/ISwapRouterV2.sol";

contract DCAV2 is DCACore {
    address public WETH = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;

    function executePurchase(
        uint256 positionIndex,
        uint256 feeMultiplier,
        address[] calldata path,
        uint256 amountOutMin,
        uint256 deadline
    ) external {
        Position storage pos = _allPositions[positionIndex];
        require(pos.executor == msg.sender);

        _exactInputSwap(positionIndex, feeMultiplier, pos, path, amountOutMin, deadline);
    }

    function _exactInputSwap(
        uint256 _positionIndex,
        uint256 _feeMultiplier,
        Position storage _pos,
        address[] memory _path,
        uint256 _amountOutMin,
        uint256 _deadline
    ) internal {
        require(
            block.timestamp - _pos.lastPurchaseTimestamp > EXECUTION_COOLDOWN,
            'DCA: Too early for a next purchase'
        );

        uint256 last = _path.length - 1;
        require(_path[0] == _pos.tokenToSpend, 'DCA: Wrong input token');
        require(_path[last] == _pos.tokenToBuy, 'DCA: Wrong output token');

        uint256 amountIn = _pos.singleSpendAmount;
        address recipient = _pos.beneficiary;

        _handleFees(_path[0], amountIn, _feeMultiplier);

        require(IERC20(_path[0]).balanceOf(address(this)) >= amountIn, 'DCA: Not enough funds');

        uint256[] memory swappedAmounts;

        if (_path[last] == WETH) {
            swappedAmounts = ISwapRouterV2(swapRouter).swapExactTokensForETH(
                amountIn,
                _amountOutMin,
                _path,
                recipient,
                _deadline
            );
        } else {
            swappedAmounts = ISwapRouterV2(swapRouter).swapExactTokensForTokens(
                amountIn,
                _amountOutMin,
                _path,
                recipient,
                _deadline
            );
        }

        uint256 amountOut = swappedAmounts[last];
        _pos.lastPurchaseTimestamp = block.timestamp;

        emit PurchaseExecuted(_positionIndex, _pos.tokenToSpend, _pos.tokenToBuy, amountIn, amountOut);
    }
}
