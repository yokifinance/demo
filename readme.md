# Brownie based project

## Setup and Installation

Before you start, you need to set up a Python virtual environment and install the necessary libraries.

To do this:

1. Install `virtualenv` if you haven't already. You can install it globally with pip:
    ```
    pip install virtualenv
    ```
2. Create a new virtual environment in your project directory:
    ```
    virtualenv venv
    ```
3. Activate the virtual environment:

   On Windows, run:
    ```
    venv\Scripts\activate
    ```
   On Unix or MacOS, run:
    ```
    source venv/bin/activate
    ```
4. Once your virtual environment is active (your terminal should show `(venv)` before the command line), install the required libraries using the `requirements.txt` file:
    ```
    pip install -r requirements.txt
    ```

Now you're ready to deploy and interact with the contracts.



## Contract deploy sequence:

| Contract name      | Brownie command                             |
|--------------------|---------------------------------------------|
| AssetsWhitelist.sol| `brownie run script/deploy_assets_white_list.py` |
| DcaV3.sol          | `brownie run script/deploy_dca_v3.py`             |
| DCAV3Factory.sol   | `brownie run script/deploy_dca_v3_factory.py`     |


## Protocol interaction flow:

1. Call the `createDCA` method from the deployed `DCAV3Factory.sol` contract, providing the following parameters to represent the future strategy:
   ```solidity
   struct Position {
       address beneficiary;         // Who will benefit from the strategy
       address executor;            // Who will execute the strategy when the time comes
       uint256 singleSpendAmount;   // AmountIn for a single swap
       address tokenToSpend;        // Token to sell
       address tokenToBuy;          // Token to buy
       uint256 lastPurchaseTimestamp; // Last purchase timestamp, initially set to 0
   }

2. After strategy creation  with `createDCA` we got contract strategy address deployed for user  
3. Set allowance to spend tokenToSpend from user address to strategy
4. Execute strategy depends from purchase interval using worker backend service you want
