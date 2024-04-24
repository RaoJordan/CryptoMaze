from igraph import *

def main_func(g, height, source, sink):
    while True:
        flag = 0
        for vid in range(g.vcount()):
            if g.vs[vid]["type"] != "source" and g.vs[vid]["type"] != "sink":
                excess = g.vs[vid]["excess"]
                if excess > 0:
                    flag = 1
                    for vid_neighbour in g.neighbors(vid, mode=OUT):
                        excess = g.vs[vid]["excess"]
                        eid1 = g.get_eid(vid, vid_neighbour, directed=True, error=False)
                        if eid1 == -1:
                            continue
                        flow = g.es[eid1]["flow"]
                        res_cap = g.es[eid1]["weight"] - flow
                        if (height[vid_neighbour] < height[vid] and
                                g.es[eid1]["flow"] < g.es[eid1]["weight"]):
                            amount_subtract = min(excess, res_cap)
                            g.vs[vid]["excess"] -= amount_subtract
                            g.es[eid1]["flow"] += amount_subtract
                            eid2 = g.get_eid(vid_neighbour, vid, directed=True, error=False)
                            g.es[eid2]["flow"] = g.es[eid1]["weight"] - flow - amount_subtract
                            if (g.es[eid2]["flow_true"] == 0 and g.es[eid1]["flow"] != 0):
                                g.es[eid1]["flow_true"] = 1
                            approve_push(g, vid_neighbour, amount_subtract, height)
                        else:
                            lift(g, height, vid)
                        if g.vs[vid]["excess"] == 0:
                            break
        if flag == 0:
            break
