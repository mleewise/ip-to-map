import os, sys, xlwt, re, geoip2.database

class Log:
	def __init__(self):
		self.initFile() #opens log file
		self.initExcel()
		self.initGeo()
		self.currentLine = 0
	#Helper function to get total number of lines
	def file_len(self, file):
		for i, l in enumerate(file):
			pass
		print('File is ' + str(i) + ' lines long.')
		file.seek(0) #resets file pos to beginning
		return i + 1
	#adds attributes fileObject and numLines
	def initFile(self):
		try: 
			self.file = open(sys.argv[1],'r')
		except:
			self.file = open('testIPdata.log','r')
			self.numLines = self.file_len(self.file)
	#sets file pos to beginning and currentline attribute to 0
	def seek(self):
		self.file.seek(0)
		self.currentLine=0
	#returns line and sets current line.
	def readline(self):
		line = self.file.readline()
		self.currentLine+=1
		return line
	#invokes readline and returns any on that line.
	#https://developers.google.com/edu/python/regular-expressions
	def getIP(self):
		match = re.search(r'[\d]+.[\d]+.[\d]+.[\d]+',self.readline())
		if match:
			return match.group()

	##--IP/COORDINATE HANDLING--##
	#adds reader(transcriber) method as geoTranscriber
	def initGeo(self):
		try:
			self.geoTranscriber = geoip2.database.Reader('GeoLite2-City.mmdb')
		except:
			print "Cannot locate GeoLite2-City.mmdb in working directory"
	#gets IP and returns lat,long
	def latLong(self):
		try:
			geoResponse = self.geoTranscriber.city(self.getIP())
			self.currentLat = geoResponse.location.latitude
			self.currentLong = geoResponse.location.longitude
			return True
		except:
			print "encountered line with no IP"
			return False
	#http://geoip2.readthedocs.org/en/latest/
	#https://dev.maxmind.com/geoip/geoip2/geolite2/
	##--END--IP/COORDINATE HANDLING--##


	##--EXCEL HANDLING--##
	#prepares for excel writing
	def initExcel(self):
		self.wb=xlwt.Workbook()
		self.ws=self.wb.add_sheet('coordinates') #later, insert datetime range from log file
	def writeRow(self,rowIndex,latitude,longitude):
		self.ws.write(rowIndex,0,latitude)
		self.ws.write(rowIndex,1,longitude)
	#https://github.com/python-excel/xlwt
	##--END--EXCEL HANDLING--##

	def traverseFile(self):
		while self.latLong():
			self.writeRow(self.currentLine,self.currentLat,self.currentLong)
			print 'currentLine: ' + str(self.currentLine)
		try:
			self.wb.save('latLong.xls')
		except:
			print "ABORTED: Could not save latlong.xls output. Maybe you have the file open?"

log1=Log()
log1.traverseFile()
log1.file.close()


##converting excel file to KML
#https://www.earthpoint.us/ExcelToKml.aspx
##Loading KML file into google maps.
#https://support.google.com/mymaps/answer/3024836?hl=en
#merging KML files
#https://www.gps-data-team.com/pda-gps-navigation/topic/318.html
#http://www.gearthhacks.com/forums/showthread.php?14609-How-to-unite-several-kml-files-into-only-one