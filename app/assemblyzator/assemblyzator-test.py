#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True
import unittest

from assemblyzator import Node



class AssemblyzatorTest(unittest.TestCase):
	
	
	def setUp(self):
		
		self.staticNode = Node()
	
	
	# constant formula

	def test_constant_formula_simple_pos(self):
		self.assertTrue(self.staticNode.isConstantFormula( "12" ))

	def test_constant_formula_simple_pos_op(self):
		self.assertTrue(self.staticNode.isConstantFormula( "9+1" ))

	def test_constant_formula_letter_neg_var(self):
		self.assertFalse(self.staticNode.isConstantFormula( "x" ))


	# atomic formula
	
	def test_atomic_formula_simple_pos(self):			
		self.assertTrue(self.staticNode.isAtomicFormula( "myVar" ))

	def test_atomic_formula_add(self):
		self.assertFalse(self.staticNode.isAtomicFormula( "myVar + 1" ))

	def test_atomic_formula_sub(self):
		self.assertFalse(self.staticNode.isAtomicFormula( "myVar - 2" ))

	def test_atomic_formula_mul(self):
		self.assertFalse(self.staticNode.isAtomicFormula( "myVar * 2" ))

	def test_atomic_formula_div(self):
		self.assertFalse(self.staticNode.isAtomicFormula( "myVar / 2" ))

	def test_atomic_formula_mod(self):
		self.assertFalse(self.staticNode.isAtomicFormula( "myVar % 2" ))		


	# formula cleanup
	
	def test_formula_cleanup_strip_simple(self):		
		f = self.staticNode.cleanupFormula(" a + 2 ")
		self.assertEqual(f,"a+2")

	def test_formula_cleanup_unchanged_complex(self):		
		f = self.staticNode.cleanupFormula("(a / 3) + (b / 4)")
		self.assertEqual(f,"(a/3)+(b/4)")

	def test_formula_cleanup_strip_complex(self):		
		f = self.staticNode.cleanupFormula(" (a * 6) + (b * 7) ")
		self.assertEqual(f,"(a*6)+(b*7)")

	def test_formula_cleanup_cut_parens(self):		
		f = self.staticNode.cleanupFormula("(d+9)")
		self.assertEqual(f,"d+9")

	def test_formula_cleanup_cut_and_strip(self):		
		f = self.staticNode.cleanupFormula(" (x * 55) ")
		self.assertEqual(f,"x*55")


	# parse operator

	def test_parse_operator_simple(self):

		self.staticNode.text = "a + 2"
		r = self.staticNode.findSpecifiedPairOperators( ("+",) )

		self.assertTrue(r)
		self.assertEqual(self.staticNode.leftOperand,"a")
		self.assertEqual(self.staticNode.operator,"+")
		self.assertEqual(self.staticNode.rightOperand,"2")

	def test_parse_operator_left_to_right_a(self):

		self.staticNode.text = "a + b - c"
		r = self.staticNode.findSpecifiedPairOperators( ("+","-") )

		self.assertTrue(r)
		self.assertEqual(self.staticNode.leftOperand,"a")
		self.assertEqual(self.staticNode.operator,"+")
		self.assertEqual(self.staticNode.rightOperand,"b - c")

	def test_parse_operator_left_to_right_b(self):

		self.staticNode.text = "a + b - c"
		r = self.staticNode.findSpecifiedPairOperators( ("-","+") )

		self.assertTrue(r)
		self.assertEqual(self.staticNode.leftOperand,"a")
		self.assertEqual(self.staticNode.operator,"+")
		self.assertEqual(self.staticNode.rightOperand,"b - c")
		
	def test_parse_operator_not_found(self):

		self.staticNode.text = "a + b - c"
		r = self.staticNode.findSpecifiedPairOperators( ("*","/") )

		self.assertFalse(r)


	# const calc

	def test_calc_const_simple(self):
		self.assertEqual(self.staticNode.calculateConstFormula( "3*3" ), "9" )

	def test_calc_const_complex(self):
		self.assertEqual(self.staticNode.calculateConstFormula( "3*3-3*3" ), "0" )
		

	# const value

	def test_const_value(self):
		node = Node(None,"5 * 5")
		node.parseNode()
		self.assertEqual( node.getRepresentation(), "25" )


if __name__ == "__main__":
	unittest.main()
