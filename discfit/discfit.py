import sys, math, scipy, numpy, warnings
from scipy import stats

def main(argv=sys.argv[1:]):    
    warnings.filterwarnings('error')
    
    if len(sys.argv) < 4:
        print ('Usage:',sys.argv[0],'Filename dd dp')
        sys.exit()
    csvfile = sys.argv[1] # Filename of csv file
    dd = float(sys.argv[2]) # diameter of the disc
    dp = float(sys.argv[3]) # diameter of the pipe
    
    # Read data file
    data = open(csvfile, 'r') # open csv file
    t = []; le = []; h = []
    for line in data:
        s=line.strip().split(',')[0:3]
        if s[0].find('#') == -1:
            t.append(float(s[0])); le.append(float(s[1])); h.append(float(s[2]))
    data.close()
    
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
    x=[]; y=[]
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
            print ('{0:d} - {1:d} s: {2:.1f} cm, R2 = {3:.3f}'.format(int(t[left]), int(t[i]), -head, r_value**2))
            q = -slope * dp * dp / dd / dd
            x.append(head)
            y.append(math.log(q))
    
    # Estimate Ks by Wooding equation
    if len(x) == 0:
        print ("No period of steady infiltration.")
    elif len(x) == 1:
        print ('Only one period of constant head ({0:.1f} cm) and steady infiltration.'.format(-x[0]))
    elif max(x)-min(x) < 5:
        print ('Too narrow range of constant head: {0:.1f} to {1:.1f} cm).'.format(-min(x),-max(x)))
    else:
        if len(x) == 2:
            print ('Warning: only 2 period of steady state.')
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        alpha = -slope
        # Equation based on Wooding (1968) http://dx.doi.org/10.1029/WR004i006p01259
        ks = math.exp(intercept) / (1 + 4 / math.pi / alpha / (dd / 2))
        pre = int(-math.log10(ks))+3 # Precision of Ks
        ks = int(ks*10**pre+0.5)*1.0/10**pre
        print ('Ks = {0} cm'.format(ks))
        print ('Alpha = {0:.4f} /cm'.format(alpha))
        print ('R2 = {0:.3f}'.format(r_value**2))
