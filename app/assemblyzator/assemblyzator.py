#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True

import os


class Node:

	lastId = 0


	def __init__(self,parent):

		self.parent = parent

		Node.lastId += 1
		self.id = Node.lastId


	def getName(self):
		return "var" + str(self.lastId)


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


	def processRoot(self,fnam):

		self.load(fnam)
		self.mormalize()
		self.process()


	def load(self,fnam):
		with open(fnam,"r") as file:
			self.text = file.read()


	def mormalize(self):
		
		self.text = self.text.replace(";","\n")
		raw = self.text.split("\n")
		self.text = ""

		for line in raw:
			if "//" in line: line = line.split("//")[0]
			line = line.strip()
			if line == "": continue
			self.text = self.text + line


	def process(self):

		pass



if __name__ == '__main__':

	try: 
		root = Node(None)
		root.processRoot(sys.argv[1])
		print("---- dump ----")
		root.dump()
		print("==============")
	
	except KeyboardInterrupt:
		print(" - interrupted")