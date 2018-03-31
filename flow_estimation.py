import numpy as np
import pdb
import scipy as sp

def estimate_flow(x,y,time,x_stmp,y_stmp,t_stmp,polarity):

	vec = 0

	rel_x = x_stmp - x - np.mean(x_stmp - x) 
	rel_y = y_stmp - y - np.mean(y_stmp - y)
	rel_t = t_stmp - time - np.mean(t_stmp - time )
	rel_t*=1e6

	xyt = np.array((rel_x,rel_y,rel_t))
	W = np.matmul(xyt, xyt.T)

	eig,vecs = np.linalg.eig(W)

	vec = vecs[:,np.argmax(eig)]

	vx = 1e4*vec[0]/vec[2]
	vy = 1e4*vec[1]/vec[2]


	# if polarity == 0:
	# 	vx = -vx
	# 	vy = -vy

	
	return vx,vy