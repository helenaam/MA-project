import numpy as np
np.set_printoptions(threshold = "nan")
from author import *
from reference_v2 import *
from igraph import *
import sys

# Gets network data (vertex/edge betweenness, clusters) from network of authors
# and stores it in a file
def get_data_authors(g, filename):
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

# Gets network data (vertex/edge betweenness, clusters) from network of papers
# and stores it in a file
def get_data_papers(g, filename):
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
