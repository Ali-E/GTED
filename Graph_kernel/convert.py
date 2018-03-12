from copy import deepcopy

from pygraphml import Graph
from pygraphml import GraphMLParser
from chinesepostman import eularian, network
import xml

def get_graph(filename):
    """
    Reads a graphml file
    """
    try:
        g = Graph()
        parser = GraphMLParser()
        g = parser.parse(filename)
        return g
    except xml.parsers.expat.ExpatError as e:
        print(e)


def get_postman_format(graph):
    """
    Converts the pygraphml graph to list of edge tuples. Corresponding edge label are stored into edgeLabelMap dict.
    """
    edges = []
    edgeLabelMap = {}
    for e in graph.edges():
        sourceNode = int(e.node1['label'].replace("n",""))
        destNode = int(e.node2['label'].replace("n",""))
        key = (sourceNode, destNode,1)
        edges.append(key)
        # if there's edge label use it else concat node labels as "v1.v2" to form edge label.
        if 'e_label' in e.attributes():
            edgeLabelMap[key]=e['e_label']
        else:
            edgeLabelMap[key]=str(e.node1['v_label'])+"."+str(e.node2['v_label'])
    return edges, edgeLabelMap

def chinese_postman(edges):
    """
    Returns minimum edges to add to graph to make it eularian using chinese postman.
    """
    original_graph = network.Graph(edges)

    #print('{} edges'.format(len(original_graph)))
    new_edges_toadd = []
    if not original_graph.is_eularian:
        new_edges_toadd = eularian.make_eularian2(original_graph)
    else:
        new_edges_toadd = []

    return new_edges_toadd

def write_ali_input(filename, nodes, edges, new_edges, edgeLabelMap):
    """
    Write the eularian graph into file in the format that LP writer can understand
    """
    f = open(filename, 'w')
    f.write("%d\t%d\n" % (len(nodes), len(edges)))
    for e in edges:
        revE = (e[1],e[0],e[2])
        weight = 1
        label = edgeLabelMap[e]
        if e in new_edges:
            weight += 1
        elif revE in new_edges:
            weight += 1
        f.write("%d\t%d\t%d\t%s\n" % (e[0],e[1],weight,label))
    f.close()
            
def main(rootDir, f, outDir):
    """
    Tasks for each file:
    - Reads graphml, makes eularian and writes into a format that LP writer can understand
    """
    g = get_graph(rootDir+f)
    supermitch, edgeLabelMap = get_postman_format(g)
    new_edges = chinese_postman(supermitch)
    write_ali_input(outDir + "/"+f.split(".")[0], g.nodes(), supermitch, new_edges, edgeLabelMap)

if __name__ == "__main__":
    import sys
    import os
    if len(sys.argv) < 3:
        print("Usage: ", sys.argv[0], "<input graphml dir>", "<output dir>")
        exit(1)

    #sys.stdout = open(os.devnull, 'w')
    rootDir = sys.argv[1]
    outDir = sys.argv[2]
    if not os.path.exists(outDir):
        os.makedirs(outDir)

    files = os.listdir(rootDir)
    for i,f in enumerate(files):
        main(rootDir, f, outDir)
        if (i+1)%100 == 0:
            print(i, "complete...")
    print("Complete...")
