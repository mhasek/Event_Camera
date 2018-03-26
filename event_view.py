import sys
import os
import numpy as np
import cv2
from utils import *
from flow_estimation import *
import matplotlib.pyplot as plt

fname = sys.argv[1]

def main(fname):
	events = event_stream(fname)
	image = np.zeros((events.nr,events.nc,3))

	N_buffer = 5
	s_window = 10
	e_window = (s_window*2 + 1)**2  * 0.1
	N_events_sum = 0

	events_buffer = event_image(nr = events.nr, nc = events.nc , pixel_buffer = N_buffer)

	cnt = 0;
	while True:
		(x,y,polarity,time) = events.get_event()

		not_in_corner = (y - s_window) >= 0 and (y + s_window) < events.nr \
		 and (x - s_window) >= 0 and (x + s_window) < events.nc


		if not_in_corner:
			(x_stmp,y_stmp,t_stmp) = events_buffer.extract_stmp_window(x,y,polarity,\
				time,s_window)

		N_events = len(x_stmp)

		N_events_sum += len(x_stmp)

		if N_events > e_window:
			vx,vy = estimate_flow(x,y,time,x_stmp,y_stmp,t_stmp,polarity)
			events_buffer.insert_flow(x, y, vx, vy, polarity)
			print vx,vy


		events_buffer.insert_event(x, y, polarity, time)

		cnt += 1
		
		if cnt == 1000:
			# print N_events_sum/cnt,time
			events_buffer.reset_buffer(time, t_expire = 0.03)
			events_buffer.update_image()
			cv2.imshow('events',events_buffer.event_im)

			plt.figure(1)
			plt.quiver(events_buffer.vx,events_buffer.vy)
			plt.draw()

			cv2.waitKey(1)
			cnt = 0
			N_events_sum = 0


if __name__ == "__main__":
	main(fname)

