#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True


class Note:


	def __init__(self,sheet):
		self.sheet = sheet
		self.values = {}


	def set(self,type,value):

		self.values[type] = value

		if type == "text":
			self.values["raw"] = self.convertTextToValue(value)


	def get(self,type):
		return self.values[type]


	def convertTextToValue(self,text):

		pitch = None

		textNote = text[0:2]
		if textNote == "c-": pitch = 0
		elif textNote == "c#": pitch = 1
		elif textNote == "d-": pitch = 2
		elif textNote == "d#": pitch = 3
		elif textNote == "e-": pitch = 4
		elif textNote == "f-": pitch = 5
		elif textNote == "f#": pitch = 6
		elif textNote == "g-": pitch = 7
		elif textNote == "g#": pitch = 8
		elif textNote == "a-": pitch = 9
		elif textNote == "a#": pitch = 10
		elif textNote == "h-": pitch = 11

		if pitch is None:
			print("invalid note: " + str(text))
			quit()

		try:
			octave = int(text[2]) * 12
		except:
			print("invalid octave: " + str(text))
			quit()

		return octave + pitch


	def render(self,typeMixed,isComment):
		
		if type(typeMixed) is tuple: 
			return self.renderTuple(typeMixed,isComment)
		else:
			return self.renderSingle(typeMixed,isComment)


	def renderTuple(self,typeTuple,isComment):

		line = ""
		for typeIndex in range(0,len(typeTuple)):
			type = typeTuple[typeIndex]
			if typeIndex != 0: line += ":"
			line += self.render(type,isComment)

		return line


	def renderSingle(self,type,isComment):

		value = self.values[type]
		try: strAbsValue = str(abs(value))
		except TypeError: strAbsValue = str(value)

		if not isComment or type == "text": return strAbsValue

		if len(strAbsValue) < 2: strAbsValue = "0" + strAbsValue 
		if type == "raw" or type == "mapped": return strAbsValue

		if value is None: return "N/A"
		elif value > 0: return "+" + strAbsValue
		elif value < 0: return "-" + strAbsValue
		return "=00"
