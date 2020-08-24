"""
This code computes an error estimate for the average of a 
correlated dataset using block averaging

See "Computer Simulation of Liquids" by Allen & Tildesley 
(2nd ed., Oxford University Press, 2017, p. 282-283)

author: Rasmus Kronberg
email: rasmus.kronberg@aalto.fi

"""

import numpy as np
from scipy.optimize import curve_fit
import warnings

class Blocked:
	def __init__(self, data, bmin):

		self.df = data

		# Mean and variance of full timeseries
		self.run_ave = np.mean(data)
		self.run_var = np.var(data, ddof=1)
	
		# Length of timeseries and a list of all block sizes
		self.ntot = len(data)
		self.sizes = range(1, int(len(data)/bmin))

	# Block average
	def run(self):

		# Initialize blocked variances
		self.vars = np.empty(len(self.sizes))

		for i, size in enumerate(self.sizes):
			progress = 100*i/len(self.sizes)
			print('Processing blocks %.1f %%' % progress, end='\r')

			# Truncate data appropriately from the beginning
			mod = self.ntot%size
			tmp = self.df[mod:]

			# Reshape so that each row corresponds a block
			nblocks = int(self.ntot/size)
			tmp = tmp.reshape((nblocks, size))

			# Average blocks
			block_aves = np.mean(tmp, axis=1)

			# Compute variance of block averages
			self.vars[i] = np.var(block_aves, ddof=1)

	# Statistical inefficiency
	def error(self):

		self.s = self.sizes*self.vars/self.run_var
		self.fit = lambda x, a, b: a*(1-np.exp(-b*x))

		# Fit asymptotic function to s
		with warnings.catch_warnings():
			warnings.simplefilter('ignore')
			self.popt, self.pcov = curve_fit(self.fit, self.sizes, self.s)
		
		# Statistical inefficiency given by the limit as x -> inf (popt[0])
		self.err = np.sqrt(self.run_var*self.popt[0]/self.ntot)
