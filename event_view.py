import sys
import os
import numpy as np
import cv2
from utils import *
from flow_estimation import *
import matplotlib.pyplot as plt
import time as get_t

fname = sys.argv[1]

def main(fname):
	events = event_stream(fname)

	N_buffer = 5
	s_window = 10
	e_min = (s_window*2 + 1)
	t_window = 0.005

	N_events_sum = 0

	events_buffer = event_image(nr = events.nr, nc = events.nc , pixel_buffer = N_buffer)
	flow = flow_image(nr = events.nr, nc = events.nc) 
	cv2.namedWindow('events',cv2.WINDOW_NORMAL)
	cv2.resizeWindow('events', 692,520)


	e_cnt = 0
	t_start = 0
	start_t_fps = 0
	ts = 0.03

	# initialize stats
	t_proc = 0
	cnt = 0
	f_cnt = 0

	# plt.ion()
	# ys,xs = np.meshgrid(np.arange(events.nr),np.arange(events.nc))

	while True:

		(x,y,polarity,time) = events.get_event()

		# update temnporal window size
		if e_cnt > events.nr*events.nc*0.03:
			t_window = time - t_start
			# print t_window, e_cnt
			t_start = time
			e_cnt = 0



		# check event is not in corner
		not_in_corner = (y - s_window) >= 0 and (y + s_window) < events.nr \
		 and (x - s_window) >= 0 and (x + s_window) < events.nc
		if not_in_corner:
			(x_stmp,y_stmp,t_stmp) = events_buffer.extract_stmp_window(x,y,polarity,\
				time,s_window,t_window)

		# calculate flow
		N_events = len(x_stmp)

		if N_events > e_min:
			vx,vy = estimate_flow(x,y,time,x_stmp,y_stmp,t_stmp,polarity)
			flow.insert_flow(x, y, vx, vy, polarity)
			f_cnt += 1
			print vx,vy

		e_cnt += 1 #count events that occured

		

		events_buffer.insert_event(x, y, polarity, time)

		# gather stats
		N_events_sum += len(x_stmp)
		cnt += 1



		if (time - start_t_fps) > ts:
			# n_events, ave_stmp_w size,r_events , curr_time,	t_proc	
			print cnt, round(float(N_events_sum)/cnt,3), round(float(f_cnt)/cnt,3)\
			, round(time,3), round((get_t.time() - t_proc),3)

			img = events_buffer.event_im
			img = flow.draw_arrow(img)
			cv2.imshow('events', img)

		# 	# plt.figure(1)
		# 	# plt.quiver(xs,ys,flow.vx.reshape(-1)*1e6,flow.vy.reshape(-1)*1e6)
		# 	# plt.pause(1)
		# 	# plt.draw()

			cv2.waitKey(1)
			events_buffer.reset_image()
			flow.reset_flow()

			# reset fps timer
			start_t_fps = time

			# reset stats
			N_events_sum = 0
			t_proc = get_t.time()
			cnt = 0
			f_cnt = 0


if __name__ == "__main__":
	main(fname)

