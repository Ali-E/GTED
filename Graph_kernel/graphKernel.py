from copy import deepcopy
import numpy as np

from pygraphml import Graph
from pygraphml import GraphMLParser
from chinesepostman import eularian, network
import xml


def main_sub(rootDir, f, outDir, log=False, graphml=True):
    """
    Tasks for each file:
    - Reads graphml, makes eularian and writes into a format that LP writer can understand
    """
    if graphml:
        g = get_graph(rootDir+f)
        print(f)
        supermitch, edgeLabelMap = get_postman_format(g)
        print(edgeLabelMap)
        print(supermitch)
    else:
        supermitch, edgeLabelMap = sgf_to_postman(rootDir+f)
        
    exit(0)
    new_edges = chinese_postman(supermitch)
    write_ali_input(outDir + "/"+f.split(".")[0], g.nodes(), supermitch, new_edges, edgeLabelMap)
    
    if log:
        log_file = outDir + "/"+f.split(".")[0]+'.log'
        write = "Number of added edges to make the graph Eulerian: " + str(len(new_edges))
        for edge in new_edges:
            write += '\n' + str(edge)
        
        with open(log_file, 'w') as f:
            f.write(write)
    
    return len(new_edges)


def extract_score(filename):
    score = -1
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            if line[:19] == "Optimal objective: ":
                score = float(line.split("Optimal objective: ")[1]) 
    return score



def main(argv):
    rootDir = argv[0]
    outFile = argv[1]

    LP_writer = "./lp_writer.out"
    LP_solver = "./vars_then_optimizer.sh"

    graphml_flag = False
    log_flag = False
    log_flag_str = 'F'
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
            log_flag_str = 'T'
        elif opt in ("-s", "--summary"):
            summary_flag = True
    
    print('-----------------Options--------------------')
    # print("graphml option", graphml_flag)
    print("log option", log_flag)
    print("summary option", summary_flag)
    print('--------------------------------------------')


    score_dict = {}
    files = sorted([f for f in os.listdir(rootDir) if len(f.split(".")) > 1 and f.split(".")[-1] == 'sgf'])
    score_list = []
    for i in range(1,len(files)):
        if log_flag:
            print('---------------',i,'---------------')
        elif i%10 == 0:
            print(i, "complete...")
        for j in range(i):
            # new_edges_count = main_sub(rootDir, f, outDir, log=log_flag)
            f1 = files[i]
            f2 = files[j]
            write_LP_command = LP_writer + " " + rootDir +"/"+ f1 + " " + rootDir +"/"+ f2 + " temptemp.lp " + log_flag_str
            if log_flag:
                print(write_LP_command)
            os.system(write_LP_command)
            os.system(LP_solver + " " + "temptemp.lp" + " > tempres.txt")
            cur_score = extract_score("tempres.txt")
            if log_flag:
                print('-----score: ', cur_score)

            idx_1 = int(str(f1.split(".")[0]).split("_")[-1]) -1
            idx_2 = int(str(f2.split(".")[0]).split("_")[-1]) -1

            score_dict[(idx_1, idx_2)] = cur_score
            score_list.append(cur_score)
    print("Completed!")
    os.system('rm temptemp.lp')
    os.system('rm tempres.txt')


    if summary_flag:
        print('-----------------Summary--------------------')
        print('Avg new edges added: ', np.mean(score_list))
        print('Std new edges added: ', np.std(score_list))
        print('Max new edges added: ', np.max(score_list))
        print('Min new edges added: ', np.min(score_list))

    dist_mat = np.zeros((len(files), len(files)))
    for i in range(1, len(files)):
        for j in range(i):
            if (i,j) in score_dict:
                dist_mat[i,j] = score_dict[(i,j)]
                dist_mat[j,i] = score_dict[(i,j)]
            elif (j,i) in score_dict:
                dist_mat[i,j] = score_dict[(j,i)]
                dist_mat[j,i] = score_dict[(j,i)]

    np.savetxt(outFile, dist_mat, delimiter=',', fmt='%.3f')


if __name__ == "__main__":
    import sys
    import getopt
    import os
    if len(sys.argv) < 3:
        print("Usage: ", sys.argv[0], "<input graphml dir>", "<output dir>", "[options]")
        exit(1)
    main(sys.argv[1:])


