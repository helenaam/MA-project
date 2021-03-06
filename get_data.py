import numpy as np
np.set_printoptions(threshold = "nan")
from author import *
from reference_v2 import *
from igraph import *
import sys
import os
import matplotlib.pyplot as plt

def vbetween(g):
    i = 0
    for v in g.vs:
        betweenness = g.betweenness()[v.index]
        g.vs[i]['betweenness'] = betweenness
        i += 1
    return g

def ebetween(g):
    i = 0
    for e in g.es:
        eb = g.edge_betweenness()[e.index]
        g.es[i]['betweenness'] = eb
        i += 1
    return g

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
    # If graph contains no vertices, end function
    if len(g.vs) == 0:
        return
    data = False
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
            if len(vertices) > 0:
                data = True
        vertices.sort(key = operator.itemgetter('betweenness'), reverse = True)
        for v in vertices:
            file.write("%.2f (" % (v['effect']))
            v["authors"] = v["authors"].tolist()
            for a in v["authors"]:
                file.write("%s" % a.name)
                if v["authors"].index(a) < len(v["authors"]) - 1:
                    file.write(", ")
            file.write("): %.2f\n" % v['betweenness'])
        file.write("\n\n")
        # Get cluster data and write it to the file
        file.write("Clusters\n\n")
        clusters = g.clusters(mode = STRONG)
        for c in clusters:
            if len(c) >=  5:
                data = True
                # Write the list of effect sizes
                effects = []
                for vertex in c:
                    v = g.vs[vertex]
                    effects.append(v["effect"])
                    file.write("%.2f" % v["effect"])
                    if c.index(vertex) < len(c) - 1:
                        file.write(", ")
                file.write("\n")
                # Record the mean and standard deviation of effect sizes
                file.write("Mean: %.2f\n" % np.mean(effects))
                file.write("Standard deviation: %.2f\n" % np.std(effects))
                # Calculate average effect size difference within cluster
                diff = []
                for vertex1 in c:
                    v1 = g.vs[vertex]
                    for vertex2 in c[:c.index(vertex1)]:
                        v2 = g.vs[vertex2]
                        diff.append(abs(v1['effect'] - v2['effect']))
                file.write("Average difference: %.2f\n" % abs(np.mean(diff)))
                # Record the size of the cluster
                file.write("Cluster size: %d\n" % len(c))
                # Record authors of each paper in cluster
                for vertex in c:
                    v = g.vs[vertex]
                    file.write("\t")
                    for author in v["authors"][:len(v["authors"]) - 1]:
                        file.write(author.name + ", ")
                    file.write(v["authors"][len(v["authors"]) - 1].name + "\n")
                file.write("\n")
        # Calculate mean and standard deviation of effect sizes in network
        file.write("Network mean: %.2f\n" % np.mean(g.vs['effect']))
        file.write("Network standard deviation: %.2f\n" % np.std(g.vs['effect']))
        # Record average ES difference for whole network
        diff = []
        for v1 in g.vs:
            for v2 in g.vs[:v1.index]:
                diff.append(abs(v1['effect'] - v2['effect']))
        file.write("Average difference: %.2f\n" % abs(np.mean(diff)))
        # Record size of network
        file.write("Network size: " + str(len(g.vs)) + "\n\n")
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
        if len(edges) > 0:
            data = True
        edges.sort(key = operator.itemgetter('betweenness'), reverse = True)
        for e in edges:
            file.write("%.2f, %.2f ([" % (g.vs[e.source]["effect"], g.vs[e.target]["effect"]))
            for auth in g.vs[e.source]['authors'][:len(g.vs[e.source]['authors']) - 1]:
                file.write(auth.name + ", ")
            file.write(g.vs[e.source]['authors'][len(g.vs[e.source]['authors']) - 1].name + "] to [")
            for auth in g.vs[e.target]['authors'][:len(g.vs[e.target]['authors']) - 1]:
                file.write(auth.name + ", ")
            file.write(g.vs[e.target]['authors'][len(g.vs[e.target]['authors']) - 1].name + "]): %.2f\n" % e['betweenness'])
        if not data:
            os.remove(filename)

# Creates a scatterplot of effect size vs vertex betweenness
def scatterplot(g):
    g = vbetween(g)
    x = g.vs['betweenness']
    y = g.vs['effect']
    plt.scatter(x, y)
    plt.xlabel('Betweenness centrality')
    plt.ylabel('Effect size')
    plt.show()
