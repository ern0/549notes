#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True
import os
import math
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
		if len(sys.argv) < 3:
			self.renderAnalysis()
		else:
			if str(sys.argv[2]) == "1":
				self.renderData1()
			else:
				self.renderData2()
		self.saveFile()


	def renderAnalysis(self):

		diffs = (1,2,3,4,5,6,7,8,9,10,"mixed/1/5",)
		extras = (1,2,3,4,5,6,7,8,9,10,1,)

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

				for split in (1,2,3,4,5,6,):
					self.renderEstimation(diffId,split,extra,False)
					if rm == "raw":
						self.renderEstimation(diffId,split,extra,True)

		self.renderStoreRawWithTable()
		self.renderStoreRawWithoutTable()

		self.renderTotal()


	def __init__(self):

		self.render = Render(self)
		self.totals = {}


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

		for noteText in data.codaText:
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
			"part1: A B C D E [C D E] - " +
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

		self.render.renderComment()

		eff = int( self.splitPoint / 5 * 8 ) * 2

		self.render.renderComment(
			"eff. notes: " +
			str( eff ).rjust(3)
		)
		self.render.renderComment(
			"data notes: " +
			str( len(self.notes) ).rjust(3)
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


	def renderTotal(self):

		self.render.renderHeader("total")

		self.totals = OrderedDict(sorted(
			self.totals.items(),
			key = lambda item: item[1],
			reverse = False
		))

		for sig in self.totals:
			self.render.renderComment(
				sig.rjust(40) +
				"  =" +
				str(self.totals[sig]).rjust(5)
			)

		self.render.renderLine()


	def renderEstimation(self,noteType,cBitLen,extra,noCompTab):

		if noCompTab: nct = " nctab"
		else: nct = ""
		self.render.renderHeader(
			"estimation for " +
			str(noteType) +
			" @ " +
			str(cBitLen) +
			nct
		)

		occurrences = self.countOccurrences(noteType)
		occurrences = OrderedDict(sorted(
			occurrences.items(),
			key = lambda item: item[1],
			reverse = True
		))

		cNoteNum = 0
		uNoteNum = 0
		tNoteNum = 0
		cNoteCount = 0
		uNoteCount = 0
		tNoteCount = 0
		cTabLo = - (2 ** (cBitLen - 1)) + 1
		cTabHi = 2 ** (cBitLen - 1) - 1
		cTabSize = 2 ** (cBitLen) - 1
		index = 0
		for value in occurrences:
			(count,formatted) = occurrences[value]

			tNoteNum += 1
			tNoteCount += count

			if noCompTab:
				if value < cTabLo or value > cTabHi:
					uNoteNum += 1
					uNoteCount += count
				else:
					cNoteNum += 1
					cNoteCount += count

			else:
				if index < cTabSize:
					cNoteNum += 1
					cNoteCount += count
				else:
					uNoteNum += 1
					uNoteCount += count

			index += 1

		# todo: nct table size

		self.render.renderComment(
			"note num:  " +
			str(cNoteNum).rjust(5) + ".c" +
			str(uNoteNum).rjust(5) + ".u" +
			str(tNoteNum).rjust(5) + ".t"
		)

		self.render.renderComment(
			"note count: " +
			str(cNoteCount).rjust(4) + ".c" +
			str(uNoteCount).rjust(5) + ".u" +
			str(tNoteCount).rjust(5) + ".t"
		)

		if uNoteNum <= 0:
			uBitLen = 0
		else:
			uBitLen = math.ceil( math.log(uNoteNum,2) )
			uBitLen += cBitLen

		self.render.renderComment(
			"note bits: " +
			str(cBitLen).rjust(5) + ".c" +
			str(uBitLen).rjust(5) + ".u"
		)

		cStorage = cNoteCount * cBitLen
		uStorage = uNoteCount * uBitLen
		tStorage = cStorage + uStorage

		self.render.renderComment(
			"storage:    " +
			str(int(cStorage/8)).rjust(4) + ".c" +
			str(int(uStorage/8)).rjust(5) + ".u" +
			str(int(tStorage/8)).rjust(5) + ".t"
		)

		if noCompTab:	cTable = 0
		else: cTable = cNoteNum
		uTable = uNoteNum
		tTable = cTable + uTable

		self.render.renderComment(
			"table:      " +
			str(int(cTable)).rjust(4) + ".c" +
			str(int(uTable)).rjust(5) + ".u" +
			str(int(tTable)).rjust(5) + ".t"
		)

		total = math.ceil(tStorage / 8) + extra + tTable

		self.render.renderComment(
			"total bytes (storage + leading + table): " +
			str(total)
		)

		self.render.renderLine()

		self.totals[noteType + " @ " + str(cBitLen) + nct] = total


	def renderStoreRawWithTable(self):

		self.render.renderHeader("estimation for 5-bit raw + table")

		storage = int( len(self.notes) * 5 / 8)

		occurrences = self.countOccurrences("raw")
		table = len(occurrences)

		eff = int( self.splitPoint / 5 * 8 ) * 2

		self.render.renderComment(
			"data notes: " +
			str( len(self.notes) ).rjust(3)
		)
		self.render.renderComment(
			"storage: " +
			str(storage).rjust(6) +
			" bytes"
		)
		self.render.renderComment(
			"table: " +
			str(table).rjust(8) +
			" bytes"
		)
		self.render.renderComment(
			"total: " +
			str(storage + table).rjust(8) +
			" bytes"
		)

		self.render.renderLine()

		self.totals["store raw 5-bit + table"] = storage + table


	def renderStoreRawWithoutTable(self):

		self.render.renderHeader("estimation for raw w/o table")

		minValue = 999
		maxValue = 0

		for note in self.notes:
			value = note.get("raw")

			if value < minValue: minValue = value
			if value > maxValue: maxValue = value

		valueRange = maxValue - minValue
		valueBits = math.ceil( math.log(valueRange,2) )

		storage = math.ceil( len(self.notes) * valueBits / 8 )

		self.render.renderComment(
			"note min. value: " +
			str( minValue ).rjust(3)
		)
		self.render.renderComment(
			"note max. value: " +
			str( maxValue ).rjust(3)
		)
		self.render.renderComment(
			"value range: " +
			str( valueRange ).rjust(7)
		)
		self.render.renderComment(
			"value bits: " +
			str( valueBits ).rjust(8)
		)
		self.render.renderComment(
			"data notes: " +
			str( len(self.notes) ).rjust(8)
		)
		self.render.renderComment(
			"total: " +
			str(storage).rjust(13) +
			" bytes"
		)

		self.render.renderLine()

		self.totals["store raw " +str(valueBits) + "-bit w/o table"] = storage


# ---- data, method 1 -----------------------------------------------------------------

	def renderData1(self):

		noteType = "raw-diff-5"
		self.resetDataResult()

		self.renderData1Stat(noteType)
		self.render.renderHeader("data")
		self.render.renderLine()

		self.renderFirstBytes(noteType)
		self.renderData1Table(noteType)
		self.renderData1Notes(noteType)


	def renderData1Stat(self,diffId):

		self.calcDiff("raw",diffId,5)
		self.render.renderScore(diffId,("text","raw",diffId,))
		self.renderHistogram(diffId,orderBy = "count")
		self.renderEstimation(diffId,3,5,False)


	def renderData1Table(self,diffId):

		occurrences = self.countOccurrences(diffId)

		occurrences = OrderedDict(sorted(
			occurrences.items(),
			key = lambda item: item[1],
			reverse = True
		))

		self.topDiffs = list(occurrences.keys())

		self.render.renderLine("tab3: ; table for 3-bit index (item 0 is missing)")
		self.render.renderLine()
		line = ""
		self.tab3 = {}

		for index in range(0,7):

			diff = self.topDiffs[index]
			self.tab3[diff] = index + 1  # slot 0 is used for special purpose

			if line == "": line += "\tdb "
			else: line += ","
			line += str(diff)

		self.render.renderLine(line)
		self.render.renderLine()

		self.render.renderLine("tab5: ; table for 5-bit index (item 0 is missing)")
		self.render.renderLine()
		line = ""
		self.tab5 = {}

		for index in range(7,len(self.topDiffs)):

			diff = self.topDiffs[index]
			self.tab5[diff] = index - 7 # index 7 is the new index 0

			if (index - 7) % 8 == 0:
				if line != "": self.render.renderLine(line)
				line = "\tdb "
			else: line += ","
			line += str(diff)

		self.render.renderLine(line)
		self.render.renderLine()


	def renderData1Notes(self,noteType):

		self.render.renderLine("data_notes: ; compressed note data")
		self.render.renderLine()

		for i in range(0,len(self.notes)):
			note = self.notes[i]
			diff = note.get(noteType)

			if diff is None: diff = 0

			if diff in self.tab3:
				index = self.tab3[diff]
				self.renderDataBits(3,index)
			else:
				index = self.tab5[diff]
				# 0 is a special value: read next 5 bit
				self.renderDataBits(3,0)
				# add 1 to index: avoid 0 value
				self.renderDataBits(5,index + 1)

		self.renderPaddingBits()
		self.renderDataLine()

# ---- data, method 2 -----------------------------------------------------------------

	def renderData2(self):

		self.render.renderHeader("data")
		self.render.renderLine()

# ---- data, common -------------------------------------------------------------------

	def renderFirstBytes(self,noteType):

		line = ""

		for i in range(0,len(self.notes)):
			note = self.notes[i]
			diff = note.get(noteType)
			if diff is not None: continue

			if line != "": line += ","
			line += str(note.get("raw"))

		self.render.renderLine("data_start: ; starting raw bytes")
		self.render.renderLine("\tdb " + line)
		self.render.renderLine()


	def resetDataResult(self):

		self.latchByte = 0
		self.shiftCounter = 0
		self.dataLine = ""
		self.itemCounter = 0


	def renderDataBits(self,length,value):

		if length != 0: value <<= 8 - length

		for i in range(0,length):

			value <<= 1
			if value & 0x100: bit = 1
			else: bit = 0
			value = value & 0xff

			self.latchByte <<= 1
			self.latchByte |= bit

			self.shiftCounter += 1
			if self.shiftCounter < 8: continue
			self.shiftCounter = 0

			self.renderDataItem()
			self.latchByte = 0


	def renderPaddingBits(self):

		if self.shiftCounter == 0: return
		self.renderDataBits(8 - self.shiftCounter,0x55)


	def renderDataItem(self):

		if self.itemCounter == 0: self.dataLine = "\tdb "
		if self.itemCounter > 0: self.dataLine += ","
		self.dataLine += "$"
		self.dataLine += hex(self.latchByte).replace("x","")[-2:]
		self.itemCounter += 1

		if self.itemCounter != 8: return
		self.renderDataLine()
		self.itemCounter = 0


	def renderDataLine(self):

		if self.itemCounter == 0: return
		self.render.renderLine(self.dataLine)

# -------------------------------------------------------------------------------------

if __name__ == '__main__':

	try:
		sheet = Sheet()
		sheet.main()
		#sheet.test()

	except KeyboardInterrupt:
		print(" - interrupted")
