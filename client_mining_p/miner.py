import hashlib
import requests # axios for python?
import json
from time import time

import sys


# TODO: Implement functionality to search for a proof 
def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(last_proof, proof) contain 6
    leading zeroes?
    """
    # TODO
    guess = f'{block_string}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    # print('guess', guess)
    # print('guess hash', guess_hash)

    return guess_hash[:6] == "000000"


def proof_of_work(block):
    """
    Simple Proof of Work Algorithm
    - Find a number p such that hash(last_block_string, p) contains 6 leading
    zeroes, 
    """
    block_string = json.dumps(block, sort_keys=True).encode()
    p = 0
    while not valid_proof(block_string, p):
        p += 1
    
    return p


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        # TODO: Get the last proof from the server and look for a new one
        req = requests.get(f'{node}/last_block')
        block = req.json()
        print('Starting to solve block...')
        start = time()
        proof = proof_of_work(block['last-block'])
        print('Finished solving block!')
        end = time()
        total_time = end - start
        print(f'Solved block in {total_time} seconds')
        # TODO: When found, POST it to the server {"proof": new_proof}
        response = requests.post(url = f'{node}/mine', json = {"proof": proof})
        # TODO: If the server responds with 'New Block Forged'
        response = response.json()
        if response['message'][0] == 'N':
            print('Successfully mined the block!')
            coins_mined += 1
            print(f'You now how {coins_mined} total coins!')
        else:
            print('Sorry, you failed to mine the block... Keep trying')
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        pass
