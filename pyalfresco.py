import urllib
import urllib2
import xml.etree.ElementTree as ET
import re
import logging

class Alfresco:

	def __init__(self, host, username, password, SSL=False):
		self.LOGGER = logging.getLogger(__name__)
		self.protocol = "http"
		if SSL:
			self.protocol += "s"
		self.host = host
		self.username = username
		self.password = password
	
	def http_post(self, URL, parameters):
		data = urllib.urlencode(parameters)
		return urllib2.urlopen(
			urllib2.Request(URL, data)		
		).read()
	
	def ticket_authentication(self):
		self.ticket = urllib2.urlopen("{}://{}/alfresco/service/api/login?u={}&pw={}".format(self.protocol, self.host, self.username, self.password)).read()
		self.ticket = re.match(r".*(TICKET_.*)<", self.ticket, re.DOTALL).group(1)
		self.LOGGER.debug(("alfresco ticket", self.ticket))

	def call_webscript(self, request_path):
		if "?" in request_path:
			ticket_seperator = "&"
		else:
			ticket_seperator = "?"
		service_uri = "{}://{}/alfresco/service{}{}alf_ticket={}".format(self.protocol, self.host, request_path, ticket_seperator, self.ticket)
		self.LOGGER.debug(service_uri)
		return urllib2.urlopen(service_uri).read()
	
	def basic_authentication(self):
		password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
		password_mgr.add_password(
			None,
			# "{}://{}/alfresco/service/bulkfsimport".format(self.protocol, self.host),
			"{}://{}/alfresco/service/".format(self.protocol, self.host),
			self.username,
			self.password)
		handler = urllib2.HTTPBasicAuthHandler(password_mgr)
		opener = urllib2.build_opener(handler)
		urllib2.install_opener(opener)

	def initiate_bulk_import(self, parameters):
		self.http_post("{}://{}/alfresco/service/bulkfsimport/initiate".format(self.protocol, self.host), parameters)

	def get_bulk_import_status(self):
		status_response = urllib2.urlopen("{}://{}/alfresco/service/bulkfsimport/status?format=xml".format(self.protocol, self.host)).read()
		e = ET.fromstring(status_response)
		status = {
			"CurrentStatus": e.find("CurrentStatus").text,
			"ResultOfLastExecution": e.find("ResultOfLastExecution").text,
			"ContentNodesCreated": e.find("TargetStatistics").find("ContentNodesCreated").text,
			"ContentNodesReplaced": e.find("TargetStatistics").find("ContentNodesReplaced").text,
			"FilesScanned": e.find("SourceStatistics").find("FilesScanned").text
		}
		print "ResultOfLastExecution", e[1].text
		print "status,result,created,replaced,read\n{},{},{},{},{}".format(
				e.find("CurrentStatus").text,
				e.find("ResultOfLastExecution").text,
				e.find("TargetStatistics").find("ContentNodesCreated").text,
				e.find("TargetStatistics").find("ContentNodesReplaced").text,
				e.find("SourceStatistics").find("FilesScanned").text)
		return status
