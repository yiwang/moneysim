import sys
import random
import numpy as np
import matplotlib.pyplot as plt

Nb=5 # number of banks
Nc=5 # number of comsumers

#===============================================================================
# Consumer init
#===============================================================================
Consumer_C = [10,10,10,10,10]
Consumer_D = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
Consumer_L = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]

Fed_L =[0,0,0,0,0]

#===============================================================================
# Initial value of concerned variables
#===============================================================================
Fed_R = [0]# total money from bank reserves
M=[550]
B=[100]
rr=[0.1]
cr=0.1
#===============================================================================
# Bank init
#===============================================================================
Bank_C = [100,100,100,100,100]
Bank_L = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
Bank_R = range(Nb)
for i in range(Nb):
    Bank_R[i] = Bank_C[i]*rr[0]
    Bank_C[i] = Bank_C[i] - Bank_R[i]
    Fed_R[0] = Fed_R[0] + Bank_R[i]

# Number of simulation cycles
Ntime = 101  
for step in range(Ntime):
    #===============================================================================
    # Consumer & Bank # Nc
    #===============================================================================
    for i in range(Nc):
        deposit_state = random.randrange(0,2)
        loan_state = random.randrange(0,2)
        if (Consumer_C[i]>0) and (deposit_state == 1):
            Consumer_D[i][i] = Consumer_D[i][i] + 0.5 * Consumer_C[i] 
        if (Consumer_C[i]>0) and (loan_state == 1):
            Consumer_L[i][i] = Consumer_L[i][i] + 0.25 * Bank_C[i]
        Consumer_C[i] = Consumer_C[i] + Consumer_L[i][i] - Consumer_D[i][i]
        
    #===============================================================================
    # Bank & Bank
    # b loan from b+1
    #===============================================================================
    for b in range(Nc):
        bank_loan_state = random.randrange(0,2)
        if (b != 4) and (Bank_C[b+1]>0) and (bank_loan_state == 1):
            Bank_L[b][b+1] = 0.1 * Bank_C[b+1] + Bank_L[b][b+1]
        elif(Bank_C[0]>0) and (bank_loan_state == 1) and (b == 4):
            Bank_L[4][0] = 0.1 * Bank_C[0] + Bank_L [4][0]
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
    Fed_R.append(0)
    for b in range(Nb):
        if(0 < Bank_C[b]<=20):
            Fed_L[b]=Fed_L[b]+10
        if(Bank_C[b]<0):
            """ bank failure """
            Fed_L[b]=Fed_L[b]+30
        Bank_C[b] = Bank_C[b]+ Fed_L[b]
        #    sum of all banks reserves
        Fed_R[-1] = Fed_R[-1] + Bank_R[i]
        
    #===============================================================================
    # find new M B
    #===============================================================================
    Total_Bank_Currency = 0
    for b in range(Nb):
        Total_Bank_Currency = Total_Bank_Currency + Bank_C[b]
    
    Total_Consumer_Currency = 0
    for c in range(Nc):
        Total_Consumer_Currency = Total_Consumer_Currency + Consumer_C[c]

    M.append(Total_Bank_Currency + Total_Consumer_Currency)
    B.append(Total_Consumer_Currency+Fed_R[-1])
    #===============================================================================
    # Fed adjust rr based on new M/B
    #===============================================================================
    
# step is old    
#    if M[step]/B[step]> M[-1]/B[-1]:
        
    rr.append(0)
    rr[-1] = rr[step]
    
    #===============================================================================
    # Feb regulate banks through reserve
    # change Bank_R
    #===============================================================================
    for b in range(Nb):
#        brr = Bank_R[b]/(Bank_R[b]+Bank_C[b])
        tempR = rr[step]*(Bank_R[b]+Bank_C[b])
        Bank_C[b] = Bank_C[b] + Bank_R[b] - tempR
        Bank_R[b] = tempR
        
#end of one cycle        
        

# MB = M/B
MB = [x/y for x,y in zip(M, B)]

#===============================================================================
# Output table
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
    print str(i).ljust(4),\
    str(round(M[i],2)).rjust(WIDTH),\
    str(round(B[i],2)).rjust(WIDTH),\
    str(round(Fed_R[i],2)).rjust(WIDTH),\
    str(round(MB[i],2)).rjust(WIDTH),\
    (str(round(rr[i]*100,2))+'%').rjust(WIDTH)

#===============================================================================
# Chart
#===============================================================================

fig = plt.figure()
ax = fig.add_subplot(231)
ax.plot(M, 'o-')
ax.set_title('M')

ax = fig.add_subplot(232)
ax.plot(B, 'o-')
ax.set_title('B')

ax = fig.add_subplot(233)
ax.plot(Fed_R, 'o-')
ax.set_title('Fed_R')

ax = fig.add_subplot(234)
ax.plot(MB, 'o-')
ax.set_title('M/B')

ax = fig.add_subplot(235)
ax.plot(rr, 'o-')
ax.set_title('rr')

plt.show();



