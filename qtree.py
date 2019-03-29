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

Range = qt.rectangle(
      (randint(0, width//2),
       randint(0, height//2),
       randint(width//4, width),
       randint(height//4, height)))

def get_range():
  py.draw.rect(screen, (0,0,255), Range.boundary, 4)
  return Qtree.query(Range, [])


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
    for point in get_range():
      py.draw.circle(screen, (255,0,0), (point.x, point.y), 2, 2)
  py.display.update()


py.quit()