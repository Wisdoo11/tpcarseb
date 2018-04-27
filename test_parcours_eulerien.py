#!/usr/bin/env python3

"""
display given segment files
"""
import sys
from geo.segment import load_segments
from geo.graph import *
from geo.tycat import tycat
from geo.point import *
import time

# p1 = Point([0,0])
# p2 = Point([0,1])
# p3 = Point([1,0])
# p4 = Point([1,1])
# p5 = Point([1,2])
# p6 = Point([2,0])
# p7 = Point([2,1])
# p8 = Point([2,2])
# p9 = Point([3,0])
# p10 = Point([3,1])
#
# liste_segments= [Segment([p1,p2]),Segment([p1,p3]),Segment([p2,p4]),Segment([p3,p4]),Segment([p4,p7]),Segment([p4,p5]),Segment([p5,p8]),Segment([p7,p8]),Segment([p7,p10]),Segment([p7,p6]),Segment([p6,p9]),Segment([p9,p10])]
# print(Segment([p1,p2])==Segment([p2,p1]))
# graph_test = Graph(liste_segments)
# # tycat (p1,p2)
# # tycat(graph_test)
# graph_test.eulerian_cycle()
# tycat(graph_test)

def main():
    filename = sys.argv[1]
    segments = load_segments(filename)
    graphe_def = Graph(segments)
    tycat(graphe_def)
    hash_points = True
    graphe_def.reconnect(hash_points)
    tycat(graphe_def)
    graphe_def.even_degrees(hash_points)
    tycat(graphe_def)
    liste=graphe_def.eulerian_cycle()
    n= len(liste)
    if n==0:
        pass
    elif n==1:
        pass
    else:
        segments_rep =[]
        for k in range(n-1):
            segments_rep.append(Segment([liste[k],liste[k+1]]))
            #graphe_rep = Graph(segments_rep)
            #tycat(graphe_rep)
        for k in range(n-1):
            segments_rep.pop()
            graphe_rep = Graph(segments_rep)
            tycat(graphe_rep)





main()
