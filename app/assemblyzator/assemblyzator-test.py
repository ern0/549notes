#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True
import unittest

from assemblyzator import Node



class AssemblyzatorTest(unittest.TestCase):
	
	
	def setUp(self):
		
		self.staticNode = Node()
	
	
	# atomic expression checking
	
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
		
	
	# formula cleanup
	
	def test_formula_cleanup_strip_simple(self):		
		f = self.staticNode.cleanupFormula(" a + 2 ")
		self.assertEqual(f,"a + 2")

	def test_formula_cleanup_unchanged_complex(self):		
		f = self.staticNode.cleanupFormula("(a / 3) + (b / 4)")
		self.assertEqual(f,"(a / 3) + (b / 4)")

	def test_formula_cleanup_strip_complex(self):		
		f = self.staticNode.cleanupFormula(" (a * 6) + (b * 7) ")
		self.assertEqual(f,"(a * 6) + (b * 7)")

	def test_formula_cleanup_cut_parens(self):		
		f = self.staticNode.cleanupFormula("(d + 9)")
		self.assertEqual(f,"d + 9")

	def test_formula_cleanup_cut_and_strip(self):		
		f = self.staticNode.cleanupFormula(" (x * 55) ")
		self.assertEqual(f,"x * 55")

		
if __name__ == "__main__":
	unittest.main()
