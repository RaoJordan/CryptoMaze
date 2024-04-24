from igraph import *

def preflow(g, height, source):
    excess_val = g.vs[source]["excess"]
    vs = g.neighborhood(source, mode=OUT)
    for to in vs:
        excess_val = g.vs[source]["excess"]
        eid = g.get_eid(source, to, directed=True)
        cap = g.es[eid]["weight"] - g.es[eid]["flow"]
        amount_subtract = min(excess_val, cap)
        if amount_subtract > 0:
            g.vs[source]["excess"] -= amount_subtract
            g.es[eid]["flow"] += amount_subtract
            g.es[eid]["flow_true"] = 1
            eid1 = g.get_eid(to, source, directed=True)
            g.es[eid1]["flow"] += cap - amount_subtract
            g.vs[to]["excess"] = amount_subtract
            if g.vs[to]["type"] != "sink":
                lift(g, height, to)#bhavyas part.

