#/usr/bin/env python

import serial
from PIL import Image

#Adapted from github: haniview@haum

def init_ser():
   ser = serial.Serial()
   ser.port = "/dev/ttyUSB0"
   ser.baudrate = 57600
   ser.bytesize = 8
   ser.stopbits = 1
   ser.parity = serial.PARITY_EVEN
   # TODO: reduce timeout by waiting for the correct amount of bytes
   ser.timeout = 0.4
   try:
     ser.open()
   except serial.SerialException:
      print "ERROR"
      exit(1)
   return ser

def print_hex(s):
    print ("len(): " + str(len(s)))
    for i in range(0, len(s)):
        print(hex(s[i])),
    print ""

def get_bytes(filename):
   im = Image.open(filename)
   rgb_im = im.convert('RGB')
   for y in range(0, 32):
     for column_byte in range(0, 20):
       byte_red = 0x00
       byte_green = 0x00
       for column_bit in range(0, 8):
          x = column_byte * 8 + column_bit
          r, g, b = rgb_im.getpixel((x, y))
          if (r>127): byte_red |= (1 << (7-column_bit))
          if (g>127): byte_green |= (1 << (7-column_bit))
   return byte_red, byte_green 

class Haniview: 
   def __init__(self):
      self.ser=init_ser()
      self.frame_dict=cp.load(open(frame_dict))
      self.byte_red=0
      self.byte_green=0

   def send_frame(self, frame):
       print("send frame:")
       print_hex(frame)
       while len(frame):
         chunk = frame[:100]
         print("send chunk:")
         print_hex(chunk)
         ser.write(chunk)
         frame = frame[100:]
       self.ser.flush()
       s = ser.read(100)
       print "read:"
       print_hex(bytearray(s))

   def get_bytes(filename):
      im = Image.open(filename)
      rgb_im = im.convert('RGB')
      for y in range(0, 32):
         for column_byte in range(0, 20):
            self.byte_red = 0x00
            self.byte_green = 0x00
            for column_bit in range(0, 8):
                x = column_byte * 8 + column_bit
                r, g, b = rgb_im.getpixel((x, y))
                if (r>127): self.byte_red |= (1 << (7-column_bit))
                if (g>127): self.byte_green |= (1 << (7-column_bit))
           p = y * 20 + column_byte
           self.update_redgreen(p)

   def update_redgreen(self, p):
      if (p<209): # First 209 red bytes go in first frame
         self.frame_dict["frame_image_0"][57+p] = byte_red
      elif (p<(209+256)):
         self.frame_dict["frame_image_1"][10+(p-209)] = byte_red
      else:
         self.frame_dict["frame_image_2"][10+(p-465)] = byte_red
      if (p<81): # First 81 green bytes go at the end of 3rd frame
         self.frame_dict["frame_image_2"][10+175+p] = byte_green
      elif (p<(81+256)):
         self.frame_dict["frame_image_3"][10+(p-81)] = byte_green
      elif (p<(81+256+256)):
         self.frame_dict["frame_image_4"][10+(p-(81+256))] = byte_green
      else:
         self.frame_dict["frame_image_5"][10+(p-(81+256+256))] = byte_green

   def send_image(self, filename):
      self.get_bytes(filename)
      for frame in self.frame_dict:
        self.send_frame(frame)
     self.ser.close()

frame_file="frames"
im_file="plop.png"
haniview=Haniview(frame_file)
if haniview.ser.isOpen():
       

    ser.close()

    
exit(0)
