import unittest

from Node import Block, Node


class BlockTests(unittest.TestCase):
    node = Node()

    def testCheckHash(self):
        block = Block(1, "addsa", "aaaaaaaaa", 0, "asdsdada")
        self.assertFalse(block.checkHash())

        block = self.node.generateBlock()
        self.assertTrue(block.checkHash())

        block.nonce += 1
        self.assertFalse(block.checkHash())

        block.nonce -= 1
        block.hash += " "
        self.assertFalse(block.checkHash())

        str.strip(block.hash)
        block.data += " "
        self.assertFalse(block.checkHash())

        str.strip(block.data)
        block.prev_hash += " "
        self.assertFalse(block.checkHash())

        str.strip(block.prev_hash)
        block.index += 1
        self.assertFalse(block.checkHash())

    def testTypes(self):
        block = Block("1", "addsa", "aaaaaaaaa", "0", "asdsdada")
        self.assertFalse(block.checkHash())
        self.assertRaises(TypeError, Block(1, 2, 3, 4, 5))
        self.assertRaises(TypeError, Block([111, 12], 2, 3, 4, 5))
        self.assertRaises(TypeError, Block(1, 2, None, 4, 5))
