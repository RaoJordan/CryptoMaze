import igraph
import sys
import time
import random

def main():
    g = igraph.Graph()
    height = []
    t = time.time()
    total_bytes = 0
    
    # Set up random seed
    random.seed(time.time())
    
    # Open and read graph from file
    try:
        with open(sys.argv[1], "r") as fp:
            g = igraph.Graph.Read_Edgelist(fp)
    except FileNotFoundError:
        print("File does not exist")
        sys.exit(1)
    
    # Initialize height array
    for _ in range(g.vcount()):
        height.append(0)
        
    # Open and read flow and value from file
    try:
        with open(sys.argv[2], "r") as fp:
            for line in fp:
                flow, value = map(int, line.split())
                # Set edge attributes
                g.es["weight"] = value
                g.es["flow"] = flow
                g.es["flow_true"] = 0
    except FileNotFoundError:
        print("File does not exist")
        sys.exit(1)
    
    source = int(sys.argv[4])
    sink = int(sys.argv[5])
    
    try:
        with open(sys.argv[6], "a") as fp7, open(sys.argv[7], "r") as fp:
            value = int(fp.read())
            # Initialize excess attribute for each vertex
            g.vs["excess"] = 0
            
            # Set vertex types
            for vid in range(g.vcount()):
                g.vs[vid]["type"] = "normal"
                height[vid] = 0
            g.vs[source]["type"] = "source"
            g.vs[sink]["type"] = "sink"
            
            # Set excess attribute for source vertex
            g.vs[source]["excess"] = value
            
            # Call main_func (assuming it's defined elsewhere)
            main_func(g, height, source, sink)
            
            # Check if excess at sink is equal to value
            if g.vs[sink]["excess"] == value:
                payment(g, height, source, sink, total_bytes)
                e = time.time()
                time_taken = e - t
                print("success")
                with open(sys.argv[3], "a") as fp6:
                    fp6.write(f"{source} {sink} {value} {g.vcount()} {g.ecount()} {time_taken} {total_bytes / 1024}KB success\n")
                fp7.write(f"{value}.00 {source} {sink}\n")
            else:
                e = time.time()
                time_taken = e - t
                with open(sys.argv[3], "a") as fp6:
                    fp6.write(f"{source} {sink} {value} {g.vcount()} {g.ecount()} {time_taken} failure\n")
    except FileNotFoundError:
        print("File does not exist")
        sys.exit(1)

    # Destroy the graph object
    g = None

if __name__ == "__main__":
    main()
