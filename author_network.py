# coding: utf-8

import numpy as np
np.set_printoptions(threshold = 'nan')
from reference_v2 import *
from author import *
from sys import *
from igraph import *
import fix_dendrogram
import operator

def get_data(g, filename):
    # Get betweenness data and write it to the file
    with open(filename, 'w') as file:
        file.write("Vertex betweenness\n\n")
        vertices = []
        i = 0
        for v in g.vs:
            betweenness = g.betweenness()[v.index]
            g.vs[i]['betweenness'] = betweenness
            i += 1
            if betweenness > 0:
                vertices.append(v)
        vertices.sort(key = operator.itemgetter('betweenness'), reverse = True)
        for v in vertices:
            file.write("%s: %.2f\n" % (v['name'], g.betweenness()[v.index]))
        file.write("\n\n")
    # Get cluster data and write it to the file
        file.write("Clusters\n\n")
        clusters = g.clusters(mode = STRONG)
        for c in clusters:
            if len(c) >= 5:
                for vertex in c:
                    file.write(g.vs[vertex]["name"])
                    if c.index(vertex) < len(c) - 1:
                        file.write(", ")
                file.write("\n\n")
        file.write("\n")
    # Get edge betweenness data and write to file
        file.write("Edge betweenness\n\n")
        edges = []
        i = 0
        for e in g.es:
            eb = g.edge_betweenness()[e.index]
            g.es[i]['betweenness'] = eb
            i += 1
            if eb > 1:
                edges.append(e)
        edges.sort(key = operator.itemgetter('betweenness'), reverse = True)
        for e in edges:
            file.write("%s, %s: %.2f\n" % (g.vs[e.source]['name'], g.vs[e.target]['name'], g.edge_betweenness()[e.index]))

def main():
    if(len(argv) < 2 or len(argv) > 4):
        print "Usage: {0} input_file [-d][-p]".format(argv[0])
        return -1
    references = []
    # Store each citation into a Reference object, add it to list of references
    with open(argv[1], "r") as inputFile:
        for citation in inputFile:
            if(citation != "\n"):
                ref = Reference(citation)
                ref.get_authors()
                references.append(ref)
    hashtable = {}
    # Record the connections between authors
    g = Graph()
    j = 0
    g.vs["name"] = []
    for ref in references:
        for auth in ref.authors:
            if auth.name not in hashtable.keys() and auth.name != "":
                hashtable[auth.name] = auth
                g.add_vertices(1)
                g.vs[j]["name"] = auth.name
                j += 1
            for i in range(where(ref.authors == auth)[0] + 1, len(ref.authors)):
                if ref.authors[i] != "":
                    if ref.authors[i].name not in hashtable.keys():
                        hashtable[ref.authors[i].name] = ref.authors[i]
                        g.add_vertices(1)
                        g.vs[j]["name"] = ref.authors[i].name
                        j += 1
            for auth2 in ref.authors:
                if auth2.name != auth.name and auth2.name != "" and auth.name != "":
                    auth.connections.append(auth2)
    # Create an adjacency matrix of the graph
    adjacency = {}
    for name1 in hashtable.keys():
        adjacency[name1] = {}
        for name2 in hashtable.keys():
            adjacency[name1][name2] = 0
    for ref in references:
        for auth1 in ref.authors:
            for auth2 in ref.authors:
                adjacency[auth1.name][auth2.name] += 1
    # Use adjacency matrix to calculate edge weights
    i = 0
    for name1 in adjacency.keys():
        for name2 in adjacency.keys():
            if adjacency[name1][name2] > 0 and name1 != name2:
                if not g.are_connected(name1, name2):
                    g.add_edges([(name1, name2)])
                    g.es[i]["weight"] = adjacency[name1][name2]
                    i += 1
    # Read data from graph into file
    if "-d" in sys.argv:
        get_data(g, "data/" + sys.argv[1][:sys.argv[1].index("references")] + "dataa")
    # Plot graph
    if "-p" in sys.argv or "-d" not in sys.argv:
        clusters = g.clusters(mode = STRONG)
        colors = RainbowPalette(n = len(g.vs))
        visual_style = {}
        visual_style["vertex_size"] = [5 * (deg + 2) for deg in g.vs.degree()]
        visual_style["vertex_label"] = g.vs["name"]
        visual_style["vertex_color"] = [colors[clusters[clusters.membership[v.index]][len(clusters[clusters.membership[v.index]]) / 2]] for v in g.vs]
        visual_style["layout"] = "kk"
        visual_style["bbox"] = (1200, 700)
        visual_style["margin"] = (60, 20, 60, 20)
        visual_style["edge_width"] = g.es["weight"]
        plot(g, **visual_style)
        
if __name__ == "__main__":
    main()
