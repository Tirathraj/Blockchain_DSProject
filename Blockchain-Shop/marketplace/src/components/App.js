import React, { Component } from 'react';
import logo from '../logo.png';
import Web3 from 'web3';
import Navbar from './Navbar';
import ArtStore from '../abis/ArtStore.json';
import Main from './Main';
import './App.css';

class App extends Component {
  async componentWillMount(){
    await this.loadweb3()
    await this.loadBlockchain()
  }

  async loadweb3(){
    if (window.ethereum){
      window.web3 = new Web3(window.ethereum)
      await window.ethereum.enable()
    }
    else if (window.web3){
      window.web3 = new Web3(window.web3.currentProvider)
    }
    else{
      window.alert('Non-ethereum browser detected. You should consider trying Meta Mask')
    }
  }

  async loadBlockchain(){
    const web3 = window.web3
    const accounts = await web3.eth.getAccounts()
    console.log(accounts)
    this.setState({account: accounts[0]})
    const networkId = await web3.eth.net.getId()
    const network = ArtStore.networks[networkId]
    if(network){
      const artstore = web3.eth.Contract(ArtStore.abi, network.address)
      this.setState({ artstore })
      const itemCount = await artstore.methods.itemCount().call()
      console.log(itemCount.toString())
      this.setState({ processing: false })
      console.log(artstore)
    }
    else{
      window.alert('ArtStore contract not connected to network.')
    }
  }

  addItem(itemName, itemPrice, itemDescription){
    this.setState({ processing: true })
    this.state.artstore.methods.addItem(itemName, itemPrice, itemDescription).send({ from: this.state.account })
    .once('receipt', (receipt) => {
      this.setState({ processing: false })
    })
  }

  constructor(props){
    super(props)
    this.state = {
      account: '',
      itemCount: 0,
      items: [],
      processing: true
    }
    this.addItem = this.addItem.bind(this)
  }
  
  render() {
    return (
      <div>
        <Navbar account={this.state.account}/>
      <div className="container mt-5">
        <div className="row justify-content-md-center">
        <main role="main" className="col-lg-12 d-flex">
        { this.state.processing
          ? <div id="loader" className="text-center"><p className="text-center">Processing...</p></div>
          : <Main addItem={this.addItem}/>
        }
      </main>
        </div>
      </div>
      </div>
    );
  }
}

export default App;
