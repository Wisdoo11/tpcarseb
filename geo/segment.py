"""
segment between two points.
"""
import struct
from geo.point import Point
from geo.quadrant import Quadrant


class Segment:
    """
    oriented segment between two points.

    for example:

    - create a new segment between two points:

        segment = Segment([point1, point2])

    - create a new segment from coordinates:

        segment = Segment([Point([1.0, 2.0]), Point([3.0, 4.0])])

    - compute intersection point with other segment:

        intersection = segment1.intersection_with(segment2)

    """
    def __init__(self, points):
        """
        create a segment from an array of two points.
        """
        self.endpoints = points

    def copy(self):
        """
        return duplicate of given segment (no shared points with original,
        they are also copied).
        """
        return Segment([p.copy() for p in self.endpoints])

    def length(self):
        """
        return length of segment.
        example:
            segment = Segment([Point([1, 1]), Point([5, 1])])
            distance = segment.length() # distance is 4
        """
        return self.endpoints[0].distance_to(self.endpoints[1])

    def bounding_quadrant(self):
        """
        return min quadrant containing self.
        """
        quadrant = Quadrant.empty_quadrant(2)
        for point in self.endpoints:
            quadrant.add_point(point)
        return quadrant

    def svg_content(self):
        """
        svg for tycat.
        """
        return '<line x1="{}" y1="{}" x2="{}" y2="{}"/>\n'.format(
            *self.endpoints[0].coordinates,
            *self.endpoints[1].coordinates)

    def endpoint_not(self, point):
        """
        return first endpoint which is not given point.
        """
        if self.endpoints[0] == point:
            return self.endpoints[1]

        return self.endpoints[0]

    def contains(self, possible_point):
        """
        is given point inside us ?
        be careful, determining if a point is inside a segment is a difficult problem
        (it is in fact a meaningless question in most cases).
        you might get wrong results for points extremely near endpoints.
        """
        distance = sum(possible_point.distance_to(p) for p in self.endpoints)
        return abs(distance - self.length()) < 0.000001

    def __eq__(self, other):
        return (self.endpoints[0] == other.endpoints[0] \
                and self.endpoints[1] == other.endpoints[1]) \
                or \
                (self.endpoints[0] == other.endpoints[1] and \
                self.endpoints[1] == other.endpoints[0])

    def __str__(self):
        return "Segment([" + str(self.endpoints[0]) + ", " + \
            str(self.endpoints[1]) + "])"

    def __repr__(self):
        return "[" + repr(self.endpoints[0]) + ", " + \
            repr(self.endpoints[1]) + "])"

    def __hash__(self):
        return hash(tuple(self.endpoints))


def load_segments(filename):
    """
    loads given .bo file.
    returns a vector of segments.
    """
    coordinates_struct = struct.Struct('4d')
    segments = []

    with open(filename, "rb") as bo_file:
        packed_segment = bo_file.read(32)
        while packed_segment:
            coordinates = coordinates_struct.unpack(packed_segment)
            points = [Point(coordinates[0:2]), Point(coordinates[2:])]
            segments.append(Segment(points))
            packed_segment = bo_file.read(32)

    return segments
