# this is the most stupid way to re-implement the functionality of an example of dpdak:
# gisaxsP03 dpdak

# three parts in total:
# 1. image reading
# 2. yoneda slicing
# 3. fitting

####################################
####################################
### 1 read an image
####################################
####################################

import fabio


filename = "/home/rosem/workspace/dpdak_example_gisaxsP03/measurements_gisaxsP03/saxs/10010801_raw/ms_ps_4k_1/haspp03pilatus/ms_ps_4k_1_sputter_1000s_01102.cbf"
f = fabio.open(filename)
image_array = f.data


# now there is a numpy array keeping the image


####################################
####################################
### 2 proceed with slicing : "line cut"
####################################
####################################

import numpy
from numpy import sin, cos, arctan, degrees, radians, pi, ceil, floor

# pp: pixel position
# db: direct beam position [pixel]
# ps: pixel size [mm]
# ssd: sample detector distance [mm]
# a_i: incident angle [deg]

def alpha_f(pp_y, db_y, ps_y, sdd, a_i):
    return degrees(arctan((pp_y - db_y) * ps_y / sdd)) - a_i

def ttheta_f(pp_x, db_x, ps_x, sdd):
    return degrees(arctan((pp_x - db_x) * ps_x / sdd))

# wl: wave length [nm]
def q_z(wl, a_f, a_i):
    return (2 * pi / wl) * (sin(radians(a_f)) + sin(radians(a_i)))

def q_y(wl, tt_f, a_f):
    return (2 * pi / wl) * sin(radians(tt_f)) * cos(radians(a_f))

cut_dir = 'Horizontal'
width, height = 487, 3    # values in "pixel"
wl = 0.9445 * 0.1         # wavelength in ??? -- that's neither this nor that
sdd = 1836.2              # sample to detector distance in mm
ps_x = 172. * 0.001       # pixel size in x in nm
ps_y = 172. * 0.001       # pixel size in x in nm
a_i = 0.502               # alpha angle (what's this?)
axis = 0                  # if cut_dir == 'Horizontal' else 1

### this is more than strange -- what does this have to do with display?
x, y = 0, 234         ## pixel x/y, input parameter     
db_x, db_y = 28, 124  ## direct beam (???) x/y, input parameter 

cut = image_array[y:y+height,x:x+width].sum(axis=axis)  ## the actual slice command
cut =  cut / float(height)   # renormalize for horizontal cut

pixel = x + numpy.arange(width)
a_f = alpha_f(y + (height / 2.), db_y, ps_y, sdd, a_i)
tt_f = ttheta_f(pixel, db_x, ps_x, sdd)
x_range = q_y(wl, tt_f, a_f)

# the results of the slice:
#print list(x_range)   ## the q_y values
#print list(cut)       ## the intensities


####################################
####################################
### now fit the peak(s)
####################################
####################################


from scipy.odr import Data
from scipy.odr import Model
from scipy.odr import ODR

# basic usage of odr (orthogonal distance regression):
# 1) define function
# 2) define model
# 3) create data instance
# 4) create odr instance
# 5) run the fit

#1     Define the function you want to fit against:
# GA(0*, 10000,0.02) : gaussian with fixed mean at 0.
# LO(0.06*,200,0.02) : lorentz with fixed peak at 0.06
# LO(0.4,120,0.345) : free gaussian, with certain starting values
    
# the fit function
def fcn(p, x):
    # the gaussian part: p[0] is amplitude, 0. is mean, p[1] is FWHM
    # the first lorentzian:  fixed pos = 0.06, p[2] is amp, p[3] is fwhm
    # the second lorentzian: p[4] is pos, p[5] is amp, p[6] is fwhm
    return numpy.abs(p[0]) * numpy.exp(-(numpy.power(x - 0., 2) / ( p[1]*p[1] / 4.0 / numpy.log(2.0)))) + numpy.abs(p[2]) / (1 + numpy.power((x - 0.06) / (p[3] / 2.0), 2)) +  numpy.abs(p[5]) / (1 + numpy.power((x - p[4]) / (p[6] / 2.0), 2))

#def fit(model, guess, data, fix=None, fit_type=0, maxit=50):

#2 Create a Model to fit:
fit_model = Model(fcn)

#3    Create a Data or RealData instance.:
fit_data = Data(x_range, cut)

#4     Instantiate ODR with your data, model and initial parameter estimate.:
odr = ODR(fit_data, fit_model, beta0 = [10000, 0.02, 200, 0.02, 0.4, 120, .0345],maxit=1000)

#5 Run the fit.:
result = odr.run()
# and print results
result.pprint()
