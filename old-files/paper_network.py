import numpy as np
np.set_printoptions(threshold = 'nan')
#import gspread
#from oauth2client.service_account import ServiceAccountCredentials
from reference_v2 import *
from author import *
from sys import *
from igraph import *

# Use creds to create a client to interact with Google Drive API
# scope = ['https://spreadsheets.google.com/feeds']
# creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
# client = gspread.authorize(creds)

# # Find and open the spreadsheets
# favoritism_cooperation = client.open("favoritism_in_cooperation").sheet1
# moral_licensing = client.open("moral_licensing").sheet1
# syntactic_priming = client.open("syntactic.priming").sheet1

def main():
    if(len(argv) > 3 or len(argv) < 2):
        print "Usage: {0} input_file [-p]".format(argv[0])
        return -1
    references = []
    # Store each citation into a Reference object, add it to list of references
    with open(argv[1]) as inputFile:
        for citation in inputFile:
            if(citation != "\n"):
                ref = Reference(citation)
                ref.get_authors()
                references.append(ref)
    g = Graph()
    g.vs["name"] = []
    i = 0
    # Add a vertex to the graph for each reference
    for ref in references:
       g.add_vertices(1)
       g.vs[i]["name"] = ref.citation
       i += 1
    i = 0
    for r1 in references:
       for r2 in references[references.index(r1) + 1:]:
          num = float(r1.compare(r2)) / r1.total(r2)
          if num > 0:
             g.add_edges([(r1.citation, r2.citation)])
             g.es[i]["weight"] = num * 6
             i += 1
    if "-p" in argv:
        for ref in references:
            if g.degree(ref.citation) == 0:
                g.delete_vertices(ref.citation)

    # Read effect size values from spreadsheets
#    if argv[1] == "balliet.2014.references"

    visual_style = {}
#    visual_style["vertex_label"] = g.vs["name"]
    visual_style["vertex_size"] = [4 * (deg + 1) for deg in g.vs.degree()]
    visual_style["layout"] = "kk"
    visual_style["bbox"] = (1200, 700)
    visual_style["margin"] = (120, 25, 120, 25)
    visual_style["edge_width"] = g.es["weight"]
    plot(g, **visual_style)


if __name__ == "__main__":
   main()
