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
	
	norm_factor = np.max(np.abs(xyt),axis=1) + np.finfo(float).eps

	xyt_norm = xyt/np.tile(norm_factor,(len(rel_x),1)).T
	xyt_norm[2,:]*=1e3


	# if np.isnan(xyt_norm).sum() >= 1 or np.isinf(xyt_norm).sum() >= 1:
	# 	pdb.set_trace()

	W = np.matmul(xyt_norm, xyt_norm.T)

	eig,vecs = np.linalg.eig(W)

	flag = 1
	# rat = 10
	# if eig[1]/eig[2] < rat or eig[1]/eig[2] > 1/rat:
	# 	flag = 1

	vec = vecs[:,np.argmax(eig)]*norm_factor

	# print vec, round(eig[0], 2),round(eig[1], 2) ,round(eig[2], 2), flag

	vx = vec[0]*1e3/vec[2]
	vy = vec[1]*1e3/vec[2]


	# if polarity == 1:
	# 	vx = -vx
	# 	vy = -vy

	
	return vx,vy,flag