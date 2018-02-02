import math
import numpy as np
import json

gap_penalty = 1
mismatch_penalty = 1
match_reward = 0


def read_gr(filename):
    """Reas a single graph from a file."""
    f = open(filename, "r")
    string = f.readline().split()
    num_nodes = int(string[0])
    num_edges = int(string[1])
    graph = {}
    indeg_graph = {}
    g_map = {}
    inv_map = {}
    g_list = []
    counter = 0
    for line in f:
        line = line.split()
        u = int(line[0])
        v = int(line[1])
        weight = int(float(line[2]))
        label = line[3]
        if u not in graph:
            graph[u] = [(v, weight, label)]
            g_map[u] = counter
            inv_map[counter] = u
            counter += 1
        else:
            graph[u].append((v, weight, label))
        #######
        if v not in graph:
            graph[v] = []
            g_map[v] = counter
            inv_map[counter] = v
            counter += 1

        if v not in indeg_graph:
            indeg_graph[v] = [(u, weight, label)]
        else:
            indeg_graph[v].append((u, weight, label))
        if u not in indeg_graph:
            indeg_graph[u] = []

        #######

    # g_list = [i for i in range(len(g_map))]
    f.close()
    return graph, g_list, g_map, inv_map, indeg_graph


def read_graphs(filename):
    """Always breaks the edges with more character to single characters."""
    f = open(filename, "r")
    g2_nodes = set()
    g1_nodes = set()
    g2_list = []
    g1_list = []
    g1_map = {}
    g2_map = {}
    g1_inv_map = {}
    g2_inv_map = {}
    string = f.readline().split()
    print(string[0], ' ', string[1])
    num_nodes = int(string[0])
    num_edges = int(string[1])
    graph_3 = {}
    graph_4 = {}

    for line in f:
        line = line.split()
        u = int(line[0])
        v = int(line[1])
        cov_1_tmp = line[2]
        cov_2_tmp = line[3]
        if cov_1_tmp == '-nan':
            cov_1_tmp = 0
        if cov_2_tmp == '-nan':
            cov_2_tmp = 0
        cov_1 = float(cov_1_tmp)
        cov_2 = float(cov_2_tmp)
        label = line[4]
        char_list = list(label)

        temp_node = u
        for i in range(len(char_list) - 1):
            if cov_1 != 0:
                g1_list_len = len(g1_list)
                if temp_node not in graph_3:
                    graph_3[temp_node] = [(num_nodes, math.ceil(cov_1), char_list[i])]
                else:
                    graph_3[temp_node] += [(num_nodes, math.ceil(cov_1), char_list[i])]
                if temp_node not in g1_nodes:
                    g1_nodes.add(temp_node)
                    g1_list.append(temp_node)
                    # g1_map[temp_node] = len(g1_list)-1
                    g1_map[temp_node] = g1_list_len
                    g1_inv_map[g1_list_len] = temp_node
                    g1_list_len += 1
                if num_nodes not in g1_nodes:
                    graph_3[num_nodes] = []
                    g1_nodes.add(num_nodes)
                    g1_list.append(num_nodes)
                    # g1_map[num_nodes] = len(g1_list)-1
                    g1_map[num_nodes] = g1_list_len
                    g1_inv_map[g1_list_len] = num_nodes
                    g1_list_len += 1
            if cov_2 != 0:
                g2_list_len = len(g2_list)
                if temp_node not in graph_4:
                    graph_4[temp_node] = [(num_nodes, math.ceil(cov_2), char_list[i])]
                else:
                    graph_4[temp_node] += [(num_nodes, math.ceil(cov_2), char_list[i])]
                if temp_node not in g2_nodes:
                    g2_nodes.add(temp_node)
                    g2_list.append(temp_node)
                    # g2_map[temp_node] = len(g2_list)-1
                    g2_map[temp_node] = g2_list_len
                    g2_inv_map[g2_list_len] = temp_node
                    g2_list_len += 1
                if num_nodes not in g2_nodes:
                    graph_4[num_nodes] = []
                    g2_nodes.add(num_nodes)
                    g2_list.append(num_nodes)
                    # g2_map[num_nodes] = len(g2_list)-1
                    g2_map[num_nodes] = g2_list_len
                    g2_inv_map[g2_list_len] = num_nodes
                    g2_list_len += 1
            temp_node = num_nodes
            num_nodes += 1
        if cov_1 != 0:
            if temp_node not in graph_3:
                graph_3[temp_node] = [(v, math.ceil(cov_1), char_list[-1])]
            else:
                graph_3[temp_node] += [(v, math.ceil(cov_1), char_list[-1])]
            if temp_node not in g1_nodes:
                g1_nodes.add(temp_node)
                g1_list.append(temp_node)
                g1_map[temp_node] = len(g1_list)-1
                g1_inv_map[len(g1_list)-1] = temp_node
            if v not in g1_nodes:
                graph_3[v] = []
                g1_nodes.add(v)
                g1_list.append(v)
                g1_map[v] = len(g1_list)-1
                g1_inv_map[len(g1_list)-1] = v
        if cov_2 != 0:
            if temp_node not in graph_4:
                graph_4[temp_node] = [(v, math.ceil(cov_2), char_list[-1])]
            else:
                graph_4[temp_node] += [(v, math.ceil(cov_2), char_list[-1])]
            if temp_node not in g2_nodes:
                g2_nodes.add(temp_node)
                g2_list.append(temp_node)
                g2_map[temp_node] = len(g2_list) - 1
                g2_inv_map[len(g2_list) - 1] = temp_node
            if v not in g2_nodes:
                graph_4[v] = []
                g2_nodes.add(v)
                g2_list.append(v)
                g2_map[v] = len(g2_list) - 1
                g2_inv_map[len(g2_list) - 1] = v

    f.close()
    return graph_3, graph_4, g1_list, g2_list, g1_map, g2_map, g1_inv_map, g2_inv_map
    # return graph_3, g1_list, g1_map, g1_inv_map, graph_4, g2_list, g2_map, g2_inv_map


def read_graphs_1(filename):
    """Never breaks the edges with more than one character to smaller pieces."""
    f = open(filename, "r")
    g2_nodes = set()
    g1_nodes = set()
    g2_list = []
    g1_list = []
    g1_map = {}
    g2_map = {}
    g1_inv_map = {}
    g2_inv_map = {}
    string = f.readline().split()
    print(string[0], ' ', string[1])
    num_nodes = int(string[0])
    num_edges = int(string[1])
    graph_3 = {}
    graph_4 = {}

    for line in f:
        line = line.split()
        u = int(line[0])
        v = int(line[1])
        cov_1_tmp = line[2]
        cov_2_tmp = line[3]
        if cov_1_tmp == '-nan':
            cov_1_tmp = 0
        if cov_2_tmp == '-nan':
            cov_2_tmp = 0
        cov_1 = float(cov_1_tmp)
        cov_2 = float(cov_2_tmp)
        label = line[4]
        # char_list = list(label)

        temp_node = u
        if cov_1 != 0:
            if temp_node not in graph_3:
                graph_3[temp_node] = [(v, math.ceil(cov_1), label)]
            else:
                graph_3[temp_node] += [(v, math.ceil(cov_1), label)]
            if temp_node not in g1_nodes:
                g1_nodes.add(temp_node)
                g1_list.append(temp_node)
                g1_map[temp_node] = len(g1_list)-1
                g1_inv_map[len(g1_list)-1] = temp_node
            if v not in g1_nodes:
                graph_3[v] = []
                g1_nodes.add(v)
                g1_list.append(v)
                g1_map[v] = len(g1_list)-1
                g1_inv_map[len(g1_list)-1] = v
        if cov_2 != 0:
            if temp_node not in graph_4:
                graph_4[temp_node] = [(v, math.ceil(cov_2), label)]
            else:
                graph_4[temp_node] += [(v, math.ceil(cov_2), label)]
            if temp_node not in g2_nodes:
                g2_nodes.add(temp_node)
                g2_list.append(temp_node)
                g2_map[temp_node] = len(g2_list) - 1
                g2_inv_map[len(g2_list) - 1] = temp_node
            if v not in g2_nodes:
                graph_4[v] = []
                g2_nodes.add(v)
                g2_list.append(v)
                g2_map[v] = len(g2_list) - 1
                g2_inv_map[len(g2_list) - 1] = v

    f.close()
    return graph_3, graph_4, g1_list, g2_list, g1_map, g2_map, g1_inv_map, g2_inv_map


def read_graphs_2(filename):
    """Only breaks the edges with more than one character to single character pieces when
    that edge is not in both of the graphs (coverage for one of them is zero)."""
    f = open(filename, "r")
    g2_nodes = set()
    g1_nodes = set()
    g2_list = []
    g1_list = []
    g1_map = {}
    g2_map = {}
    g1_inv_map = {}
    g2_inv_map = {}
    string = f.readline().split()
    print(string[0], ' ', string[1])
    num_nodes = int(string[0])
    num_edges = int(string[1])
    graph_3 = {}
    graph_4 = {}

    for line in f:
        line = line.split()
        u = int(line[0])
        v = int(line[1])
        cov_1_tmp = line[2]
        cov_2_tmp = line[3]
        if cov_1_tmp == '-nan':
            cov_1_tmp = 0
        if cov_2_tmp == '-nan':
            cov_2_tmp = 0
        cov_1 = float(cov_1_tmp)
        cov_2 = float(cov_2_tmp)
        label = line[4]
        char_list = list(label)

        temp_node = u

        #####
        if cov_1 == 0 or cov_2 == 0:
            for i in range(len(char_list) - 1):
                if cov_1 != 0:
                    g1_list_len = len(g1_list)
                    if temp_node not in graph_3:
                        graph_3[temp_node] = [(num_nodes, math.ceil(cov_1), char_list[i])]
                    else:
                        graph_3[temp_node] += [(num_nodes, math.ceil(cov_1), char_list[i])]
                    if temp_node not in g1_nodes:
                        g1_nodes.add(temp_node)
                        g1_list.append(temp_node)
                        # g1_map[temp_node] = len(g1_list)-1
                        g1_map[temp_node] = g1_list_len
                        g1_inv_map[g1_list_len] = temp_node
                        g1_list_len += 1
                    if num_nodes not in g1_nodes:
                        graph_3[num_nodes] = []
                        g1_nodes.add(num_nodes)
                        g1_list.append(num_nodes)
                        # g1_map[num_nodes] = len(g1_list)-1
                        g1_map[num_nodes] = g1_list_len
                        g1_inv_map[g1_list_len] = num_nodes
                        g1_list_len += 1
                if cov_2 != 0:
                    g2_list_len = len(g2_list)
                    if temp_node not in graph_4:
                        graph_4[temp_node] = [(num_nodes, math.ceil(cov_2), char_list[i])]
                    else:
                        graph_4[temp_node] += [(num_nodes, math.ceil(cov_2), char_list[i])]
                    if temp_node not in g2_nodes:
                        g2_nodes.add(temp_node)
                        g2_list.append(temp_node)
                        # g2_map[temp_node] = len(g2_list)-1
                        g2_map[temp_node] = g2_list_len
                        g2_inv_map[g2_list_len] = temp_node
                        g2_list_len += 1
                    if num_nodes not in g2_nodes:
                        graph_4[num_nodes] = []
                        g2_nodes.add(num_nodes)
                        g2_list.append(num_nodes)
                        # g2_map[num_nodes] = len(g2_list)-1
                        g2_map[num_nodes] = g2_list_len
                        g2_inv_map[g2_list_len] = num_nodes
                        g2_list_len += 1
                temp_node = num_nodes
                num_nodes += 1

        #####
        if cov_1 != 0:
            if temp_node not in graph_3:
                graph_3[temp_node] = [(v, math.ceil(cov_1), char_list[-1])]
            else:
                graph_3[temp_node] += [(v, math.ceil(cov_1), char_list[-1])]
            if temp_node not in g1_nodes:
                g1_nodes.add(temp_node)
                g1_list.append(temp_node)
                g1_map[temp_node] = len(g1_list)-1
                g1_inv_map[len(g1_list)-1] = temp_node
            if v not in g1_nodes:
                graph_3[v] = []
                g1_nodes.add(v)
                g1_list.append(v)
                g1_map[v] = len(g1_list)-1
                g1_inv_map[len(g1_list)-1] = v
        if cov_2 != 0:
            if temp_node not in graph_4:
                graph_4[temp_node] = [(v, math.ceil(cov_2), char_list[-1])]
            else:
                graph_4[temp_node] += [(v, math.ceil(cov_2), char_list[-1])]
            if temp_node not in g2_nodes:
                g2_nodes.add(temp_node)
                g2_list.append(temp_node)
                g2_map[temp_node] = len(g2_list) - 1
                g2_inv_map[len(g2_list) - 1] = temp_node
            if v not in g2_nodes:
                graph_4[v] = []
                g2_nodes.add(v)
                g2_list.append(v)
                g2_map[v] = len(g2_list) - 1
                g2_inv_map[len(g2_list) - 1] = v

    f.close()
    return graph_3, graph_4, g1_list, g2_list, g1_map, g2_map, g1_inv_map, g2_inv_map


def vertex_num(u, v, graph_size):
    return u*graph_size + v


def cross_product(graph_1, graph_2, g1_nodes, g2_nodes, g1_map, g2_map, indeg_1, indeg_2, match_reward):
    depart = {}
    arrive = {}
    edge_to_nodes = {}
    res_graph = []
    result_graph = {}
    weight_1 = []
    weight_2 = []
    project_1 = {}
    project_2 = {}
    op_project_1 = {}
    op_project_2 = {}
    str_rev_proj_1 = {}
    str_rev_proj_2 = {}
    edge_counter = 0
    print("start reading the keys: ")
    graph_1_keys = graph_1.keys()
    graph_2_keys = graph_2.keys()
    g2_size = len(graph_2_keys)
    print("read the keys.")
    for node in graph_1_keys:
        print(node)
        for edge in graph_1[node]:
            dest_node = edge[0]
            u = g1_map[node]
            v = g1_map[dest_node]
            weight_1.append((u, v, edge[1], edge[2]))
            project_1[tuple([node] + list(edge))] = []
            for node_2 in graph_2_keys:
                u_2 = g2_map[node_2]
                new_source = vertex_num(u, u_2, g2_size)
                new_dest = vertex_num(v, u_2, g2_size)
                new_edge = (new_source, new_dest, gap_penalty)
                res_graph.append(new_edge)
                result_graph[new_edge] = edge_counter
                op_project_1[edge_counter] = tuple([node] + list(edge))
                str_rev_proj_1[edge_counter] = edge[2]
                edge_to_nodes[edge_counter] = (new_source, new_dest)
                edge_counter += 1
                project_1[tuple([node] + list(edge))].append(new_edge)
                if new_source not in depart:
                    depart[new_source] = [(new_dest, gap_penalty)]
                else:
                    depart[new_source].append((new_dest, gap_penalty))
                if new_dest not in arrive:
                    arrive[new_dest] = [(new_source, gap_penalty)]
                else:
                    arrive[new_dest].append((new_source, gap_penalty))
    print('Vertical edges, done!')
    # print(res_graph)

    for node in graph_2_keys:
        for edge in graph_2[node]:
            dest_node = edge[0]
            u = g2_map[node]
            v = g2_map[dest_node]
            weight_2.append((u, v, edge[1], edge[2]))
            project_2[tuple([node] + list(edge))] = []
            for node_1 in graph_1_keys:
                u_1 = g1_map[node_1]
                new_source = vertex_num(u_1, u, g2_size)
                new_dest = vertex_num(u_1, v, g2_size)
                new_edge = (new_source, new_dest, gap_penalty)
                res_graph.append(new_edge)
                result_graph[new_edge] = edge_counter
                op_project_2[edge_counter] = tuple([node] + list(edge))
                str_rev_proj_2[edge_counter] = edge[2]
                edge_to_nodes[edge_counter] = (new_source, new_dest)
                edge_counter += 1
                project_2[tuple([node] + list(edge))].append(new_edge)
                if new_source not in depart:
                    depart[new_source] = [(new_dest, gap_penalty)]
                else:
                    depart[new_source].append((new_dest, gap_penalty))
                if new_dest not in arrive:
                    arrive[new_dest] = [(new_source, gap_penalty)]
                else:
                    arrive[new_dest].append((new_source, gap_penalty))

    print("Horizontal edges, done!")
    # print(res_graph)

    for node_1 in graph_1_keys:
        for edge_1 in graph_1[node_1]:
            u_1 = g1_map[node_1]
            v_1 = g1_map[edge_1[0]]
            for node_2 in graph_2_keys:
                for edge_2 in graph_2[node_2]:
                    u_2 = g2_map[node_2]
                    v_2 = g2_map[edge_2[0]]
                    new_source = vertex_num(u_1, u_2, g2_size)
                    new_dest = vertex_num(v_1, v_2, g2_size)
                    new_score = -1
                    if edge_1[2] == edge_2[2]:
                        new_score = match_reward
                    else:
                        new_score = mismatch_penalty
                    new_edge = (new_source, new_dest, new_score)
                    res_graph.append(new_edge)
                    result_graph[new_edge] = edge_counter
                    op_project_1[edge_counter] = tuple([node_1] + list(edge_1))
                    op_project_2[edge_counter] = tuple([node_2] + list(edge_2))
                    str_rev_proj_1[edge_counter] = edge_1[2]
                    str_rev_proj_2[edge_counter] = edge_2[2]
                    edge_to_nodes[edge_counter] = (new_source, new_dest)
                    edge_counter += 1
                    project_1[tuple([node_1] + list(edge_1))].append(new_edge)
                    project_2[tuple([node_2] + list(edge_2))].append(new_edge)
                    if new_source not in depart:
                        depart[new_source] = [(new_dest, new_score)]
                    else:
                        depart[new_source].append((new_dest, new_score))
                    if new_dest not in arrive:
                        arrive[new_dest] = [(new_source, new_score)]
                    else:
                        arrive[new_dest].append((new_source, new_score))
    print("Diagonal edges, done!")

    # print(str_rev_proj_1)
    # print(str_rev_proj_2)
    return result_graph, depart, arrive, project_1, project_2, weight_1, weight_2, str_rev_proj_1, str_rev_proj_2, edge_to_nodes


def write_LP(filename, result_graph, depart, arrive, project_1, project_2):
    file = open(filename, 'w')
    print("Writing the LP into file: ", filename)
    file.write("Minimize\n")
    out_str = ''
    for edge in result_graph.keys():
        score = edge[2]
        if score != 0:
            out_str += ' + ' + str(score) + ' x' + str(result_graph[edge])
    out_str = out_str[3:] + '\n'

    out_str += 'Subject To\n'

    counter = 0
    for node in depart.keys():
        # out_str = ''
        out_str += 'v' + str(counter) + ': '
        counter += 1
        temp_str = ''
        for decendent in depart[node]:
            edge_num = result_graph[(node, decendent[0], decendent[1])]
            temp_str += ' + x' + str(edge_num)
        for pred in arrive[node]:
            edge_num = result_graph[(pred[0], node, pred[1])]
            temp_str += ' - x' + str(edge_num)
        temp_str += ' = 0\n'
        out_str += temp_str[3:]

    counter = 0
    project_1_keys = project_1.keys()
    for edge in project_1_keys:
        out_str += 'w' + str(counter) + ': '
        counter += 1
        temp_str = ''
        for proj in project_1[edge]:
            temp_str += ' + x' + str(result_graph[proj])
        temp_str += ' = ' + str(edge[2]) + '\n'
        out_str += temp_str[3:]

    project_2_keys = project_2.keys()
    for edge in project_2_keys:
        out_str += 'w' + str(counter) + ': '
        counter += 1
        temp_str = ''
        for proj in project_2[edge]:
            temp_str += ' + x' + str(result_graph[proj])
        temp_str += ' = ' + str(edge[2]) + '\n'
        out_str += temp_str[3:]

    out_str += 'End'
    file.write(out_str)
    file.close()


def write_LP_apr_abs(filename, result_graph, depart, arrive, project_1, project_2):
    file = open(filename, 'w')
    print("Writing the LP into file: ", filename)
    file.write("Minimize\n")
    out_str = ''
    project_1_keys = project_1.keys()
    project_2_keys = project_2.keys()
    depart_keys = depart.keys()
    result_graph_keys = result_graph.keys()
    tot_edges_size = len(result_graph_keys)
    weight_size = len(project_1_keys) + len(project_2.keys())
    for edge in result_graph_keys:
        score = edge[2]
        if score != 0:
            out_str += ' + ' + str(score) + ' x' + str(result_graph[edge])
    out_str = out_str[3:] #  + '\n'

    for i in range(weight_size):
        out_str += ' + x' + str(tot_edges_size + i)

    out_str += '\nSubject To\n'

    counter = 0

    for node in depart_keys:
        # out_str = ''
        out_str += 'v' + str(counter) + ': '
        counter += 1
        temp_str = ''
        for decendent in depart[node]:
            edge_num = result_graph[(node, decendent[0], decendent[1])]
            temp_str += ' + x' + str(edge_num)
        for pred in arrive[node]:
            edge_num = result_graph[(pred[0], node, pred[1])]
            temp_str += ' - x' + str(edge_num)
        temp_str += ' = 0\n'
        out_str += temp_str[3:]

    counter = 0

    for edge in project_1_keys:
        out_str += 'w' + str(counter) + ': '
        temp_str = ''
        for proj in project_1[edge]:
            temp_str += ' + x' + str(result_graph[proj])
        temp_str += ' + x' + str(tot_edges_size + weight_size + counter) +\
                    ' - x' + str(tot_edges_size + counter) + ' = ' + str(edge[2]) + '\n'
        out_str += temp_str[3:]
        counter += 1

    for edge in project_2_keys:
        out_str += 'w' + str(counter) + ': '
        temp_str = ''
        for proj in project_2[edge]:
            temp_str += ' + x' + str(result_graph[proj])
        temp_str += ' + x' + str(tot_edges_size + weight_size + counter) + \
                    ' - x' + str(tot_edges_size + counter) + ' = ' + str(edge[2]) + '\n'
        out_str += temp_str[3:]
        counter += 1

    counter = 0
    ###################

    for edge in project_1_keys:
        out_str += 'w' + str(weight_size + counter) + ': '
        temp_str = ''
        for proj in project_1[edge]:
            temp_str += ' - x' + str(result_graph[proj])
        temp_str += ' + x' + str(tot_edges_size + 2*weight_size + counter) +\
                    ' - x' + str(tot_edges_size + counter) + ' = -' + str(edge[2]) + '\n'
        out_str += temp_str[1:]
        counter += 1

    for edge in project_2_keys:
        out_str += 'w' + str(weight_size + counter) + ': '
        temp_str = ''
        for proj in project_2[edge]:
            temp_str += ' - x' + str(result_graph[proj])
        temp_str += ' + x' + str(tot_edges_size + 2*weight_size + counter) + \
                    ' - x' + str(tot_edges_size + counter) + ' = -' + str(edge[2]) + '\n'
        out_str += temp_str[1:]
        counter += 1

    out_str += 'End'
    file.write(out_str)
    file.close()


def write_LP_apr(filename, result_graph, depart, arrive, project_1, project_2):
    file = open(filename, 'w')
    print("Writing the LP into file: ", filename)
    file.write("Minimize\n")
    out_str = ''
    project_1_keys = project_1.keys()
    depart_keys = depart.keys()
    result_graph_keys = result_graph.keys()
    tot_edges_size = len(result_graph_keys)
    weight_size = len(project_1_keys) + len(project_2.keys())
    for edge in result_graph_keys:
        score = edge[2]
        if score != 0:
            out_str += ' + ' + str(score) + ' x' + str(result_graph[edge])
    out_str = out_str[3:] #  + '\n'

    for i in range(weight_size):
        out_str += ' + x' + str(tot_edges_size + i)

    out_str += '\nSubject To\n'

    counter = 0

    for node in depart_keys:
        # out_str = ''
        out_str += 'v' + str(counter) + ': '
        counter += 1
        temp_str = ''
        for decendent in depart[node]:
            edge_num = result_graph[(node, decendent[0], decendent[1])]
            temp_str += ' + x' + str(edge_num)
        for pred in arrive[node]:
            edge_num = result_graph[(pred[0], node, pred[1])]
            temp_str += ' - x' + str(edge_num)
        temp_str += ' = 0\n'
        out_str += temp_str[3:]

    counter = 0

    for edge in project_1_keys:
        out_str += 'w' + str(counter) + ': '
        temp_str = ''
        for proj in project_1[edge]:
            temp_str += ' + x' + str(result_graph[proj])
        temp_str += ' + x' + str(tot_edges_size + counter) + ' = ' + str(edge[2]) + '\n'
        out_str += temp_str[3:]
        counter += 1

    for edge in project_2.keys():
        out_str += 'w' + str(counter) + ': '
        temp_str = ''
        for proj in project_2[edge]:
            temp_str += ' + x' + str(result_graph[proj])
        temp_str += ' + x' + str(tot_edges_size + counter) + ' = ' + str(edge[2]) + '\n'
        out_str += temp_str[3:]
        counter += 1

    out_str += 'End'
    file.write(out_str)
    file.close()


def write_rev_dicts(filename, str_rev_1, str_rev_2, edge_to_nodes):
    file_1 = open(filename+"_rev1", 'w')
    file_1.write(json.dumps(str_rev_1))
    file_1.close()
    file_2 = open(filename + "_rev2", 'w')
    file_2.write(json.dumps(str_rev_2))
    file_2.close()
    file_3 = open(filename + "_e2n", 'w')
    file_3.write(json.dumps(edge_to_nodes))
    file_3.close()


if __name__ == '__main__':
    import sys

    filename_1 = sys.argv[1]
    filename_2 = sys.argv[2]
    match_reward = int(sys.argv[3])

    g1_elems = read_gr(filename_1)
    print("read graph 1")
    g2_elems = read_gr(filename_2)
    print("read graph 2")
    res_graph, depart, arrive, project_1, project_2, weight_1, weight_2, str_rev_1, str_rev_2, edge_to_nodes = \
        cross_product(g1_elems[0], g2_elems[0], g1_elems[1], g2_elems[1], g1_elems[2], g2_elems[2], \
                      g1_elems[4], g2_elems[4], match_reward)

    print("finish cross product!")
    write_LP_apr_abs(filename_1.split('.')[0] + '_' + filename_2.split('.')[0] + '_' + str(match_reward) + '_apr_abs.lp', \
                 res_graph, depart, arrive, project_1, project_2)

    write_rev_dicts(filename_1.split('.')[0] + '_' + filename_2.split('.')[0] + '_' + str(match_reward) + '_apr_abs', str_rev_1, str_rev_2, edge_to_nodes)
