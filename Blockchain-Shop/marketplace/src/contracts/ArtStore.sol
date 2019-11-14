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
        address invader; //The user who attempts to tamper with the item
        string notifMsg; //Check if a person tried to tamper with the item
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
        items[itemCount] = Item(itemCount, _itemName, _itemPrice, _itemDescription, _ipfsHash, msg.sender, false, address(0), "");
        //Triggering an event on item addition
        emit ItemAdded(itemCount, _itemName, _itemPrice, _itemDescription, _ipfsHash, msg.sender, false, address(0), "");
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
        bool purchased,
        address invader,
        string notifMsg
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
        emit ItemPurchased(itemCount, _item.itemName, _item.itemPrice, _item.itemDescription, _item.ipfsHash, msg.sender, true, address(0), "");
    }

    event ItemPurchased(
        uint itemId,
        string itemName,
        uint itemPrice,
        string itemDescription,
        string ipfsHash,
        address payable owner,
        bool purchased,
        address invader,
        string notifMsg
    );

    /**
    This is the function to edit an item in blockchain.
     */
    function editItemCheck(uint _itemId) public{
        Item memory _item = items[_itemId];
        address payable _seller = _item.owner;
        //Validating the sender
        if(_seller != msg.sender){
            _item.invader = msg.sender;
            _item.notifMsg = " attempted to tamper with the price";
        }
        else{
            _item.invader = address(0);
            _item.notifMsg="Owner updated the price";
        }
        //Updating the item
        items[_itemId] = Item(_item.itemId, _item.itemName, _item.itemPrice, _item.itemDescription, _item.ipfsHash, _item.owner, false, _item.invader, _item.notifMsg);
        //Triggering an event on item addition
        emit ItemEdited(_item.itemId, _item.itemName, _item.itemPrice, _item.itemDescription, _item.ipfsHash, _item.owner, false, _item.invader, _item.notifMsg);
    }

        /**
    This event gives notification to the buyers that an item has been added to the blockchain
     */
    event ItemEdited(
        uint itemId,
        string itemName,
        uint itemPrice,
        string itemDescription,
        string ipfsHash,
        address payable owner,
        bool purchased,
        address invader,
        string notifMsg
    );
}