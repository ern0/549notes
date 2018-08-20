#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True


class Prelude1:

	def main(self):

		self.sheet = [

			c3,e3,g3,c4,e4,
			c3,d3,a3,d4,f4,
			h2,d3,g3,d4,f4,
			c3,e3,g3,c4,e4,

			c3,e3,a3,e4,a4,
			c3,d3,fis3,a3,d4,
			h2,d3,g3,d4,g4,
			h2,c4,e3,g3,c4,

			a2,c3,e3,g3,c4,
			d2,a2,d3,fis3,c4,
			g2,h2,d3,g3,h3,
			g2,ais2,e3,g3,cis4,

			f2,a2,d3,a3,d4,
			f2,gis2,d3,f3,h3,
			e2,g2,c3,g3,c4,
			e2,f2,a2,c3,f3,

			d2,f2,a2,c3,f3,
			d2,f2,a2,c3,f3,
			g1,d2,g2,h2,f3,
			c2,e2,g2,c3,e3,
		
			c2,g2,ais2,c3,e3,
			f1,f2,a2,c3,e3,
			fis1,c2,a2,c3,e3,
			gis1,f2,h2,dis3,

			g1,f2,g2,h2,d3,
			g1,e2,g2,c3,e3,
			g1,d2,g2,c3,f3,
			g1,d2,g2,h3,f3,

			g1,dis2,a2,c3,fis3,
			g1,e2,g2,c3,g3,
			g1,d2,g2,c3,f3,
			g1,d2,g2,h3,f3,

			c1,c2,g2,ais2,e3,
			
		]



import os
if __name__ == '__main__':

	try: 

		sheet = Perlude1()
		sheet.main()

	except KeyboardInterrupt:
		print(" - interrupted")
