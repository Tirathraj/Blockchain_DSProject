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
                        {this.props.items.map((item, key) => {
                            return(
                                <tr key={key}>
                                    <th scope="row">{item.itemId.toString()}</th>
                                    <td>{item.itemName}</td>
                                    <td>{window.web3.utils.fromWei(item.itemPrice.toString(), 'Ether')} Eth</td>
                                    <td>{item.owner}</td>
                                    <td>{!item.purchased
                                        ? <button
                                            name={item.itemId}
                                            value={item.itemPrice} 
                                            desc={item.itemDescription}
                                            onClick={(event)=>{
                                                this.props.itemPurchase(event.target.name, event.target.value, event.target.desc)
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