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
		
		self.const = ""
		self.leftOperand = ""
		self.operator = ""
		self.rightOperand = ""
		self.text = text


	def getRepresentation(self):

		if self.const != "": return self.const
		return self.name


	def processFile(self,fnam):
		
		with open(fnam,"r") as file:
			fileContent = file.read()
		self.processString(fileContent)
		
	
	def processString(self,text):
		
		self.text = self.cleanupFormula(text)
		self.processRoot()
		

	def processRoot(self):
		
		self.normalizeFullText()
		self.splitStatements()
		self.parse()
		self.applyIdentity()
		self.generateRootInstructions()


	def normalizeFullText(self):
		
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
			self.parseSingleLine()
		else:
			self.parseMultiLine()


	def parseSingleLine(self):

		self.text = self.text.replace(";","")
		if self.text == "":	return
		
		self.parse()


	def parseMultiLine(self):

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

		self.text = self.cleanupFormula(self.text)

		p = self.findSplitPoint( ("=",) )
		if p is not None: 
			self.name = self.text[0:p].strip()
			self.text = self.text[(1 + p):].strip()

		if self.findPairOperator():
			self.parsePairNode()
			return

		if self.findArrayOperator():
			self.parseArrayNode()
			return
			
			
	def parsePairNode(self):
		
		if self.isConstantFormula(self.leftOperand) and self.isConstantFormula(self.rightOperand):			
			self.const = self.calculateConstFormula(
				self.leftOperand
				+ self.operator
				+ self.rightOperand
			)
			if self.parent is not None:
				if self.parent.leftOperand == self.name:
					self.parent.leftOperand = self.const
				if self.parent.rightOperand == self.name:
					self.parent.rightOperand = self.const
				self.parent.text = self.parent.leftOperand + self.parent.operator + self.parent.rightOperand
			return

		if not self.isAtomicFormula(self.leftOperand):
			node = self.createChild(self.leftOperand)
			self.leftOperand = node.getRepresentation()
		
		if not self.isAtomicFormula(self.rightOperand):
			node = self.createChild(self.rightOperand)
			self.rightOperand = node.getRepresentation()		
		
		self.text = self.leftOperand + self.operator + self.rightOperand


	def parseArrayNode(self):
		pass
		

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


	def findPairOperator(self):
		
		if self.findSpecifiedPairOperators( ("^",) ): return True
		if self.findSpecifiedPairOperators( ("&",) ): return True
		if self.findSpecifiedPairOperators( ("|",) ): return True
		if self.findSpecifiedPairOperators( ("<",">") ): return True
		if self.findSpecifiedPairOperators( ("+","-") ): return True
		if self.findSpecifiedPairOperators( ("*","/","%") ): return True
		
		return False

	
	def findSpecifiedPairOperators(self,operatorList):

		p = self.findSplitPoint(operatorList)
		if p is None: return False

		self.leftOperand = self.text[0:p].strip()
		self.operator = self.text[p]
		self.rightOperand = self.text[(1 + p):].strip()

		return True
		

	def findArrayOperator(self):
		pass
	

	def parseChildren(self):
		
		for child in self.children:
			child.parse()


	def findSplitPoint(self,separatorList):
		# TODO: handle quotation and aphostrophe

		indent = 0
		square = 0
		for i in range(0,len(self.text)):
			c = self.text[i]

			if c == "(": 
				indent += 1
				continue

			if c == ")":
				indent -= 1
				continue
				
			if c == "[":
				square += 1
				continue
			
			if c == "]":
				square -= 1
				continue

			if (indent > 0) or (square > 0): 
				continue

			if c in separatorList:
				return i

		return None


	def isAtomicFormula(self,formula):
		return self.isContainsOnly("_0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",formula)


	def isConstantFormula(self,formula):
		# TODO: handle negatives
		return self.isContainsOnly("0123456789.+-*/%^&|<>",formula)


	def isContainsOnly(self,charsAllowed,formula):		
		# TODO: handle quotation and apostrophe
		# TODO: handle arrays

		formula = formula.replace(" ","")
		
		insideApostrophe = 0
		insideQuotation = 0
		for i in range(0,len(formula)):
			c = formula[i]
			if not c in charsAllowed: return False

		return True


	def cleanupFormula(self,text):

		if text is None: return
		
		text = text.strip()
		text = text.replace("<<","<")
		text = text.replace(">>",">")
				
		insideApostrophe = False
		insideQuotation = False
		squareDepth = 0
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

			if c == "[": squareDepth += 1
				
			if squareDepth > 0:
				result += c
				if c == "]": squareDepth -= 1
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


	def calculateConstFormula(self,text):
		# TODO: some error checking
		return str( eval(text) )

		
	def applyIdentity(self):

		return ###############################

		for node in Node.nodeList:
			print(node.name,node.refCount)

		print("-- before:")
		self.generateInstructions()
		print(self.render())

		print("-- after:")
		self.generateInstructions()
		print(self.render())

		print("--")
		

	def generateRootInstructions(self):

		Node.instructionList = []
		self.generateInstructions()


	def generateInstructions(self):
		
		self.generateChildren()
		self.generateNode()


	def generateChildren(self):

		for child in self.children:
			child.generateInstructions()


	def generateNode(self):

		if self.text.strip() == "": return

		if self.const != "": return

		if self.operator == "-" and self.rightOperand != "0": 
			self.generateNeg()		
			return

		self.operator = self.operator.replace("<","<<")
		self.operator = self.operator.replace(">",">>")
		
		self.createInstruction(
			self.name,
			self.leftOperand,
			self.operator,
			self.rightOperand
		)


	def createInstruction(self,name,left,op,right):

		instruction = Instruction(name,left,op,right)
		Node.instructionList.append(instruction)


	def generateNeg(self):
		
		self.createInstruction(
			self.name,
			"",
			self.operator,
			self.rightOperand
		)

		self.createInstruction(
			self.name,
			self.name,
			"+",
			self.leftOperand
		)
				

	def render(self):

		result = ""
		for instr in Node.instructionList:
			result += instr.render() + "\n"

		return result
		

	def quote(self,text):
		return "\"" + self.text.replace("\n","\", \"") + "\""


	def dump(self):

		print(self.name)

		if self.parent is not None:
			pnam = self.parent.name
		else:
			pnam = "n.a."
		print(" parent: " + pnam)
		
		if self.const != "":
			print(" const: " + self.const)
		else:
			print(" left: " + self.leftOperand)
			print(" operator: " + self.operator)
			print(" right: " + self.rightOperand)
		
		for child in self.children: child.dump()


if __name__ == '__main__':

	try: 

		root = Node()
		root.processFile( sys.argv[1] )
		root.dump()
		#print("--")
		#print( root.render() ,end="")
		#print(root.cleanupFormula("[2dfs]"))

	except KeyboardInterrupt:
		print(" - interrupted")
