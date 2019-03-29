import pygame as py

class point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

class rectangle:
  def __init__(self, boundary):
    self.x, self.y, self.w, self.h = boundary
    self.boundary = boundary

  def contain(self, point):
    return self.x <= point.x < self.x + self.w and self.y <= point.y < self.y + self.h

  def intersect_rectangle(self, Range):
    if self.x + self.w < Range.x \
      or self.x > Range.x + Range.w \
      or self.y > Range.y + Range.h \
      or self.y + self.h < Range.y:
      return False
    return True

  def intersect_circle(self, Range):
    if self.contain(point(Range.x, Range.y)):
      return True
    if (self.x + self.w//2 - Range.x)**2 + (self.y - Range.y)**2 <= Range.radius**2 \
      or (self.x - Range.x)**2 + (self.y + self.h//2- Range.y)**2 <= Range.radius**2 \
      or (self.x + self.w - Range.x)**2 + (self.y + self.h//2 - Range.y)**2 <= Range.radius**2 \
      or (self.x + self.w//2 - Range.x)**2 + (self.y + self.h - Range.y)**2 <= Range.radius**2:
      return True
    return False


class circle:
  def __init__(self, center, radius):
    self.x, self.y = center
    self.radius = radius

  def contain(self, point):
    return (point.x - self.x)**2 + (point.y - self.y)**2 < self.radius**2

class qtree:
  def __init__(self, boundary, capacity):
    self.boundary = rectangle(boundary)
    self.capacity = capacity
    self.points = []
    self.divided = False
    self.northwest, self.northeast, self.southwest, self.southeast = (None,None,None,None)

  def insert(self, point):
    if not self.boundary.contain(point):
      return False
    if self.capacity > len(self.points):
      self.points.append(point)
      return True
    else:
      if not self.divided:
        self.divide()
        self.assign_points()
      if self.northwest.insert(point):
        return True
      elif self.northeast.insert(point):
        return True
      elif self.southwest.insert(point):
        return True
      elif self.southeast.insert(point):
        return True

  def divide(self):
    x = self.boundary.x
    y = self.boundary.y
    w = self.boundary.w
    h = self.boundary.h

    self.northwest = qtree((x, y, w//2, h//2), self.capacity)
    self.northeast = qtree((x + w//2, y, w//2, h//2), self.capacity)
    self.southwest = qtree((x, y + h//2, w//2, h//2), self.capacity)
    self.southeast = qtree((x + w//2, y + h//2, w//2, h//2), self.capacity)
    self.divided = True

  def show(self, screen):
    x = self.boundary.x
    y = self.boundary.y
    w = self.boundary.w
    h = self.boundary.h
    py.draw.rect(screen, (255,255,255), (x,y,w,h), 1)

    for p in self.points:
      py.draw.circle(screen, (255,255,255), (p.x, p.y), 2, 1)

    if self.divided:
      if len(self.northwest.points) != 0:
        self.northwest.show(screen)
      if len(self.northeast.points) != 0:
        self.northeast.show(screen)
      if len(self.southwest.points) != 0:
        self.southwest.show(screen)
      if len(self.southeast.points) != 0:
        self.southeast.show(screen)

  def assign_points(self):
    for point in self.points:
      if self.northwest.boundary.contain(point):
        self.northwest.points.append(point)
      elif self.northeast.boundary.contain(point):
        self.northeast.points.append(point)
      elif self.southeast.boundary.contain(point):
        self.southeast.points.append(point)
      else:
        self.southwest.points.append(point)

  def query(self, Range, found):
    try:
      if not self.boundary.intersect_circle(Range):
       return
    except AttributeError:
      if not self.boundary.intersect_rectangle(Range):
        return
    if self.divided:
      self.northwest.query(Range, found)
      self.northeast.query(Range, found)
      self.southeast.query(Range, found)
      self.southwest.query(Range, found)
    else:
      for point in self.points:
        if Range.contain(point):
          found.append(point)
    return found