"""
graph structure
"""
from itertools import chain, combinations
from geo.quadrant import Quadrant
from geo.union import UnionFind
from geo.segment import Segment
from geo.hash import ordered_segments


class Graph:
    """
    create a graph from given set of segments.
    each endpoint is a vertex, each segment an edge.
    """
    def __init__(self, segments):
        self.vertices = dict()
        for segment in segments:
            for point in segment.endpoints:
                if point not in self.vertices:
                    self.vertices[point] = []
                self.vertices[point].append(segment)

    def bounding_quadrant(self):
        """
        return min quadrant containing underlying objects.
        """
        quadrant = Quadrant.empty_quadrant(2)
        for point in self.vertices:
            quadrant.add_point(point)
        return quadrant

    def svg_content(self):
        """
        svg for tycat.
        """
        edges = (e for (p, edges) in self.vertices.items() for e in edges if e.endpoints[0] == p)
        return "\n".join(c.svg_content() for c in chain(self.vertices.keys(), edges))


    def quadratic_segments_iterator(self):
        """ quadratic segments iterator """
        liste_points = list(self.vertices.keys())
        liste_segments = []
        n = len(liste_points)
        for i in range(n):
            for j in range(i+1, n):
                liste_segments.append(Segment([liste_points[i], liste_points[j]]))
        for segment in sorted(liste_segments, key=lambda segment: segment.length()):
            yield segment

        # def union(list_a, list_b):
        #     """ return the union of two lists """
        #     return list(set(list_a) | set(list_b))
        #
        # segments = []
        # for vertex in self.vertices.keys():
        #     segments = union(segments, self.vertices[vertex])
        # # segments is now a list containing all the segments of the graph
        #
        # for segment in sorted(segments, key=lambda segment: segment.length()):
        #     yield segment

    def hasher(self, t):
        """ description """
        collision = False
        table_hachage = [{}, {}, {}, {}]
        for point in self.vertices.keys():
            for i in range(4):
                point_carre = point.hash_function(t, i)
                if point_carre not in table_hachage[i]:
                    table_hachage[i][point_carre] = []
                else:
                    collision = True
                table_hachage[i][point_carre].append(point)
        return table_hachage, collision

    def hashed_segments_iterator(self):
        """description"""
        tables = []
        t = 1 # precision de depart
        table_hachage, collision = self.hasher(t)
        tables.append(table_hachage)
        while collision:
            t /= 2
            table_hachage, collision = self.hasher(t)
            tables.append(table_hachage)
        for table_hachage in reversed(tables):
            for elt in table_hachage:
                for point_carre in elt.keys():
                    n = len(list(elt.keys()))
                    for i in range(n):
                        for j in range(i+1, n):
                            yield Segment([elt[point_carre][i], elt[point_carre][j]])

    def construire_composante_connexe(self, comp_connexes, point, point_ref):
        comp_connexes.add(point)
        comp_connexes.union(point, point_ref)
        for segment in self.vertices[point]:
            if segment.endpoint_not(point) not in comp_connexes.parents:
                self.construire_composante_connexe(comp_connexes, segment.endpoint_not(point), point_ref)


    def composantes_connexes(self):
        comp_connexes = UnionFind()
        for vertex in self.vertices.keys():
            if vertex not in comp_connexes.parents:
                comp_connexes.add(vertex)
                self.construire_composante_connexe(comp_connexes, vertex, vertex)

    def reconnect(self, hash_points):
        """
        greedily add edges until graph is fully connected.
        if hash_points is true then use hashed segments iterator
        else use quadratic segments iterator.
        """
        pass

    def even_degrees(self, hash_points):
        """
        greedily add edges until all degrees are even.
        if hash_points is true then use hashed segments iterator
        else use quadratic segments iterator.
        """
        if hash_points:
            iterator = self.hashed_segments_iterator()
        else:
            iterator = self.quadratic_segments_iterator()

        odd = 0
        for vertex in self.vertices.keys():
            if len(self.vertices[vertex]) % 2 == 1:
                odd += 1
        while odd != 0:
            segment = next(iterator)
            p1 = segment.endpoints[0]
            p2 = segment.endpoints[1]
            if len(self.vertices[p1]) % 2 == 1 and len(self.vertices[p1]) % 2 == 1:
                self.vertices[p1].append(segment)
                self.vertices[p2].append(segment)
                odd -= 2

    def eulerian_cycle(self):
        """
        return eulerian cycle. precondition: all degrees are even.
        """
        pass
