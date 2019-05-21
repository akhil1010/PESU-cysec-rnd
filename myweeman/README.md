Weeman - HTTP server for phishing


DISCLAIMER
-----------

Usage of Weeman for attacking targets without prior mutual consent is illegal.

About:
------

HTTP server for phishing in python.
Usually you will want run Weeman with DNS spoof attack.

Weeman will do the following steps:
------------------------------------

1. Create a fake html page.
2. Wait for clients.
3. Grab the data (POST).
4. Try to login the client to the original page. 

Requirements:
-------------

1. Python3
2. Python BeautifulSoup 4


Platforms:
----------

* Linux (any)


Usage:
------

Type 'help'

Run server:
-----------

* Set the website to clone:   
	 weeman>> set url http://www.facebook.com

* Set the url where you want to redirect the victim after they give username and password, example for facebook:   
	 weeman>> set action_url http://www.facebook.com

* Set the port Weeman server will listen:   
	 weeman>> set port port_no (ex: 8080)

* Start the server:   
	 weeman>> run


