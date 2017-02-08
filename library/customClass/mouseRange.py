##############################################################################
# CustomClass Rules                                                          #
# =================                                                          #
#                                                                            #
#1. All custom classes must inherit sreb.EBObject and the constructor        #
#   must call sreb.EBObject's constructor. If a class starts with _ then it  #
#   is considered internal and will not be treated as a custom class.        #
#                                                                            #
#2. The custom class will only use the default constructor.                  #  
#   ie. a constructor with no parameters.                                    #
#                                                                            #
#3. To add a property provide getter and have an attribute that does not     #
#   starts with an underscore(_) or an upper case letter, and have the       #
#   attribute of a know type. Known types are int,float,str,EBPoint,EBColor, #
#   tuple, and list.                                                         #
#   If an attribute's default value is of type tuple and only has two        #
#   items, the property will be treated as an EBPoint. Similarly, if an      #
#   attribute's default value is a tuple of 3 items the property will be     #
#   treated as an EBColor.  The input type of the setter and the output type #
#   of the getter is expected to be the same as the type of the attribute.   #
#                                                                            #
#4. If only getter is provided, the property will be a readonly property.    # 
#                                                                            #
#6. The custom class may be instanciated during development to obtain        # 
#   class info. Avoid such things as display mode change, remote connections # 
#   in the constructor.                                                      #
#                                                                            # 
#7. Any method in the custom class can be called using the Execute action    #
#   By default, the return type of the method is string unless a doc string  #
#   with the following constraint is available                               #
#	a. The doc string starts with "RETURN:" (case matters)               #
#       b. Following the text "RETURN:" provide a default value of the type  #
#          or the __repr__ value of the class. eg. str for string            #
#8. If a property's setter metthod has default values for it's parameters,   #
#    the property will not accept references or equation.                    #
##############################################################################


import sreb
import sreb.time
import sreb.graphics
import pygame.mouse
import PIL.ImageGrab
from PIL import *
import time
#import winsound
#import os


class CustomClassTemplate(sreb.EBObject):
	def __init__(self):
		sreb.EBObject.__init__(self)
		self.mouseX = 200
		self.mouseY = 200
		self.oldX = 200
		self.oldY = 200
		self.time = 0
		self.still_time = -1
		self.out_time = 0
		self.out = 0
		self.startX= 200
		self.startY = 200
		self.color = (255,0,0)
#		self.loc = os.getcwd()
#		self.sound_loc = self.loc + '\library\\audio\\audio.wav'
#		
	def getStartX(self):	
		return self.startX 
		
	def setStartX(self, v):	
		self.startX = v
		
	def getStartY(self):	
		return self.startY
		
	def setStartY(self, v):	
		self.startY = v
		
	def getMouseX(self):
		return self.mouseX
			
	def setMouseX(self, v):
		self.mouseX = v
		
	def getMouseY(self):
		return self.mouseY
		
	def setMouseY(self, v):
		self.mouseY = v
		
	def getColor(self):
		return self.color
	
	def setColor(self,v):
		self.color = v
		
	def updateMouseRange(self, x, y):
		(r1,g1,b1) = self.get_pixel_color(self.mouseX-1,self.mouseY-1)
		(r2,g2,b2) = self.get_pixel_color(self.mouseX+6,self.mouseY+6)
		limit=200
		ulimit = 100
		still_limit = 1.9
		if(((r1==0) and (g1==0) and (b1 > limit)) or ((r2==0) and (g2==0) and (b2>limit))):
			self.oldX = self.mouseX
			self.oldY = self.mouseY
			self.mouseY = self.startY
			self.mouseX = self.startX
			pygame.mouse.set_pos([self.startX,self.startY])
			self.still_time = time.time()
			self.out = 0
		elif((time.time()-self.still_time) > still_limit):
			self.mouseY = self.startY
			self.mouseX = self.startX
			self.oldX = self.mouseX
			self.oldY = self.mouseY
			pygame.mouse.set_pos([self.startX,self.startY])
			self.still_time = time.time()
		elif(((time.time()-self.out_time) > still_limit) and (self.out ==1)):
			
			self.mouseY = self.startY
			self.mouseX = self.startX
			self.oldX = self.mouseX
			self.oldY = self.mouseY
			pygame.mouse.set_pos([self.startX,self.startY])
			self.still_time = time.time()
			self.out = 0
		elif ((self.out == 0) and (((r1<limit) and (g1<limit) and (b1<limit)) or ((r2<limit) and (g2<limit) and (b2<limit)))):
			self.out = 1
			self.out_time = time.time()
			self.oldX = self.mouseX
			self.oldY = self.mouseY
			self.mouseY = y
			self.mouseX = x
			self.still_time = time.time()
			#winsound.PlaySound(self.sound_loc, winsound.SND_FILENAME)
		elif((self.mouseX != x) and (self.mouseY != y) and (not(((r1<limit) and (g1<limit) and (b1<limit)) or ((r2<limit) and (g2<limit) and (b2<limit))))):
			self.out = 0
			self.oldX = self.mouseX
			self.oldY = self.mouseY
			self.mouseY = y
			self.mouseX = x
			self.still_time = time.time()
		elif((self.mouseX != x)and (self.mouseY != y) and (self.out ==1)):
			self.oldX = self.mouseX
			self.oldY = self.mouseY
			self.mouseY = y
			self.mouseX = x
			self.still_time = time.time()
			#winsound.PlaySound(self.sound_loc, winsound.SND_FILENAME)
		elif((self.mouseX != x) or (self.mouseY != y)):
			self.oldX = self.mouseX
			self.oldY = self.mouseY
			self.mouseY = y
			self.mouseX = x
			self.still_time = time.time()
		else:
			self.mouseY = y
			self.mouseX = x

			
	def get_pixel_color(self, i_x, i_y):
		im = PIL.ImageGrab.grab()
		return(im.getpixel((i_x, i_y)))
#		print(' ')
#		print(im)
#		print(' ')
#		return im[i_x,i_y]
#    		i_desktop_window_id = win32gui.GetDesktopWindow()
#    		i_desktop_window_dc = win32gui.GetWindowDC(i_desktop_window_id)
#    		long_colour = win32gui.GetPixel(i_desktop_window_dc, i_x, i_y)
#    		i_color = int(long_colour)
#    		return((i_color & 0xff), ((i_color >>8) & 0xff), ((i_color >>16) & 0xff))
			
