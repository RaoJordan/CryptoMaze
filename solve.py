from typing import List
from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Util.number import bytes_to_long
from igraph import Graph
import numpy as np

def solve_puzzle(g, edge_set, track, curve, ctx, store, vertex_sum, buffer, source, sink, totalBytes):
    mark = np.zeros(len(g.es), dtype=int)
    soln = [None] * len(g.es)

    for i in range(len(g.es)):
        soln[i] = 0

    for j in range(track):
        from_idx, to_idx = g.es[edge_set[j]].tuple
        eid1 = g.get_eid(from_idx, to_idx, directed=True)
        if mark[eid1] == 0:
            mark[eid1] = 1
            if to_idx != sink:
                vs = g.neighbors(to_idx, mode="out")
                for vid_neighbour in vs:
                    eid2 = g.get_eid(to_idx, vid_neighbour, directed=True)
                    if mark[eid2] == 1:
                        soln[eid1] += soln[eid2]

            d_temp = f"{bytes_to_long(buffer[to_idx]):x}{eid1}"
            d = SHA256.new(d_temp.encode()).digest()
            sol = int.from_bytes(d, "big")
            sum_mid = sol + bytes_to_long(buffer[to_idx]) + int(vertex_sum[to_idx])
            soln[eid1] += sum_mid

            R_u = curve.mul(soln[eid1], None)
            str_val = R_u.export_key(format="HEX").decode()
            str1 = curve.mul(soln[eid1], None).export_key(format="HEX").decode()

            if str_val == str1:
                totalBytes[0] += len(str_val)
                print(f"preimage released e({from_idx},{to_idx})")
            else:
                print(f"preimage not e({from_idx},{to_idx}) Ru,{str_val}")

# Example usage
# g = ...  # Initialize your graph
# edge_set = [...]  # Initialize your edge set
# curve = ECC.import_key(...)  # Initialize your elliptic curve
# ctx = ...  # Initialize your BN_CTX
# store = [...]  # Initialize your store array
# vertex_sum = [...]  # Initialize your vertex_sum array
# buffer = [...]  # Initialize your buffer array
# source = ...  # Initialize your source vertex
# sink = ...  # Initialize your sink vertex
# totalBytes = [0]  # Initialize your totalBytes array
# solve_puzzle(g, edge_set, 0, curve, ctx, store, vertex_sum, buffer, source, sink, totalBytes)
