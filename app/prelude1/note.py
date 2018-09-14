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


	def render(self,type,isComment):
		
		value = self.values[type]
		strValue = str(value)

		if not isComment or type == "text": return strValue

		if len(strValue) < 2: strValue = "0" + strValue 
		if type == "raw" or type == "mapped": return strValue

		if value > 0: return "+" + strValue
		else: return "-" + strValue
		return "=00"
