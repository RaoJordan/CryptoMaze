from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import igraph
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import utils
import os

def payment(g, height, source, sink, totalBytes):
    curve = ec.SECP224R1()
    G = curve.generator
    order = curve.order
    ctx = ec.default_backend()

    rnd = [os.urandom(28) for _ in range(len(g.vs))]

    buffer = [None] * len(g.vs)
    bfs_edge_marker = [0] * len(g.es)

    for vid in range(len(g.vs)):
        if vid != source:
            rnd[vid] = os.urandom(28)

    bfs_mark(g, bfs_edge_marker, height, source, sink, curve, ctx, rnd, totalBytes)

