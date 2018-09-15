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
		self.calcMapping()
		self.renderIntro()

		for rm in ("raw","mapped",):

			self.render.renderScore(rm,("text",rm,))

			self.renderHistogram(rm,orderBy = "value")
			self.renderHistogram(rm,orderBy = "count")

			for diff in (1,5,10,"mixed/1/5",):
				diffId = rm + "-diff-" + str(diff)
				
				self.calcDiff(rm,diffId,diff)
				self.render.renderScore(diffId,("text",rm,diffId,))
				
				self.renderHistogram(diffId,orderBy = "value")
				self.renderHistogram(diffId,orderBy = "count")

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


	def calcDiff(self,sourceType,targetType,distance):
		
		try: d = int(distance)
		except: d = 0

		if d > 0: 
			self.calcSimpleDiff(sourceType,targetType,distance)
		elif distance == "mixed/1/5": 
			self.calcMixed1x5xDiff(sourceType,targetType)
		else:
			print("invalid diff type: " + distance)
			quit()


	def calcSimpleDiff(self,sourceType,targetType,distance):

		for i in range(0,len(self.notes)):
			note = self.notes[i]

			if i < distance:
				diff = None
			else:
				diff = note.get(sourceType)
				diff -= self.notes[i - distance].get(sourceType)

			note.set(targetType,diff)


	def calcMixed1x5xDiff(self,sourceType,targetType):

		for i in range(0,len(self.notes)):
			note = self.notes[i]

			if i == 0:
				diff = None

			else:

				if i % 5 == 0: distance = 5
				else: distance = 1

				diff = note.get(sourceType)
				diff -= self.notes[i - distance].get(sourceType)

			note.set(targetType,diff)


	def countOccurrences(self,noteType):

		result = {}

		for note in self.notes:

			value = note.get(noteType)
			if value is None: continue

			if value not in result:
				formatted = note.renderSingle(noteType,True)
				if noteType == "raw": 
					formatted = note.renderSingle("text",True) + ":" + formatted
				result[value] = [0,formatted]

			result[value][0] += 1

		return result


	def renderHistogram(self,noteType = "raw",orderBy = "value"):

		occurrences = self.countOccurrences(noteType)

		self.render.renderHeader(
			"Histogram of " +
			noteType + 
			" (" + 
			str(len(occurrences)) + 
			" values)"
		)

		if orderBy == "value":
			occurrences = OrderedDict(sorted(
				occurrences.items(),
				key = itemgetter(0),
				reverse = False
			))
		elif orderBy == "count":
			occurrences = OrderedDict(sorted(
				occurrences.items(),
				key = lambda item: item[1],
				reverse = True
			))
		else:
			print("invalid histogram order: " + orderBy)
			quit()


		for value in occurrences:

			(count,formatted) = occurrences[value]
		
			line = formatted
			line += str(count).rjust(3)
			line += " "
			line += "#" * count
			self.render.renderComment(line)

		self.render.renderLine()


	def calcMapping(self):

		self.mapping = {}
		mapId = 0

		for note in self.notes:

			value = note.get("raw")
			if value in self.mapping: continue

			note.set("mapped",mapId)
			mapId += 1
			self.mapping[value] = note

		for note in self.notes:

			rawId = note.get("raw")
			mappedNote = self.mapping[rawId]
			mapId = mappedNote.get("mapped")
			note.set("mapped",mapId)


########################################################################

if __name__ == '__main__':

	try:

		sheet = Sheet()
		sheet.main()

	except KeyboardInterrupt:
		print(" - interrupted")
