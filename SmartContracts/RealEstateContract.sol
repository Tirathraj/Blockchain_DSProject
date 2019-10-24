pragma solidity >= 0.4.11 < 0.5.12;

contract LandRegistration{
    uint256 ownerEntry = 0;
    mapping (uint => Member) public owners;
    
    struct Member{
    uint256 _id;
    string _sin;
    string _firstName;
    string _lastName;
    string _dateOfBirth;
    string _placeOfBirth;
    string _occupation;
    }
    
    constructor() public{
    }
    
    function addMember(string memory _sin, string memory _firstName, string memory _lastName, string memory _dateOfBirth, string memory _placeOfBirth, string memory _occupation) public{
        ownerEntry += 1;
        owners[ownerEntry] = Member(ownerEntry, _sin, _firstName, _lastName, _dateOfBirth, _placeOfBirth, _occupation);
    }
}
