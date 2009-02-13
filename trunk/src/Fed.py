#! C:\Python25\python.exe
# -*- coding: utf-8 -*-

import random


#---------------------------------------------------------------------#
#------------------------------Function-------------------------------#
#---------------------------------------------------------------------#
def Fed_M(B,rr,cr):
    M=round(((cr+1)/(cr+rr)*B),2)
    return M

#def Fed_C()

def Get_Consumer_Deposit(cr,c,i):
    deposit_state = random.randrange(0,2)
    get_deposit_state = random.randrange(0,2)
    print "%s %s" %(deposit_state,get_deposit_state) 
    #con_deposit=[]
    d=([0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0])
  #  if(j>0):
    #    d = Get_Consumer_Deposit(cr,c,
    #while(i<5):
    if (deposit_state == 1) and (c>0):
        k=random.randrange(0,5)
        print "%s" %(k)
        d[i][k]=round(random.uniform(0,c),2)
  #  if(con_deposit[i]>0 and get_deposit_state ==1) or (c<0):
  #      d[i]=[0,0,0,0,0]
    return d
        
#def Get_Consumer_Currency(cr,c):
   # l=Get_Consumer_Loan
   # d=Get_Consumer_Deposit
    #c = c + l - d 
    

#---------------------------------------------------------------------#
#------------------------------parameter------------------------------#
#---------------------------------------------------------------------#

B=100
rr=0.2
cr=0.2

M=round(((cr+1)/(cr+rr)*B),2)
C=round( (M*cr)/(1+cr),2)
print "%s" %(C)
c=0.1 * C
i=0

#---------------------------------------------------------------------#
#-------------------------------Test----------------------------------#
#---------------------------------------------------------------------#

print "The M is %s" % (Fed_M(B,rr,cr))
print "%s" %(c)

d= Get_Consumer_Deposit(cr,c,i)
for results in d:
    print results
