#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True
import unittest

from assemblyzator import Node



class AssemblyzatorTest(unittest.TestCase):
	
	
	def setUp(self):
		
		self.staticNode = Node()
	
	
	# atomic expression check
	
	def test_atomic_expression_simple_pos(self):			
		self.assertTrue(self.staticNode.isAtomicExpression( "myVar" ))

	def test_atomic_expression_add(self):
		self.assertFalse(self.staticNode.isAtomicExpression( "myVar + 1" ))

	def test_atomic_expression_sub(self):
		self.assertFalse(self.staticNode.isAtomicExpression( "myVar - 2" ))

	def test_atomic_expression_mul(self):
		self.assertFalse(self.staticNode.isAtomicExpression( "myVar * 2" ))

	def test_atomic_expression_div(self):
		self.assertFalse(self.staticNode.isAtomicExpression( "myVar / 2" ))

	def test_atomic_expression_mod(self):
		self.assertFalse(self.staticNode.isAtomicExpression( "myVar % 2" ))
		
if __name__ == "__main__":
	unittest.main()
