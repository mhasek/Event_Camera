import numpy as np
import pdb
import scipy as sp
import matplotlib.pyplot as plt

def estimate_flow(x,y,t,x_stmp,y_stmp,t_stmp,polarity):

	vec = 0

	rel_x = np.float64(np.append(x_stmp,x))
	rel_x -= np.mean(rel_x)

	rel_y = np.float64(np.append(y_stmp,y))
	rel_y -= np.mean(rel_y)

	rel_t = np.float64(np.append(t_stmp,t))
	rel_t -= np.mean(rel_t)


	xyt = np.array((rel_x,rel_y,rel_t))
	norm_factor = np.max(np.abs(xyt),axis=1)

	xyt_norm = xyt/np.tile(norm_factor,(len(rel_x),1)).T
	xyt_norm[2,:]*=1e3

	W = np.matmul(xyt_norm, xyt_norm.T)

	eig,vecs = np.linalg.eig(W)

	vec = vecs[:,np.argmax(eig)]

	vx = 1e4*vec[0]/vec[2]
	vy = 1e4*vec[1]/vec[2]


	# if polarity == 0:
	# 	vx = -vx
	# 	vy = -vy

	
	return vx,vy