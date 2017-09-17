import sys
from .calc import (steadystate, wooding)

def main(argv=sys.argv[1:]):    
    
    if len(sys.argv) < 4:
        print ('Usage: discfit Filename dd dp')
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

    # Fitting of water level change
    t1, t2, x, y, R2 = steadystate(t, le, h)
    
    if len(x) == 0:
        print ("No period of steady infiltration.")
    elif len(x) == 1:
        print ('Only one period of constant head ({0:.1f} cm) and steady infiltration.'.format(-x[0]))
    elif max(x)-min(x) < 5:
        print ('Too narrow range of constant head: {0:.1f} to {1:.1f} cm).'.format(-min(x),-max(x)))
    else:
        q = []
        for yi in y:
            q.append(yi * dp * dp / dd / dd)
        ks, alpha, r2 = wooding(x, q, dd) # Calculate Ks and alpha
        print ('Ks = {0} cm/s'.format(ks))
        print ('Alpha = {0:.4f} /cm'.format(alpha))
        if len(x) > 2:
            print ('R2 = {0:.3f}'.format(r2))
        for i in range(len(x)):
            print ('{0:d} - {1:d} s: {2:.1f} cm, R2 = {3:.3f}'.format(t1[i], t2[i], -x[i], R2[i]))
