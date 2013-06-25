import sys, string, os
from bottle import route, run, template
from bottle import static_file
from bottle import error,request
import pyRserve
from platform_client import *
conn = pyRserve.connect()
conn.eval("source('/tmp/server.r')")

cache = []

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='public/')

@error(404)
def error404(error):
    return 'Nothing here, sorry'

@route('/discover')
def getdiscover():
    l = request.query['items']
    data = discover(l)
    print data
    return str(data)

@route('/random')
def get_rserve_random():
    l = request.query['items']
    lst = []
    if int(l)>0:
        items = str(conn.eval("item_choosing("+str(l)+")"))
        items = items[1:-1].translate(None,'\n').strip(' ')
        templst = [int(x) for x in items.split()]
        for j in templst:
            lst.append({'id':j,'tags':[1,2,3,4,5,6,7,8,9,10]})
    return str(lst)

print "## in case you want to push your own host\port just use the command line - when running the server."
print "## argv[1] = host, argv[2] = port"
print "#############"

host = '0.0.0.0'
if len(sys.argv) > 1:
	host = sys.argv[1]
	print 'argument #1: ' + sys.argv[1]

port = '3000'
if len(sys.argv) > 2:
	port = sys.argv[2]
	print 'argument #2: ' + sys.argv[2]

run(host=host, port=port)
