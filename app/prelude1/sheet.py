#!/usr/bin/env python3
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

			"c-3","e-3","g-3","c-4","e-4",
			"c-3","d-3","a-3","d-4","f-4",
			"h-2","d-3","g-3","d-4","f-4",
			"c-3","e-3","g-3","c-4","e-4",

			"c-3","e-3","a-3","e-4","a-4",
			"c-3","d-3","f#3","a-3","d-4",
			"h-2","d-3","g-3","d-4","g-4",
			"h-2","c-4","e-3","g-3","c-4",

			"a-2","c-3","e-3","g-3","c-4",
			"d-2","a-2","d-3","f#3","c-4",
			"g-2","h-2","d-3","g-3","h-3",
			"g-2","a#2","e-3","g-3","c#4",

			"f-2","a-2","d-3","a-3","d-4",
			"f-2","g#2","d-3","f-3","h-3",
			"e-2","g-2","c-3","g-3","c-4",
			"e-2","f-2","a-2","c-3","f-3",

			"d-2","f-2","a-2","c-3","f-3",
			"d-2","f-2","a-2","c-3","f-3",
			"g-1","d-2","g-2","h-2","f-3",
			"c-2","e-2","g-2","c-3","e-3",

			"c-2","g-2","a#2","c-3","e-3",
			"f-1","f-2","a-2","c-3","e-3",
			"f#1","c-2","a-2","c-3","e-3",
			"g#1","f-2","h-2","c-3","d-3",

			"g-1","f-2","g-2","h-2","d-3",
			"g-1","e-2","g-2","c-3","e-3",
			"g-1","d-2","g-2","c-3","f-3",
			"g-1","d-2","g-2","h-3","f-3",

			"g-1","d#2","a-2","c-3","f#3",
			"g-1","e-2","g-2","c-3","g-3",
			"g-1","d-2","g-2","c-3","f-3",
			"g-1","d-2","g-2","h-3","f-3",

			"c-1","c-2","g-2","a#2","e-3",

		]

		self.part2Text = [

			"c-1","c-2","f-2","a-2","c-3","f-3","c-3","a-2",
			"c-3","a-2","f-2","a-2","f-2","d-2","f-2","d-2",
			"c-1","h-1","g-3","h-3","d-4","f-4","d-4","h-3",
			"d-4","h-3","g-3","h-3","d-3","f-3","e-3","d-3",

		]

		self.codaText = [
			"c-1","c-2","e-3","g-3","c-4"
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


	def renderHeader(self,text,char = "-",emptyLine = True):

		line = char * 4
		line += " "
		line += text
		line += " "
		line += (self.WIDTH - len(line)) * char

		self.renderComment(line)
		if emptyLine: self.renderComment()


	def renderNotes(self,datas,isComment = True,isSigned = None):

		itemsInLine = 5
		line = None

		for i in range(0,self.comboLength):

			if i == self.part1Length: itemsInLine = 8

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

			line += self.renderNote(datas,i,isComment,isSigned)

			if not isComment:
				if i % itemsInLine != itemsInLine - 1:
					line += ","


	def renderNote(self,datas,index,isComment,isSigned):

		note = ""

		if isComment: note += self.comboText[index]

		tupleIndex = 0
		for data in datas:
			value = data[index]

			try: isNoteSigned = isSigned[tupleIndex]
			except: isNoteSigned = False

			if isComment: note += ":"
			note += self.renderFormatted(value,isComment,isNoteSigned)

			if not isComment: break
			tupleIndex += 1

		return note


	def renderFormatted(self,value,isComment = True,isSigned = False):

		if value is None:
			if isSigned: return "N/A"
			else: return "**"

		formatted = ""

		if isSigned:
			if value == 0: formatted = "="
			elif value > 0: formatted = "+"
			else:
				formatted = "-"
				value = -value

		if isComment and value < 10: value = "0" + str(value)
		else: value = str(value)

		formatted += value

		return formatted


	def convertTextToRaw(self,textArray):

		result = []
		for text in textArray:

			note = text[0:2]
			octave = text[-1:]

			value = (int(octave) - 1) * 12
			value += self.convertNoteToRaw(note)

			result.append(value)

		return result


	def convertNoteToRaw(self,note):

		if note == "c-": return 0
		elif note == "c#": return 1
		elif note == "d-": return 2
		elif note == "d#": return 3
		elif note == "e-": return 4
		elif note == "f-": return 5
		elif note == "f#": return 6
		elif note == "g-": return 7
		elif note == "g#": return 8
		elif note == "a-": return 9
		elif note == "a#": return 10
		elif note == "h-": return 11

		print("bad note: " + note)
		quit()


	def countOccurrences(self,values):

		result = {}
		for value in values:
			try: result[value] += 1
			except: result[value] = 1

		return result


	def renderHistogram(self,data,orderBy = "value",isNote = False):

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
			line = ""

			if isNote:
				line += self.comboText[value]
				line += ":"
				line += self.renderFormatted(value) 
				line += " "
			else:
				line += self.renderFormatted(value,isSigned = True) 
				line += ":"

			line += str(count).rjust(3)
			line += " "
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

		p1 = str( int(self.part1Length / 5) )
		p2 = str( int(self.part2Length / 8) )
		self.renderComment("part1: A B C D E [A B C] - " + p1 + " lines" )
		self.renderComment("part2: A B C D E  F G H  -  " + p2 + " lines")
		self.renderComment("combo: part1+part2")
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

		self.renderHeader("generated file, do not edit","*",False)
		self.renderLine()

		self.renderConstants()
		self.renderLine()

		self.renderComment(
			"number of different raw notes:"
			,len( self.countOccurrences(self.comboRawNotes) )
		)
		self.renderLine()

		self.renderHeader("combo raw note histogram")
		self.renderHistogram(self.comboRawNotes,orderBy = "value",isNote = True)
		self.renderLine()

		self.renderHeader("combo raw note histogram")
		self.renderHistogram(self.comboRawNotes,orderBy = "count",isNote = True)
		self.renderLine()

		self.comboRawNotes[0] = None
		self.renderHeader("raw notes")
		self.renderNotes(
			(self.comboRawNotes,self.comboRawNotes),
			isSigned = (False,True),
			isComment = True,
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
