#!/usr/bin/env python3

"""
display given segment files
"""
import sys
from geo.segment import load_segments
from geo.graph import *
from geo.tycat import tycat
import random
from geo.point import *
import time

def display(filename):
    """
    load segment file, get back connexity, get even degrees, display eulerian path.
    """
    segments = load_segments(filename)
    graphe1 = Graph(segments)
    graphe2 = Graph(segments)

    tycat(graphe1)

    t1 = time.time()
    graphe1.reconnect(False)
    t2 = time.time()

    t1h = time.time()
    graphe2.reconnect(True)
    t2h = time.time()

    tycat(graphe1)
    tycat(graphe2)

    print("Temps mis pour reconnecter le graphe : ")
    print("Sans hash : {}".format(t2-t1))
    print("Avec hash : {}".format(t2h-t1h))


    t1 = time.time()
    graphe1.even_degrees(False)
    t2 = time.time()

    t1h = time.time()
    graphe2.even_degrees(True)
    t2h = time.time()

    tycat(graphe1)
    tycat(graphe2)

    print("Temps mis par even_degrees: ")
    print("Sans hash : {}".format(t2-t1))
    print("Avec hash : {}".format(t2h-t1h))


    t1 = time.time()
    cycle1 = graphe1.eulerian_cycle()
    t2 = time.time()

    t1h = time.time()
    cycle2 = graphe2.eulerian_cycle()
    t2h = time.time()

    tycat(cycle1)
    tycat(cycle2)

    print("Temps mis pour trouver un cycle eulérien : ")
    print("Sur graphe1 : {}".format(t2-t1))
    print("Sur graphe2 : {}".format(t2h-t1h))


    print("Nombres de sommets : {}".format(len(graphe2.vertices.keys())))
    print("Nombres d'arêtes {}".format(len(segments)))

def main():
    """
    launch test on each file.
    """
    for filename in sys.argv[1:]:
        display(filename)

main()
