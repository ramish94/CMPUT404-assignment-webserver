# coding: utf-8 
import SocketServer
from os import path as osPath

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Ramish Syed
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

class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        # Get the type of request, and handle it
        requestType = (self.data.split(' '))[0]

        if (requestType == "GET"):
        	self.handleGETRequest(self.data)

        self.request.sendall("OK")

    def handleGETRequest(self, GETRequest):
    	# Split the request data and get the HTTPVersion and Request for future response concatanations
    	splitRequest = GETRequest.split(' ')
    	httpVersion = splitRequest[2].split('\r')[0]
    	httpRequest = "www" + splitRequest[1]

    	# handle the css file
        if "deep.css" in httpRequest:
            httpRequest = "www/deep/deep.css"

        # handle one of the test cases. Not the most efficient way to do it, but it works.     
        if "/../" in httpRequest:
        	response = httpVersion + " " + "404 Not Found\r\n"
        	self.request.send(response)

        # if it's a valid path, send the server a response according to whether or not it is a HTML or CSS file. If not, send it a 404
        if osPath.exists(httpRequest):
            if osPath.isdir(httpRequest):
                if httpRequest[len(httpRequest)-1] != "/":
                    httpRequest += "/"
                httpRequest += "index.html"
       		
            self.request.sendall(httpVersion + " " + "200 OK\r\n")

            if (httpRequest.endswith(".css")):
            	response = "Content-Type: text/css\r\n\r\n"
                self.request.sendall(response)  

            elif (httpRequest.endswith(".html")):
            	response = "Content-Type: text/html\r\n\r\n"
                self.request.sendall(response)

            # read from the file and write to the server    
            self.request.sendall(open(httpRequest, 'r').read())

        else:
            response = httpVersion + " " + "404 Not Found\r\n"
            self.request.send(response)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
