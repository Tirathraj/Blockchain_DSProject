# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 03:13:02 2019

@author: Keshav Ramburn
"""

#Packages Used:
#1. FLASK: Web framework to build web application that will contain the blockchain.
#Aim: Build a blockchain that can be used by anyone online using some servers.
#Version: 0.12.2: pip install Flask==0.12.2

#2. Postman HTTP Client: To get user-friendly interface to make requests to server and interact with blockchain

#----------------------------------------------------------------------------------------------------------------

#PART 1 - Building Blockchain --- ARCHITECTURE OF BLOCKCHAIN

import datetime #Each block will have its own timestamp

import hashlib #To hash the blocks

import json #TO encode blocks before hashing

from flask import Flask,jsonify 

class Blockchain:
    
    def __init__(self):   #self refers to the object we create
        
        #chain containing the blocks - list containing the blocks
        self.chain=[] 
        
        #creation of genesis block (1st block)
        #1st param: proof - each block will have its own proof
        #2nd param: previous hash - genesis block will not have any previous block
        #therefore prev hash of genesis block is 0
        self.createBlock(proof=1, previousHash='0') 
        
    #Used after Mining a new block, then we create the new block
    #with all key info we need to create the block
    def createBlock(self, proof, previousHash):
        #dictionary that defines each block in the blockchain with
        #its 4 essential keys: index of block, timestamp, proof of block, previousHash
        #can add other things as well: data,...
        #index: length of chain + 1
        #timestamp converted to string because we'il work with jsonlib
        #proof: we get it after solving proof of work algo
        block={'index': len(self.chain)+1,
               'timestamp': str(datetime.datetime.now()),
               'proof': proof,
               'previousHash': previousHash}

        #Append new block to chain
        self.chain.append(block)        
        return block #to display info of block in POSTMAN


    def getPreviousBlock(self):
        return self.chain[-1] #-1 gives last index of chain
    
    #Proof of Work: Number/Piece of data that miners have to find
    #in roder to mine a new block
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
        
        while blockIndex < len(chain):
            currentBlock=chain[currentBlockIndex]
            
            if block['previousHash'] != self.hash(previousBlock):
                return False
            
            #2nd check: check if proof has 4 leading zeros
            previousProof=previousBlock['proof']
            proof=currentBlock['proof']
            
            hashOperation=hashlib.sha256(str(proof**2-previousProof**2).encode()).hexdigest()
            
            if hashOperation[:4] != '0000':
                return False
            
            #update previousBlock Variable and currentBlock Variable
            previousBlock=currentBlock
            blockIndex+=1
            
        return True
            
    
    #Hashh Function that returns SHA256 hash of a block
    #Make dictionary a string using jsonlib's dumpts function
    #because blocks will have json format
    #We encode block in right format so that it can be accepted by sha 256 function
    def hash(self, block):
        encodedBlock=json.dumps(block, sort_keys=True).encode()
        
        return hashlib.sha256(encodedBlock).hexdigest()
        
#----------------------------------------------------------------------------------------------------------
        
    
#Part 2 - Mining the blocks
#Start interacting with blockchain
#Start making requests to mine block/display whole chain

#1. Create flask-based web app by creating object of flask class
#2. Create blockchain by creating instance of blockchain class
#3. GET Request to mine a block by solving proof of work
#4. GET Request to display whole chain
        
    
#1. CREATING WEB APP
webApplication=Flask(__name__)

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
    
    #returns current block and appends it as well
    currentBlock = blockchain.createBlock(currentProof, previousHash)

    #display current new block   #JSON format
    response = {'message': 'Congratulations! You have successfully mined a new block',
                'index': currentBlock['index'],
                'timestamp': currentBlock['timestamp'],
                'proof': currentBlock['proof'],
                'previousHash': currentBlock['previousHash']}
    
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


#RUNNING THE APP
# 2 args: host, port
#If we trust users on network, can make server publicly available:
    #--host='0.0.0.0'
    #Flask URL: http://127.0.0.1:5000/
    
#REQUESTS:
#1. http://127.0.0.1:5000/mineBlock
#2. http://127.0.0.1:5000/getBlockchain
webApplication.run(host='0.0.0.0', port=5000)
