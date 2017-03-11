import time
import BaseHTTPServer
from twilio.rest import TwilioRestClient
import urlparse
import urllib2
from bs4 import BeautifulSoup
import string
import WolframInterface

account_sid = "AC4f02d451f59ae0003a8cf9e6d93cc62d"  # Account SID from www.twilio.com/console
auth_token = "471c765325b85fd73e3629a2ef1cbad1"  # Auth Token from www.twilio.com/console

client = TwilioRestClient(account_sid, auth_token)

# Only likes ASCII characters for some reason somewhere, need to apply,
# restrictions at some point

HOST_NAME = 'localhost'
PORT_NUMBER = 8080


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_POST(s):
        post_data = s.rfile.read(int(s.headers['Content-Length']))
        fields = urlparse.parse_qs(post_data)
        body = fields['Body'][0]
        phone_no = fields['From'][0]
        print(phone_no)
        print(body)
        wolf_answer = WolframInterface.respond(body)
        message = client.messages.create(body=wolf_answer,
                                         to=phone_no,  # Replace with your phone number
                                         from_="+441455561048")  # Replace with your Twilio number
        print("response: " + wolf_answer)

if __name__ == '__main__':
    response = urllib2.urlopen("https://www.google.com/")
    page_source = response.read()

    page_source = page_source.join(ch for ch in string.printable if ch.isalnum())

    soup = BeautifulSoup(page_source, "lxml")

    print(soup.prettify())

    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
