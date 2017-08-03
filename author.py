import numpy as np

class Author(object):
      def __init__(self, name):
      	  self.name = name
          self.connections = []

      def compare(self, auth2):
            if(self.name == auth2.name):
                  return True
            else:
                  return False
