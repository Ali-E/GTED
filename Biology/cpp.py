from chinesepostman import eularian, network
import readAssemb as ra


def get_postman_format(graph):
    edges = []
    edges_map = {}
    for node in graph.keys():
        for edge in graph[node]:
            new_edge = (node, edge[0], edge[1])
            edges.append(new_edge)
            edges_map[(node, edge[0])] = (edge[1], edge[2])
    return edges, edges_map


def chinese_postman(edges):
    original_graph = network.Graph(edges)
    # print('{} edges'.format(len(original_graph)))
    new_edges_toadd = []
    if not original_graph.is_eularian:
        print('Converting to Eularian path...')
        new_edges_toadd = eularian.make_eularian2(original_graph)
        print('New edges found...')
    else:
        new_edges_toadd = []
    return new_edges_toadd


def chinese_postman_1(edges):
    pass


def add_new_edges(graph):
    final_edges = []
    edges, edges_map = get_postman_format(graph)
    # print(len(edges))
    new_edges_toadd = chinese_postman(edges)
    # print("new to add: ", new_edges_toadd)
    for edge in new_edges_toadd:
        key = (edge[0], edge[1])
        prev_edge = edges_map[key]
        edges_map[key] = (prev_edge[0]+edge[2], prev_edge[1])
        # new_edge = (edge[0], edge[1], edge[2]+prev_edge[0], prev_edge[1])
        # final_edges.append(new_edge)
    for edge in edges_map.keys():
        final_edges.append((edge[0], edge[1], edges_map[edge][0], edges_map[edge][1]))
    return final_edges


def add_new_edges_1(graph):
    final_edges = []
    for node in graph.keys():
        for edge in graph[node]:
            final_edges.append((node, edge[0], edge[1], edge[2]))
    return final_edges


def add_new_edges_eff(graph):
    final_edges = []



if __name__ == '__main__':
    graph, g_list, g_map, inv_map = ra.read_gr('g_eulerian')
    print(graph)
    final_edges = add_new_edges(graph)
    print(final_edges)
