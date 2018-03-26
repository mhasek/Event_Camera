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
		self.event_im = np.zeros((nr,nc,3))
		
		self.v_pos_x = np.zeros((nr,nc))
		self.v_pos_y = np.zeros((nr,nc))
		self.v_neg_x = np.zeros((nr,nc))
		self.v_neg_y = np.zeros((nr,nc))
		
		self.vx = np.zeros((nr,nc))
		self.vy = np.zeros((nr,nc))

	def reset_buffer(self,t,t_expire):
		self.v_pos_x[ (self.events_pos < (t - t_expire))[:,:,0] ] = 0
		self.v_pos_y[ (self.events_pos < (t - t_expire))[:,:,0] ] = 0
		self.v_neg_x[ (self.events_neg < (t - t_expire))[:,:,0] ] = 0
		self.v_neg_y[ (self.events_neg < (t - t_expire))[:,:,0] ] = 0

		self.events_pos[self.events_pos < (t - t_expire)] = 0
		self.events_neg[self.events_neg < (t - t_expire)] = 0

	def insert_event(self,x,y,polarity,time):

		if polarity == 1:
			self.events_pos[y][x][1:] = self.events_pos[y][x][0:-1]
			self.events_pos[y][x][0] = time
		else:
			self.events_neg[y][x][1:] = self.events_neg[y][x][0:-1]
			self.events_neg[y][x][0] = time			

	def update_image(self):
		self.event_im[:,:,0] = self.events_pos[:,:,0] > 0
		self.event_im[:,:,2] = self.events_neg[:,:,0] > 0

	def insert_flow(self,x,y,vx,vy,polarity):
		if polarity == 1:
			self.v_pos_x[y][x] = vx
			self.v_pos_y[y][x] = vy
		else:
			self.v_pos_x[y][x] = vx
			self.v_pos_y[y][x] = vy

		self.vx = self.v_pos_x + self.v_neg_x
		self.vy = self.v_pos_x + self.v_neg_x

	def extract_stmp_window(self,x,y,polarity,time,s_window):
		xmin = x - s_window
		xmax = x + s_window
		ymin = y - s_window
		ymax = y + s_window

		N = s_window*2 + 1

		xs = np.tile(np.arange(xmin,xmax+1),N)
		ys = np.repeat(np.arange(ymin,ymax+1),N)

		if polarity == 1:
			events = self.events_pos[ys,xs].reshape(-1)
		else:
			events = self.events_neg[ys,xs].reshape(-1)

		xs = np.repeat(xs, self.N_buffer)
		ys = np.repeat(ys, self.N_buffer)

		e_idx = events>0

		xs = xs[e_idx]
		ys = ys[e_idx]
		events = events[e_idx]


		return (xs,ys,events)