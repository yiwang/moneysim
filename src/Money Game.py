from time import localtime, strftime
import sys
import random
import numpy as np
import matplotlib.pyplot as plt
import pylab

# note.txt records bank failure info etc.
sys.stdout = open('note.txt','w')
print '# note file', strftime("%a, %d %b %Y %H:%M:%S +0000", localtime())

Nb=5 # number of banks
Nc=5 # number of comsumers

#===============================================================================
# Initial value of concerned variables, for Chart Later
#===============================================================================

Fed_R = [0]# total money from bank reserves
#M=[550.]
M=[]
B=[100.]
#rr=[0.1]
#cr=0.1

rr= []

#give cr and rr a random init
cr = random.uniform(0.1,0.2)
rr_init = random.uniform(0.1,0.2)
rr.append(rr_init)
M_init = (cr+1) * B[0] /(cr+rr[0])

M.append(M_init)

#get D which is Total_B_C + R
D_init = M[0]/(cr+1)

Total_Consumer_C_init = M[0]-D_init



#===============================================================================
# Consumer init
#===============================================================================
Consumer_D = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
Consumer_L = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
#Consumer_C = [10,10,10,10,10]
Consumer_C =[0,0,0,0,0]

for i in range(Nc):
    Consumer_C[i] = Total_Consumer_C_init / 5

GDP = 0.05

Fed_L =[0,0,0,0,0]

# Bank init
#===============================================================================
#Bank_C = [100,100,100,100,100]
Bank_C = [0,0,0,0,0]
for i in range(Nb):
    Bank_C[i]= D_init / 5

Bank_L = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
Bank_R = np.zeros((Nb,1))
for i in range(Nb):
    Bank_R[i] = Bank_C[i]*rr[0]
    Bank_C[i] = Bank_C[i] - Bank_R[i]
    
Fed_R[0] = sum(Bank_R)

# Number of simulation cycles
Ntime = 100 
for step in range(Ntime):
    for j in range(int(5*np.random.rand())):
        #===============================================================================
        # Consumer & Bank # Nc
        #===============================================================================
        for i in range(Nc):
            deposit_state = random.randrange(0,2)
            loan_state = random.randrange(0,2)
            if (Consumer_C[i]>0) and (deposit_state == 1):
                Consumer_D[i][i] =  0.5 * Consumer_C[i]
                Consumer_C[i] = Consumer_C[i] - Consumer_D[i][i]
            if (Consumer_C[i]>0) and (loan_state == 1):
                # if change 0.25 to 0.5, some banks maybe fail
                #0.25 no fail condition
                Consumer_L[i][i] =  0.5 * Bank_C[i]
                Consumer_C[i] = Consumer_C[i] + Consumer_L[i][i]
    #        print step,i,str(Consumer_C[i]),str(Consumer_L[i][i]),str(Consumer_D[i][i]),'BEFORE'
    #        if Consumer_C[i]<0:
    #            pass
    #            print step,i,str(Consumer_C[i]),str(Consumer_L[i][i]),str(Consumer_D[i][i])
            
        #===============================================================================
        # Bank & Bank
        # b loan from b+1
        #===============================================================================
        for b in range(Nb):
            bank_loan_state = random.randrange(0,2)
            if (b != 4) and (Bank_C[b+1]>0) and (bank_loan_state == 1):
                Bank_L[b][b+1] = 0.1 * Bank_C[b+1]
    #            print step,b,'bank loan',Bank_L[b][b+1]
            elif(Bank_C[0]>0) and (bank_loan_state == 1) and (b == 4):
                Bank_L[4][0] = 0.1 * Bank_C[0]
            
        #    if (b==0) and (Bank_C[1]>0) and (bank_loan_state == 1):
        #        Bank_L[0][1] = 0.1 * Bank_C[1] + Bank_L[0][1]
        
        #===============================================================================
        # Bank_C update
        #===============================================================================
        for b in range(Nb):
            if(b==0):
                Bank_C[0] = Bank_C[0] + Bank_L[0][1]+ Consumer_D[0][0] - Consumer_L[0][0]-Bank_L[4][0]
            elif(b==4):
                Bank_C[4] = Bank_C[4] + Bank_L[4][0]+ Consumer_D[4][4] - Consumer_L[4][4]-Bank_L[3][4]
            else :
                Bank_C[b] = Bank_C[b] + Bank_L[b][b+1]+ Consumer_D[b][b] - Consumer_L[b][b]-Bank_L[b-1][b]
                
            
    #===============================================================================
    # Fed loan to Bank
    #===============================================================================
    # calculate Fed_L to Bank
    # if Bank_C<20; Fed loan 10 to Bank
    
    for b in range(Nb):
        if(0 < Bank_C[b]<=20):
            Fed_L[b]=Fed_L[b]+10
            Bank_C[b] = Bank_C[b]+ 10
        # fail condition: if Bank_C<0 or Bank_C < Consumer_D + Bank_Loan (from other bank)
        if (Bank_C[b]<0) or (b!=4 and Bank_C[b]<Consumer_D[b][b]+Bank_L[b][b+1]):
        # In part B and C, we can judge whether Bank_C[b] is failed or not every 10 times   
            """ bank failure """
            print step,'\tBank',b,'fail',round(Bank_C[b],2),
            # Fed bail out bank            
            Bank_C[b] = Bank_C[b]+ 30
            Fed_L[b] = Fed_L[b]+ 30
            print '\tbail out', round(Bank_C[b],2)
        if Bank_C[4]<0 or (Bank_C[4]<Consumer_D[4][4]+Bank_L[4][0]):
            print step,'\tBank',4,'fail',round(Bank_C[4],2),
            # Fed bail out bank            
            Bank_C[4] = Bank_C[4]+ 30
            Fed_L[4] = Fed_L[4]+ 30
            print '\tbail out', round(Bank_C[4],2)
            
        
    #===============================================================================
    # find new M B
    #===============================================================================
    Total_Bank_Currency = sum(Bank_C)
    Total_Consumer_Currency = sum(Consumer_C)
#    sum all banks reserves
    Fed_R.append(sum(Bank_R))
    # M= Total_Consumer_C + Total_Bank_C + Fed_R
    M.append(Total_Bank_Currency + Total_Consumer_Currency+Fed_R[-1])
    B.append(Total_Consumer_Currency+Fed_R[-1])
    #===============================================================================
    # Fed adjust rr based on new M/B
    #===============================================================================
    
# var step is old step
    if M[step]/B[step]< M[-1]/B[-1]:
        #everytime increase will between 0 and i_max
        i_max=(1-rr[step])/5
        increase = random.uniform(0,i_max)
        rr.append(rr[step]+increase)
    elif M[step]/B[step] > M[-1]/B[-1]:
        #everytime decrease will between 0 and c
        d_min=rr[step]/5
        decrease = random.uniform(0,d_min)
        rr.append(rr[step]-decrease)
        
    else:
        rr.append(rr[step])
     #   rr[-1] = rr[step]
    
    #===============================================================================
    # Feb regulate banks through reserve
    # change Bank_R
    #===============================================================================
    for b in range(Nb):
#        brr = Bank_R[b]/(Bank_R[b]+Bank_C[b])
        tempR = rr[step+1]*(Bank_R[b]+Bank_C[b])
        Bank_C[b] = Bank_C[b] + Bank_R[b] - tempR
        Bank_R[b] = tempR
        
#end of one cycle        
        

# MB = M/B
MB = [x/y for x,y in zip(M, B)]

#===============================================================================
# Output table to file out.txt
#===============================================================================
sys.stdout = open('out.txt','w')
WIDTH = 14

# Header
print 'step'.ljust(4),\
'M'.rjust(WIDTH),\
'B'.rjust(WIDTH),\
'Fed_R'.rjust(WIDTH),\
'M/B'.rjust(WIDTH),\
'rr'.rjust(WIDTH)

for i in range(Ntime):
    print str(i+1).ljust(4),\
    str(round(M[i],2)).rjust(WIDTH),\
    str(round(B[i],2)).rjust(WIDTH),\
    str(round(Fed_R[i],2)).rjust(WIDTH),\
    str(round(MB[i],2)).rjust(WIDTH),\
    (str(round(rr[i]*100,2))+'%').rjust(WIDTH)

#===============================================================================
# Chart
#===============================================================================

fig = plt.figure()
ax = fig.add_subplot(3,1,1)
ax.plot(M, 'r-',B,'b-',Fed_R,'g-')
ax.legend(('M', 'B', 'Fed_R'), shadow = True,loc='upper right')


ax = fig.add_subplot(3,1,2)
ax.plot(MB, '-')
ax.legend(('v=M/B',), shadow = True,loc='upper right')

ax = fig.add_subplot(3,1,3)
ax.plot(rr, '-')
ax.legend((r'rr',), shadow = True,loc='upper right')

plt.show();

