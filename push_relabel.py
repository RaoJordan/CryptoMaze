import igraph
import time

def main(argv):
    g = igraph.Graph()
    height = [0] * g.vcount()
    source, sink = int(argv[3]), int(argv[4])

    # Reading graph from the first file
    with open(argv[1], "r") as fp:
        g = igraph.Graph.Read_Edgelist(fp, directed=True)

    # Setting vertex types and heights
    with open(argv[2], "r") as fp:
        for vid in range(g.vcount()):
            g.vs[vid]["type"] = "normal"
            height[vid] = 0
        g.vs[source]["type"] = "source"
        g.vs[sink]["type"] = "sink"
        height[source] = g.vcount()

    # Setting edge weights and flows
    with open(argv[3], "r") as fp:
        for eid, line in enumerate(fp):
            flow, value = map(int, line.split())
            from_vertex, to_vertex = g.es[eid].tuple
            g.es[eid]["weight"] = value
            g.es[eid]["flow"] = flow

    # Setting excess for all vertices
    value = int(argv[5])
    for vid in range(g.vcount()):
        g.vs[vid]["excess"] = 0
    g.vs[source]["excess"] = value

    # Start time
    t = time.time()
    main_func(g, height, source, sink)
    e = time.time()

    # Calculating time taken
    time_taken = e - t

    # Writing results to the output file
    with open(argv[6], "a") as fp6:
        fp6.write(f"{source} {sink} {g.vcount()} {g.ecount()} {argv[5]} {time_taken} ")
        if g.vs[sink]["excess"] == int(argv[5]):
            fp6.write("success\n")
        else:
            fp6.write("failure\n")

if __name__ == "__main__":
    import sys
    main(sys.argv)
