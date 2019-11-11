import React, {Component} from 'react';
import ipfs from './ipfs';

class Main extends Component{
    
    constructor(props){
        super(props)
        this.state  = {
            buffer: null,
            ipfsHash: ''
        }
        this.captureFile = this.captureFile.bind(this)
    }
    
    captureFile(event){
        console.log('capture file...')
        const file = event.target.files[0]
        const reader = new window.FileReader()
        reader.readAsArrayBuffer(file)
        reader.onloadend = () =>{
            this.setState({buffer : Buffer(reader.result)})
            console.log('buffer', this.state.buffer)
        }
    }

    render(){
        return(
            <div id="content">
                <form onSubmit={(event)=> {
                    event.preventDefault()
                    console.log('on submit...')
                    ipfs.files.add(this.state.buffer, (error, result) => {
                        if(error){
                            console.error(error)
                            return
                        }
                        this.setState({ ipfsHash: result[0].hash })
                        console.log('ipfshash ', this.state.ipfsHash)
                        const name = this.itemName.value
                        const price = window.web3.utils.toWei(this.itemPrice.value.toString(), 'Ether')
                        const desc = this.itemDescription.value
                        this.props.addItem(name, price, desc, this.state.ipfsHash)
                    })
                }}>
                <div className="form-group mr-md-3">
                    <input
                        id="itemName"
                        type="text"
                        ref={(input) => { this.itemName = input }}
                        className="form-control"
                        placeholder="Item Name"
                        required/>
                 </div>
                 <div className="form-group mr-md-3">
                    <input
                        id="itemPrice"
                        type="text"
                        ref={(input) => { this.itemPrice = input }}
                        className="form-control"
                        placeholder="Item Price"
                        required/>
                 </div>
                 <div className="form-group mr-md-3">
                    <input
                        id="itemDescription"
                        type="text"
                        ref={(input) => { this.itemDescription = input }}
                        className="form-control"
                        placeholder="Item Description"
                        required/>
                 </div>
                 <div className="form-group mr-md-3">
                 <input type='file' onChange={this.captureFile}/>
                 </div>
                 <button type="submit" className="btn btn-primary">Add Item</button>
                </form>
                <p></p>
                <table className="table">
                    <thead>
                        <tr>
                            <th scope="col">Id</th>
                            <th scope="col">Name</th>
                            <th scope="col">Price</th>
                            <th scope="col">Description</th>
                            <th scope="col">Owner</th>
                            <th scope="col">Image Hash</th>
                            <th scope="col">Attempted Purchase</th>
                            <th scope="col"></th>
                        </tr>
                    </thead>
                    <tbody id="itemList">
                        {this.props.items.map((item, key) => {
                            return(
                                <tr key={key}>
                                    <th scope="row">{item.itemId.toString()}</th>
                                    <td>{item.itemName}</td>
                                    <td>{window.web3.utils.fromWei(item.itemPrice.toString(), 'Ether')} Eth</td>
                                    <td>{item.itemDescription}</td>
                                    <td>{item.owner}</td>
                                    <td><img src={`https://ipfs.io/ipfs/${item.ipfsHash}`} width='128' height='auto'/></td>
                                    <td>{item.attempt.toString()}</td>
                                    <td></td>
                                    <td>{!item.purchased
                                        ? <button
                                            name={item.itemId}
                                            value={item.itemPrice} 
                                            onClick={(event)=>{
                                                this.props.itemPurchase(event.target.name, event.target.value)
                                            }}
                                            >
                                            Buy
                                            </button>
                                            : null
                                        }</td>
                                </tr>
                            )
                        })
                    }
                    </tbody>
                </table>
            </div>
        );
    }
}
export default Main;