"""
graph structure
"""
from itertools import chain, combinations
from geo.quadrant import Quadrant
from geo.union import UnionFind
from geo.segment import Segment


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
        """ retourne un itérateur sur les segments, du plus petit au plus grand """
        liste_points = list(self.vertices.keys())
        liste_segments = []
        n = len(liste_points)
        for i in range(n):
            for j in range(i+1, n):
                liste_segments.append(Segment([liste_points[i], liste_points[j]]))
        for segment in sorted(liste_segments, key=lambda segment: segment.length()):
            yield segment


    def hasher(self, t):
        """
        retourne un tableau de 4 tables de hachages et un booléen indiquant s'il y a des collision
        """
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
        """ retourne un itérateur sur les segments en utilisant le hash """
        tables = []
        t = 3 * max(self.bounding_quadrant().max_coordinates[0] - \
                self.bounding_quadrant().min_coordinates[0], \
                self.bounding_quadrant().max_coordinates[1] - \
                self.bounding_quadrant().min_coordinates[1]) # precision de depart
        table_hachage, collision = self.hasher(t)
        tables.append(table_hachage)
        while collision:
            t /= 2
            table_hachage, collision = self.hasher(t)
            tables.append(table_hachage)

        tables.reverse()
        tables = tables[1:]

        for table_hachage in tables:
            for dico in table_hachage:
                for point_carre in dico.keys():
                    n = len(dico[point_carre])
                    for i in range(n):
                        for j in range(i+1, n):
                            yield Segment([dico[point_carre][i], dico[point_carre][j]])

    def composantes_connexes(self):
        """ retourne les composantes connexes sous la structure UnionFind"""
        sommets = list(self.vertices.keys())
        unionfind = UnionFind(sommets)
        for sommet in sommets:
            for segment in self.vertices[sommet]:
                unionfind.union(sommet, segment.endpoint_not(sommet))
        return unionfind


    def reconnect(self, hash_points):
        """
        greedily add edges until graph is fully connected.
        if hash_points is true then use hashed segments iterator
        else use quadratic segments iterator.
        """

        if hash_points:
            iterator = self.hashed_segments_iterator()
        else:
            iterator = self.quadratic_segments_iterator()

        unionfind = self.composantes_connexes()

        for segment in iterator:
            p1 = segment.endpoints[0]
            p2 = segment.endpoints[1]
            if unionfind.find(p1) != unionfind.find(p2):
                self.vertices[p1].append(segment)
                self.vertices[p2].append(segment)
                unionfind.union(p1, p2)
            if len(unionfind) == 1:
                return

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
        sommets_impairs = []
        segments_ajoutes = []
        for vertex in self.vertices.keys():
            if len(self.vertices[vertex]) % 2 == 1:
                odd += 1
                sommets_impairs.append(vertex)

        while odd != 0:
            segment = next(iterator)
            p1 = segment.endpoints[0]
            p2 = segment.endpoints[1]
            if len(self.vertices[p1]) % 2 == 1 and len(self.vertices[p2]) % 2 == 1:
                self.vertices[p1].append(segment)
                self.vertices[p2].append(segment)
                segments_ajoutes.append(segment)
                odd -= 2

    def copy(self):
        """ return a deepcopy of a graph """
        copie = Graph([])
        for point in self.vertices.keys():
            copie.vertices[point] = self.vertices[point][:] #deepcopy
        return copie

    def parcours_aleatoire(self, point_depart, liste, pos):
        """ à partir de point_depart, insère dans liste, à partir de l'indice pos, des sommets formant un cycle """
        ajouts = 1
        point = point_depart
        while self.vertices[point] != []:
            point_pre = point
            seg = self.vertices[point].pop() # supprime le segment de choix et le retourne
            point = seg.endpoint_not(point_pre)
            self.vertices[point].remove(Segment([point_pre, point])) # supprime le segment "doublon"
            liste.insert(pos + ajouts, point)
            ajouts += 1

    def eulerian_cycle(self):
        """
        return eulerian cycle. precondition: all degrees are even.
        """
        graphe_copie = self.copy()
        point = list(graphe_copie.vertices.keys())[0]
        liste = [point]
        pos = 0
        while pos < len(liste):
            p = liste[pos]
            graphe_copie.parcours_aleatoire(p, liste, pos)
            pos += 1

        def listpoints_to_listsegments(listpoints):
            """retourne une liste de segments à partir d'une liste de points"""
            listsegments = []
            for i in range(len(listpoints)-1):
                listsegments.append(Segment([listpoints[i], listpoints[i+1]]))
            return listsegments

        return listpoints_to_listsegments(liste)
