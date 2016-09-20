# string library
import string

# reading file at python

# read file function	
def getFile(filename):
	try:
		f = open(filename, "r")
		listOfParsed = []
		for aline in f:
			line = aline.split('\n')
			aline = line[0]
			if (aline == "Ruangan" or aline == "" or aline == "Jadwal"):
				continue
			else:
				listOfParsed.append(aline)
		pass
	except Exception, e:
		raise e
	return listOfParsed;

# unit test
listing = getFile('Testcase.txt')
for s in listing:
	pass
	print s
