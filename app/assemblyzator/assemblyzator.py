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
		return child
		

	def processRoot(self,fnam):
		
		self.load(fnam)
		self.normalize()
		self.splitStatements()
		self.process()
		self.render()


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
		
		if self.findOpAssignment(): return
		if self.findOpPlusMinus(): return
		

	def findOpAssignment(self):
		
		p = self.findSplitPoint( ("=",) )
		if p is None: return False
		
		self.name = self.text[0:p].strip()
		self.text = self.text[(1 + p):].strip()
		
		return True


	def findOpPlusMinus(self):

		p = self.findSplitPoint( ("+","-") )
		if p is None: return False


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


	def render(self):

		if False:
			return self.dump()

		for child in self.children:
			child.render()

		if self.text != "": 
			print(self.name + " = " + self.text)


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
		root.processRoot(sys.argv[1])

		if False:
			print("---- dump ----")
			root.dump()
			print("==============")
	
	except KeyboardInterrupt:
		print(" - interrupted")
