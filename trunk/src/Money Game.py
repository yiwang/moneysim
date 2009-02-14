#! C:\Python25\python.exe
# -*- coding: utf-8 -*-

import random

Nb=5
Nc=5

#C=[50]
#===============================================================================
# Consumer init
#===============================================================================
Consumer_C = [10,10,10,10,10]
Consumer_D = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
Consumer_L = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]

Fed_L =[0,0,0,0,0]

# Time Variation 
Fed_R = [0]
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

# simulation time
Ntime = 10    
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
    # find M B
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
    # Fed adjust rr based on M/B
    #===============================================================================
    
    M[-1]/B[-1]
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
        
#===============================================================================
# Final
#===============================================================================

print Fed_R
print B
print M
print rr
#M[1]
while(c<2):
    print "The Money Supply is %0.2f" %(float(M[c]))
    c=c+1
c=0
print "It ends"


