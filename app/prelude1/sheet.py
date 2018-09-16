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

		diffs = (1,5,10,"mixed/1/5",)
		extras = (1,5,10,1,)

		self.totals = {}

		for rm in ("raw","mapped",):

			self.render.renderScore(rm,("text",rm,))

			self.renderHistogram(rm,orderBy = "value")
			self.renderHistogram(rm,orderBy = "count")

			for i in range(0,len(diffs)):
				diff = diffs[i]
				extra = extras[i]
				diffId = rm + "-diff-" + str(diff)
				
				self.calcDiff(rm,diffId,diff)
				self.render.renderScore(diffId,("text",rm,diffId,))
				
				self.renderHistogram(diffId,orderBy = "value")
				self.renderHistogram(diffId,orderBy = "count")
				
				for split in (2,3,4,5,):
					self.renderEstimation(diffId,0,extra)
					self.renderEstimation(diffId,1,extra)
					self.renderEstimation(diffId,2,extra)
					self.renderEstimation(diffId,3,extra)
					self.renderEstimation(diffId,4,extra)
					self.renderEstimation(diffId,5,extra)

		self.renderTotal()

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

		count = 0
		for note in self.notes:
			if note.get(noteType) is not None: count += 1

		occurrences = self.countOccurrences(noteType)

		self.render.renderHeader(
			"Histogram of " +
			noteType + 
			" (" + 
			str(len(occurrences)) + 
			" values, " +
			str(count) + 
			"/" + 
			str(len(self.notes)) +
			" notes)"
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

		cumulated = 0
		numero = 1
		for value in occurrences:
			line = ""

			(count,formatted) = occurrences[value]
			cumulated += count
		
			if orderBy == "count":
				line = str(numero).rjust(2)
				line += ". "
			line += formatted
			line += str(count).rjust(3)
			line += str(cumulated).rjust(4)
			line += " "
			line += "#" * count
			self.render.renderComment(line)

			numero += 1

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


	def renderEstimation(self,noteType,cBitLen,extra):

		self.render.renderHeader(
			"estimation for " + 
			str(noteType) +
			" @ " +
			str(cBitLen)
		)

		occurrences = self.countOccurrences(noteType)
		occurrences = OrderedDict(sorted(
			occurrences.items(),
			key = lambda item: item[1],
			reverse = True
		))

		tNoteNum = len(occurrences)
		cNoteNum = 2 ** cBitLen - 1
		uNoteNum = tNoteNum - cNoteNum

		uBitLen = 0
		if uNoteNum > 0: uBitLen = 1
		if uNoteNum > 2: uBitLen = 2
		if uNoteNum > 4: uBitLen = 3
		if uNoteNum > 8: uBitLen = 4
		if uNoteNum > 16: uBitLen = 5
		if uNoteNum > 32: uBitLen = 6
		if uNoteNum > 64: uBitLen = 7
		if uNoteNum > 128: uBitLen = 8
		if uNoteNum > 256: uBitLen = 9
		uBitLen += cBitLen

		self.render.renderComment(
			"note bits: " + 
			str(cBitLen).rjust(5) + ".c" +
			str(uBitLen).rjust(5) + ".u"
		)

		self.render.renderComment(
			"note num:  " + 
			str(cNoteNum).rjust(5) + ".c" +
			str(uNoteNum).rjust(5) + ".u" +
			str(tNoteNum).rjust(5) + ".t"
		)

		index = 0
		cNoteCount = 0
		uNoteCount = 0
		tNoteCount = 0
		for value in occurrences:
			(count,formatted) = occurrences[value]
			
			tNoteCount += count

			if index < cNoteNum:
				cNoteCount += count
			else:
				uNoteCount += count

			index += 1

		self.render.renderComment(
			"note count: " + 
			str(cNoteCount).rjust(4) + ".c" +
			str(uNoteCount).rjust(5) + ".u" +
			str(tNoteCount).rjust(5) + ".t"
		)

		cStorage = cNoteCount * cBitLen
		uStorage = uNoteCount * uBitLen
		tStorage = cStorage + uStorage

		self.render.renderComment(
			"storage:    " + 
			str(cStorage).rjust(4) + ".c" +
			str(uStorage).rjust(5) + ".u" +
			str(tStorage).rjust(5) + ".t"
		)

		storage = int(tStorage / 8)
		table = len(occurrences)
		total = storage + extra + table

		self.render.renderComment(
			"total bytes (storage + leading + table): " +
			str(storage).rjust(4) + 
			" + " +
			str(extra) +
			" + " + 
			str(table) +
			" = " +
			str(total)
		)

		self.render.renderLine()

		self.totals[noteType + " @ " + str(cBitLen)] = total


	def renderTotal(self):

		self.render.renderHeader("total")

		self.totals = OrderedDict(sorted(
			self.totals.items(),
			key = lambda item: item[1],
			reverse = False
		))

		for sig in self.totals:
			self.render.renderComment(
				sig.rjust(27) + 
				"  =" + 
				str(self.totals[sig]).rjust(5)
			)

		self.render.renderLine()


if __name__ == '__main__':

	try:

		sheet = Sheet()
		sheet.main()

	except KeyboardInterrupt:
		print(" - interrupted")
