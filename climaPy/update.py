import urllib2,os
from subprocess import call
archive = urllib2.urlopen("http://192.168.1.8:2007/arquivo")
arduino_file = open("/home/pi/Desktop/share/climaPy/captura/src/bilu.ino","w")
arduino_file.write(archive.read())
arduino_file.close()

call("platformio run --target upload",cwd="/home/pi/Desktop/share/climaPy/captura",shell=True)

