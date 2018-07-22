#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True

import os


class Assemblyzator:

	def main(self):
		print("hello")


if __name__ == '__main__':
	try: (Assemblyzator()).main()
	except KeyboardInterrupt: print(" - interrupted")