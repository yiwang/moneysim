Consumer

fffff

ff

Yi change

consumer state:

con_d[cid] += d_c2b[cid][:]

con_l[cid] += l_b2c[:][cid]

con_c[cid] += l_b2c[:][cid] - d_c2b[cid][:]

con_credit[cid] = (con_c[cid] + con_d[cid] - con_l[cid])

con_fail[cid] = con_credit[cid] < 0

Fed

fed_r =



Bank

bank_r[bid] += b2f[bid] # b2f + or - , when rr change

# consumer related
bank_d[bid] += d_c2b[:][bid] - w_b2c[bid][:]

# loan comsumer + banks
bank_l[bid] += l_b2c[bid][:] + l_b2b[bid][:]



bank_c[bid] = bank_d[bid] - bank_l[bid]

bank_c[bid] += fed_l[bid] + l_b2b[:][bid]  ?


# consumer
 


action:

# deposit at certain step
d_c2b[cid][bid]

# bank to consumer
l_b2c[][]

# withdraw from bank to consumer
w_b2c[bid][cid]

w_b2b[bid][bid]

# loan from bank 1 to bank 2
l_b2b[b1][b2]

