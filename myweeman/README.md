Weeman - HTTP server for phishing


About:
------

HTTP server for phishing in python.
Usually you will want run Weeman with DNS spoof attack.

Weeman will do the following steps:
------------------------------------

1. Create fake html page.
2. Wait for clients
3. Grab the data (POST).
4. Try to login the client to the original page 

Requirements:
-------------

* Python3
* Python BeautifulSoup 4


Platforms
-----------

* Linux (any)
* Mac (Not tested)
* Windows (Not tested)


Usage
------

Just type `help`

Run server:
-----------

* set the website to clone
> set url http://www.facebook.com

* set the url where you want to redirect the victim after they give username and password, example for facebook
> set action_url http://www.facebook.com

* set the port Weeman server will listen
> set port port_no (ex: 8080)

* Start the server
> run


