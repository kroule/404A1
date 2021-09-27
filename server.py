#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

#Got a request of: b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-CA,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1'

#Got a request of: b'GET /base.css HTTP/1.1\r\nHost: localhost:8080\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0\r\nAccept: text/css,*/*;q=0.1\r\nAccept-Language: en-CA,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nReferer: http://localhost:8080/\r\nConnection: keep-alive'

#Got a request of: b'GET / HTTP/1.1\r\nHost: www.localhost:8080\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-CA,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1'

#Got a request of: b'GET /base.css HTTP/1.1\r\nHost: www.localhost:8080\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0\r\nAccept: text/css,*/*;q=0.1\r\nAccept-Language: en-CA,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nReferer: http://www.localhost:8080/\r\nConnection: keep-alive'

#Got a request of: b'GET /favicon.ico HTTP/1.1\r\nHost: www.localhost:8080\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-CA,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive'

#Got a request of: b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-CA,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1'

#Got a request of: b'GET /base.css HTTP/1.1\r\nHost: localhost:8080\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0\r\nAccept: text/css,*/*;q=0.1\r\nAccept-Language: en-CA,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nReferer: http://localhost:8080/\r\nConnection: keep-alive'


import re
import os.path

class MyWebServer(socketserver.BaseRequestHandler):

	def handle(self):
		self.data = self.request.recv(1024).strip()
		print ("Got a request of: %s\n" % self.data)
		strdata = self.data.decode()
		print(strdata)
		self.parse_request(strdata)

	def file_exists(self, target_data):
		return os.path.isfile(target_data)

	def path_exists(self, target_data):
		return os.path.isdir(target_data)

	def fetch_data(self, target_data):
		data_path = target_data.replace('../', '')

		data_pref = './www'



		resource_name= ''
		resource_extension = ''
		resource_type = ''
		fix_path = False

		payload = 'HTTP/1.1 '
		code = ''

		if data_path[-1] == '/':
			resource_type = 'DIR'
		else:
			result = re.match('.*/(.*)\Z', data_path)
			if result:
				resource_name = result.group(1)

				result = re.match(".*\.(.*)\Z", resource_name)
				if result:
					resource_extension = '.'+result.group(1)
					resource_type = 'FILE'
				else:
					resource_type = 'DIR'
					fix_path = True

		print(data_pref+data_path)
		if resource_type == 'DIR':
			if self.path_exists(data_pref+data_path):
				if fix_path:
					payload = 'HTTP/1.1 301 Moved Permanently\r\nLocation: http://'+self.server.server_address[0]+':'+str(self.server.server_address[1])+data_path+'/'+'\r\n\r\n'
					return payload
				else:
					data_path += 'index.html'
					resource_type = 'FILE'
					resource_extension = '.html'
			else:
				payload = 'HTTP/1.1 404 Not Found\r\n\r\n'
				return payload

		if resource_type == 'FILE':
			if self.file_exists(data_pref+data_path):
				try:
					source_data = open(data_pref+data_path, 'r')
					fetched = source_data.read()
					source_data.close()
					payload = 'HTTP/1.1 200 OK\r\n'
					if resource_extension != '':
						payload += 'Content-Type: text/'+resource_extension[1:]+'\r\n'
					payload += '\r\n'
					payload += fetched
					return payload
				except IOError:
					payload = 'HTTP/1.1 404 Not Found\r\n\r\n'
					return payload
			else:
				payload = 'HTTP/1.1 404 Not Found\r\n\r\n'
				return payload

		print(resource_name, resource_extension, resource_type, fix_path)
		return 'HTTP/1.1 418 I\'m a teapot\r\n\r\n'
		
	def handle_request_get(self, request):
		request_target = re.match("GET (\S*) (\S*)", request).group(1)
		
		payload = self.fetch_data(request_target)
		self.request.sendall(payload.encode())
		return


	#Return a status code of “405 Method Not Allowed” for any method you cannot handle (POST/PUT/DELETE)
	def unhandled_request(self, request):
		reply = 'HTTP/1.1 405 METHOD NOT ALLOWED\r\n\r\n'
		self.request.sendall(reply.encode())
		
	def parse_request(self, request):
		request_type = re.match("(\S*) (\S*) (\S*)(\r|\n|\b)", request)

		if request_type == None:
			self.unhandled_request(request)
			return

		if request_type.group(1) == 'GET':
			self.handle_request_get(request)
		else:
			self.unhandled_request(request)

if __name__ == "__main__":
	HOST, PORT = "localhost", 8080

	socketserver.TCPServer.allow_reuse_address = True
	# Create the server, binding to localhost on port 8080
	server = socketserver.TCPServer((HOST, PORT), MyWebServer)

	# Activate the server; this will keep running until you
	# interrupt the program with Ctrl-C
	server.serve_forever()
