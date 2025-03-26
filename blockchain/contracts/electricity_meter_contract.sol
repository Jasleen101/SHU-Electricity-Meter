// SPDX-License-Identifier: MIT
pragma solidity >=0.4.16 <0.9.0;

contract ElectricityMeterReading {

    struct MeterReading {
        string uid;
        uint256 mtr_reading;  // Use scaled integer to represent the decimal value
    }

    address public owner;
    uint128 private costPerUnit;

    modifier onlyOwner() {
        require(msg.sender == owner, "Not Authorized");
        _;
    }

    event MeterReadingSubmission(address addr, MeterReading mtr);
    event GridAlert(string message);

    mapping(address => MeterReading[]) private _meterReadings;
    mapping(address => uint256) private _bills;

    uint256 private cost_per_kwh = 22; // Representing 0.001 as 1 after scaling by 1000
    uint256 private constant SCALING_FACTOR = 1000; // Scaling factor to handle 3 decimal places

    function getMeterReadings() public view returns (MeterReading[] memory) {
        uint length = _meterReadings[msg.sender].length;
        MeterReading[] memory readings = new MeterReading[](length); 
        for(uint i = 0; i<length; i++){
            MeterReading memory reading = _meterReadings[msg.sender][i];
            readings[i] = reading;
        }   
        return readings;
    }

    function getSpecificMeterReading(string memory uidValue) public view returns (MeterReading memory) {
        uint length = _meterReadings[msg.sender].length;

        for (uint i = 0; i < length; i++) {
            if (keccak256(abi.encodePacked(_meterReadings[msg.sender][i].uid)) == keccak256(abi.encodePacked(uidValue))) {
                return _meterReadings[msg.sender][i];
            }
        }
        revert("Meter reading not found");
    }

    function getMeterBill() public view returns (uint256) {
        return _bills[msg.sender];
    }

    function storeMeterReading(string memory uid, uint256 mtr_reading) public {
        // Input Validation for ensuring uid and meter reading are valid and not empty
        require(bytes(uid).length > 0, "UID can not be empty");
        require(mtr_reading > 0, "Meter reading must be greater than zero");

        // Duplicate readings check
        for (uint i = 0; i < _meterReadings[msg.sender].length; i++) {
            require(keccak256(abi.encodePacked(_meterReadings[msg.sender][i].uid)) != keccak256(abi.encodePacked(uid)), "Duplicate reading is not allowed");
        }

        uint256 scaledReading = mtr_reading; // Scale up the meter reading to store as integer
        MeterReading memory reading = MeterReading({uid: uid, mtr_reading: scaledReading });
        _meterReadings[msg.sender].push(reading);
        emit MeterReadingSubmission(msg.sender, reading);

        // Update the bill with scaled cost calculation
        _bills[msg.sender] += (scaledReading * cost_per_kwh)/SCALING_FACTOR;
    }

    function sendGridAlert(string memory _message) public {
        emit GridAlert(_message);
    }
}
