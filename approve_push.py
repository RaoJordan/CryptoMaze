from lift import *

def approve_push(g, vid_neighbour, flow, height):
    excess = g.vs[vid_neighbour]["excess"]
    g.vs[vid_neighbour]["excess"] = excess + flow
    if g.vs[vid_neighbour]["type"] != "sink":
        lift(g, height, vid_neighbour)
