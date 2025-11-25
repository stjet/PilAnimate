#pilanimate version 0.4.1
from PIL import Image, ImageDraw, ImageOps, ImageFilter, ImageEnhance, ImageColor, ImageFont, ImageSequence
import cv2
import numpy
from time import sleep
import os, math

class Animation:
  def __init__(self, layer_num, size=(1600,900), fps=25, mode="RGBA", color=0):
    self.layers = []
    self.fps = fps
    self.mode = mode
    self.size = size
    for i in range(layer_num):
      self.layers.append(Layer(size, fps, mode=mode, color=color))
  def export(self, filename="hey"):
    video = cv2.VideoWriter(filename+".avi", cv2.VideoWriter_fourcc(*'XVID'), self.fps, self.size)
    for frame_num in range(len(self.layers[0].frames)):
      frame = Image.new(self.mode, self.size)
      for i in range(len(self.layers)):
        frame.paste(self.layers[i].frames[frame_num], mask=self.layers[i].frames[frame_num])
      video.write(cv2.cvtColor(numpy.array(frame), cv2.COLOR_RGB2BGR))
    video.release()

class Layer:
  def __init__(self, size, fps, mode="RGBA", color=0):
    self.size = size
    self.img = Image.new(mode, size, color=0)
    self.layer = ImageDraw.Draw(self.img)
    self.fps = fps
    self.frames = []
    self.mode = mode

  #functions that draw stuff on
  def createPoint(self, coords, fill=None):
    self.layer.point(coords, fill=fill)
  def createLine(self, coords, fill=None, width=0, joint=None):
    self.layer.line(coords, fill=fill, width=width, joint=joint)
  def createArc(self, boundingBox, startAngle, endAngle, fill=None, width=0):
    self.layer.arc(boundingBox, startAngle, endAngle, fill=fill, width=width)
  def createEllipse(self, boundingBox, fill=None, outline=None, width=0):
    self.layer.ellipse(boundingBox, fill=fill, outline=outline, width=width)
  def createPolygon(self, coords, fill=None, outline=None):
    self.layer.polygon(coords, fill=fill, outline=outline)
  def createRectangle(self, boundingBox, fill=None, outline=None, width=1):
    self.layer.rectangle(boundingBox, fill=fill, outline=outline, width=width)
  def createRoundedRectangle(self, boundingBox, radius=0, fill=None, outline=None, width=0):
    self.layer.rounded_rectangle(boundingBox, radius=radius, fill=fill, outline=outline, width=width)
  def fillAll(self, fill=None, outline=None, width=0):
    self.layer.rectangle(((0,0),self.size), fill=fill, outline=outline, width=width)
  def createText(self, anchorCoords, text, fill=None, font=None, anchor=None, spacing=4, align='left', direction=None, features=None, language=None, stroke_width=0, stroke_fill=None, embedded_color=False):
    self.layer.text(anchorCoords, text, fill=fill, font=font, anchor=anchor, spacing=spacing, align=align, direction=direction, features=features, language=language, stroke_width=stroke_width, stroke_fill=stroke_fill, embedded_color=embedded_color)
  def addImage(self, imageToAdd, coords=None):
    self.img.paste(imageToAdd,box=coords)
  def addGif(self, gif_location, times_to_repeat, coords=None):
    for i in range(times_to_repeat):
      gif = Image.open(gif_location)
      for frame in ImageSequence.Iterator(gif):
        self.img.paste(frame, box=coords)
        self.frames.append(self.img.copy())

  #translation functions
  def rotate(self, angle, center=None, outsideFillColor=None, copy=None):
    if copy:
      self.img = copy.rotate(angle, resample=0, center=center, fillcolor=outsideFillColor)
      self.layer = ImageDraw.Draw(self.img)
    else:
      self.img = self.img.rotate(angle, resample=0, center=center, fillcolor=outsideFillColor)
      self.layer = ImageDraw.Draw(self.img)
  def translate(self, x, y, img):
    newimg = Image.new(self.mode, self.size, color=0)
    newimg.paste(img, (round(0+x),round(0+y)), img)
    self.img = newimg
    self.layer = ImageDraw.Draw(self.img)

  #transparency functions
  def changeOpacity(self, value):
    pixels = self.img.load()
    for x in range(0,self.size[0]):
      for y in range(0,self.size[1]):
        if pixels[x,y] != (0,0,0,0):
          pixels[x,y] = (pixels[x,y][0], pixels[x,y][1], pixels[x,y][2], value)
  def changeEntireOpacity(self, value):
    self.img.putalpha(value)

  #UNTESTED
  def fadeIn(self, frames):
    original = self.img.copy()
    current = 0
    for i in range(frames-1):
      self.img = original
      self.changeOpacity(current+math.floor(100/frames))
      current = current+math.floor(100/frames)
      self.saveFrame()
    self.changeOpacity(100)
    self.saveFrame()
  def fadeOut(self, frames):
    original = self.img.copy()
    current = 100
    for i in range(frames-1):
      self.img = original
      self.changeOpacity(current-math.floor(100/frames))
      current = current-math.floor(100/frames)
      self.saveFrame()
    self.changeOpacity(0)
    self.saveFrame()

  #transform
  def transform(self, size, method, data=None, resample=0, fill=1, fillcolor=None):
    self.img = self.img.transform(size, method, data=data, resample=resample, fill=fill, fillcolor=fillcolor)
    self.layer = ImageDraw.Draw(self.img)

  #color change functions

  #image filter functions
  def blur(self):
    self.img = self.img.filter(ImageFilter.BLUR)
    self.layer = ImageDraw.Draw(self.img)

  #blend

  #clear image functions
  def clear(self, coords):
    self.img.paste(0, coords)
  def clearAll(self):
    self.img.paste(Image.new(self.mode, self.size, color=0))

  #save frame image
  def saveFrame(self):
    self.frames.append(self.img.copy())
  def doNothing(self, frames):
    self.frames = self.frames+[self.img.copy()]*frames
    #for i in range(frames): self.saveFrame()
  
  #turn frame into png
  def save(self, filename):
    self.img.save(filename+".png")

  #shortcut save functions (ie a function that translates every frame and also saves frame)
  def rise(self, frames, total_rise_amount):
    copy = self.img.copy()
    for i in range(frames):
      self.clearAll()
      #if last frame
      if i == frames-1:
        newimg = Image.new(self.mode, self.size, color=0)
        newimg.paste(copy, (0,total_rise_amount), copy)
        self.img = newimg
      self.translate(0,total_rise_amount/frames*(i+1),copy)
      self.saveFrame()
  def descend(self, frames, total_descend_amount):
    copy = self.img.copy()
    for i in range(frames):
      self.clearAll()
      #if last frame
      if i == frames-1:
        newimg = Image.new(self.mode, self.size, color=0)
        newimg.paste(copy, (0,total_descend_amount), copy)
        self.img = newimg
      self.translate(0,total_descend_amount/frames*(i+1),copy)
      self.saveFrame()
  def slide(self, frames, total_slide_amount):
    copy = self.img.copy()
    for i in range(frames):
      self.clearAll()
      #if last frame
      if i == frames-1:
        newimg = Image.new(self.mode, self.size, color=0)
        newimg.paste(copy, (total_slide_amount,0), copy)
        self.img = newimg
      self.translate(total_slide_amount/frames*(i+1), 0, copy)
      self.saveFrame()
  def spin(self, frames, degrees, center):
    copy = self.img.copy()
    for i in range(frames):
      self.rotate(degrees/frames*(i+1), center=center, copy=copy)
      self.saveFrame()
