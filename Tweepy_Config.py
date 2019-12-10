#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 12:04:12 2019

@author: akshaypunwatkar
"""

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import socket
import json
import re


# Set up your credentials
consumer_key    = 'qeOHPPgeHflJgixKFTVF1TUXk'
consumer_secret = 'CfDFI0Eyg75p61qOjBHb4XDU0dJdZRt4mICEzmjblqKe26M5I1'
access_token    = '96082570-hxSpQU4SBskn4hYweizzsgnBKfvfgipyvuvVES5ac'
access_secret   = 'cNgDJQYTcQKpqpT5D2AUMx2u19TQYLCSBDkwIasZohctZ'

class TweetsListener(StreamListener):

  def __init__(self, csocket):
      self.client_socket = csocket

  def on_data(self, data):
      try:
          #Changing candidate name corresponding to filters
        
          #candidate = 'Bernie_Sanders'
          candidate = 'Pete_Buttigieg'
          #candidate = 'Cory_Booker'
          #candidate = 'Andrew_Yang'
          #candidate = 'Kamala_Harris'
          #candidate = 'Joe_Biden'
          #candidate = 'Elizabeth_Warren'

          
          msg = json.loads(data)
          
          tweet = str(msg['text'].encode('utf-8'))
          device = str(msg['source'])
          device_stripped = re.findall(r"\>(.*?)\<",device)
          location = str(msg['user']['location']).strip()
          
          print( msg['text'].encode('utf-8') )
          
          f = open("twitter_data.tsv", "a")
          f.write(tweet+"\t"+device_stripped[0]+"\t"+location+"\t"+candidate+"\n")
          f.close()
          self.client_socket.send( msg['text'].encode('utf-8') )
          
          return True
      except BaseException as e:
          print("Error on_data: %s" % str(e))
      return True

def on_error(self, status):
      print(status)
      return True

def sendData(c_socket):
  auth = OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_secret)

  twitter_stream = Stream(auth, TweetsListener(c_socket))
    
  #filters = ['berniesanders', 'BernieSanders2020', 'sanders', 'berni2020']
  filters = ['petebuttigiegforpresident','peteforamerica','petebuttigieg','buttigieg','mayorpete']
  #filters = ['CoryBooker','corybooker','SenBooker'] 
  #filters = ['yang2020','AndrewYang','andrewyang','yanggang2020'] 
  #filters = ['KamalaHarris','kamalaharris','kamalaharris2020']
  #filters = ['joebiden','biden2020','biden']
  #filters = ['ElizabethWarren','elizabethwarren','senwarren','SenWarren','ewarren']

  # Election - ['2020election','election2020','presidentialelection','2020poll','2020_presidential_election']  

  # Biden > Bernie > harris > Pete > warren 

  
  
  twitter_stream.filter(track=filters)

if __name__ == "__main__":
  s = socket.socket()         # Create a socket object
  host = "127.0.0.1"          # Get local machine name
  port = 5556        # Reserve a port for your service.
  s.bind((host, port))        # Bind to the port

  print("Listening on port: %s" % str(port))

  s.listen(5)                 # Now wait for client connection.
  c, addr = s.accept()        # Establish connection with client.

  print( "Received request from: " + str( addr ) )

  sendData( c )

