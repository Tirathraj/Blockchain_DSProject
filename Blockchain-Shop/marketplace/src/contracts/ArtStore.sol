pragma solidity >=0.5.8;

/**
This is a smart contract for storing pictures, their prices,
their buyers and sellers,as well as their descriptions.
 */
contract ArtStore{
    string public itemName;
    uint public itemCount = 0;
    mapping(uint => Item) public items;

    constructor() public{
        itemName = "Market";
    }

    //The data structure of the item
    struct Item{
        uint itemId; //Unique ID for the item
        string itemName; //Name of the item
        uint itemPrice; //Cost of the item
        string itemDescription; //Short description of the item
        string ipfsHash; //The IPFS Hash
        address payable owner; //The owner of the item
        bool purchased; //Whether or not the item is purchased
        //string imageHash; //The hash of the image in the IPFS
    }



    /**
    This is the function to add an item in blockchain.
     */
    function addItem(string memory _itemName, uint _itemPrice, string memory _itemDescription, string memory _ipfsHash) public{
        //The name should be at least 1 byte
        require(bytes(_itemName).length > 0,"The name should be at least 1 byte.");
        //Item price should be greater than zero
        require(_itemPrice > 0,"Item price should be greater than zero");
        //Stock count should be greater than zero
    
        //This is for counting the item
        itemCount++;
        //Adding the item
        items[itemCount] = Item(itemCount, _itemName, _itemPrice, _itemDescription, _ipfsHash, msg.sender, false);
        //Triggering an event on item addition
        emit ItemAdded(itemCount, _itemName, _itemPrice, _itemDescription, _ipfsHash, msg.sender, false);
    }

    /**
    This event gives notification to the buyers that an item has been added to the blockchain
     */
    event ItemAdded(
        uint itemId,
        string itemName,
        uint itemPrice,
        string itemDescription,
        string ipfsHash,
        address payable owner,
        bool purchased
    );

    function itemPurchase(uint _itemId) public payable{
        Item memory _item = items[_itemId];
        address payable _seller = _item.owner;
        require(_item.itemId > 0 && _item.itemId <= itemCount, "illigal index.");
        require(msg.value >= _item.itemPrice, "value must be greater than itemprice.");
        //require(!_item.purchased,"item is already purchased.");
        require(_seller != msg.sender,"ownership is invalid.");
        _item.owner = msg.sender;
        _item.purchased = true;
        items[_itemId] = _item;
        address(_seller).transfer(msg.value);
        emit ItemPurchased(itemCount, _item.itemName, _item.itemPrice, _item.itemDescription, _item.ipfsHash, msg.sender, true);
    }

    event ItemPurchased(
        uint itemId,
        string itemName,
        uint itemPrice,
        string itemDescription,
        string ipfsHash,
        address payable owner,
        bool purchased
    );

}