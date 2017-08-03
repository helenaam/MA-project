from numpy import *
from author import *

class Reference(object):

      def __init__(self, citation):
          self.citation = citation
          self.authors = []
          self.effect = 0
          self.experiment = ""
          self.conditions = []

      def count_auth(self):
            count = 0
            num_commas = 0
            curr = self.citation[0]
            i = 0
            while(curr != '('):
                  if(curr == ',' and (self.citation[i+2] != 'J' or self.citation[i+3] != 'r' or self.citation[i+4] != '.')):
                        num_commas += 1
                  i += 1
                  curr = self.citation[i]
                  if num_commas is 2:
                        count += 1
                        num_commas = 0
            count += 1
            return count

# This version of the get_authors() function treats all authors with the same last name
# as the same author, regardless of the other initials

      def get_authors(self):
            num = self.count_auth()
            name = ""
            commas = 0
            pos = 0
            index = 0
            c = self.citation[pos]
            if(c == '*'):
                  pos += 1
                  c = self.citation[pos]
            for i in xrange(num):
                  index = 0
                  while(c != ','):
                        name += c
                        index += 1
                        pos += 1
                        c = self.citation[pos]
                  pos += 2
                  c = self.citation[pos]
                  while c != ',' and c != '(':
                        pos += 1
                        c = self.citation[pos]
                  if c == ',':
                        pos += 2
                        c = self.citation[pos]
                  if(c == '&'):
                        pos += 2
                        c = self.citation[pos]
                  name = name[:index] #+ '\0'
                  if(name[0] == '.' and name[2] == '.' and name[4] == '.'):
                        if name[5] == ' ':
                              name = name[6:]
                        else:
                              name = name[5:]
                  self.authors.append(Author(name))
                  name = ""
            self.authors = array(self.authors)

      # Returns the number of authors in common with ref2
      def compare(self, ref2):
            common = 0
            for i in xrange(self.count_auth()):
                  for j in xrange(ref2.count_auth()):
                        if(self.authors[i].compare(ref2.authors[j])):
                              common += 1
            return common

      # Returns total number of distinct authors in self and ref2
      def total(self, ref2):
            return self.count_auth() + ref2.count_auth() - self.compare(ref2)
