#!/usr/bin/env python3

"""
display given segment files
"""
import sys
from geo.segment import load_segments
from geo.graph import *
from geo.tycat import tycat

def display(filename):
    """
    load segment file, get back connexity, get even degrees, display eulerian path.
    """
    segments = load_segments(filename)
    mon_graphe = Graph(segments)
    print("Nombre de points: {}".format(len(mon_graphe.vertices.keys())))
    iterateur_quadratique = list(mon_graphe.quadratic_segments_iterator())
    iterateur_hash = list(mon_graphe.hashed_segments_iterator())
    print(len(list(iterateur_hash)))
    print("{}: nous avons {} segments".format(filename, len(segments)))
    tycat(list(iterateur_quadratique),list(mon_graphe.vertices.keys()))

#Modification

def main():
    """
    launch test on each file.
    """
    for filename in sys.argv[1:]:
        display(filename)

main()
