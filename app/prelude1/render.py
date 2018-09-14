#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True


class Render:

	WIDTH = 78


	def __init__(self,sheet):
		self.sheet = sheet
		self.lines = []


	def saveFile(self):

		with open(sys.argv[1],"w+") as f:
			for line in self.lines:
				f.write(line + "\n")


	def renderLine(self,line = ""):

		self.lines.append(line)


	def renderScore(self,header,typeTuple,isComment = True):

		self.renderHeader(header)

		notes = self.sheet.notes
		splitPoint = self.sheet.splitPoint

		itemsInLine = 5
		line = None

		for i in range (0,len(notes)):
			note = notes[i]

			if i == splitPoint: itemsInLine = 8

			if i % itemsInLine == 0 and line is not None:
				if itemsInLine == 5 and isComment: line += "  (...)"
				self.renderLine(line)
				line = None

			if line is None:
				if isComment: line = ";"
				else: line = "  db "

			if isComment:
				if i % itemsInLine != 0: line += " "
				line += " "
				line += note.render(typeTuple,isComment)

			else:
				if i % itemsInLine != itemsInLine - 1:
					line += ","
					line += note.render(typeTuple[0],isComment)

		self.renderLine()


	def renderConst(self,name,value,comment):

		self.renderLine(
			"score_"
			+ name
			+ (7 - len(name)) * " "
			+ " = "
			+ str(value)
			+ (5 - len(str(value))) * " "
			+ " ; "
			+ comment
		)


	def renderComment(self,*kwargs):

		line = ""
		for arg in kwargs:
			if line != "": line += " "
			line += str(arg)

		self.renderLine("; " + line)


	def renderHeader(self,text,char = "-",emptyLine = True):

		line = char * 4
		line += " "
		line += text
		line += " "
		line += (self.WIDTH - len(line)) * char

		self.renderComment(line)
		if emptyLine: self.renderComment()
