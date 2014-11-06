#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import urllib, threading, os, re
from Queue import Queue

PORT_NUMBER = 8000


# NB: http://www.bbc.co.uk/iplayer/episode/b04mqc4z/<something>
g_rex = re.compile("http://www.bbc.co.uk/iplayer/episode/([0-9a-z]{8})/.+")
g_Queue = Queue()


class Worker(threading.Thread):
  def run(self):
    while True:
      pid = g_Queue.get()
      os.system("./get_iplayer/get_iplayer --pid=%s" % pid)


class DownloadHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    url = urllib.unquote(self.path[1:])
    m = g_rex.match(url)
    if m:
      pid = m.groups()[0]
      g_Queue.put(pid)
      print "Queued PID for download:", pid
    else:
      print "Can't handle URL:", url
    self.send_response(200)
    self.end_headers()
    self.wfile.write("OK")


if __name__ == "__main__":
  server = HTTPServer(('localhost', PORT_NUMBER), DownloadHandler)
  print 'Started download server on port ', PORT_NUMBER
  worker = Worker()
  worker.start()
  server.serve_forever()

	