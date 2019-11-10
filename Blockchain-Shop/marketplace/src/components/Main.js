import React, {Component} from 'react';

class Main extends Component{

    render(){
        return(
            <div id="content">
                <form onSubmit={(event)=> {
                    event.preventDefault()
                    const name = this.itemName.value
                    const price = window.web3.utils.toWei(this.itemPrice.value.toString(), 'Ether')
                    const desc = this.itemDescription.value
                    this.props.addItem(name, price, desc)
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
                 <button type="submit" className="btn btn-primary">Add Item</button>
                </form>
                <p></p>
                <table className="table">
                    <thead>
                        <tr>
                            <th scope="col">#</th>
                            <th scope="col">Name</th>
                            <th scope="col">Price</th>
                            <th scope="col">Description</th>
                            <th scope="col">Owner</th>
                            <th scope="col"></th>
                        </tr>
                    </thead>
                    <tbody id="itemList">
                        <tr>
                            <th scope="row"></th>
                            <td>Mona Lisa</td>
                            <td>1 Eth</td>
                            <td>Masterpiece by Leonardo Da Vinci 
                                ams,ansmaasnkanskasasnamsnmansmasnamsn
                                ansmaasnkanskasasnamsnmansmasnamsnasnmansmamnbmnbs
                                dsmmndmsnd,snd
                                sdnsmndmsdn
                                nadbanbd
                            </td>
                            <td>Owner</td>
                            <td><button className="buyButton">Buy</button></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        )
    }
}
export default Main;