import sys
import os
import numpy as np
import cv2
from utils import *

fname = sys.argv[1]

def main(fname):
	events = event_stream(fname)
	image = np.zeros((events.nr,events.nc,3))

	events_buffer = event_image(nr = events.nr, nc = events.nc , pixel_buffer = 5)

	cnt = 0;
	while True:
		(x,y,polarity,time) = events.get_event()

		not_in_corner = (y - s_window) >= 0 && (y + s_window) < event.nr \
		 && (x - s_window) >= 0 && (x + s_window) < event.nc


		if not_in_corner:
			(curr_x,curr_y,curr_t) = events_buffer.extract_stmp_window(x,y,polarity,\
				time,s_window,e_window)



		events_buffer.insert_event(x, y, polarity, time)

		print (x,y,polarity,time)
		


		if polarity == 1:
			image[y][x][0] = 1
		else:
			image[y][x][2] = 1
		
		cnt += 1
		
		if cnt == 1000:
			cv2.imshow('events',image)
			cv2.waitKey(1)
			image = np.zeros((events.nr,events.nc,3))
			cnt = 0
			pdb.set_trace()


if __name__ == "__main__":
	main(fname)

