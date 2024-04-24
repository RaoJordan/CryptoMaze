#include "header.h"

# void approve_push(igraph_t *g, igraph_integer_t vid_neighbour, int flow, int *height)
# {
#     int excess;
#     excess = (igraph_integer_t)igraph_cattribute_VAN(g, "excess", vid_neighbour);
#     igraph_cattribute_VAN_set(g, "excess", vid_neighbour, excess + flow);
#     if (strcmp("sink", igraph_cattribute_VAS(g, "type", vid_neighbour)) != 0)
#     {
#         //		printf("exit=%s\n",igraph_cattribute_VAS(g,"type",vid_neighbour));
#         lift(g, height, vid_neighbour);
#     }
# }

from header import lift

def approve_push(g, vid_neighbour, flow, height):
    excess = g.vs[vid_neighbour]["excess"]
    g.vs[vid_neighbour]["excess"] = excess + flow
    if g.vs[vid_neighbour]["type"] != "sink":
        lift(g, height, vid_neighbour)
