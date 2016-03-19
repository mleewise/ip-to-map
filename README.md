# ip-to-map
Generates an excel file with latitude/longitude columns which can be externally converted to KML format, then uploaded to google maps for plotting points.

Probably platform independent, but fyi developed/tested on windows.

uses os, sys, re. 
External libraries:
pip install xlwt
pip install geoip2
Download GeoLite2-City.mmdb from https://dev.maxmind.com/geoip/geoip2/geolite2/ and place in same directory as generateXLSfromIP.py. I believe it comes as a .gz file, so may be necessary to unzip with 7zip.
The log file must also live in the same directory as generateXLSfromIP.py

I used regular expressions to find all occurances of an ip address on each line. I have not tested if there are multiple IP's per line. It currently will process only one ip per line.
TLDR: the RE [\d]+.[\d]+.[\d]+.[\d]+ is run on each line.

Either name your ip log file 'testIPdata.log' or pass it as an argument in shell.
python generateXLSfromIP.py myLogFile.txt

An .xls file is generated. Place at the top of Column A: Latitude and Column B: Longitude. Save the file.

Use the tool located here at
https://www.earthpoint.us/ExcelToKml.aspx
to upload your file and create the KML file. It is limited to 200 entries per file.

Follow these instructions to load your shiny new KML file into google maps
https://support.google.com/mymaps/answer/3024836?hl=en

As a final note, if you want to do more than 200, the most straightforward and obvious solution is to split your log file into chunks of 200, produce as many KML's as needed, then before going on to google, merge those KMLs together using a text editor. In general, choose a target KML file, and into that paste from the others the contents of each starting from the end of the first  <Document> tag and before the last </Document> tag (de memoria). If this doesn't work for you, google "merging KML files"

