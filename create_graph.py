import igraph
import time
import sys
import random

class num:
    def __init__(self, vid, deg):
        self.vid = vid
        self.deg = deg

def sort(array, count):
    for i in range(count - 1):
        for j in range(i + 1, count):
            if array[i].deg < array[j].deg:
                temp1 = array[i].deg
                temp2 = array[i].vid
                array[i].deg = array[j].deg
                array[i].vid = array[j].vid
                array[j].deg = temp1
                array[j].vid = temp2

if __name__ == "__main__":
    if len(sys.argv) < 8:
        print("Usage: python script.py num_nodes output_graphml output_edgelist output_flow output_gtna output_credit_links output_degree_sorted")
        sys.exit(1)

    num_nodes = int(sys.argv[1])
    fp = open(sys.argv[2], "w")
    out = open(sys.argv[3], "w")
    fp1 = open(sys.argv[4], "w")
    gtna = open(sys.argv[5], "w")
    fp2 = open(sys.argv[6], "w")
    fp3 = open(sys.argv[7], "w")

    igraph.set_attribute_table(igraph.AttributeTable())
    random_seed = int(time.time())
    random.seed(random_seed)
    g = igraph.Graph.Barabasi(num_nodes, 1, 4, outpref=True, directed=True, start_from=None, start_with=1)
    val = g.ecount()
    fp2.write("# Graph Property Class\ntreeembedding.credit.CreditLinks\n# Key\nCREDIT_LINKS\n")

    for eid in range(val):
        from_node, to_node = g.es[eid].tuple
        if eid % 4 == 0:
            cap = random.randint(250, 259)
        elif eid % 5 == 0:
            cap = random.randint(400, 404)
        elif eid % 7 == 0:
            cap = random.randint(1000, 1009)
        elif eid % 3 == 0:
            cap = random.randint(200, 207)
        else:
            cap = random.randint(1000, 1006)
        fp2.write(f"{to_node} {from_node} -0.0 0.0 {cap}.0\n")
        g.add_edge(to_node, from_node)
        g.es[g.get_eid(to_node, from_node, directed=True)]["weight"] = cap
        g.es[g.get_eid(from_node, to_node, directed=True)]["weight"] = cap
        g.es[g.get_eid(to_node, from_node, directed=True)]["flow"] = cap
        g.es[g.get_eid(from_node, to_node, directed=True)]["flow"] = 0

    fp2.close()
    g.write_graphml(fp.name)
    g.write_edgelist(out)

    for eid in range(g.ecount()):
        from_node, to_node = g.es[eid].tuple
        eid1 = g.get_eid(from_node, to_node, directed=True)

    out.close()
    read = open(sys.argv[3], "r")
    g = igraph.Graph.Read_Edgelist(read, directed=True)
    read.close()

    for eid in range(g.ecount()):
        from_node, to_node = g.es[eid].tuple
        eid1 = g.get_eid(from_node, to_node, directed=True)
        fp1.write(f"{g.es[eid1]['flow']} {g.es[eid1]['weight']}\n")

    fp1.close()

    gtna.write(f"# Name of the Graph: \ncredit network basic \n# Number of Nodes:\n{g.vcount()} \n# Number of Edges: \n{g.ecount()} \n")

    list_nodes = [num(vid, g.degree(vid, mode="out")) for vid in range(g.vcount())]
    sort(list_nodes, g.vcount())

    for vid in range(g.vcount()):
        gtna.write(f"\n{list_nodes[vid].vid}:")
        neighbors = g.neighbors(list_nodes[vid].vid, mode="out")
        gtna.write("".join(f"{neighbor};" for neighbor in neighbors))

    track = list_nodes[0].deg
    for node in list_nodes:
        if track != node.deg:
            fp3.write("\n")
            track = node.deg
        fp3.write(f"{node.vid} ")

    fp.close()
    gtna.close()
    fp3.close()