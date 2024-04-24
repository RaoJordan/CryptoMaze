from igraph import *

def lift(g, height, vid):
    if g.vs[vid]["type"] != "source":
        height_min = g.vcount() + 100
        flag = False
        for neighbor in g.neighbors(vid, mode=OUT):
            eid1 = g.get_eid(vid, neighbor, directed=True, error=False)
            if eid1 == -1:
                continue
            if g.es[eid1]["flow"] < g.es[eid1]["weight"]:
                flag = True
                height_min = min(height_min, height[neighbor])
        if flag and height[vid] <= height_min:
            height[vid] = height_min + 1
