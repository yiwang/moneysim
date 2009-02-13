#! C:\Python25\python.exe
# -*- coding: utf-8 -*-

import random



B=100
rr=[0.1]
N1=5
N2=5
cr=0.1
#C=[50]
Total_C = []
D=[500]
Consumer_C = [10,10,10,10,10]
Consumer_D = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
Consumer_L = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
Bank_C = [100,100,100,100,100]
Bank_L = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
Bank_R = [0,0,0,0,0]
Fed_L =[0,0,0,0,0]
Fed_R = [0]


i=0
c=0
b=0

while (i<5):
    deposit_state = random.randrange(0,2)
    loan_state = random.randrange(0,2)
    if (Consumer_C[i]>0) and (deposit_state == 1):
        Consumer_D[i][i] = Consumer_D[i][i] + 0.5 * Consumer_C[i] 
    if (Consumer_C[i]>0) and (loan_state == 1):
        Consumer_L[i][i] = Consumer_L[i][i] + 0.25 * Consumer_C[i]
    Consumer_C[i] = Consumer_C[i] + Consumer_L[i][i] - Consumer_D[i][i]
    i=i+1
i=0
print "The Consumer's Currency is"
while (c<5):
    print "%0.2f" % (float(Consumer_C[c])),
    c=c+1
c=0
print " "
print "The Consumer's Deposit is"
while (c<5):
    print "%0.2f" % (float(Consumer_D[c][c])),
    c=c+1
c=0
print " "
print "The Consumer's Loan is"
while (c<5):
    print "%0.2f" % (float(Consumer_L[c][c])),
    c=c+1
c=0
while(b<5):
    Bank_C[b]= Bank_C[b] * (1-rr[0])
    Bank_R[b] = Bank_C[b] * rr[0]
    bank_loan_state = random.randrange(0,2)
    if (b!=0) and (b != 4) and (Bank_C[b+1]>0) and (bank_loan_state == 1):
        Bank_L[b][b+1] = 0.1 * Bank_C[b+1] + Bank_L[b][b+1]
    if(Bank_C[0]>0) and (bank_loan_state == 1) and (b == 4):
        Bank_L[4][0] = 0.1 * Bank_C[0] + Bank_L [4][0]
    if (b==0) and (Bank_C[1]>0) and (bank_loan_state == 1):
        Bank_L[0][1] = 0.1 * Bank_C[1] + Bank_L[0][1]
    b=b+1
b=0


while(b<5):
    if(b==0):
        Bank_C[0] = Bank_C[0] + Bank_L[0][1]+ Consumer_D[0][0] - Consumer_L[0][0]-Bank_L[4][0]
    elif(b==4):
        Bank_C[4] = Bank_C[4] + Bank_L[4][0]+ Consumer_D[4][4] - Consumer_L[4][4]-Bank_L[3][4]
    else :
        Bank_C[b] = Bank_C[b] + Bank_L[b][b+1]+ Consumer_D[b][b] - Consumer_L[b][b]-Bank_L[b-1][b]
    b=b+1
b=0
# calculate Fed_L to Bank
# if Bank_C<20; Fed loan 10 to Bank
while(b<5):
    if(0 < Bank_C[b]<=20):
        Fed_L[b]=Fed_L[b]+10
    if(Bank_C[b]<0):
        Fed_L[b]=Fed_L[b]+30
    Bank_C[b] = Bank_C[b]+ Fed_L[b]
    b=b+1
b=0

print ""
print "The Bank's Loan from other bank is "
while(c<5):
    if(c<4):
        print "%0.2f" % (float(Bank_L[c][c+1])),
    if(c==4):
        print "%0.2f" % (float(Bank_L[4][0]))
    c=c+1
c=0
print "The Fed's Loan to the Bank is"
while(c<5):
    print "%0.2f" % (float(Fed_L[c])),
    c=c+1
c=0
print ""
print "The Bank's Currency is "
while(c<5):
    print "%0.2f" % (float(Bank_C[c])),
    c=c+1
c=0
print ""
while(c<5):
    Total_Bank_Currency = 0
    Total_Bank_Currency = Total_Bank_Currency + Bank_C[c]
    c=c+1
c=0
while(c<5):
    Total_Consumer_Currency = 0
    Total_Consumer_Currency = Total_Consumer_Currency + Consumer_C[c]
    c=c+1
c=0
M = Total_Bank_Currency + Total_Consumer_Currency
print "The Money Supply is %0.2f" %(float(M))

