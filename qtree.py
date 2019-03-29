import  pygame as py
import qtreeClass as qt
from random import randint
py.init()

width, height = 800, 800
screen = py.display.set_mode((width,height))

Qtree = qt.qtree((0,0,width,height), 4)
points = []
for i in range(300):
  points.append(qt.point(randint(0, width), randint(0, height)))

def get_point():
  for point in points:
    yield points.pop(0)

range_rectangle = qt.rectangle(
      (randint(0, width//2),
       randint(0, height//2),
       randint(width//4, width),
       randint(height//4, height)))
def get_range_rectangle():
  py.draw.rect(screen, (0,0,255), range_rectangle.boundary, 3)
  return Qtree.query(range_rectangle, [])

range_circle = qt.circle((randint(0,width),randint(0,height)), 300)
def get_range_circle():
  py.draw.circle(
      screen, (255,0,0), (range_circle.x, range_circle.y), range_circle.radius, 3)
  return Qtree.query(range_circle, [])

clock = py.time.Clock()
game = True
while game:
  for event in py.event.get():
    if event.type == py.QUIT:
      game = False
    if event.type == py.MOUSEBUTTONDOWN:
      points.append(qt.point(*py.mouse.get_pos()))

  for point in get_point():
    Qtree.insert(point)
    Qtree.show(screen)
    py.display.update()
    # clock.tick(60)
  if len(points) == 0:
    circle_points = get_range_circle()
    rectanle_points = get_range_rectangle()
    for point in circle_points:
      py.draw.circle(screen, (255,0,0), (point.x, point.y), 2, 2)
    for point in rectanle_points:
      py.draw.circle(screen, (0,0,255), (point.x, point.y), 2, 2)
    intersecting_points = list(set(circle_points).intersection(set(rectanle_points)))
    for point in intersecting_points:
      py.draw.circle(screen, (0,255,0), (point.x, point.y), 2, 2)
  py.display.update()

py.quit()