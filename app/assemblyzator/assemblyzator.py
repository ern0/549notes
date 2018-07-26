#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True

import os


class Node:

	nextId = 0


	def __init__(self,parent = None,text = None):

		self.children = []
		self.parent = parent

		if Node.nextId == 0:
			self.name = "root"
		else:
			self.name = "var" + str(Node.nextId)
		Node.nextId += 1
		
		self.text = text


	def createChild(self,text):
		
		child = Node(self,text)
		self.children.append(child)
		return child


	def processFile(self,fnam):
		
		self.load(fnam)
		return self.processRoot()
		
	
	def processString(self,text):
		
		self.text = text
		return self.processRoot()
		

	def processRoot(self):
		
		self.normalize()

		print(self.text) ##
		print("--")	##

		self.splitStatements()
		self.process()
		
		self.dump() ##
		print("--")	##
		
		return self.render()


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
			self.process()
			return
		
		statements = self.text.split(";")
		self.text = ""

		for stat in statements:
			if stat == "": continue

			child = self.createChild(stat)
			self.children.append(child)

			child.process()
				

	def process(self):
		
		self.procNode()
		self.procChildren()
		
		
	def procNode(self):
		
		while True:

			if self.procAssignment(): break
			if self.procPairOperator( ("|",) ): break
			if self.procPairOperator( ("^",) ): break
			if self.procPairOperator( ("&",) ): break
			if self.procPairOperator( ("+","-") ): break
			if self.procPairOperator( ("*","/","%") ): break

			if self.procParenthesis(): break

			break


	def procChildren(self):
		
		for child in self.children:
			child.process()


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


	def procAssignment(self):
		
		p = self.findSplitPoint( ("=",) )
		if p is None: return False
		
		self.name = self.text[0:p].strip()
		self.text = self.text[(1 + p):].strip()
		
		return True


	def procPairOperator(self,operatorList):

		p = self.findSplitPoint(operatorList)
		if p is None: return False

		leftFormula = self.text[0:p].strip()
		leftReplacement = self.createNodeIfNotAtomic(leftFormula)

		operator = self.text[p]

		rightFormula = self.text[(1 + p):].strip()
		rightReplacement = self.createNodeIfNotAtomic(rightFormula)		

		self.text = (leftReplacement + " " + operator + " " + rightReplacement)


	def createNodeIfNotAtomic(self,formula):
		
		if self.isAtomicExpression(formula):
			return formula
			
		node = self.createChild(formula)
		return node.name
		
		
	def isAtomicExpression(self,formula):
		# TODO: handle quotation marks
		
		formula = formula.replace(" ","")
		
		for i in range(0,len(formula)):
			c = formula[i]
		
			if not c in "_0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
				return False

		return True
		
		
	def procParenthesis(self):
		#TODO
		return  False


	def render(self):

		result = self.renderChildren()
		result += self.renderNode()
		
		return result
		
	
	def renderChildren(self):
		
		result = ""
		for child in self.children:
			result += child.render()

		return result


	def renderNode(self):
		
		if self.text == "": return ""		
		return self.name + " = " + self.text + "\n"


	def dump(self):

		print(self.name)
		
		print("  formula: " 
			+ "\"" 
			+ self.text.replace("\n","\", \"") 
			+ "\""
		)

		if self.parent is not None:
			pnam = self.parent.name
		else:
			pnam = "n.a."
		print("   parent: " + pnam)
		
		
		for child in self.children: child.dump()


if __name__ == '__main__':

	try: 

		root = Node()
		result = root.processFile(sys.argv[1])
		print(result)

		if False:
			print("---- dump ----")
			root.dump()
			print("==============")
	
	except KeyboardInterrupt:
		print(" - interrupted")
