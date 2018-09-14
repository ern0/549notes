#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True
import os
from collections import OrderedDict
from operator import itemgetter

import data
from note import Note
from render import Render


class Sheet:


	def main(self):

		self.createScore()
		self.renderIntro()

		diffs = (1,5,10,)
		diffs = (1,)
		for diff in diffs:
			diffId = "diff" + str(diff)
			
			self.calcSimpleDiff("raw",diffId,diff)
			self.render.renderScore("raw and " + diffId,("text","raw",diffId,))
			
			#self.calcHistogram("raw")

		#...

		self.saveFile()


	def __init__(self):
		self.render = Render(self)


	def createScore(self):

		self.notes = []

		for noteText in data.part1Text:
			note = Note(self)
			note.set("text",noteText)
			self.notes.append(note)

		self.splitPoint = len(self.notes)

		for noteText in data.part2Text:
			note = Note(self)
			note.set("text",noteText)
			self.notes.append(note)


	def saveFile(self):

		with open(sys.argv[1],"w+") as f:
			for line in self.render.lines:
				f.write(line + "\n")


	def renderIntro(self):

		self.render.renderHeader("generated file, do not edit","*",False)
		self.render.renderLine()

		self.render.renderComment("Transformed score data and analysis of")
		self.render.renderComment(" J.S.Bach: Prelude in C major, BWV 846")
		self.render.renderComment(" from the Prelude and Fugue in C major, BWV 846")
		self.render.renderComment(" from Book I of The Well-Tempered Clavier")
		self.render.renderComment("for PC-DOS 256-byte intro")
		self.render.renderLine()

		self.render.renderComment(
			"part1: A B C D E [A B C] - " + 
			str( int(len(data.part1Text) / 5) )  + 
			" lines" 
		)
		self.render.renderComment(
			"part2: A B C D E  F G H  -  " + 
			str( int(len(data.part2Text) / 8) ) + 
			" lines"
		)
		self.render.renderComment(
			"coda: " +
			str( int(len(data.codaText))) + 
			"-notes chord"
		)
		self.render.renderLine()


	def calcSimpleDiff(self,sourceType,targetType,distance):

		for i in range(0,len(self.notes)):
			note = self.notes[i]

			if i < distance:
				diff = None
			else:
				diff = note.get(sourceType)
				diff -= self.notes[i - distance].get(sourceType)

			note.set(targetType,diff)








	def countOccurrences(self,values):

		result = {}
		for value in values:

			if value is None: continue

			try: result[value] += 1
			except: result[value] = 1

		return result


	def renderHistogram(self,header,data,orderBy = "value",noteType = "raw"):

		occurrences = self.countOccurrences(data)

		self.renderHeader(header + " (" + str(len(occurrences)) + " values)")

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
				line += self.convertRawToNote(value)
				line += ":"
				line += self.renderFormatted(value)
				line += " "
			else:
				line += self.renderFormatted(value,noteTyope)
				line += ":"

			line += str(count).rjust(3)
			line += " "
			line += "#" * count
			self.renderComment(line)

		self.renderLine()














	def calcMapping(self,rawNotes):

		mapIdByRawNotes = {}
		rawNoteByMapIds = {}
		mapped = []

		mapId = 0
		for rawNote in sorted(rawNotes):
			if rawNote in mapIdByRawNotes: continue

			rawNoteByMapIds[mapId] = rawNote
			mapIdByRawNotes[rawNote] = mapId
			mapId += 1

		for rawNote in rawNotes:
			mapId = mapIdByRawNotes[rawNote]
			mapped.append(mapId)

		return ( mapped,mapIdByRawNotes,rawNoteByMapIds )


########################################################################


	def renderBasics(self):

		self.renderHistogram(
			"combo raw note histogram",
			self.comboRawNotes,
			orderBy = "value",
			noteType = "raw"
		)

		self.renderHistogram(
			"combo raw note histogram",
			self.comboRawNotes,
			orderBy = "count",
			noteType = "raw"
		)

		self.renderNotes(
			"raw notes",
			(self.comboRawNotes,),
			("raw",),
			isComment = True
		)


	def renderDiffs(self,diffs):

		for diff in diffs:

			self.comboDiffNotes = self.calcDiff(self.comboRawNotes,diff)

			self.renderNotes(
				"combo diff-" + str(diff) + " notes",
				(self.comboRawNotes,self.comboDiffNotes),
				noteTypes = ("text","signed",),
				isComment = True
			)

			self.renderHistogram(
				"combo diff-" + str(diff) + " note histogram",
				self.comboDiffNotes,orderBy = "value",
				isNote = False
			)

			self.renderHistogram(
				"combo diff-" + str(diff) + " note histogram",
				self.comboDiffNotes,
				orderBy = "count",
				isNote = False
			)


########################################################################

if __name__ == '__main__':

	try:

		sheet = Sheet()
		sheet.main()

	except KeyboardInterrupt:
		print(" - interrupted")
