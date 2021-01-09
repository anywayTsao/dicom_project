from shapely.geometry import Polygon
from shapely.geometry.polygon import BaseGeometry

# https://shapely.readthedocs.io/en/stable/manual.html
p = Polygon([(1, 1), (2, 2), (4, 2), (3, 1)])
q = Polygon([(1.5, 2), (3, 5), (5, 4), (3.5, 1)])

intersection: BaseGeometry = p.intersection(q)
union: BaseGeometry = p.union(q)

print(intersection.area)  # 1.0
print(union.area)  # 1.0

print(intersection.area/union.area)
