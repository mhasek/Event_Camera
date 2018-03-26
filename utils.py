import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
import pdb
import sys

class event_stream:
	def __init__(self,fname):
		
		self.file = open(fname,'r')

		file_format = self.file.readline()

		self.nc = int(file_format.split()[-1])
		self.nr = int(file_format.split()[-3])
		self.t0_nsecs = int(file_format.split()[-5])
		self.t0_secs = int(file_format.split()[-6])		

	def get_event(self):

		event_txt = self.file.readline()

		event_txt = event_txt.split()

		x = int(event_txt[0])
		y = int(event_txt[1])
		polarity = int(event_txt[2])
		time_secs = int(event_txt[3]) - self.t0_secs
		time_nsecs = int(event_txt[4]) - self.t0_nsecs
		time = round(time_secs + time_nsecs*1e-9,6)

		return (x,y,polarity,time)


class event_image:
	def __init__ (self,nr,nc,pixel_buffer):

		self.nr = nr
		self.nc = nc
		self.N_buffer = pixel_buffer
		self.events_pos = np.zeros((nr,nc,pixel_buffer))
		self.events_neg = np.zeros((nr,nc,pixel_buffer))


	def insert_event(self,x,y,polarity,time):

		if polarity == 1:
			self.events_pos[y][x][1:] = self.events_neg[y][x][0:-1]
			self.events_pos[y][x][0] = time
		else:
			self.events_neg[y][x][1:] = self.events_neg[y][x][0:-1]
			self.events_neg[y][x][0] = time			

	def extract_stmp_window(self,x,y,polarity,time,s_window,e_window):
		xmin = x - s_window
		xmax = x + s_window
		ymin = y - s_window
		ymax = y + s_window

		N = s_window*2 + 1

		xs = np.tile(np.arange(xmin,xmax+1),N)
		ys = np.repeat(np.arange(ymin,ymax+1),N)

		if polarity == 1:
			events = self.events_pos[ys][xs].reshape(-1)
		else:
			events = self.events_neg[ys][xs].reshape(-1)

		xs = np.repeat(xs, self.N_buffer)
		ys = np.repeat(ys, self.N_buffer)

		e_idx = events>0

		xs = xs[e_idx]
		ys = ys[e_idx]
		events = events[e_idx]


		return (xs,ys,events)