# -*- coding: utf-8 -*-
"""
                                            CREATING OUR CRYPTOCURRENCY: NOTbitcoin
                                            
        Transactions make a blockchain a cryptocurrency
        We can exchange the cryptos through transactions that are secured and mined in the most secure way and immutable
        Transactions are then registered in a fraudless and immutable way.


Created on Fri Oct 25 03:42:00 2019

@author: Keshav Ramburn

"""



'''


#Packages Used:
#1. FLASK: Web framework to build web application that will contain the blockchain.
#Aim: Build a blockchain that can be used by anyone online using some servers.
#Version: 0.12.2: pip install Flask==0.12.2

#2. Postman HTTP Client: To get user-friendly interface to make requests to server and interact with blockchain

----------------------------------------------------------------------------------------------------------------

WE NEED ADDITONAL LIBRARIES NOW:
    
1. requests library version 2.18.4 : pip install requests==2.18.4

2. import request module from flask because we'il be connecting some nodes in a decentralised blockchain network
we'il use the getJson function from the request module

3. UUID lib to create an address for each node in the network

4. URLPARSE to parse the url of each of these nodes

'''

import datetime #Each block will have its own timestamp

import hashlib #To hash the blocks

import json #TO encode blocks before hashing

from flask import Flask,jsonify 

import requests

from flask import request

from uuid import uuid4

from urllib.parse import urlparse

'''
                                            PART 1 ----- Creating the Blockchain Architecture                              
'''


class Blockchain:
    
    '''
    Init method modified to add a list of transactions that can be recorded and appended to the block after successful mining
    Originally transactions are not in the block.
    They are added to the block as soon as the block is mined.
    
    Therefore we need to create separate list of transactions first before the createBlock function
    
    '''
    
    def __init__(self):   #self refers to the object we create
        '''
        #chain containing the blocks - list containing the blocks
        '''
        self.chain=[] 
        
        '''
        separate transactions list
        '''
        self.transactions=[]
        
        '''
        #creation of genesis block (1st block)
        #1st param: proof - each block will have its own proof
        #2nd param: previous hash - genesis block will not have any previous block
        #therefore prev hash of genesis block is 0
        '''
        self.createBlock(proof=1, previousHash='0')
        
        '''
        nodes in the blockchain network...initialised as empty set
        '''
        self.nodes=set()
        
    '''   
    #Used after Mining a new block, then we create the new block
    #with all key info we need to create the block
    '''
    def createBlock(self, proof, previousHash):
        #dictionary that defines each block in the blockchain with
        #its 4 essential keys: index of block, timestamp, proof of block, previousHash
        #can add other things as well: data,...
        #index: length of chain + 1
        #timestamp converted to string because we'il work with jsonlib
        #proof: we get it after solving proof of work algo
        '''
        Modify constructor and add transaction key as well
        '''
        block={'index': len(self.chain)+1,
               'timestamp': str(datetime.datetime.now()),
               'proof': proof,
               'previousHash': previousHash,
               'transactions': self.transactions}
        
        '''
        empty list of transacs after adding to block
        '''
        self.transactions=[]
        
        #Append new block to chain
        self.chain.append(block)        
        return block #to display info of block in POSTMAN


    def getPreviousBlock(self):
        return self.chain[-1] #-1 gives last index of chain
    
    #Proof of Work: Number/Piece of data that miners have to find
    #in order to mine a new block
    #We define a problem.
    #Miners solve that problem (a specific number)
    #Problem must be challenging to find but easy to verify
    #Hard to find not to lose value and to avoid probability that
    #2 blocks are mined simultaneously
    #If that happens, we have to fork the chain and wait for which block gets longer
    def proofOfWork(self, previousProof):
    #previousProof needs to be considered to get current proof

    #we'il solve problem with trial & error
    #we'il loop until we find current value
    
        newProof=1    
        proofFound=False

        while proofFound is False:
        #leading zeros id
        #The more leading zeros, the harder it is to solve the problem
        
        #SHA256 hash of 64 hexadecimal charactors
        #Operation needs to be non-symmetrical
        #eg: cannot be newProof+singleProof
        #bcoz above statement is same as singleProof+newProof
        #We'il then have same proof every 2 blocks...we don't want that
        #Here we'il use newProof-previousProof bcoz it is non-symmetrical
        #It's not equal to previousProof-newProof
        #Square of newProof - Square of previousProof
            hashOperation=hashlib.sha256(str(newProof**2-previousProof**2).encode()).hexdigest()
        
            #check if 1st 4 characters are 4 zeros-proofFound=True
            #upperbound of range is excluded
            if hashOperation[:4] == '0000':
                proofFound=True
            else:
                newProof+=1
        
        return newProof
    
    
    
    #Hashh Function that returns SHA256 hash of a block
    #Make dictionary a string using jsonlib's dumpts function
    #because blocks will have json format
    #We encode block in right format so that it can be accepted by sha 256 function
    def hash(self, block):
        encodedBlock=json.dumps(block, sort_keys=True).encode()
        
        return hashlib.sha256(encodedBlock).hexdigest()
    
    
    
    #Function that checks if everything is right in Blockchain:
    #Iterate on each block of chain
    #Checks 2 essential things:
    #1. Each block in blockchain has correct proof of work
    #2. previousHash of each block is equal to hash of previous block
    #Returns True if blockchain valid
    def isChainValid(self, chain):
        #blockIndex is looping variable starts at 1
        #previousBlock variable is first block of chain at first (index 0)
        
        previousBlock=chain[0]
        currentBlockIndex=1
        
        while currentBlockIndex < len(chain):
            currentBlock=chain[currentBlockIndex]
            
            if currentBlock['previousHash'] != self.hash(previousBlock):
                return False
            
            #2nd check: check if proof has 4 leading zeros
            previousProof=previousBlock['proof']
            proof=currentBlock['proof']
            
            hashOperation=hashlib.sha256(str(proof**2-previousProof**2).encode()).hexdigest()
            
            if hashOperation[:4] != '0000':
                return False
            
            #update previousBlock Variable and currentBlock Variable
            previousBlock=currentBlock
            currentBlockIndex+=1
            
        return True
            
    '''
    Method for new transaction
    Add transac to list as well
    3 key args: sender, receiver, aount of coin exchanged
    
    Returns index of new block that will receive the transactions :
        we get index of last block of chain and increment by 1
    '''
    
    def addTransaction(self, sender, receiver, amount):
        self.transactions.append({'sender': sender,
                                  'receiver': receiver,
                                  'amount': amount})
            
        previousBlock=self.getPreviousBlock()
        
        return previousBlock['index'] + 1
    
    
    '''
    Method to add new node to set of nodes in network
    1 arg: address of new node
    
    1. We parse address of new node first using urlparse function of urllib
    
    '''
    def addNode(self, address):
        
        parsedUrl=urlparse(address)
        
        self.nodes.add(parsedUrl.netloc)
       
    
    
    '''
                                                            CONSENSUS FUNCTION replaceChain    
                       1. Looks at all node in decentralised network
                       2. Checks chain of each node
                       3. Finds longest chain
                       4. Replaces chain which is shorter in any node by the longest one
    '''
    
    def replaceChain(self):
        
        network= self.nodes
        
        longestChain= None
        
        maxLength=len(self.chain)
        
        for node in network:
            #Request each node to get their chain using request library to get response of getChain request (chain,chain length)
            response=requests.get(f'http://{node}/getBlockchain')
            
            if response.status_code==200:
                length=response.json()['length']
                chain=response.json()['chain']
                
                if length>maxLength and self.isChainValid(chain):
                    maxLength=length
                    longestChain=chain
        '''            
        #Checks if longestChain is not None, means longestChain was updated and a replacement was made
        #Replace chain with longest chain
        '''
        if longestChain:    
            self.chain=longestChain
            return True
        
        return False #Chain was not replaced
        
        
        
#----------------------------------------------------------------------------------------------------------
'''        
                                                             #Part 2 - Mining the blocks
#Start interacting with blockchain
#Start making requests to mine block/display whole chain

#1. Create flask-based web app by creating object of flask class
#2. Create blockchain by creating instance of blockchain class
#3. GET Request to mine a block by solving proof of work
#4. GET Request to display whole chain
                                                             
                                                             
                                                             
Need to integrate transactions as well now 

'''        
    
                                                                    #1. CREATING WEB APP
webApplication=Flask(__name__)

'''
Creating address for the node on Port 5000
Because whenever node mines a block, it gets some coins
therefore need to have transaction to this nodeAddress as well
uuid generates unique address...replace dashes by nothing to delete them
'''
nodeAddress=str(uuid4()).replace('-','')


                                                            #2. Create instance of PART 1 Class blockchain
blockchain=Blockchain()

                                                            #3. Mine new block by making GET 1st request
@webApplication.route('/mineBlock', methods=['GET'])
def mineBlock():
    #1. Solve proof of work based on previousProof
    #2. Then get other 3 keys we need
    previousBlock=blockchain.getPreviousBlock()
    previousProof=previousBlock['proof']
    currentProof=blockchain.proofOfWork(previousProof)
    
    previousHash=blockchain.hash(previousBlock)
    
    '''
    Add transaction to the new block to reward miner
    '''
    blockchain.addTransaction(sender=nodeAddress, receiver='Myself', amount=1)
    
    #returns current block and appends it as well
    currentBlock = blockchain.createBlock(currentProof, previousHash)
    
    '''
    #display current new block   #JSON format
    include transaction list as well - modified response
    '''
    response = {'message': 'Congratulations! You have successfully mined a new block',
                'index': currentBlock['index'],
                'timestamp': currentBlock['timestamp'],
                'proof': currentBlock['proof'],
                'previousHash': currentBlock['previousHash'],
                'transactions': currentBlock['transactions']}
    
    #Return Response in JSON FORMAT
    #And HTTP STATUS CODE FOR SUCCESS  200 OK
    return jsonify(response), 200

#4. Getting full Blockchain to display in POSTMAN
@webApplication.route('/getBlockchain', methods=['GET'])
def getBlockchain():
    #blockchain in json format
    response={'chain': blockchain.chain,
              'length': len(blockchain.chain)}
    
    return jsonify(response), 200

'''
5. CREATING A POST REQUEST TO ADD NEW TRANSACTION TO THE BLOCKCHAIN
We create a json file that contains keys for the transaction
Transaction will go to the next mined block
'''
@webApplication.route('/addTransaction', methods=['POST'])
def addTransaction():
    #1. Create a transaction
    #2. Retrieve sender receiver and amount from POST request
    json=request.get_json()
    
    #3. Check that all 3 keys are present
    transactionKeys=['sender', 'receiver', 'amount']
    if not all (key in json for key in transactionKeys):
        return 'Some parameters of the transaction are missing', 400  #Bad Request (Malformed Request Syntax)
    
    
    #Add transaction to next block that will be mined (Use index of next block)
    index=blockchain.addTransaction(json['sender'], json['receiver'], json['amount'])
    
    #Return Response
    response={'message': f'Transaction will be added to the next block mined with index {index}'}
    
    return jsonify(response), 201 #Created



'''
                                                            PART 3 - Decentralising the Blockchain
'''

#1.Connecting new nodes (POST REQUEST)
#All nodes will be in a json file
#Whenever we want to add a new node, we just append the json file
@webApplication.route('/connectNode', methods=['POST'])
def connectNode():
    
    json=request.get_json()
    nodes=json.get('nodes')  #gets all addresses in json file
    
    if nodes is None:
        return "No node found", 400
    
    for node in nodes:
        blockchain.addNode(node)
    
    response={'message': 'All nodes connected: ',
              'totalNodes': list(blockchain.nodes)}
    
    return jsonify(response), 201


#2. REQUEST TO REPLACE CHAIN BY LONGEST CHAIN IF NEEDED (GET REQUEST)
@webApplication.route('/replaceChain', methods=['GET'])
def replaceChain():
    isChainReplaced=blockchain.replaceChain()
    
    if isChainReplaced:
        response={'message': 'The node had different chains; so the chain was replaced by the longest one',
                 'newChain': blockchain.chain}
    
    else:
        response={'message':'Everything is good. Chain is longest chain',
                  'actualChain': blockchain.chain}

    return jsonify(response), 200


'''
                                                                    #RUNNING THE APP
# 2 args: host, port
#If we trust users on network, can make server publicly available:
    #--host='0.0.0.0'
    #Flask URL: http://127.0.0.1:5000/
    
#REQUESTS:
#1. http://127.0.0.1:5000/mineBlock
#2. http://127.0.0.1:5000/getBlockchain
    
'''    
webApplication.run(host='0.0.0.0', port=5000)
