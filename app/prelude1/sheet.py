#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True
import os
from collections import OrderedDict
from operator import itemgetter

class Prelude1:

	WIDTH = 60

########################################################################


	def fillTextData(self):

		self.part1Text = [

			"c3","e3","g3","c4","e4",
			"c3","d3","a3","d4","f4",
			"h2","d3","g3","d4","f4",
			"c3","e3","g3","c4","e4",

			"c3","e3","a3","e4","a4",
			"c3","d3","fis3","a3","d4",
			"h2","d3","g3","d4","g4",
			"h2","c4","e3","g3","c4",

			"a2","c3","e3","g3","c4",
			"d2","a2","d3","fis3","c4",
			"g2","h2","d3","g3","h3",
			"g2","ais2","e3","g3","cis4",

			"f2","a2","d3","a3","d4",
			"f2","gis2","d3","f3","h3",
			"e2","g2","c3","g3","c4",
			"e2","f2","a2","c3","f3",

			"d2","f2","a2","c3","f3",
			"d2","f2","a2","c3","f3",
			"g1","d2","g2","h2","f3",
			"c2","e2","g2","c3","e3",

			"c2","g2","ais2","c3","e3",
			"f1","f2","a2","c3","e3",
			"fis1","c2","a2","c3","e3",
			"gis1","f2","h2","c3","d3",

			"g1","f2","g2","h2","d3",
			"g1","e2","g2","c3","e3",
			"g1","d2","g2","c3","f3",
			"g1","d2","g2","h3","f3",

			"g1","dis2","a2","c3","fis3",
			"g1","e2","g2","c3","g3",
			"g1","d2","g2","c3","f3",
			"g1","d2","g2","h3","f3"

		]

		self.part2Text = [

			"c1","c2","g2","ais2","e3","g2","ais2","g2",
			"c1","c2","f2","a2","c3","f3","c3","a2",
			"c3","a2","f2","a2","f2","d2","f2","d2",
			"c1","h1","g3","h3","d4","f4","d4","h3",
			"d4","h3","g3","h3","d3","f3","e3","d3",

		]

		self.codaText = [
			"c1","c2","e3","g3","c4"
		]


	def combineTextData(self):

		self.comboText = []

		for note in self.part1Text:
			self.comboText.append(note)

		for note in self.part2Text:
			self.comboText.append(note)


########################################################################


	def __init__(self):
		self.lines = []


	def saveFile(self):

		with open(sys.argv[1],"w+") as f:
			for line in self.lines:
				f.write(line + "\n")


	def renderLine(self,line = ""):

		self.lines.append(line)


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


	def renderCommentHeader(self,text,char = "-",emptyLine = True):

		line = char * 4
		line += " "
		line += text
		line += " "
		line += (self.WIDTH - len(line)) * char

		self.renderComment(line)
		if emptyLine: self.renderComment()


	def renderNotes(self,datas,isComment = True):

		itemsInLine = 5
		line = None
		lineCounter = 0

		for i in range(0,self.comboLength):

			if i % itemsInLine == 0 and line is not None:

				if itemsInLine == 5 and isComment: line += " (...)"
				self.renderLine(line)
				line = None

				lineCounter += 1
				if lineCounter % 4 == 0 and lineCounter < 9 * 4: self.renderComment()

			if line is None:

				if isComment: line = "; "
				else: line = "    db "

			line += self.renderNote(datas,i,isComment)

			if i == self.part1Length: itemsInLine = 8



	def renderNote(self,datas,index,isComment):

		item = ""

		if isComment:
			noteText = self.comboText[index]
			if len(noteText) < 4: noteText = " " + noteText + " "
			item += noteText + " "

		return item


	def convertTextToRaw(self,textArray):

		result = []
		for text in textArray:

			note = text[:-1]
			octave = text[-1:]

			value = (int(octave) - 1) * 12
			value += self.convertNoteToRaw(note)

			result.append(value)

		return result


	def convertNoteToRaw(self,note):

		if note == "c": return 0
		elif note == "cis": return 1
		elif note == "d": return 2
		elif note == "dis": return 3
		elif note == "e": return 4
		elif note == "f": return 5
		elif note == "fis": return 6
		elif note == "g": return 7
		elif note == "gis": return 8
		elif note == "a": return 9
		elif note == "ais": return 10
		elif note == "h": return 11

		print("bad note: " + note)
		quit()


	def countOccurrences(self,values):

		result = {}
		for value in values:
			try: result[value] += 1
			except: result[value] = 1

		return result


	def renderHistogram(self,data,orderBy = "value"):

		occurrences = self.countOccurrences(data)

		if orderBy == "value":
			ig = 0
			rv = False
		elif orderBy == "count":
			ig = 1
			rv = True
		else:
			quit()

		occurrences = OrderedDict(
			sorted(occurrences.items(),
			key = itemgetter(ig),
			reverse = rv)
		)

		for value in occurrences:
			count = occurrences[value]

			line = str(value).rjust(2)
			line += ":"
			line += str(count).rjust(3)
			line += "  "
			line += "#" * count
			self.renderComment(line)


	def calcDiff(self,rawNotes,distance):

		diffs = []

		for i in range(0,len(rawNotes)):
			if i < distance: continue

			diff = rawNotes[i] - rawNotes[i - distance]
			diffs.append(diff)

		return diffs


########################################################################


	def renderConstants(self):

		self.renderComment("Transformed score data and analysis of")
		self.renderComment(" J.S.Bach: Prelude in C major, BWV 846")
		self.renderComment(" from the Prelude and Fugue in C major, BWV 846")
		self.renderComment(" from Book I of The Well-Tempered Clavier")
		self.renderComment("for PC-DOS 256-byte intro")
		self.renderLine()

		self.renderComment("part1 (p1): A B C D E [A B C] 5x32 notes")
		self.renderComment("part2 (p2): A B C D E  F G H  8x5 notes")
		self.renderComment("combo (c): part1+part2")
		self.renderComment("coda: last 5 notes")
		self.renderLine()

		self.renderConst("p1_data",self.part1Length,"part1 number of data notes")
		self.renderConst("p1_eff",self.part1EffectiveLength,"part1 number of effective notes")

		self.renderConst("p2_data",self.part2Length,"part2 number of notes")

		self.renderConst("c_data",self.comboLength,"combo number of data notes")
		self.renderConst("c_eff",self.comboEffectiveLength,"combo number of effective notes")


	def calcStuff(self):

		self.part1RawNotes = self.convertTextToRaw(self.part1Text)
		self.part2RawNotes = self.convertTextToRaw(self.part2Text)
		self.codaRawNotes = self.convertTextToRaw(self.codaText)
		self.comboRawNotes = self.convertTextToRaw(self.comboText)

		self.part1Length = len(self.part1RawNotes)
		self.part1EffectiveLength = int(self.part1Length / 5) * 8
		self.part2Length = len(self.part2RawNotes)
		self.comboLength = self.part1Length + self.part2Length
		self.comboEffectiveLength = self.part1EffectiveLength + self.part2Length

		#...



	def renderStuff(self):

		self.renderCommentHeader("generated file, do not edit","*",False)
		self.renderLine()

		self.renderConstants()
		self.renderLine()

		self.renderComment(
			"raw note set:"
			,len( self.countOccurrences(self.comboRawNotes) )
		)
		self.renderLine()

		self.renderCommentHeader("combo raw note histogram")
		self.renderHistogram(self.comboRawNotes,orderBy = "value")
		self.renderLine()

		self.renderCommentHeader("combo raw note histogram")
		self.renderHistogram(self.comboRawNotes,orderBy = "count")
		self.renderLine()

		self.renderHeader("raw notes")
		self.renderNotes(
			(self.comboRawNotes,self.comboRawNotes),
			isComment = True
		)

		#...



	def main(self):

		self.fillTextData()
		self.combineTextData()

		self.calcStuff()
		self.renderStuff()
		self.saveFile()


########################################################################



if __name__ == '__main__':

	try:

		sheet = Prelude1()
		sheet.main()

	except KeyboardInterrupt:
		print(" - interrupted")
