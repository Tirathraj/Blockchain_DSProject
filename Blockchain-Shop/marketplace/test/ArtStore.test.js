const ArtStore = artifacts.require('./ArtStore.sol')
require('chai').use(require('chai-as-promised')).should()

contract('ArtStore', ([deployer, seller, buyer]) => {
    let artstore

    before(async () => {
        artstore = await ArtStore.deployed()
    })

    contract('deployment', async () => {
        it('deploys successfully', async() => {
            const address = await artstore.address
            assert.notEqual(address, 0x0)
            assert.notEqual(address, '')
            assert.notEqual(address, null)
            assert.notEqual(address, undefined)
        })

        it('has a name', async() => {
            const name = await artstore.name()
            assert.equal(name, 'Market')
        })
    })

    contract('items', async() => {
        let output, itemCount

        before(async () => {
            output = await artstore.addItem('Mona Lisa', web3.utils.toWei('1','Ether'), 'A masterpiece by Leonardo Da Vinci', {from: seller})
            itemCount = await artstore.itemCount()
        })

        it('adds items', async() => {
            //This for checking if item count is 1
            assert.equal(itemCount,1)
            //Logging an event to a history log
            const event = output.logs[0].args
            //Check item content is correct
            assert.equal(event.itemId.toNumber(), itemCount.toNumber, 'Item ID is correct')
            assert.equal(event.itemName, 'Mona Lisa', 'Item name is correct')
            assert.equal(event.itemPrice, '1000000000000000000', 'Item price is correct')
            assert.equal(event.itemDescription, 'A masterpiece by Leonardo Da Vinci', 'Item description is correct')
            assert.equal(event.owner, seller, 'Item owner is correct')
            assert.equal(event.purchased, false, 'Item purchased is correct')
            //Purposely make the tests wrong
            await artstore.addProduct('', web3.utils.toWei('1', 'Ether'), '', {from: seller}).should.be.rejected;
            await artstore.addProduct('Mona Lisa', 0, 'A masterpiece by Michelangelo', {from: seller}).should.be.rejected;
        })
    })
})