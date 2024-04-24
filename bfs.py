from igraph import Graph
from header import create_puzzle
from bfs_header import Queue

def check_correct(g, q, vid, height):
    for vid_neighbour in g.neighbors(vid, mode="out"):
        if height[vid_neighbour] > 0:
            eid1 = g.get_eid(vid, vid_neighbour, directed=True, error=False)
            if q.eid[eid1] == 0 and g.es[eid1]["flow_true"] > 0 and g.es[eid1]["flow"] > 0:
                return 1
    return 0

def bfs_mark(g, bfs_edge_marker, height, source, sink, curve, ctx, buffer, totalBytes):
    count = 1
    i = 0
    track = 0
    num = 0
    start = source
    edge_set = []
    q = Queue(g.ecount())
    q.append((sink, count))
    q.push(sink,count)
    while (not q.empty()):
        vid = q.pop()
        count = vid[1];
        num += 1
        for vid_neighbour in g.neighbors(vid[0], mode="out"):
            if height[vid_neighbour] > 0 or vid_neighbour == source:
                eid1 = g.get_eid(vid[0], vid_neighbour, directed=True, error=False)
                eid2 = g.get_eid(vid_neighbour, vid[0], directed=True, error=False)

                if q.eid[eid2] == 0 and g.es[eid2]["flow_true"] > 0 and g.es[eid2]["flow"] > 0 :
                    q.eid[eid2] = count
                    if vid_neighbour != source and check_correct(g,q,vid_neighbour,height) == 0:
                        q.push(vid_neighbour,count+1)
                        edge_set[track] = eid2
                        track += 1
                        g.es[eid2]["level"] = count

    create_puzzle(g, curve, ctx, buffer, edge_set, track, source, sink, totalBytes)
