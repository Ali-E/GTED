import random
import copy
import sys
import readAssemb as ra
import operator


def process_depart_arrive(depart, arrive):
    """not useful!"""
    outdeg_graph = copy.deepcopy(depart)
    indeg_graph = copy.deepcopy(arrive)
    for key in indeg_graph:
        if key not in outdeg_graph:
            outdeg_graph[key] = []
    for key in outdeg_graph:
        if key not in indeg_graph:
            indeg_graph[key] = []
    return outdeg_graph, indeg_graph


def DFS_itr(in_graph, st_ver, leader, visited_1, leader_node):
    leader_node[st_ver] = leader
    stack = []
    stack.append(st_ver)
    visited_1[st_ver] = 1
    while stack:
        node = stack.pop()
        for neigh_tup in in_graph[node]:
            neigh = neigh_tup[0]
            if visited_1[neigh] == 0:
                leader_node[neigh] = leader
                visited_1[neigh] = 1
                # flag = 1
                stack.append(neigh)


def DFS_rev_itr(indeg_graph, st_ver, visited_2, T, finishing_time, inv_map):
    T = T
    stack = []
    stack.append(st_ver)
    taken_out = set()
    while stack:
        node = stack[-1]
        flag = 0
        if node in taken_out:
            stack.pop()
            continue

        visited_2[node] = 1
        for neigh_tup in indeg_graph[node]:
            neigh = neigh_tup[0]
            if visited_2[neigh] == 0:
                flag = 1
                stack.append(neigh)
        if flag == 0:
            taken_out.add(node)
            stack.pop()
            if T >= len(finishing_time):
                print(node)
            finishing_time[T] = node
            T += 1
    return T


def all_dfs_rev(indeg_graph, inv_map, outdeg_graph):
    visited_2 = [0 for idx in range(len(indeg_graph))]
    finishing_time = [0 for idx in range(len(outdeg_graph))]
    T = 0
    for node in indeg_graph.keys():
        if visited_2[node] == 0:
            T = DFS_rev_itr(indeg_graph, node, visited_2, T, finishing_time, inv_map)

    return finishing_time


def SCC(outdeg_graph, finishing_time):
    visited_1 = [0 for idx in range(len(outdeg_graph))]
    leader_node = [0 for idx in range(len(outdeg_graph))]
    for idx in range(len(finishing_time) - 1, -1, -1):
        node = finishing_time[idx]
        if visited_1[node] == 0:
            leader = node
            DFS_itr(outdeg_graph, node, leader, visited_1, leader_node)
    return leader_node


def find_scc(leader_node):
    scc_list = {}
    for idx in range(len(leader_node)):
        if leader_node[idx] in scc_list:
            scc_list[leader_node[idx]] += 1
        else:
            scc_list[leader_node[idx]] = 1
    return scc_list


def big_5(scc_list):
    big_list = [0, 0, 0, 0, 0]
    for scc in scc_list.keys():
        num = scc_list[scc]
        # print num
        for idx in range(0, 5):
            if num > big_list[idx]:
                big_list = big_list[:idx] + [num] + big_list[idx:-1]
                big_list = big_list[:5]
                break
    return big_list


def prep_gted(graph, g_list, g_map, inv_map):
    # graph, g_list, g_map, inv_map = ra.read_gr(filename)
    outdeg_graph = {}
    indeg_graph = {}
    for node in graph:
        trans_node = g_map[node]
        outdeg_graph[trans_node] = []
        if trans_node not in indeg_graph:
            indeg_graph[trans_node] = []
        for edge in graph[node]:
            trans_dest = g_map[edge[0]]
            outdeg_graph[trans_node].append((trans_dest, edge[1], edge[2]))

            if trans_dest not in indeg_graph:
                indeg_graph[trans_dest] = [(trans_node, edge[1], edge[2])]
            else:
                indeg_graph[trans_dest].append((trans_node, edge[1], edge[2]))

    return outdeg_graph, indeg_graph, inv_map


def get_n_scc(leader_nodes, inv_map, n=5):
    scc_len = {}
    scc_dict = {}
    top_n_scc = {}
    top_n_len = []
    for idx in range(len(leader_nodes)):
        if inv_map[leader_nodes[idx]] not in scc_dict:
            scc_dict[inv_map[leader_nodes[idx]]] = set([inv_map[idx]])
            scc_len[inv_map[leader_nodes[idx]]] = 1
        else:
            scc_dict[inv_map[leader_nodes[idx]]].add(inv_map[idx])
            scc_len[inv_map[leader_nodes[idx]]] += 1

    sorted_len = sorted(scc_len.items(), key=operator.itemgetter(1))
    # print(sorted_len)
    for i in range(min(n, len(sorted_len))):
        top_n_len.append(sorted_len[-1-i][1])
        top_n_scc[sorted_len[-1-i][0]] = scc_dict[sorted_len[-1-i][0]]
    return top_n_scc, top_n_len


def get_graph_of_scc(scc, all_graph):
    graph = {}
    node_list = list(scc)
    for node in node_list:
        graph[node] = []
        for edge in all_graph[node]:
            if edge[0] in scc:
                graph[node].append(edge)
    return graph


def get_graph_of_scc_1(scc, all_graph):
    graph = {}
    in_graph = {}
    node_list = list(scc)
    for node in node_list:
        graph[node] = []
        for edge in all_graph[node]:
            if edge[0] in scc:
                graph[node].append(edge)
                if edge[0] not in in_graph:
                    in_graph[edge[0]] = [node]
                else:
                    in_graph[edge[0]].append(node)
    return graph, in_graph


def get_scc_final(graph, g_list, g_map, inv_map, n):
    outdeg_graph, indeg_graph, inv_map = prep_gted(graph, g_list, g_map, inv_map)
    finishing_time = all_dfs_rev(indeg_graph, inv_map, outdeg_graph)
    leader_nodes = SCC(outdeg_graph, finishing_time)
    # scc_list = find_scc(leader_nodes)
    scc_dict_res = get_n_scc(leader_nodes, inv_map, n)
    all_graphs = []
    for key in scc_dict_res[0].keys():
        all_graphs.append(get_graph_of_scc(scc_dict_res[0][key], graph))
    return all_graphs


def get_scc_final_1(graph, g_list, g_map, inv_map, n):
    outdeg_graph, indeg_graph, inv_map = prep_gted(graph, g_list, g_map, inv_map)
    finishing_time = all_dfs_rev(indeg_graph, inv_map, outdeg_graph)
    leader_nodes = SCC(outdeg_graph, finishing_time)
    # scc_list = find_scc(leader_nodes)
    scc_dict_res = get_n_scc(leader_nodes, inv_map, n)
    all_graphs = []
    all_in_graphs = []
    for key in scc_dict_res[0].keys():
        out_graph, in_graph = get_graph_of_scc_1(scc_dict_res[0][key], graph)
        all_graphs.append(out_graph)
        all_in_graphs.append(in_graph)
    return all_graphs, all_in_graphs

