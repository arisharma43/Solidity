//SPDX-License_Identifier:MIT

pragma solidity >=0.6.6 <0.9.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

contract FundMe{

    mapping(address => uint256) public addressToAmtFunded;

    function fund() public payable{
        addressToAmtFunded[msg.sender]+=msg.value;
        //what is the ETH->USD Conversion rate
    }

    function getVersion() public view returns (uint256){
        AggregatorV3Interface priceFeed=AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256){
        AggregatorV3Interface priceFeed=AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
        (,int256 answer,,,)=priceFeed.latestRoundData();
        return uint256(answer);
        //179728000000
        //1Eth=1,797.28000000USD
    }

    //1000000000
    function getConversionRate(uint256 ethAmt) public view returns (uint256){
        uint256 ethPrice=getPrice();
        uint256 ethAmtInUSD=(ethPrice*ethAmt)/1000000000000000000;
        return ethAmtInUSD;
    }

}
