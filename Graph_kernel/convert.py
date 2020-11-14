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


def sgf_to_postman(filename):
    """
    Converts the SGF graph to list of edge tuples. Corresponding edge label are stored into edgeLabelMap dict.
    """
    edges = []
    edgeLabelMap = {}
    nodes = set()
    with open(filename) as f:
        lines = f.readlines()
        for idx in range(1, len(lines)):
            line = lines[idx]
            s, d, w, l = line.split()
            nodes.add(int(s))
            nodes.add(int(d))
            edge = (int(s), int(d), int(w))
            edges.append(edge)
            edgeLabelMap[edge] = l

    return edges, edgeLabelMap, list(nodes)


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
        weight = e[2]
        label = edgeLabelMap[e]
        if e in new_edges:
            weight += 1
        elif revE in new_edges:
            weight += 1
        f.write("%d\t%d\t%d\t%s\n" % (e[0],e[1],weight,label))
    f.close()
            

def main_sub(rootDir, f, outDir, log=False, graphml=True):
    """
    Tasks for each file:
    - Reads graphml, makes eularian and writes into a format that LP writer can understand
    """
    if graphml:
        g = get_graph(rootDir+f)
        # print(f)
        supermitch, edgeLabelMap = get_postman_format(g)
        # print(edgeLabelMap)
        # print(supermitch)
        graph_nodes = g.nodes()
    else:
        supermitch, edgeLabelMap, graph_nodes = sgf_to_postman(rootDir+f)
        
    new_edges = chinese_postman(supermitch)
    write_ali_input(outDir + "/"+f.split(".")[0] + '.sgf', graph_nodes, supermitch, new_edges, edgeLabelMap)
    
    if log:
        log_file = outDir + "/"+f.split(".")[0]+'.log'
        write = "Number of added edges to make the graph Eulerian: " + str(len(new_edges))
        for edge in new_edges:
            write += '\n' + str(edge)
        
        with open(log_file, 'w') as f:
            f.write(write)
    
    return len(new_edges)


def main(argv):
    rootDir = argv[0]
    outDir = argv[1]


    graphml_flag = False
    log_flag = False
    summary_flag = False

    try:
        opts, args = getopt.getopt(argv[2:],"hg:l:s:",["graphml","log","summary"])
    except getopt.GetoptError:
        print('Error! Correct usage:\npython convert.py <input_directory> <output_directory> [options]\noptions:\n\t--graphml: when the input graphs are in graphml format\n\t--log: save logs about changes made to each graph\n\t--summary: summary of the changes made to all the graphs in the directory')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Correct usage:\npython convert.py <input_directory> <output_directory> [options]\noptions:\n\t--graphml: when the input graphs are in graphml format\n\t--log: save logs about changes made to each graph\n\t--summary: summary of the changes made to all the graphs in the directory')
            sys.exit()
        elif opt in ("-g", "--graphml"):
            graphml_flag = True
        elif opt in ("-l", "--log"):
            log_flag = True
        elif opt in ("-s", "--summary"):
            summary_flag = True
    
    print('-----------------Options--------------------')
    print("graphml option", graphml_flag)
    print("log option", log_flag)
    print("summary option", summary_flag)
    print('--------------------------------------------')


    if not os.path.exists(outDir):
        os.makedirs(outDir)

    files = os.listdir(rootDir)
    new_edges_count_list = []
    for i,f in enumerate(files):
        new_edges_count = main_sub(rootDir, f, outDir, log=log_flag, graphml=graphml_flag)
        new_edges_count_list.append(new_edges_count)
        if (i+1)%100 == 0:
            print(i, "complete...")
    print("Complete...")


    if summary_flag:
        import numpy as np
        print('-----------------Summary--------------------')
        print('Avg new edges added: ', np.mean(new_edges_count_list))
        print('Std new edges added: ', np.std(new_edges_count_list))
        print('Max new edges added: ', np.max(new_edges_count_list))
        print('Min new edges added: ', np.min(new_edges_count_list))



if __name__ == "__main__":
    import sys
    import getopt
    import os
    if len(sys.argv) < 3:
        print("Usage: ", sys.argv[0], "<input graphml dir>", "<output dir>", "[options]")
        exit(1)
    main(sys.argv[1:])


