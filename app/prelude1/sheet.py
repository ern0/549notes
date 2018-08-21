#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True
import os
from collections import OrderedDict
from operator import itemgetter  


class Prelude1:


	def main(self):


		self.fillTextData()

		self.baseRaw = self.convertTextToRaw(self.baseText)
		self.endRaw = self.convertTextToRaw(self.endText)
		self.codaRaw = self.convertTextToRaw(self.codaText)

		self.deltaPrevLine = self.calcDeltaPrevLine(self.baseRaw)
		self.baseCount = self.countValues(self.baseRaw)
		self.deltaCount = self.countValues(self.deltaPrevLine)

		self.dumpScore()		
		self.dumpFrequency(self.baseCount,"raw base",False)
		self.dumpFrequency(self.deltaCount,"delta base",True)


	def dumpFrequency(self,values,title,isDelta):

		print(title + ":",len(values))

		# sort by values
		values = OrderedDict(
			sorted(values.items(),
			key = itemgetter(1),
			reverse = True)
		)

		for i in values:
			
			v = values[i]
			
			if isDelta and i > 0: pl = "+"
			else: pl = ""
			
			print(
				str(pl + str(i)).rjust(4) + ":" + str(v).rjust(3)
				,end="  "
			)
			
			for bar in range(0,v):
				print("#",end="")
			
			print()


	def countValues(self,values):

		result = {}
		for value in values:
			try: result[value] += 1
			except: result[value] = 1

		return result


	def dumpScore(self):

		for i in range(0,len(self.baseText)):

			if i > 0 and i % 5 == 0: print("")
			if i > 0 and i % 20 == 0: print("")

			v = self.baseText[i]
			v += ":"
			v += str(self.baseRaw[i])
			v = v.rjust(8)

			if i < 5:
				d = "--"
			else:
				d = self.deltaPrevLine[i - 5]
				if d > 0: d = "+" + str(d)
			d = str(d).rjust(3)

			print(v,d,end="")

		print("")


	def fillTextData(self):

		self.baseText = [

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
			"g1","d2","g2","h3","f3",

			"c1","c2","g2","ais2","e3",
		]

		self.endText = [

			"c1","c2","f2","a2","c3","f3","c3","a2",
			"c3","a2","f2","a2","f2","d2","f2","d2",
			"c1","h1","g3","h3","d4","f4","d4","h3",
			"d4","h3","g3","h3","d3","f3","e3","d3",

			"c1"

		]

		self.codaText = [
			"c1","c2","e3","g3","c4"
		]


	def convertTextToRaw(self,textArray):

		result = []
		for text in textArray:

			note = text[:-1]
			octave = text[-1:]

			value = (int(octave) - 1) * 12
			value += self.note2value(note)

			result.append(value)
		
		return result		


	def note2value(self,note):

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


	def calcDeltaPrevLine(self,raw):

		result = []

		for i in range(0,len(raw)):
			v = raw[i]

			if i < 5:
				continue
			else:
				delta = v - raw[i - 5]

			result.append(delta)

		return result


if __name__ == '__main__':

	try: 

		sheet = Prelude1()
		sheet.main()

	except KeyboardInterrupt:
		print(" - interrupted")
