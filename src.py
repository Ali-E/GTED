import SCC
import readAssemb as ra
import cpp
import os
import errno


def write_graph(edges, num_node, filename):
    file = open(filename, 'w')
    string = ''
    string += str(num_node) + ' ' + str(len(edges)) + '\n'
    for edge in edges:
        string += str(edge[0]) + ' ' + str(edge[1]) + ' ' + str(edge[2]) + ' ' + edge[3] + '\n'
    file.write(string)
    file.close()


if __name__ == '__main__':
    import sys
    num_files = int(sys.argv[1])

    filename_1 = ''
    graph_1, g_list_1, g_map_1, inv_map_1, graph_2, g_list_2, g_map_2, inv_map_2 = [None] * 8

    if num_files == 22:
        filename_1 = sys.argv[2]
        filename_2 = sys.argv[3]
        graph_1, g_list_1, g_map_1, inv_map_1 = ra.read_gr(filename_1)
        graph_2, g_list_2, g_map_2, inv_map_2 = ra.read_gr(filename_2)

    elif num_files == 0:
        filename_1 = sys.argv[2]
        graph_1, graph_2, g_list_1, g_list_2, g_map_1, g_map_2, inv_map_1, inv_map_2 = \
            ra.read_graphs(filename_1)

    elif num_files == 1:
        filename_1 = sys.argv[2]
        graph_1, graph_2, g_list_1, g_list_2, g_map_1, g_map_2, inv_map_1, inv_map_2 = \
            ra.read_graphs_1(filename_1)

    elif num_files == 2:
        filename_1 = sys.argv[2]
        graph_1, graph_2, g_list_1, g_list_2, g_map_1, g_map_2, inv_map_1, inv_map_2 = \
            ra.read_graphs_2(filename_1)

    print("Reading the graphs, done!")

    scc_list_1 = SCC.get_scc_final(graph_1, g_list_1, g_map_1, inv_map_1, 10)
    scc_list_2 = SCC.get_scc_final(graph_2, g_list_2, g_map_2, inv_map_2, 5)

    print("Found SCCs, done!")

    graph_list_1 = []
    graph_list_2 = []
    num_nodes_1 = []
    num_nodes_2 = []


    print("first graph:")
    for graph in scc_list_1:
        print('------------')
        print("nodes: ", len(graph.keys()))
        edges, edges_map = cpp.get_postman_format(graph)
        print("edges: ", len(edges))
    print("second graph:")
    for graph in scc_list_2:
        print('------------')
        print("nodes: ", len(graph.keys()))
        edges, edges_map = cpp.get_postman_format(graph)
        print("edges: ", len(edges))

    for graph in scc_list_1:
        if len(graph.keys()) > 1:
            print("graph 1: ", len(graph.keys()))
            final_edges = cpp.add_new_edges_1(graph)
            print("edges 1: ", len(final_edges))
            graph_list_1.append(final_edges)
            num_nodes_1.append(len(graph.keys()))
    for graph in scc_list_2:
        if len(graph.keys()) > 1:
            print("graph 2: ", len(graph.keys()))
            final_edges = cpp.add_new_edges_1(graph)
            print("edges 2: ", len(final_edges))
            graph_list_2.append(final_edges)
            num_nodes_2.append(len(graph.keys()))

    """
    for graph in scc_list_1:
        if len(graph.keys()) > 1:
            print("graph 1: ", len(graph.keys()))
            final_edges = cpp.add_new_edges(graph)
            print("edges 1: ", len(final_edges))
            graph_list_1.append(final_edges)
            num_nodes_1.append(len(graph.keys()))
    for graph in scc_list_2:
        if len(graph.keys()) > 1:
            print("graph 2: ", len(graph.keys()))
            final_edges = cpp.add_new_edges(graph)
            print("edges 2: ", len(final_edges))
            graph_list_2.append(final_edges)
            num_nodes_2.append(len(graph.keys()))
    """
    print("Made Eulerian, done!")

    file_1 = filename_1.split('.')[0] + '/' + filename_1.split('.')[0] + '_src'+ str(num_files) + '_1_'
    if not os.path.exists(os.path.dirname(file_1)):
        try:
            os.makedirs(os.path.dirname(file_1))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    file_2 = filename_1.split('.')[0] + '/' + filename_1.split('.')[0] + '_src' + str(num_files) + '_2_'
    if not os.path.exists(os.path.dirname(file_2)):
        try:
            os.makedirs(os.path.dirname(file_2))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    for idx, graph in enumerate(graph_list_1):
        write_graph(graph, num_nodes_1[idx], file_1+str(idx))
    for idx, graph in enumerate(graph_list_2):
        write_graph(graph, num_nodes_2[idx], file_2+str(idx))

