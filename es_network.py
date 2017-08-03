import numpy as np
np.set_printoptions(threshold = 'nan')
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from reference_v2 import *
from author import *
import sys
from igraph import *
#import cPickle
#import pickle

# Use creds to create a client to interact with Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Refresh data in the file by reading from Google spreadsheet
def refresh(filename):
    # Pickle doesn't work :(
#    pickle = cPickle.Pickler(open(filename, "wb"))
#    ppickle = pickle.Pickler(open(filename, "wb"))
    # Find and open the correct spreadsheet
    sheet = client.open(filename).sheet1
    # Store each citation into a Reference object, add it to list of references
    references = []
    effect_col = sheet.find("ES").col
    for i in xrange(sheet.row_count - 2):
        ref = Reference(sheet.cell(i+2, 1).value)
        ref.get_authors()
        references.append(ref)
        # Read data from spreadsheet
        ref.effect = sheet.cell(i+2, effect_col).value
        ref.experiment = sheet.cell(i+2, 3).value
        j = 4
        while sheet.cell(1, j).value[:15] == "condition_type_":
            condition = sheet.cell(i+2, j).value
            if condition != '':
                ref.conditions.append(condition)
            j += 1
    # Print data about references into file (since pickle doesn't work)
    with open(filename, "w") as file:
        for r in references:
            # citation\tauthor0;author0.conn0;...,author1;...\teffect\texperiment\t
            file.write("{0}\t".format(r.citation.encode('utf-8')))
            for a in r.authors:
                file.write("{0};".format(a.name.encode('utf-8')))
                for conn in a.connections[:len(a.connections) - 1]:
                    file.write("{0};".format(conn.name.encode('utf-8')))
                if len(a.connections) > 0:
                    file.write("{0},".format(a.connections[len(a.connections) - 1].encode('utf-8')))
            file.write("\t{0}\t{1}\t".format(r.effect.encode('utf-8'), r.experiment.encode('utf-8')))
            for c in r.conditions[:len(r.conditions) - 1]:
                file.write("{0},".format(c))
            file.write("{0}\n".format(r.conditions[len(r.conditions) - 1]))
#    for r in references:
#        ppickle.dump(r)
#    pickle.dump(references)
    return references

# Read in spreadsheet data from file on the computer
def read_refs(filename):
    references = []
    with open(filename, "r") as file:
        for r in file:
            info = r.strip().split('\t')
            ref = Reference(info[0])
#             auth = info[1].strip().split(',')
#             parts = auth.strip().split(';')
#             for a in auth:
#                 ref.authors.append(a)
            ref.get_authors()
            ref.effect = info[2]
            ref.experiment = info[3]
            cond = info[4].strip().split(',')
            for c in cond:
                ref.conditions.append(c)
            references.append(ref)
    # Pickle doesn't seem to work on Reference objects :(
#     with open(filename, "rb") as file:
#         unpickle = cPickle.Unpickler(file)
#         references = unpickle.load()
    return references

# Returns a list of all the references that meet the given condition at the
# given index (equal to condition number - 1)
def get_refs(reflist, index, condition):
    refs = []
    for r in reflist:
        if len(r.conditions) > index and r.conditions[index] == condition:
            refs.append(r)
    return refs

def main():
    if(len(sys.argv) < 2 or len(sys.argv) > 3):
        print "Usage: {0} sheet_name [-r]".format(sys.argv[0])
        return -1
    # If needed, refresh data in input file
    if "-r" in sys.argv:
        references = refresh(sys.argv[1])
    repeat = 'Y'
    while repeat == 'Y' or repeat == 'y':
        references = read_refs(sys.argv[1])
    # Read conditions as input from user, get references matching those conditions
        num_conditions = len(references[0].conditions)
        for i in xrange(num_conditions):
            condition = raw_input("condition {0}: ".format(i+1))
            if condition != "anything":
                references = get_refs(references, i, condition)
    # Combine remaining references to the same paper
        for r1 in references:
            matches = []
            for r2 in references[references.index(r1) + 1:]:
                if r1.citation == r2.citation:
                    references.remove(r2)
                    matches.append(float(r2.effect))
            r1.effect = (sum(matches) + float(r1.effect)) / (len(matches) + 1)
            r1.experiment = 0
    # Add vertex for each data point
        g = Graph()
        g.vs["name"] = []
        g.vs["effect"] = []
        i = 0
        for r in references:
            g.add_vertices(1)
            g.vs[i]["name"] = r.citation
            g.vs[i]["effect"] = r.effect
            i += 1
        i = 0
    # Calculate edge weights
        for r1 in references:
            for r2 in references[references.index(r1) + 1:]:
                num = float(r1.compare(r2)) / r1.total(r2)
                if num > 0:
                    g.add_edges([(r1.citation, r2.citation)])
                    g.es[i]["weight"] = num * 6
                    i += 1
    # Plot graph
        if len(references) > 0:
            min_effect = min(float(g.vs['effect'][v.index]) for v in g.vs)
            colors = RainbowPalette(n = (max(float(g.vs['effect'][v.index]) for v in g.vs) - min_effect) * 100 + 1, end = .8)
            visual_style = {}
            visual_style['vertex_color'] = [colors[int((float(g.vs['effect'][v.index]) - min_effect) * 100)] for v in g.vs]
            visual_style["vertex_label"] = ["%.2f" % (float(g.vs['effect'][v.index])) for v in g.vs]
            visual_style['vertex_label_dist'] = 1.5
            visual_style['vertex_label_size'] = 18
            visual_style["vertex_size"] = 15
            visual_style["bbox"] = (1200, 700)
            visual_style["margin"] = (120, 40, 120, 40)
            if len(g.es) > 0:
                visual_style['layout'] = "kk"
                visual_style["edge_width"] = g.es["weight"]
            else:
                visual_style['layout'] = "random"
            plot(g, **visual_style)
        else:
            print "No references found for given conditions"
        repeat = raw_input("Graph another reference? ")
        while repeat != 'y' and repeat != 'Y' and repeat != 'n' and repeat != 'N':
            print "Please enter either 'y' or 'n'"
            repeat = raw_input("Graph another reference? ")

if __name__ == "__main__":
   main()