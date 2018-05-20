import json
import sys
import xapian
import csv
import os

def parse_csv_file(datapath, charset='utf8'):
	"""Parse a CSV file.
	Assumes the first row has field names.
	Yields a dict keyed by field name for the remaining rows.
	"""
	with open(datapath) as fd:
		reader = csv.DictReader(fd)
		for row in reader:
			yield row

def index(datapath):
	db = xapian.WritableDatabase("./newdb2/", xapian.DB_CREATE_OR_OPEN)

	# Set up a TermGenerator that we'll use in indexing.
	termgenerator = xapian.TermGenerator()
	termgenerator.set_stemmer(xapian.Stem("pt"))

	print(datapath)

	for fields in parse_csv_file(datapath):
		# 'fields' is a dictionary mapping from field name to value.
		# Pick out the fields we're going to index.
		docid = fields.get('DOCID', u'')
		date = fields.get('DATE', u'')
		text = fields.get('TEXT', u'')

		doc = xapian.Document()
		termgenerator.set_document(doc)

		termgenerator.index_text(text, 1, 'XD')

		termgenerator.index_text(text)

		doc.set_data(docid + ": " + text)

		idterm = u"Q" + docid
		doc.add_boolean_term(idterm)
		db.replace_document(idterm, doc)

	#print(datapath + " indexed! - " + str(i))

def walker(path):
	for root, dirs, files in os.walk(path):
		if (len(files) < 1):
			print("No files found")
			sys.exit(1)
		i = 0
		for file_ in files: 
			index(datapath = os.path.join(root, file_))
			i+=1
			print(str(i) + " files indexed.")

if len(sys.argv) != 2:
	print("Usage: %s DATAPATH" % sys.argv[0])
	sys.exit(1)

walker(path = sys.argv[1])


