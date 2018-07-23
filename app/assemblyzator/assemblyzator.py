#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True

import os


class Node:

	nextId = 0


	def __init__(self,parent = None,text = None):

		self.children = []

		self.parent = parent

		self.id = Node.nextId
		Node.nextId += 1
		
		self.text = text


	def getName(self):
		if self.id == 0: return "root"
		return "var" + str(self.id)


	def createChild(self,text):
		
		child = Node(self,text)
		return child
		

	def processRoot(self,fnam):
		
		self.load(fnam)
		self.normalize()
		self.splitStatements()
		self.process()


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
		
		if self.text.count(";") < 2: return
		
		statements = self.text.split(";")
		for stat in statements:
			if stat == "": continue
			child = self.createChild(stat)
			self.children.append(child)
		
		self.text = ""
		

	def process(self):

		pass



	def dump(self):

		print(self.getName())
		
		print("  formula: " 
			+ "\"" 
			+ self.text.replace("\n","\", \"") 
			+ "\""
		)

		if self.parent is not None:
			pnam = self.parent.getName()
		else:
			pnam = "n.a."
		print("   parent: " + pnam)
		
		
		for child in self.children: child.dump()


if __name__ == '__main__':

	try: 
		root = Node()
		root.processRoot(sys.argv[1])
		print("---- dump ----")
		root.dump()
		print("==============")
	
	except KeyboardInterrupt:
		print(" - interrupted")
