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


	def __init__(self):

		self.render = Render(self)
		self.totals = {}
		self.pure8 = False
		self.mirror = True

		self.createScore()
		self.calcMapping()


	def main(self):

		if len(sys.argv) < 3:
			self.renderIntro(None)
			self.renderAnalysis()
		else:
			if str(sys.argv[2]) == "1":
				self.renderData1()
			elif str(sys.argv[2]) == "2":
				self.renderData2()
			elif str(sys.argv[2]) == "3":
				self.renderData2(mode3=True)
			elif str(sys.argv[2]) == "t":
				self.renderTest()
			else:
				self.renderData4()
		self.saveFile()


	def renderAnalysis(self):

		#self.calcDiff("raw","raw-diff-5",5)
		#self.renderHistogram("raw-diff-5",orderBy = "count")
		#return

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
					self.renderEstimation(diffId,split,extra,False,False)
					if rm == "raw":
						self.renderEstimation(diffId,split,extra,True,False)
						self.renderEstimation(diffId,split,extra,False,True)
						self.renderEstimation(diffId,split,extra,True,True)

		self.renderStoreRawWithTable()
		self.renderStoreRawWithoutTable()

		self.renderTotal()


	def createScore(self):

		self.notes = []

		if self.pure8:

			for i in range(0,len(data.part1Text)):
				noteText = data.part1Text[i]

				note = Note(self)
				note.set("text",noteText)
				self.notes.append(note)

				if i % 5 == 4:
					c = data.part1Text[i - 2]
					d = data.part1Text[i - 1]
					e = data.part1Text[i]
					for cde in (c,d,e):
						note = Note(self)
						note.set("text",cde)
						self.notes.append(note)

		else:
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


	def renderIntro(self,signature):

		self.render.renderHeader("generated file, do not edit","*",False)
		if signature is not None: self.render.renderComment("compression method: " + signature)
		self.render.renderComment()

		self.render.renderComment("Transformed score data and analysis of")
		self.render.renderComment(" J.S.Bach: Prelude in C major, BWV 846")
		self.render.renderComment(" from the Prelude and Fugue in C major, BWV 846")
		self.render.renderComment(" from Book I of The Well-Tempered Clavier")
		self.render.renderComment("for PC-DOS 256-byte intro")
		self.render.renderComment()

		if self.pure8: cde = " C D E "
		else: cde = "[C D E]"
		self.render.renderComment(
			"part1: A B C D E " + cde + " - " +
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

		if self.pure8: eff = self.splitPoint * 2
		else: eff = int( self.splitPoint / 5 * 8 ) * 2
		eff += len(data.part2Text)
		eff += len(data.codaText)

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
		elif distance == "split/5/1":
			self.calcSplit5x1xDiff(sourceType,targetType)
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


	def calcSplit5x1xDiff(self,sourceType,targetType):

		for i in range(0,len(self.notes)):
			note = self.notes[i]

			if i < 5:
				diff = None
			else:
				
				if i < self.splitPoint: distance = 5
				else: distance = 1

				diff = note.get(sourceType)
				diff -= self.notes[i - distance].get(sourceType)

			note.set(targetType,diff)


	def countOccurrences(self,noteType):

		result = {}

		for note in self.notes:

			value = note.get(noteType)

			if value not in result:
				formatted = note.renderSingle(noteType,True,True)
				if noteType == "raw":
					formatted = note.renderSingle("text",True,True) + ":" + formatted
				result[value] = [0,formatted]

			result[value][0] += 1

		return result


	def renderHistogram(self,noteType = "raw",orderBy = "value"):

		count = 0
		for note in self.notes: count += 1

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


	def renderEstimation(self,noteType,cBitLen,extra,noCompTab,noUcTab):

		notab = ""
		if noCompTab: notab += " nctab"
		if noUcTab: notab += " nutab" 
		self.render.renderHeader(
			"estimation for " +
			str(noteType) +
			" @ " +
			str(cBitLen) +
			notab
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
		uLoValue = 0
		uHiValue = 0
		index = 0
		for value in occurrences:
			(count,formatted) = occurrences[value]

			tNoteNum += 1
			tNoteCount += count

			if noCompTab:
				if value < cTabLo or value > cTabHi: u = True
				else: u = False
			else:
				if index < cTabSize: u = False
				else: u = True

			if u:
				uNoteNum += 1
				uNoteCount += count
				if uLoValue > value: uLoValue = value
				if uHiValue < value: uHiValue = value
			else:
				cNoteNum += 1
				cNoteCount += count

			index += 1

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
			if noUcTab:
				uBitLen = math.ceil( math.log(uHiValue - uLoValue,2) )
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
		if noUcTab: uTable = 0
		else: uTable = uNoteNum
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

		self.totals[noteType + " @ " + str(cBitLen) + notab] = total


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
		diffId = noteType + " @ 3"

		self.calcDiff("raw",noteType,5)

		self.renderIntro(diffId)
		self.render.renderScore(noteType,("text","raw",noteType,))
		self.renderHistogram(noteType,orderBy = "count")
		self.renderEstimation(noteType,3,5,False,False)

		self.render.renderHeader("data")
		self.render.renderLine()
		self.resetDataBits()
		self.renderFirstBytes(noteType,5)
		self.renderData1Table(noteType)
		self.renderData1Notes(noteType)


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

		self.render.renderLine("data_notes: ; bit packed note data")
		self.render.renderLine()

		for i in range(0,len(self.notes)):
			note = self.notes[i]
			diff = note.get(noteType)

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


# ---- data, method 2-3 ---------------------------------------------------------------

	def renderData2(self,mode3 = False):

		noteType = "raw-diff-5"
		diffId = noteType + " @ 3 nctab nutab"

		if mode3:
			self.calcDiff("raw",noteType,"split/5/1")
		else:
			self.calcDiff("raw",noteType,5)

		self.renderIntro(diffId)
		self.render.renderScore(noteType,("text","raw",noteType,))
		self.renderHistogram(noteType,orderBy = "count")
		if not mode3: self.renderEstimation(noteType,3,5,True,True)

		self.render.renderHeader("data")
		self.render.renderLine()
		self.resetDataBits()
		self.renderFirstBytes(noteType,5)
		self.renderData2Notes(noteType)


	def renderData2Notes(self,noteType):

		cSub = 4
		uSub = 42
		spec = 7

		self.render.renderLine("; value to substract from compressed data")
		self.render.renderLine("\tDATA_CSUB = " + str(cSub))
		self.render.renderLine("; value to substract from uncompressed data")
		self.render.renderLine("\tDATA_USUB = " + str(uSub))
		self.render.renderLine()

		self.render.renderLine("data_notes: ; bit packed note data")
		self.render.renderLine()

		for i in range(0,len(self.notes)):
			note = self.notes[i]
			diff = note.get(noteType)

			if diff in (-4,-3,-2,-1,0,1,2):
				self.renderDataBits(3,diff + cSub)
			else:
				self.renderDataBits(3,spec)
				self.renderDataBits(7,diff + uSub)

		self.renderPaddingBits()
		self.renderDataLine()
		self.render.renderLine()


# ---- data, method 4 -----------------------------------------------------------------

	def renderData4(self):

		noteType = "raw-diff-5"
		diffId = noteType + " @ 4 nctab nutab"

		self.calcDiff("raw",noteType,5)

		self.renderIntro(diffId)
		self.render.renderScore(noteType,("text","raw",noteType,))
		self.renderHistogram(noteType,orderBy = "count")
		self.renderEstimation(noteType,4,5,True,True)

		self.render.renderHeader("data")
		self.render.renderLine()
		self.resetDataBits()
		self.renderFirstBytes(noteType,5)
		self.renderData4Notes(noteType)


	def renderData4Notes(self,noteType):

		cSub = 10
		uSub = 44
		spec = 2

		self.render.renderLine("; value to substract from compressed data")
		self.render.renderLine("\tDATA_CSUB = " + str(cSub))
		self.render.renderLine("; value to substract from uncompressed data")
		self.render.renderLine("\tDATA_USUB = " + str(uSub))
		self.render.renderLine("; special value before uncompressed data")
		self.render.renderLine("\tDATA_SPEC = " + str(spec))
		self.render.renderLine()

		self.render.renderLine("data_notes: ; bit packed note data")
		self.render.renderLine()

		for i in range(0,len(self.notes)):
			note = self.notes[i]
			diff = note.get(noteType)

			if diff in (-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1 , 3,4,5):
				self.renderDataBits(4,diff + cSub)
			else:
				self.renderDataBits(4,spec)
				self.renderDataBits(7,diff + uSub)

		self.renderPaddingBits()
		self.renderDataLine()
		self.render.renderLine()

# ---- test ---------------------------------------------------------------------------

	def renderTest(self):

		line = "; note data and diff data for test"
		self.render.renderLine(line)
		self.render.renderLine()

		self.renderTestNote()
		self.render.renderLine()
		self.renderTestDiff()


	def renderTestNote(self):

		self.render.renderLine("test_note_data:")
		noteType = "raw"
		index = 0

		while True:
			
			for round in (0,1):

				line = ""
				for i in (0,1,2,3,4):
					value = self.notes[index + i].get(noteType)
					if line == "":
						line += "\tdb "
					else:
						line += ","
					line += str(value)

				for i in (2,3,4):
					value = self.notes[index + i].get(noteType)
					line += "," + str(value)

				if round == 1: index += 5

				self.render.renderLine(line)

			if index >= self.splitPoint: break

		while True:

			line = ""
			for i in range(0,8):
				if index >= len(self.notes): break

				value = self.notes[index].get(noteType)
				if line == "":
					line += "\tdb "
				else:
					line += ","
				line += str(value)
				index += 1

			self.render.renderLine(line)
			if index >= len(self.notes): break


	def renderTestDiff(self):

		self.render.renderLine("test_diff_data:")
		noteType = "raw-diff-5"

		self.calcDiff("raw",noteType,5)

		index = 0
		while True:
			
			for round in (1,):

				line = ""
				for i in (0,1,2,3,4):
					value = self.notes[index + i].get(noteType)
					if line == "":
						line += "\tdb "
					else:
						line += ","
					line += str(value)

				if round == 1: index += 5

				self.render.renderLine(line)

			if index >= self.splitPoint: break

		while True:

			line = ""
			for i in range(0,8):
				if index >= len(self.notes): break

				value = self.notes[index].get(noteType)
				if line == "":
					line += "\tdb "
				else:
					line += ","
				line += str(value)
				index += 1

			self.render.renderLine(line)
			if index >= len(self.notes): break


	def renderTestDiff_NotThisWay(self):

		self.render.renderLine("test_diff_data:")
		noteType = "raw-diff-5"

		self.calcDiff("raw",noteType,5)

		line = ""
		for index in range(0,len(self.notes)):

			value = self.notes[index].get(noteType)

			if line == "":
				line += "\tdb "
			else:
				line += ","
			line += str(value)

			if len(line) > 40:
				self.render.renderLine(line)
				line = ""

		if line != "":
			self.render.renderLine(line)


# ---- data, common -------------------------------------------------------------------

	def renderFirstBytes(self,noteType,count):

		line = ""

		for i in range(0,len(self.notes)):
			if i == count: break

			note = self.notes[i]

			if line != "": line += ","
			line += str(note.get("raw"))

		self.render.renderLine("data_start: ; starting raw bytes")
		self.render.renderLine("\tdb " + line)
		self.render.renderLine()


	def resetDataBits(self):

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
		value = self.latchByte
		if self.mirror: value = self.mirrorByte(value)
		hexValue = hex(value).replace("x","")[-2:]
		if self.mirror: hexValue = hexValue.upper()
		self.dataLine += hexValue
		self.itemCounter += 1

		if self.itemCounter != 8: return
		self.renderDataLine()
		self.itemCounter = 0


	def mirrorByte(self,value):
		return int('{:08b}'.format(value)[::-1], 2)
		

	def renderDataLine(self):

		if self.itemCounter == 0: return
		self.render.renderLine(self.dataLine)

# -------------------------------------------------------------------------------------

	def test(self):

		self.resetDataBits()
		self.renderDataBits(4,1)
		self.renderDataBits(4,2)
		self.renderDataBits(7,1)
		self.renderDataBits(1,1)
		self.renderPaddingBits()
		self.renderDataLine()

		# mirror: $12,$03 -> $48,$C0

		for line in self.render.lines:
			print(line)


# -------------------------------------------------------------------------------------

if __name__ == '__main__':

	try:
		sheet = Sheet()
		sheet.main()
		#sheet.test()

	except KeyboardInterrupt:
		print(" - interrupted")
