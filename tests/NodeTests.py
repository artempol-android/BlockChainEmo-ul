import threading
import time
import unittest

from Node import Node


class NodeTests(unittest.TestCase):

    def testNextNonce(self):
        node = Node()
        node.mode = "0"
        node.nonce = node.max_int
        node.nextNonce()
        self.assertTrue(- node.max_int == node.nonce)
        node.mode = "1"
        node.nonce = - node.max_int
        node.nextNonce()
        self.assertTrue(node.max_int == node.nonce)
        node.mode = "3"
        node.nextNonce()
        self.assertTrue(-node.max_int <= node.nonce <= node.max_int)

    def testGenerateBlock(self):
        node = Node()
        for i in range(0, 5):
            block = node.generateBlock()
            self.assertTrue(block.checkHash())
            self.assertTrue(block.index == node.getLastIndex() + 1)
            self.assertTrue(node.checkBlock(block))

    def testAddBlock(self):
        node = Node()
        for i in range(0, 5):
            block = node.generateBlock()
            self.assertTrue(node.addBlock(block))
        block = node.generateBlock()
        block.index += 1
        self.assertFalse(node.addBlock(block))
        block.index -= 2
        self.assertFalse(node.addBlock(block))
        block.index += 1
        block.prev_hash = "1"
        self.assertFalse(node.addBlock(block))

    def testCheckBlock(self):
        node = Node()
        for i in range(0, 5):
            block = node.generateBlock()
            self.assertTrue(node.checkBlock(block))
            if i % 2 == 1:
                self.assertTrue(node.addBlock(block))
        block = node.generateBlock()
        block.data += "a"
        self.assertFalse(node.checkBlock(block))
        block = node.generateBlock()
        block.hash += "a"
        self.assertFalse(node.checkBlock(block))
        block = node.generateBlock()
        block.prev_hash += "1"
        self.assertFalse(node.checkBlock(block))
        block = node.generateBlock()
        block.nonce += 1
        self.assertFalse(node.checkBlock(block))
        block.nonce -= 0.9
        self.assertFalse(node.checkBlock(block))
        node.stop = True
        block = node.generateBlock()
        self.assertFalse(node.checkBlock(block))

    def testAddBlockWithCheck(self):
        node = Node()
        for i in range(0, 5):
            block = node.generateBlock()
            self.assertTrue(node.addBlockWithCheck(block))
        block = node.generateBlock()
        block.data += "a"
        self.assertFalse(node.addBlockWithCheck(block))
        block = node.generateBlock()
        block.hash += "a"
        self.assertFalse(node.addBlockWithCheck(block))
        block = node.generateBlock()
        block.prev_hash += "1"
        self.assertFalse(node.addBlockWithCheck(block))
        block = node.generateBlock()
        block.nonce += 1
        self.assertFalse(node.addBlockWithCheck(block))
        block.nonce -= 0.9
        self.assertFalse(node.addBlockWithCheck(block))
        node.stop = True
        block = node.generateBlock()
        self.assertFalse(node.addBlockWithCheck(block))

    def testGetBlock(self):
        node = Node()
        self.assertRaises(ValueError, node.getBlockFromChain, 2)
        self.assertRaises(ValueError, node.getBlockFromChain, 1)
        self.assertRaises(ValueError, node.getBlockFromChain, 0)
        self.assertRaises(ValueError, node.getBlockFromChain, -1)
        blocks = []
        for i in range(0, 5):
            blocks.append(node.generateBlock())
            node.addBlock(blocks[i])
        for i in range(0, 5):
            self.assertTrue(node.getBlockFromChain(i + 1) == blocks[i])

    def testChainBuild(self):
        node = Node()
        t = threading.Thread(target=node.chainBuild)
        t.start()
        self.assertTrue(t.is_alive())
        time.sleep(10)
        self.assertTrue(node.getLastIndex() > 0)
        node.stop = True
        t.join()
        self.assertFalse(t.is_alive())
