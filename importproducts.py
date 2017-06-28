import xmlrpclib
import csv


server="http://localhost:8069"
database="demo"
user = "admin"
pwd="admin"

common = xmlrpclib.ServerProxy( '%s/xmlrpc/2/common' % server)

print common.version()

uid = common.authenticate(database,user,pwd, {})

print uid

OdooApi = xmlrpclib.ServerProxy('%s/xmlrpc/2/object' % server)

#filter = [[('largemeal','=',True)]]
count = OdooApi.execute_kw(database,uid,pwd,'meeting.information','search_count',[[]])

print count

