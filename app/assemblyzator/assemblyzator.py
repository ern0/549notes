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

		self.children = []
		self.parent = parent
		Node.nodeList.append(self)

		if Node.nextId == 0:
			self.name = "root"
		else:
			self.name = "var" + str(Node.nextId)
		Node.nextId += 1

		self.text = text
		
		self.leftOperand = ""
		self.operator = ""
		self.rightOperand = ""


	def createChild(self,text):

		for child in self.children:
			if child.text == text: return child
			
		child = Node(self,text)
		self.children.append(child)
		return child


	def processFile(self,fnam):
		
		self.load(fnam)
		self.processRoot()
		
	
	def processString(self,text):
		
		self.text = text
		self.processRoot()
		

	def processRoot(self):
		
		self.normalize()
		self.splitStatements()
		self.parse()
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
			self.children.append(child)

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
			+ " " + self.operator + " "
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

		try:
			if (text[0] != '('): return text
			if (text[-1] != ')'): return text
		except IndexError: return text
				
		insideApostrophe = False
		insideQuotation = False
		parenDepth = 0
		parenOv = False
		
		for i in range(1,len(text) - 1):
			c = text[i]
			
			if insideApostrophe:
				if c == "'": insideApostrophe = False
				text += c
				continue
				
			if insideQuotation:
				if c == "\"": insideQuotation = False				
				text += c
				continue
				
			if insideApostrophe or insideQuotation: continue
						
			if c == "'": 
				insideApostrophe = True
				continue
				
			if c == "\"": 
				insideQuotation = True
				continue				
			
			if c == "(": parenDepth += 1
			if c == ")": parenDepth -= 1
			if parenDepth < 0:
				parenOv = True
				break
		
		if not parenOv: text = text[1:-1]
		
		return text


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
		

	def generateInstructions(self):
		
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
		print( root.render() ,end="")
		if False:
			print("--")
			root.dump()
	
	except KeyboardInterrupt:
		print(" - interrupted")
