import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
import pdb
import sys
import time

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

	def reset_image(self):
		self.event_im = np.zeros((self.nr,self.nc,3))


	def insert_event(self,x,y,polarity,time):

		if polarity == 1:
			self.events_pos[y][x][1:] = self.events_pos[y][x][0:-1]
			self.events_pos[y][x][0] = time
			self.event_im[y,x,0] = 1
		else:
			self.events_neg[y][x][1:] = self.events_neg[y][x][0:-1]
			self.events_neg[y][x][0] = time
			self.event_im[y,x,2] = 1			



	def extract_stmp_window(self,x,y,polarity,t,s_window,t_window):
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

		e_idx = events > (t - t_window) 

		xs = xs[e_idx]
		ys = ys[e_idx]
		events = events[e_idx]

		return (xs,ys,events)


class flow_image:
	def __init__(self,nr,nc):

		self.nr = nr
		self.nc = nc
		
		# self.vx = np.zeros((nr,nc))
		# self.vy = np.zeros((nr,nc))

		# self.ys,self.xs = np.meshgrid(np.arange(nr),np.arange(nc))
		
		# self.ys = self.ys.reshape(-1)
		# self.xs = self.xs.reshape(-1)

		self.vx = []
		self.vy = []
		self.ys = []
		self.xs = []


	def insert_flow(self,x,y,vx,vy,polarity):

		if ~np.isnan(vx) and ~np.isnan(vy) and ~np.isinf(vx) and ~np.isinf(vy):
			# self.vx[y][x] = vx
			# self.vy[y][x] = vy
			self.vx.append(float(vx))
			self.vy.append(float(vy))
			self.xs.append(x)
			self.ys.append(y)

	def get_angle_im(self):
		image  = np.zeros((self.nr,self.nc))

		image[self.ys][self.xs] = np.arctan2(np.array(self.vy),np.array(self.vx))

		return image

	def reset_flow(self):
		# self.vx = np.zeros((self.nr,self.nc))
		# self.vy = np.zeros((self.nr,self.nc))

		self.vx = []
		self.vy = []
		self.ys = []
		self.xs = []
		
	def draw_arrow(self,img):
		# pts_x = np.round(self.vx.reshape(-1)*1e-2 + self.xs)
		# pts_y = np.round(self.vy.reshape(-1)*1e-2 + self.ys)

		# pts_1 = np.array((self.xs,self.ys)).T.reshape(-1,1,2)
		# pts_2 = np.array((pts_x,pts_y)).T.reshape(-1,1,2)
		N = len(self.xs)
		if N > 0:

			for i in range(N):
				# pts_1 = (int(self.xs[i]),int(self.ys[i]))
				# pts_2 = (int(pts_x[i]),int(pts_y[i]))
				pts_1 = (self.xs[i],self.ys[i])
				pts_2 = (int(self.xs[i]+self.vx[i]),int(self.ys[i]+self.vy[i]))

				cv2.arrowedLine(img, pts_1, pts_2, (255,0,255),1,line_type = 8)
		
		return img