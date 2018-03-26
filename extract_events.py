import rosbag
import sys
import os
import pickle
import pdb
import rospy

fname = sys.argv[1]

def extract_data(fname=fname):
	bag = rosbag.Bag(fname)

	t0 = bag.get_start_time()
	t0_secs = int(round(t0,0))
	t0_nsecs = int(round(t0 - t0_secs,9)*1e9)

	right = open(fname[0:-4] + '_right.txt','w')
	left = open(fname[0:-4] + '_left.txt','w')

	flag = 0
	for topic,msg,t in bag.read_messages(topics = ['/davis/left/events']):
		if flag == 0:
			nr = msg.height
			nc = msg.width
			t0 = round
			left.write('format: x (col), y (row), polarity, time (s ns), t0 '\
				+ str(t0_secs) + ' ' + str(t0_nsecs) \
				+' nrs: ' + str(nr) + ' ncs: ' + str(nc) + '\n')

		flag =1
		for event in msg.events:
			event_txt = str(event.x) + ' '
			event_txt += str(event.y) + ' '
			event_txt += str(int(event.polarity)) + ' '
			event_txt += str(event.ts.secs) + ' '
			event_txt += str(event.ts.nsecs) + '\n'
			left.write(event_txt)

			print event_txt

	left.close()

	flag = 0
	for topic,msg,t in bag.read_messages(topics = ['/davis/right/events']):
		if flag == 0:
			nr = msg.height
			nc = msg.width
			right.write('format: x (col), y (row), polarity, time (s ns), t0 '\
				+ str(t0_secs) + ' ' + str(t0_nsecs) \
				+' nrs: ' + str(nr) + ' ncs: ' + str(nc) + '\n')

		flag =1
		for event in msg.events:
			event_txt = str(event.x) + ' '
			event_txt += str(event.y) + ' '
			event_txt += str(int(event.polarity)) + ' '
			event_txt += str(event.ts.secs) + ' '
			event_txt += str(event.ts.nsecs) + '\n'
			right.write(event_txt)

			print event_txt

	right.close()


if __name__ == "__main__":
	extract_data(fname)

