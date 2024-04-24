from solve import *
import igraph
import hashlib
from binascii import hexlify

def return_count(g, edge_set, vertex, track):
    count = 0
    for j in range(track):
        from_node, to_node = g.es[edge_set[j]].tuple
        if from_node == vertex:
            count += 1
    return count

def create_puzzle(g, curve, ctx, buffer, edge_set, track, source, sink, totalBytes):
    mark = [0] * g.ecount()
    store = [None] * g.ecount()
    n = curve.new_scalar()
    sum_total = curve.new_scalar()
    vertex_sum = [curve.new_scalar() for _ in range(g.vcount())]
    edge_sum = [curve.new_scalar() for _ in range(g.ecount())]

    vertex_sum[sink] = buffer[sink]

    for j in range(track):
        from_node, to_node = g.es[edge_set[j]].tuple
        eid1 = g.get_eid(from_node, to_node, directed=True)

        if not mark[eid1]:
            mark[eid1] = 1
            store[eid1] = curve.new_point()
            if to_node != sink:
                neighbors = g.neighbors(to_node, mode="out")
                for vid_neighbor in neighbors:
                    eid2 = g.get_eid(to_node, vid_neighbor, directed=True)
                    if mark[eid2]:
                        store[eid1] += store[eid2]

            temp_count = return_count(g, edge_set, to_node, track)
            totalBytes[0] += temp_count * len(hexlify(buffer[to_node].to_bytes()))

            d_temp = hexlify(buffer[to_node].to_bytes()) + hexlify(eid1.to_bytes())
            d = hashlib.sha256(d_temp).digest()
            sol = curve.new_scalar(d)
            sum_mid = curve.new_scalar(sol + buffer[to_node])
            edge_sum[eid1] = vertex_sum[to_node] + sum_mid
            store[eid1] *= edge_sum[eid1]
            str_point = hexlify(store[eid1].to_bytes()).decode()
            totalBytes[0] += len(str_point)
            totalBytes[0] += temp_count * len(str_point)
            vertex_sum[from_node] += edge_sum[eid1]

    solve_puzzle(g, edge_set, track, curve, ctx, store, vertex_sum, buffer, source, sink, totalBytes)

def solve_puzzle(g, edge_set, track, curve, ctx, store, vertex_sum, buffer, source, sink, totalBytes):
    # Implement the solve_puzzle function as needed
    pass