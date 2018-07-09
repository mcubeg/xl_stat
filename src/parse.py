#!/usr/bin/python

import topolink
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import histogram

#
#  Main code
#

plot_dir = "./plots"

#xml_file = sys.argv[1]

#protein_name='SalbIII'
#xml_file = 'salbiii_hitsDetail.dat'
#topolink_log = 'salbiii_topolink.log'
#domain = [2,134]

protein_name='ALB'
xml_file = 'alb_hitsDetail.dat'
topolink_log = 'alb_topolink.log'
domain = [1,201] ; protein_name=protein_name+'-D1'
#domain = [202,390] ; protein_name=protein_name+'-D2' 
#domain = [391,584] ; protein_name=protein_name+'-D3' 

# Number of residues in domain

n = domain[1]-domain[0]

# Read xml file from SIM-XL

nlinks, links = topolink.readxml(xml_file,domain)

# Read topolink input to get the length of the linkers

for link in links :
  link.dmax = topolink.getdmax("linktypes.inp",link)

# Read topolink log file to define link consistency

for link in links :
  link.deuc, link.dtop = topolink.readlog(topolink_log,link)

# Score labels:

label = [ 'Average Score1', 'Average Score2', 'Number of species', \
          'Maximum Score1', 'Maximum Score2', 'Number of scans' ]
nscores = len(label)

#
# Set y array containing sim-xl scores for each link
#

y = [ np.zeros(nlinks) for i in range(0,nscores) ]
ilink=-1
for link in links :
  ilink=ilink+1
  y[0][ilink] = link.avgscore1   #Average of score1
  y[1][ilink] = link.avgscore2   #Average of score2
  y[2][ilink] = link.nspecies    #Number of spectra
  y[3][ilink] = link.maxscore1   #Maximum of score1
  y[4][ilink] = link.maxscore2   #Maximum of score2
  y[5][ilink] = link.nscans      #Number of scans

# Set the range of tols to plot tolerance dependence of correlations

tols = []
tol = -3.
while tol <= 20. :
  tols.append(tol)
  tol = tol + 0.5

# Compute point-biserial correlations as a function of tolerance

x = [ np.zeros(nlinks,dtype=bool) for i in range(0,len(tols)) ]
pbs = [ np.zeros(len(tols)) for i in range(0,nscores) ] 

itol=-1
for tol in tols :
  itol=itol+1
  ilink=-1
  for link in links :
    ilink=ilink+1
    if link.dtop > 0. and link.dtop <= link.dmax + tol :
      link.consistency = True
    else :
      link.consistency = False
    x[itol][ilink] = link.consistency

  for iscore in range(0,nscores) :
    pbs[iscore][itol] = topolink.point_biserial(x[itol],y[iscore])

# plot result

for iscore in range(0,nscores) :
  iplot=iscore+1
  plt.subplot(3,2,iplot)
  plt.plot(tols,pbs[iscore],color='black')
  plt.title(label[iscore],size=12)
  plt.xlabel('L_{max} deviation',size=12)
  plt.ylabel('correlation',size=12)

plt.subplots_adjust(left=0.14, 
                    bottom=0.10, 
                    right=0.95, 
                    top=0.90, 
                    wspace=0.4, 
                    hspace=0.6)
plt.gcf().set_size_inches(6,8)
plt.savefig(plot_dir+'/'+protein_name+'_pbs_correlations.pdf')
plt.close()

#
# Plot the actual data from which the PBS correlations are computed
#

tol = 5.
ilink=-1
x = np.zeros(nlinks,dtype=bool) 
pbs = np.zeros(nscores,dtype=float)
for link in links :
  ilink=ilink+1
  if link.dtop > 0. and link.dtop <= link.dmax + tol :
    link.consistency = True
  else : 
    link.consistency = False
  x[ilink] = link.consistency

ncons = len(x[x])

do_histogram = False
if do_histogram :
  iscore=5
  hx, hy = histogram.histogram(y[iscore][x],step=0.5,int=1)
  plt.plot(hx,hy)
  
  notx = np.ones(nlinks,dtype=bool)
  i=-1
  for val in x :
    i=i+1
    if val : notx[i] = False  
  
  hx, hy = histogram.histogram(y[iscore][notx],step=0.5,int=1)
  plt.plot(hx,hy,color='red')                         
  
  plt.show()
  plt.close()
  sys.exit()

# Final plots

for iscore in range(0,nscores) :
  pbs[iscore] = topolink.point_biserial(x,y[iscore])

for iscore in range(0,nscores) :
  iplot=iscore+1
  plt.subplot(3,2,iplot)
  plt.plot(x,y[iscore],'o',alpha=0.3,color='black')
  plt.xlabel('Consistency',size=12)
  plt.ylabel(label[iscore],size=12)
  plt.xlim(-0.5,1.5)

plt.subplots_adjust(left=0.14, 
                    bottom=0.10, 
                    right=0.95, 
                    top=0.90, 
                    wspace=0.4, 
                    hspace=0.6)
plt.gcf().set_size_inches(6,8)
plt.savefig(plot_dir+'/'+protein_name+'_scores_consistency.pdf')
plt.close()


iplot=0
for iscore in range(0,nscores-1) :
  for jscore in range(iscore+1,nscores) :
    iplot=iplot+1
    plt.subplot(5,3,iplot)
    plt.xticks(size=8)
    plt.yticks(size=8)
    plt.xlabel(label[iscore],size=8)
    plt.ylabel(label[jscore],size=8)
    plt.plot(y[iscore],y[jscore],'o',color='black',alpha=0.5)

plt.subplots_adjust(left=0.14, 
                    bottom=0.10, 
                    right=0.95, 
                    top=0.90, 
                    wspace=0.4, 
                    hspace=0.6)
plt.gcf().set_size_inches(6,8)
plt.savefig(plot_dir+'/'+protein_name+'_scores.pdf')
plt.close()

#
# Testing 22   17 2.75 1.47 1.90 0.77
#2.25 0.09 1.80
#
#2.02 0.14 1.00 13.2

#voltar
test = True
if test :
  score = [ 4.40, 2.53, 9.10, 13.2 ]
  score = [ 3.01, 2.53, 2, 24 ]
  score = [ 3.7, 2.53, 4, 33 ]
              
  nget = 0
  nc = 0
  for link in links :
    #if link.avgscore1 >= score[0] or \
    #   link.avgscore2 >= score[1] or \
    #   link.nspecies >= score[2] or \
    #   link.nscans >= score[3] :
    if link.maxscore1 >= score[0] or \
       link.nspecies >= score[2] or \
       link.nscans >= score[3] :
      nget = nget + 1
      topolink.write(link)
      if link.consistency : nc = nc + 1
  print xml_file, domain
  print '{:4} {:4} {:3.2f} {:3.2f} {:3.2f} {:3} {:3}'.format(nget, nc, score[0], score[1], score[2], score[3], float(nc)/nget)

  sys.exit()

#
# Search best set of scores
#

else :
   
  # We want a set of about 2N/10 constraints, where N is the number of
  # residues of the protein
  
  n_min = int((n-0.05*n)*(2./10.))
  n_max = int((n+0.05*n)*(2./10.))
  print n_min, n_max
  
  # We will search for all possible combinations of three of the scores to
  # get the best set (the one with the greatest number of true positives)
  
  nsteps = 10
  minscores = np.array([ min(y[0]), min(y[1]), min(y[2]), min(y[5]) ])
  maxscores = np.array([ max(y[0]), max(y[1]), max(y[2]), max(y[5]) ])
  step = (maxscores - minscores)/nsteps
  
  print 'Nget  Nc  avsc1   avsc2  nspec  nscans nc/nget  totnc'
  ncmax = 0
  for i in range(0,nsteps) :
    #for j in range(0,nsteps) :
       for k in range(0,nsteps) :
         for l in range(0,nsteps) : 
  
           score0 = minscores[0] + i*step[0]
           #score1 = minscores[1] + j*step[1]
           score2 = minscores[2] + k*step[2]
           score3 = minscores[3] + l*step[3]
  
           nget = 0
           nc = 0
           for link in links : 
              #if link.avgscore1 >= score0 or \
              #   link.avgscore2 >= score1 or \
              #   link.nspecies >= score2 or \
              #   link.nscans >= score3 :
              if link.maxscore1 >= score0 or \
                 link.nspecies >= score2 or \
                 link.nscans >= score3 :
                nget = nget + 1
                if link.consistency : nc = nc + 1
           if nget >= n_min and nget <= n_max : 
             #print '{:4} {:3} {:4.2f} {:3.2f} {:3.2f} {:3} {:3.2f} {:3}'.format(nget, nc, score0, score1, score2, score3, float(nc)/nget, ncons)
             print '{:4} {:3} {:4.2f} {:3.2f} {:3} {:3.2f} {:3}'.format(nget, nc, score0, score2, score3, float(nc)/nget, ncons)


sys.exit()
