import random
import string
import sys
import hashlib


class Node:
    max_int = sys.maxsize
    difficult = "0000"

    def __init__(self, nonce_mode=0):
        self.__chain = []
        self.mode = nonce_mode

    def nextNonce(self, nonce):
        if self.mode == 0:
            if nonce == self.max_int:
                nonce = - self.max_int
            else:
                nonce += 1
        elif self.mode == 1:
            if nonce == - self.max_int:
                nonce = self.max_int
            else:
                nonce -= 1
        else:
            nonce = random.randint(-self.max_int, self.max_int)
        return nonce

    def generateBlock(self):
        prev_hash = ''
        index = 1
        nonce = 0
        if len(self.__chain) != 0:
            prev_hash = self.__chain[-1].hash
            index = self.__chain[-1].index + 1
        data = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(256))
        block_hash = hashlib.sha256((str(index) + prev_hash + data + str(nonce)).encode('utf-8')).hexdigest()
        while not block_hash.endswith(self.difficult):
            nonce = self.nextNonce(nonce)
            block_hash = hashlib.sha256(str(index) + prev_hash + data + str(nonce)).hexdigest()
        new_block = Block(index, prev_hash, data, nonce, block_hash)
        return new_block

    # for self generated blocks
    def addBlock(self, block):
        if len(self.__chain) != 0:
            if self.__chain[-1].hash == block.prev_hash and self.__chain[-1].index + 1 == block.index:
                self.__chain.append(block)
                return True
            else:
                return False
        elif block.index == 1:
            self.__chain.append(block)
            return True
        else:
            return False

    def checkBlock(self, block):
        if hashlib.sha256(
                str(block.index) + block.prev_hash + block.data + str(block.nonce)).hexdigest() != block.hash or \
                not block.hash.endswith(self.difficult) or \
                block.prev_hash != self.__chain[-1].hash or \
                block.index != self.__chain[-1].index + 1:
            return False
        return True

    # for incoming blocks
    def addBlockWithCheck(self, block):
        if self.checkBlock(block):
            self.__chain.append(block)
            return True
        return False


class Block:
    def __init__(self, index, prev_hash, data, nonce, block_hash):
        self.index = index
        self.prev_hash = prev_hash
        self.data = data
        self.nonce = nonce
        self.hash = block_hash
