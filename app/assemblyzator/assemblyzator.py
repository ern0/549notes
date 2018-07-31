#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True

import os


class Instruction:


	def __init__(self,name,left,op,right):

		self.name = name.strip()
		self.left = left.strip()
		self.op = op.strip()
		self.right = right.strip()


	def render(self):

		result = self.name
		result += " = "

		if self.left == "":
			result += self.op + self.right
		else:
			result += self.left 
			result += " " + self.op + " "
			result += self.right
	
		return result


class Node:

	nextId = 0
	nodeList = []
	instructionList = []


	def __init__(self,parent = None,text = None):
		
		self.refCount = 0

		self.children = []
		self.parent = parent
		Node.nodeList.append(self)

		if Node.nextId == 0:
			self.name = "root"
		else:
			self.name = "var" + str(Node.nextId)
		Node.nextId += 1

		self.text = self.cleanupFormula(text)
		
		self.leftOperand = ""
		self.operator = ""
		self.rightOperand = ""


	def createChild(self,text):

		text = self.cleanupFormula(text)

		for child in self.nodeList:
			if child.text == text: 
				child.refCount += 1
				return child
			
		child = Node(self,text)
		child.refCount += 1
		self.children.append(child)

		return child


	def processFile(self,fnam):
		
		self.load(fnam)
		self.processRoot()
		
	
	def processString(self,text):
		
		self.text = self.cleanupFormula(text)
		self.processRoot()
		

	def processRoot(self):
		
		self.normalize()
		self.splitStatements()
		self.parse()
		self.applyIdentity()
		self.generateInstructions()


	def load(self,fnam):
		with open(fnam,"r") as file:
			self.text = file.read()


	def normalize(self):
		
		self.text = self.text.replace(";","\n")
		raw = self.text.split("\n")
		self.text = ""

		for line in raw:
			
			if "//" in line: line = line.split("//")[0]
			line = line.strip()
			if line == "": continue
			
			self.text = self.text + line
			self.text += ";"


	def splitStatements(self):
		
		if self.text.count(";") < 2:
			self.text = self.text.replace(";","")
			self.parse()
			return
		
		statements = self.text.split(";")
		self.text = ""

		for stat in statements:
			if stat == "": continue

			child = self.createChild(stat)
			child.parse()
				

	def parse(self):
		
		self.parseNode()
		self.parseChildren()
		
		
	def parseNode(self):

		while True:

			if self.parseAssignment(): break
			
			if self.parsePairOperator( ("|",) ): break
			if self.parsePairOperator( ("^",) ): break
			if self.parsePairOperator( ("&",) ): break
			if self.parsePairOperator( ("<",">",) ): break
			if self.parsePairOperator( ("+","-") ): break
			if self.parsePairOperator( ("*","/","%") ): break

			break
			
		self.text = (
			self.cleanupFormula(self.leftOperand)
			+ self.operator
			+ self.cleanupFormula(self.rightOperand)
		)


	def parseChildren(self):
		
		for child in self.children:
			child.parse()


	def cleanupFormula(self,text):

		if text is None: return
		
		text = text.strip()
		text = text.replace("<<","<")
		text = text.replace(">>",">")
				
		insideApostrophe = False
		insideQuotation = False
		parenDepth = 0
		parenOv = False
		result = ""
		
		for i in range(0,len(text)):
			c = text[i]
			
			if insideApostrophe:
				result += c
				if c == "'": insideApostrophe = False
				continue
				
			if insideQuotation:
				result += c
				if c == "\"": insideQuotation = False				
				continue
				
			if insideApostrophe or insideQuotation: 
				result += c
				continue

			if c != " ": result += c
						
			if c == "'": 
				insideApostrophe = True
				continue
				
			if c == "\"": 
				insideQuotation = True
				continue				
			
			isFirstOrLast = False
			if i == 0: isFirstOrLast = True
			if i == len(text) - 1: isFirstOrLast = True
			if not isFirstOrLast:
				if c == "(": parenDepth += 1
				if c == ")": parenDepth -= 1
				if parenDepth < 0: parenOv = True

		try:
			if (result[0] != '('): return result
			if (result[-1] != ')'): return result
		except IndexError: return result
		
		if not parenOv: result = result[1:-1]
		
		return result


	def findSplitPoint(self,separatorList):

		indent = 0
		for i in range(0,len(self.text)):
			c = self.text[i]

			if c == "(": 
				indent += 1
				continue

			if c == ")":
				indent -= 1
				continue

			if indent > 0: 
				continue

			if c in separatorList:
				return i

		return None


	def parseAssignment(self):
		
		p = self.findSplitPoint( ("=",) )
		if p is None: return False
		
		self.name = self.text[0:p].strip()
		self.text = self.text[(1 + p):].strip()
		
		return True


	def parsePairOperator(self,operatorList):

		p = self.findSplitPoint(operatorList)
		if p is None: return False

		leftFormula = self.text[0:p].strip()
		self.leftOperand = self.createNodeIfNotAtomic(leftFormula)

		self.operator = self.text[p]

		rightFormula = self.text[(1 + p):].strip()
		self.rightOperand = self.createNodeIfNotAtomic(rightFormula)		

		return True


	def createNodeIfNotAtomic(self,formula):
		
		if self.isAtomicExpression(formula):
			return formula
			
		node = self.createChild(formula)
		return node.name
		
		
	def isAtomicExpression(self,formula):
		# TODO: handle arrays
		
		formula = formula.replace(" ","")
		
		insideApostrophe = 0
		insideQuotation = 0
		for i in range(0,len(formula)):
			c = formula[i]
					
			if not c in "_0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
				return False

		return True
		
		
	def applyIdentity(self):

		for node in Node.nodeList:
			print(node.name,node.refCount)


		print("-- before:")
		self.generateInstructions()
		print(self.render())

		print("-- after:")
		self.generateInstructions()
		print(self.render())

		print("--")
		

	def generateInstructions(self):
		
		Node.instructionList = []

		self.generateChildren()
		self.generateNode()


	def generateChildren(self):

		for child in self.children:
			child.generateInstructions()


	def createInstruction(self,name,left,op,right):

		instruction = Instruction(name,left,op,right)
		Node.instructionList.append(instruction)


	def generateNode(self):

		if self.text.strip() == "": return

		if self.operator == "-": 
			self.generateNeg()		
			return
			
		a = self.text.split(self.operator)
		self.leftOperand = a[0]
		self.rightOperand = a[1]
		
		self.operator = self.operator.replace("<","<<")
		self.operator = self.operator.replace(">",">>")
		
		self.createInstruction(
			self.name,
			self.leftOperand,
			self.operator,
			self.rightOperand
		)


	def generateNeg(self):
		
		a = self.text.split("-")
		left = a[0].strip()
		right = a[1].strip()

		self.createInstruction(
			self.name,
			"",
			self.operator,
			right
		)

		self.createInstruction(
			self.name,
			self.name,
			"+",
			left
		)
				

	def render(self):

		result = ""
		for instr in Node.instructionList:
			result += instr.render() + "\n"

		return result
		

	def dump(self):

		print(self.name)
		
		print(" text: " 
			+ "\"" 
			+ self.text.replace("\n","\", \"") 
			+ "\""
		)

		if self.parent is not None:
			pnam = self.parent.name
		else:
			pnam = "n.a."
		print(" parent: " + pnam)
		
		print(" left: " + self.leftOperand)
		print(" operator: " + self.operator)
		print(" right: " + self.rightOperand)
		
		for child in self.children: child.dump()


if __name__ == '__main__':

	try: 

		root = Node()
		root.processFile( sys.argv[1] )
		#print( root.render() ,end="")
		if False:
			print("--")
			root.dump()
	
	except KeyboardInterrupt:
		print(" - interrupted")
