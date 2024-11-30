// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract WeatherAverages {
    int256[] public averages;

    function addAverage(int256 average) public {
        averages.push(average);
    }

    function getAveragesCount() public view returns (uint256) {
        return averages.length;
    }

    function getAverage(uint256 index) public view returns (int256) {
        require(index < averages.length, "out of boundaries");
        return averages[index];
    }
    
    function getAllAverages() public view returns (int256[] memory) {
        return averages;
    }
}
