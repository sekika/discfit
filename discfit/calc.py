import math
import scipy, numpy, warnings
from scipy import stats

# Determine steady state
# Input variables:
#   t (list)): time (sec)
#   le (list): water level (cm)
#   h: suction head (cm)
# Return values:
#   h (cm), Rate of water level going down (cm/s)

def steadystate(t, le, h):
    warnings.filterwarnings('error')

    # Identify period of constant head
    n=len(t); flag=False; p = []
    for i in range(5,n):
        if abs((h[i-5]+h[i-4]+h[i-3]-h[i-2]-h[i-1]-h[i])/3) > 2: # Changing head
            if flag and i > k+8: # More than 10 points
                if numpy.std(h[k:i]) < 1.5: # Standard deviation of head < 1.5
                    p.append([k,i-3])
            flag=False
        else:
        	if flag==False:
        	    k=i
        	flag=True
    if flag and n > k+8: # More than 10 points
        if numpy.std(h[k:n]) < 1.5:
            p.append([k,n-1])
    
    # Determine steady state infiltration rate in each period
    t1=[]; t2=[]; x=[]; y=[]; r2=[]
    for pe in p:
        flag=False; bestr=0
        for i in reversed(range(pe[0]+12,pe[1]+1)):
            try:
                pr=stats.pearsonr(t[i-6:i+1], le[i-6:i+1])[0]
            except:
                pr=0
            if pr < -0.92 and numpy.std(h[i-6:i+1]) < 0.8:
                flag=True
                if pr < bestr:
                    besti=i; bestr=pr
                    if pr < -0.985:
                        break
        if flag:
            i=besti
            j=int((pe[0]+i)/2); bestr=0
            if j > i-5:
                j = i-5
            for k in reversed(range(j,i-4)):
                slope, intercept, r_value, p_value, std_err = stats.linregress(t[k:i+1], le[k:i+1])
                if r_value < bestr:
                    bestr=r_value
                    left = k
            slope, intercept, r_value, p_value, std_err = stats.linregress(t[left:i+1], le[left:i+1])
            head = numpy.mean(h[left:i+1])
            t1.append(int(t[left]))
            t2.append(int(t[i]))
            x.append(head)
            y.append(-slope)
            r2.append(r_value**2)
    return t1, t2, x, y, r2

# Estimate Ks based on Wooding (1968) http://dx.doi.org/10.1029/WR004i006p01259
# No error handling
# Input variables:
#   h (list): suction head (cm)
#   q (list): infiltration rate (cm/s)
#   d: diameter of disk (cm)
# Return values:
#   Ks (cm/s), Gardner's alpha (/cm), R^2

def wooding(h, q, d):
    lny=[]
    for y in q:
         lny.append(math.log(y))
    slope, intercept, r_value, p_value, std_err = stats.linregress(h, lny)
    alpha = -slope
    ks = math.exp(intercept) / (1 + 4 / math.pi / alpha / (d/2))
    pre = int(-math.log10(ks))+3 # Precision of Ks
    ks = int(ks*10**pre+0.5)*1.0/10**pre
    return ks, alpha, r_value**2
