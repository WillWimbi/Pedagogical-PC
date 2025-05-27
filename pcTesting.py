current_cycle = 0

BIT_SIZE = 32

def tick_clock():
    global current_cycle

    current_cycle += 1

def halfAdder(a, b):
    s = a ^ b
    cout = a & b
    return s, cout
def HA(a,b):
    s = a ^ b
    cout = a & b
    return s, cout
def fullAdder(a, b, c):
    x1 = a ^ b
    s = x1 ^ c
    a1 = a & b
    a2 = c & x1
    cout = a1 | a2
    return s, cout
def FA(a,b,c):
    x1 = a ^ b
    s = x1 ^ c
    a1 = a & b
    a2 = c & x1
    cout = a1 | a2
    return s, cout

def bitAdd32(a, b, c_in):
    s = [False] * BIT_SIZE
    c = [False] * (BIT_SIZE+1)
    c[0] = c_in
    for i in range(BIT_SIZE):
        s[i], c[i + 1] = fullAdder(a[i], b[i], c[i])
    return s, c[BIT_SIZE]



#used for bitMul32
def bitAdd64(a, b, c_in):
    bitSize2 = 2*BIT_SIZE
    s = [False] * bitSize2
    c = [False] * (bitSize2+1)
    c[0] = c_in
    for i in range(bitSize2):
        s[i], c[i + 1] = fullAdder(a[i], b[i], c[i])
    return s, c[bitSize2]

def bitSub32(a, b):
    # Two's complement subtraction: a - b = a + (~b + 1)
    nb = [not b[i] for i in range(BIT_SIZE)]
    s, cout = bitAdd32(a, nb, True)
    return s, cout

def bitMul4(a, b):
    p = [[a[i] & b[j] for j in range(4)] for i in range(4)]
    p00, p01, p02, p03 = p[0]
    p10, p11, p12, p13 = p[1]
    p20, p21, p22, p23 = p[2]
    p30, p31, p32, p33 = p[3]

    s1, c1 = halfAdder(p10, p01)
    s2, c2 = fullAdder(p20, p11, p02)
    s3, c3 = fullAdder(p30, p21, p12)
    s3b, c3b = halfAdder(s3, c1)
    s4, c4 = fullAdder(p31, p22, p13)
    s5, c5 = halfAdder(p32, p23)

    rowA = [p00, s1, s2, s3b, s4, s5]
    rowB = [0, 0, c2, c3, c4, c5]

    out, carry = [], 0
    for a_bit, b_bit in zip(rowA, rowB):
        s, carry = halfAdder(a_bit ^ carry, b_bit)
        out.append(s)
    out.append(carry)
    return out + [0, 0]  # 8-bit product, LSB first



# Example usage:
# Multiply 6 (0110) × 11 (1011)
a = [0,1,1,0]
b = [1,1,0,1] 
print("4bit multiplier:",bitMul4(a, b))  # Should return 66 

#32bit multiplier
def bitMul32(a, b):
    outputArr = [[False,False] for _ in range(32)]
    a=[]
    b=[]
    # No, this does not work as intended.
    # [[]*32 for _ in range(32)] creates a list of 32 empty lists, because [] * 32 is still [].
    # If you want a 32x32 array (list of lists), use:
    partialProducts = [[False for _ in range(32)] for _ in range(32)]
    #simulatable. 32bit in typical partial product style would be 1024 insanity and the HA/FA optimization would be too much
    #could loop over --> 
    counter = 0
    for i in range(32):
        for j in range(32):
            partialProducts[i][j] = a[i] & b[j]  # This evaluates to either True/False (if a[i], b[j] are bools) or 1/0 (if ints)
    #peaks at a15*b0 or a0*b15 --> precisely 32 partial products
    #something like this repeated for multiplication
    for i in range(15):
        if counter == 0:
            outputArr[0][0] = partialProducts[0][0]
        elif counter == 1:
            outputArr[1][0], outputArr[1][1] = partialProducts[1][0], partialProducts[0][1]
        elif counter == 2:
            sum, cout = halfAdder(partialProducts[1][1], partialProducts[0][2]) #can't do this, need to pass cout between columns etc
            outputArr[2][0], outputArr[2][1] = partialProducts[2][0], sum
        elif counter == 3:
            pass
        elif counter == 4:
            pass
        elif counter == 5:
            pass
        elif counter == 6:
            pass
        elif counter == 7:
            pass
        elif counter == 8:
            pass
        elif counter == 9:
            pass
        elif counter == 10:
            pass
        elif counter == 11:
            pass
        elif counter == 12:
            pass
        elif counter == 13:
            pass
        elif counter == 14:
            pass
            
        print("counter:", counter)
        counter+=1

    for f,g in zip(outputArr):
        a.append(f)
        b.append(g)

def bitMul16Unsigned(a,b):
    partialProducts = [[a[i] & b[j] for j in range(16)] for i in range(16)]
    sum2Column = [[False, False] for _ in range(32)]
    
    #column 0 - 1 dot
    sum2Column[0][0] = partialProducts[0][0]
    
    #column 1 - 2 dots
    sum2Column[1][0] = partialProducts[0][1]
    sum2Column[1][1] = partialProducts[1][0]
    
    #column 2 - 3 dots → 2 dots (1 HA)
    sum_2_0, cout_2_0 = HA(partialProducts[0][2], partialProducts[1][1])
    sum2Column[2][0] = sum_2_0
    sum2Column[2][1] = partialProducts[2][0]
    carry_2_0 = cout_2_0
    
    #column 3 - 4 dots + 1 carry = 5 → 2 dots (1 FA, 1 HA)
    sum_3_0, cout_3_0 = HA(partialProducts[0][3], partialProducts[3][0])
    sum_3_1, cout_3_1 = FA(partialProducts[1][2], partialProducts[2][1], carry_2_0)
    sum2Column[3][0] = sum_3_0
    sum2Column[3][1] = sum_3_1
    carry_3_0 = cout_3_0
    carry_3_1 = cout_3_1
    
    #column 4 - 5 dots + 2 carries = 7 → 2 dots (2 FA, 1 HA)
    sum_4_0, cout_4_0 = HA(partialProducts[0][4], partialProducts[4][0])
    sum_4_1, cout_4_1 = FA(partialProducts[1][3], partialProducts[3][1], carry_3_0)
    sum_4_2, cout_4_2 = FA(partialProducts[2][2], sum_4_0, carry_3_1)
    sum2Column[4][0] = sum_4_1
    sum2Column[4][1] = sum_4_2
    carry_4_0 = cout_4_0
    carry_4_1 = cout_4_1
    carry_4_2 = cout_4_2
    
    #column 5 - 6 dots + 3 carries = 9 → 2 dots (3 FA, 1 HA)
    sum_5_0, cout_5_0 = HA(partialProducts[0][5], partialProducts[5][0])
    sum_5_1, cout_5_1 = FA(partialProducts[1][4], partialProducts[4][1], carry_4_0)
    sum_5_2, cout_5_2 = FA(partialProducts[2][3], partialProducts[3][2], carry_4_1)
    sum_5_3, cout_5_3 = FA(sum_5_0, sum_5_1, carry_4_2)
    sum2Column[5][0] = sum_5_2
    sum2Column[5][1] = sum_5_3
    carry_5_0 = cout_5_0
    carry_5_1 = cout_5_1
    carry_5_2 = cout_5_2
    carry_5_3 = cout_5_3
    
    #column 6 - 7 dots + 4 carries = 11 → 2 dots (4 FA, 1 HA)
    sum_6_0, cout_6_0 = HA(partialProducts[0][6], partialProducts[6][0])
    sum_6_1, cout_6_1 = FA(partialProducts[1][5], partialProducts[5][1], carry_5_0)
    sum_6_2, cout_6_2 = FA(partialProducts[2][4], partialProducts[4][2], carry_5_1)
    sum_6_3, cout_6_3 = FA(partialProducts[3][3], sum_6_0, carry_5_2)
    sum_6_4, cout_6_4 = FA(sum_6_1, sum_6_2, carry_5_3)
    sum2Column[6][0] = sum_6_3
    sum2Column[6][1] = sum_6_4
    carry_6_0 = cout_6_0
    carry_6_1 = cout_6_1
    carry_6_2 = cout_6_2
    carry_6_3 = cout_6_3
    carry_6_4 = cout_6_4
    
    #column 7 - 8 dots + 5 carries = 13 → 2 dots (5 FA, 1 HA)
    sum_7_0, cout_7_0 = HA(partialProducts[0][7], partialProducts[7][0])
    sum_7_1, cout_7_1 = FA(partialProducts[1][6], partialProducts[6][1], carry_6_0)
    sum_7_2, cout_7_2 = FA(partialProducts[2][5], partialProducts[5][2], carry_6_1)
    sum_7_3, cout_7_3 = FA(partialProducts[3][4], partialProducts[4][3], carry_6_2)
    sum_7_4, cout_7_4 = FA(sum_7_0, sum_7_1, carry_6_3)
    sum_7_5, cout_7_5 = FA(sum_7_2, sum_7_3, carry_6_4)
    sum2Column[7][0] = sum_7_4
    sum2Column[7][1] = sum_7_5
    carry_7_0 = cout_7_0
    carry_7_1 = cout_7_1
    carry_7_2 = cout_7_2
    carry_7_3 = cout_7_3
    carry_7_4 = cout_7_4
    carry_7_5 = cout_7_5
    
    #column 8 - 9 dots + 6 carries = 15 → 2 dots (6 FA, 1 HA)
    sum_8_0, cout_8_0 = HA(partialProducts[0][8], partialProducts[8][0])
    sum_8_1, cout_8_1 = FA(partialProducts[1][7], partialProducts[7][1], carry_7_0)
    sum_8_2, cout_8_2 = FA(partialProducts[2][6], partialProducts[6][2], carry_7_1)
    sum_8_3, cout_8_3 = FA(partialProducts[3][5], partialProducts[5][3], carry_7_2)
    sum_8_4, cout_8_4 = FA(partialProducts[4][4], sum_8_0, carry_7_3)
    sum_8_5, cout_8_5 = FA(sum_8_1, sum_8_2, carry_7_4)
    sum_8_6, cout_8_6 = FA(sum_8_3, sum_8_4, carry_7_5)
    sum2Column[8][0] = sum_8_5
    sum2Column[8][1] = sum_8_6
    carry_8_0 = cout_8_0
    carry_8_1 = cout_8_1
    carry_8_2 = cout_8_2
    carry_8_3 = cout_8_3
    carry_8_4 = cout_8_4
    carry_8_5 = cout_8_5
    carry_8_6 = cout_8_6
    
    #column 9 - 10 dots + 7 carries = 17 → 2 dots (7 FA, 1 HA)
    sum_9_0, cout_9_0 = HA(partialProducts[0][9], partialProducts[9][0])
    sum_9_1, cout_9_1 = FA(partialProducts[1][8], partialProducts[8][1], carry_8_0)
    sum_9_2, cout_9_2 = FA(partialProducts[2][7], partialProducts[7][2], carry_8_1)
    sum_9_3, cout_9_3 = FA(partialProducts[3][6], partialProducts[6][3], carry_8_2)
    sum_9_4, cout_9_4 = FA(partialProducts[4][5], partialProducts[5][4], carry_8_3)
    sum_9_5, cout_9_5 = FA(sum_9_0, sum_9_1, carry_8_4)
    sum_9_6, cout_9_6 = FA(sum_9_2, sum_9_3, carry_8_5)
    sum_9_7, cout_9_7 = FA(sum_9_4, sum_9_5, carry_8_6)
    sum2Column[9][0] = sum_9_6
    sum2Column[9][1] = sum_9_7
    carry_9_0 = cout_9_0
    carry_9_1 = cout_9_1
    carry_9_2 = cout_9_2
    carry_9_3 = cout_9_3
    carry_9_4 = cout_9_4
    carry_9_5 = cout_9_5
    carry_9_6 = cout_9_6
    carry_9_7 = cout_9_7
    
    #column 10 - 11 dots + 8 carries = 19 → 2 dots (8 FA, 1 HA)
    sum_10_0, cout_10_0 = HA(partialProducts[0][10], partialProducts[10][0])
    sum_10_1, cout_10_1 = FA(partialProducts[1][9], partialProducts[9][1], carry_9_0)
    sum_10_2, cout_10_2 = FA(partialProducts[2][8], partialProducts[8][2], carry_9_1)
    sum_10_3, cout_10_3 = FA(partialProducts[3][7], partialProducts[7][3], carry_9_2)
    sum_10_4, cout_10_4 = FA(partialProducts[4][6], partialProducts[6][4], carry_9_3)
    sum_10_5, cout_10_5 = FA(partialProducts[5][5], sum_10_0, carry_9_4)
    sum_10_6, cout_10_6 = FA(sum_10_1, sum_10_2, carry_9_5)
    sum_10_7, cout_10_7 = FA(sum_10_3, sum_10_4, carry_9_6)
    sum_10_8, cout_10_8 = FA(sum_10_5, sum_10_6, carry_9_7)
    sum2Column[10][0] = sum_10_7
    sum2Column[10][1] = sum_10_8
    carry_10_0 = cout_10_0
    carry_10_1 = cout_10_1
    carry_10_2 = cout_10_2
    carry_10_3 = cout_10_3
    carry_10_4 = cout_10_4
    carry_10_5 = cout_10_5
    carry_10_6 = cout_10_6
    carry_10_7 = cout_10_7
    carry_10_8 = cout_10_8
    
    #column 11 - 12 dots + 9 carries = 21 → 2 dots (9 FA, 1 HA)
    sum_11_0, cout_11_0 = HA(partialProducts[0][11], partialProducts[11][0])
    sum_11_1, cout_11_1 = FA(partialProducts[1][10], partialProducts[10][1], carry_10_0)
    sum_11_2, cout_11_2 = FA(partialProducts[2][9], partialProducts[9][2], carry_10_1)
    sum_11_3, cout_11_3 = FA(partialProducts[3][8], partialProducts[8][3], carry_10_2)
    sum_11_4, cout_11_4 = FA(partialProducts[4][7], partialProducts[7][4], carry_10_3)
    sum_11_5, cout_11_5 = FA(partialProducts[5][6], partialProducts[6][5], carry_10_4)
    sum_11_6, cout_11_6 = FA(sum_11_0, sum_11_1, carry_10_5)
    sum_11_7, cout_11_7 = FA(sum_11_2, sum_11_3, carry_10_6)
    sum_11_8, cout_11_8 = FA(sum_11_4, sum_11_5, carry_10_7)
    sum_11_9, cout_11_9 = FA(sum_11_6, sum_11_7, carry_10_8)
    sum2Column[11][0] = sum_11_8
    sum2Column[11][1] = sum_11_9
    carry_11_0 = cout_11_0
    carry_11_1 = cout_11_1
    carry_11_2 = cout_11_2
    carry_11_3 = cout_11_3
    carry_11_4 = cout_11_4
    carry_11_5 = cout_11_5
    carry_11_6 = cout_11_6
    carry_11_7 = cout_11_7
    carry_11_8 = cout_11_8
    carry_11_9 = cout_11_9
    
    #column 12 - 13 dots + 10 carries = 23 → 2 dots (10 FA, 1 HA)
    sum_12_0, cout_12_0 = HA(partialProducts[0][12], partialProducts[12][0])
    sum_12_1, cout_12_1 = FA(partialProducts[1][11], partialProducts[11][1], carry_11_0)
    sum_12_2, cout_12_2 = FA(partialProducts[2][10], partialProducts[10][2], carry_11_1)
    sum_12_3, cout_12_3 = FA(partialProducts[3][9], partialProducts[9][3], carry_11_2)
    sum_12_4, cout_12_4 = FA(partialProducts[4][8], partialProducts[8][4], carry_11_3)
    sum_12_5, cout_12_5 = FA(partialProducts[5][7], partialProducts[7][5], carry_11_4)
    sum_12_6, cout_12_6 = FA(partialProducts[6][6], sum_12_0, carry_11_5)
    sum_12_7, cout_12_7 = FA(sum_12_1, sum_12_2, carry_11_6)
    sum_12_8, cout_12_8 = FA(sum_12_3, sum_12_4, carry_11_7)
    sum_12_9, cout_12_9 = FA(sum_12_5, sum_12_6, carry_11_8)
    sum_12_10, cout_12_10 = FA(sum_12_7, sum_12_8, carry_11_9)
    sum2Column[12][0] = sum_12_9
    sum2Column[12][1] = sum_12_10
    carry_12_0 = cout_12_0
    carry_12_1 = cout_12_1
    carry_12_2 = cout_12_2
    carry_12_3 = cout_12_3
    carry_12_4 = cout_12_4
    carry_12_5 = cout_12_5
    carry_12_6 = cout_12_6
    carry_12_7 = cout_12_7
    carry_12_8 = cout_12_8
    carry_12_9 = cout_12_9
    carry_12_10 = cout_12_10
    
    #column 13 - 14 dots + 11 carries = 25 → 2 dots (11 FA, 1 HA)
    sum_13_0, cout_13_0 = HA(partialProducts[0][13], partialProducts[13][0])
    sum_13_1, cout_13_1 = FA(partialProducts[1][12], partialProducts[12][1], carry_12_0)
    sum_13_2, cout_13_2 = FA(partialProducts[2][11], partialProducts[11][2], carry_12_1)
    sum_13_3, cout_13_3 = FA(partialProducts[3][10], partialProducts[10][3], carry_12_2)
    sum_13_4, cout_13_4 = FA(partialProducts[4][9], partialProducts[9][4], carry_12_3)
    sum_13_5, cout_13_5 = FA(partialProducts[5][8], partialProducts[8][5], carry_12_4)
    sum_13_6, cout_13_6 = FA(partialProducts[6][7], partialProducts[7][6], carry_12_5)
    sum_13_7, cout_13_7 = FA(sum_13_0, sum_13_1, carry_12_6)
    sum_13_8, cout_13_8 = FA(sum_13_2, sum_13_3, carry_12_7)
    sum_13_9, cout_13_9 = FA(sum_13_4, sum_13_5, carry_12_8)
    sum_13_10, cout_13_10 = FA(sum_13_6, sum_13_7, carry_12_9)
    sum_13_11, cout_13_11 = FA(sum_13_8, sum_13_9, carry_12_10)
    sum2Column[13][0] = sum_13_10
    sum2Column[13][1] = sum_13_11
    carry_13_0 = cout_13_0
    carry_13_1 = cout_13_1
    carry_13_2 = cout_13_2
    carry_13_3 = cout_13_3
    carry_13_4 = cout_13_4
    carry_13_5 = cout_13_5
    carry_13_6 = cout_13_6
    carry_13_7 = cout_13_7
    carry_13_8 = cout_13_8
    carry_13_9 = cout_13_9
    carry_13_10 = cout_13_10
    carry_13_11 = cout_13_11
    
    #column 14 - 15 dots + 12 carries = 27 → 2 dots (12 FA, 1 HA)
    sum_14_0, cout_14_0 = HA(partialProducts[0][14], partialProducts[14][0])
    sum_14_1, cout_14_1 = FA(partialProducts[1][13], partialProducts[13][1], carry_13_0)
    sum_14_2, cout_14_2 = FA(partialProducts[2][12], partialProducts[12][2], carry_13_1)
    sum_14_3, cout_14_3 = FA(partialProducts[3][11], partialProducts[11][3], carry_13_2)
    sum_14_4, cout_14_4 = FA(partialProducts[4][10], partialProducts[10][4], carry_13_3)
    sum_14_5, cout_14_5 = FA(partialProducts[5][9], partialProducts[9][5], carry_13_4)
    sum_14_6, cout_14_6 = FA(partialProducts[6][8], partialProducts[8][6], carry_13_5)
    sum_14_7, cout_14_7 = FA(partialProducts[7][7], sum_14_0, carry_13_6)
    sum_14_8, cout_14_8 = FA(sum_14_1, sum_14_2, carry_13_7)
    sum_14_9, cout_14_9 = FA(sum_14_3, sum_14_4, carry_13_8)
    sum_14_10, cout_14_10 = FA(sum_14_5, sum_14_6, carry_13_9)
    sum_14_11, cout_14_11 = FA(sum_14_7, sum_14_8, carry_13_10)
    sum_14_12, cout_14_12 = FA(sum_14_9, sum_14_10, carry_13_11)
    sum2Column[14][0] = sum_14_11
    sum2Column[14][1] = sum_14_12
    carry_14_0 = cout_14_0
    carry_14_1 = cout_14_1
    carry_14_2 = cout_14_2
    carry_14_3 = cout_14_3
    carry_14_4 = cout_14_4
    carry_14_5 = cout_14_5
    carry_14_6 = cout_14_6
    carry_14_7 = cout_14_7
    carry_14_8 = cout_14_8
    carry_14_9 = cout_14_9
    carry_14_10 = cout_14_10
    carry_14_11 = cout_14_11
    carry_14_12 = cout_14_12
    
    #column 15 - 16 dots + 13 carries = 29 → 2 dots (13 FA, 1 HA)
    sum_15_0, cout_15_0 = HA(partialProducts[0][15], partialProducts[15][0])
    sum_15_1, cout_15_1 = FA(partialProducts[1][14], partialProducts[14][1], carry_14_0)
    sum_15_2, cout_15_2 = FA(partialProducts[2][13], partialProducts[13][2], carry_14_1)
    sum_15_3, cout_15_3 = FA(partialProducts[3][12], partialProducts[12][3], carry_14_2)
    sum_15_4, cout_15_4 = FA(partialProducts[4][11], partialProducts[11][4], carry_14_3)
    sum_15_5, cout_15_5 = FA(partialProducts[5][10], partialProducts[10][5], carry_14_4)
    sum_15_6, cout_15_6 = FA(partialProducts[6][9], partialProducts[9][6], carry_14_5)
    sum_15_7, cout_15_7 = FA(partialProducts[7][8], partialProducts[8][7], carry_14_6)
    sum_15_8, cout_15_8 = FA(sum_15_0, sum_15_1, carry_14_7)
    sum_15_9, cout_15_9 = FA(sum_15_2, sum_15_3, carry_14_8)
    sum_15_10, cout_15_10 = FA(sum_15_4, sum_15_5, carry_14_9)
    sum_15_11, cout_15_11 = FA(sum_15_6, sum_15_7, carry_14_10)
    sum_15_12, cout_15_12 = FA(sum_15_8, sum_15_9, carry_14_11)
    sum_15_13, cout_15_13 = FA(sum_15_10, sum_15_11, carry_14_12)
    sum2Column[15][0] = sum_15_12
    sum2Column[15][1] = sum_15_13
    carry_15_0 = cout_15_0
    carry_15_1 = cout_15_1
    carry_15_2 = cout_15_2
    carry_15_3 = cout_15_3
    carry_15_4 = cout_15_4
    carry_15_5 = cout_15_5
    carry_15_6 = cout_15_6
    carry_15_7 = cout_15_7
    carry_15_8 = cout_15_8
    carry_15_9 = cout_15_9
    carry_15_10 = cout_15_10
    carry_15_11 = cout_15_11
    carry_15_12 = cout_15_12
    carry_15_13 = cout_15_13
    
    #column 16 - 15 dots + 14 carries = 29 → 2 dots (13 FA, 1 HA)
    sum_16_0, cout_16_0 = FA(partialProducts[1][15], partialProducts[15][1], carry_15_0)
    sum_16_1, cout_16_1 = FA(partialProducts[2][14], partialProducts[14][2], carry_15_1)
    sum_16_2, cout_16_2 = FA(partialProducts[3][13], partialProducts[13][3], carry_15_2)
    sum_16_3, cout_16_3 = FA(partialProducts[4][12], partialProducts[12][4], carry_15_3)
    sum_16_4, cout_16_4 = FA(partialProducts[5][11], partialProducts[11][5], carry_15_4)
    sum_16_5, cout_16_5 = FA(partialProducts[6][10], partialProducts[10][6], carry_15_5)
    sum_16_6, cout_16_6 = FA(partialProducts[7][9], partialProducts[9][7], carry_15_6)
    sum_16_7, cout_16_7 = FA(partialProducts[8][8], sum_16_0, carry_15_7)
    sum_16_8, cout_16_8 = FA(sum_16_1, sum_16_2, carry_15_8)
    sum_16_9, cout_16_9 = FA(sum_16_3, sum_16_4, carry_15_9)
    sum_16_10, cout_16_10 = FA(sum_16_5, sum_16_6, carry_15_10)
    sum_16_11, cout_16_11 = FA(sum_16_7, sum_16_8, carry_15_11)
    sum_16_12, cout_16_12 = FA(sum_16_9, sum_16_10, carry_15_12)
    sum_16_13, cout_16_13 = HA(sum_16_11, carry_15_13)
    sum2Column[16][0] = sum_16_12
    sum2Column[16][1] = sum_16_13
    carry_16_0 = cout_16_0
    carry_16_1 = cout_16_1
    carry_16_2 = cout_16_2
    carry_16_3 = cout_16_3
    carry_16_4 = cout_16_4
    carry_16_5 = cout_16_5
    carry_16_6 = cout_16_6
    carry_16_7 = cout_16_7
    carry_16_8 = cout_16_8
    carry_16_9 = cout_16_9
    carry_16_10 = cout_16_10
    carry_16_11 = cout_16_11
    carry_16_12 = cout_16_12
    carry_16_13 = cout_16_13
    
    #column 17 - 14 dots + 14 carries = 28 → 2 dots (13 FA)
    sum_17_0, cout_17_0 = FA(partialProducts[2][15], partialProducts[15][2], carry_16_0)
    sum_17_1, cout_17_1 = FA(partialProducts[3][14], partialProducts[14][3], carry_16_1)
    sum_17_2, cout_17_2 = FA(partialProducts[4][13], partialProducts[13][4], carry_16_2)
    sum_17_3, cout_17_3 = FA(partialProducts[5][12], partialProducts[12][5], carry_16_3)
    sum_17_4, cout_17_4 = FA(partialProducts[6][11], partialProducts[11][6], carry_16_4)
    sum_17_5, cout_17_5 = FA(partialProducts[7][10], partialProducts[10][7], carry_16_5)
    sum_17_6, cout_17_6 = FA(partialProducts[8][9], partialProducts[9][8], carry_16_6)
    sum_17_7, cout_17_7 = FA(sum_17_0, sum_17_1, carry_16_7)
    sum_17_8, cout_17_8 = FA(sum_17_2, sum_17_3, carry_16_8)
    sum_17_9, cout_17_9 = FA(sum_17_4, sum_17_5, carry_16_9)
    sum_17_10, cout_17_10 = FA(sum_17_6, sum_17_7, carry_16_10)
    sum_17_11, cout_17_11 = FA(sum_17_8, sum_17_9, carry_16_11)
    sum_17_12, cout_17_12 = FA(sum_17_10, carry_16_12, carry_16_13)
    sum2Column[17][0] = sum_17_11
    sum2Column[17][1] = sum_17_12
    carry_17_0 = cout_17_0
    carry_17_1 = cout_17_1
    carry_17_2 = cout_17_2
    carry_17_3 = cout_17_3
    carry_17_4 = cout_17_4
    carry_17_5 = cout_17_5
    carry_17_6 = cout_17_6
    carry_17_7 = cout_17_7
    carry_17_8 = cout_17_8
    carry_17_9 = cout_17_9
    carry_17_10 = cout_17_10
    carry_17_11 = cout_17_11
    carry_17_12 = cout_17_12
    
    #column 18 - 13 dots + 13 carries = 26 → 2 dots (12 FA)
    sum_18_0, cout_18_0 = FA(partialProducts[3][15], partialProducts[15][3], carry_17_0)
    sum_18_1, cout_18_1 = FA(partialProducts[4][14], partialProducts[14][4], carry_17_1)
    sum_18_2, cout_18_2 = FA(partialProducts[5][13], partialProducts[13][5], carry_17_2)
    sum_18_3, cout_18_3 = FA(partialProducts[6][12], partialProducts[12][6], carry_17_3)
    sum_18_4, cout_18_4 = FA(partialProducts[7][11], partialProducts[11][7], carry_17_4)
    sum_18_5, cout_18_5 = FA(partialProducts[8][10], partialProducts[10][8], carry_17_5)
    sum_18_6, cout_18_6 = FA(partialProducts[9][9], sum_18_0, carry_17_6)
    sum_18_7, cout_18_7 = FA(sum_18_1, sum_18_2, carry_17_7)
    sum_18_8, cout_18_8 = FA(sum_18_3, sum_18_4, carry_17_8)
    sum_18_9, cout_18_9 = FA(sum_18_5, sum_18_6, carry_17_9)
    sum_18_10, cout_18_10 = FA(sum_18_7, sum_18_8, carry_17_10)
    sum_18_11, cout_18_11 = FA(sum_18_9, carry_17_11, carry_17_12)
    sum2Column[18][0] = sum_18_10
    sum2Column[18][1] = sum_18_11
    carry_18_0 = cout_18_0
    carry_18_1 = cout_18_1
    carry_18_2 = cout_18_2
    carry_18_3 = cout_18_3
    carry_18_4 = cout_18_4
    carry_18_5 = cout_18_5
    carry_18_6 = cout_18_6
    carry_18_7 = cout_18_7
    carry_18_8 = cout_18_8
    carry_18_9 = cout_18_9
    carry_18_10 = cout_18_10
    carry_18_11 = cout_18_11
    
    #column 19 - 12 dots + 12 carries = 24 → 2 dots (11 FA)
    sum_19_0, cout_19_0 = FA(partialProducts[4][15], partialProducts[15][4], carry_18_0)
    sum_19_1, cout_19_1 = FA(partialProducts[5][14], partialProducts[14][5], carry_18_1)
    sum_19_2, cout_19_2 = FA(partialProducts[6][13], partialProducts[13][6], carry_18_2)
    sum_19_3, cout_19_3 = FA(partialProducts[7][12], partialProducts[12][7], carry_18_3)
    sum_19_4, cout_19_4 = FA(partialProducts[8][11], partialProducts[11][8], carry_18_4)
    sum_19_5, cout_19_5 = FA(partialProducts[9][10], partialProducts[10][9], carry_18_5)
    sum_19_6, cout_19_6 = FA(sum_19_0, sum_19_1, carry_18_6)
    sum_19_7, cout_19_7 = FA(sum_19_2, sum_19_3, carry_18_7)
    sum_19_8, cout_19_8 = FA(sum_19_4, sum_19_5, carry_18_8)
    sum_19_9, cout_19_9 = FA(sum_19_6, sum_19_7, carry_18_9)
    sum_19_10, cout_19_10 = FA(sum_19_8, carry_18_10, carry_18_11)
    sum2Column[19][0] = sum_19_9
    sum2Column[19][1] = sum_19_10
    carry_19_0 = cout_19_0
    carry_19_1 = cout_19_1
    carry_19_2 = cout_19_2
    carry_19_3 = cout_19_3
    carry_19_4 = cout_19_4
    carry_19_5 = cout_19_5
    carry_19_6 = cout_19_6
    carry_19_7 = cout_19_7
    carry_19_8 = cout_19_8
    carry_19_9 = cout_19_9
    carry_19_10 = cout_19_10
    
    #column 20 - 11 dots + 11 carries = 22 → 2 dots (10 FA)
    sum_20_0, cout_20_0 = FA(partialProducts[5][15], partialProducts[15][5], carry_19_0)
    sum_20_1, cout_20_1 = FA(partialProducts[6][14], partialProducts[14][6], carry_19_1)
    sum_20_2, cout_20_2 = FA(partialProducts[7][13], partialProducts[13][7], carry_19_2)
    sum_20_3, cout_20_3 = FA(partialProducts[8][12], partialProducts[12][8], carry_19_3)
    sum_20_4, cout_20_4 = FA(partialProducts[9][11], partialProducts[11][9], carry_19_4)
    sum_20_5, cout_20_5 = FA(partialProducts[10][10], sum_20_0, carry_19_5)
    sum_20_6, cout_20_6 = FA(sum_20_1, sum_20_2, carry_19_6)
    sum_20_7, cout_20_7 = FA(sum_20_3, sum_20_4, carry_19_7)
    sum_20_8, cout_20_8 = FA(sum_20_5, sum_20_6, carry_19_8)
    sum_20_9, cout_20_9 = FA(sum_20_7, carry_19_9, carry_19_10)
    sum2Column[20][0] = sum_20_8
    sum2Column[20][1] = sum_20_9
    carry_20_0 = cout_20_0
    carry_20_1 = cout_20_1
    carry_20_2 = cout_20_2
    carry_20_3 = cout_20_3
    carry_20_4 = cout_20_4
    carry_20_5 = cout_20_5
    carry_20_6 = cout_20_6
    carry_20_7 = cout_20_7
    carry_20_8 = cout_20_8
    carry_20_9 = cout_20_9
    
    #column 21 - 10 dots + 10 carries = 20 → 2 dots (9 FA)
    sum_21_0, cout_21_0 = FA(partialProducts[6][15], partialProducts[15][6], carry_20_0)
    sum_21_1, cout_21_1 = FA(partialProducts[7][14], partialProducts[14][7], carry_20_1)
    sum_21_2, cout_21_2 = FA(partialProducts[8][13], partialProducts[13][8], carry_20_2)
    sum_21_3, cout_21_3 = FA(partialProducts[9][12], partialProducts[12][9], carry_20_3)
    sum_21_4, cout_21_4 = FA(partialProducts[10][11], partialProducts[11][10], carry_20_4)
    sum_21_5, cout_21_5 = FA(sum_21_0, sum_21_1, carry_20_5)
    sum_21_6, cout_21_6 = FA(sum_21_2, sum_21_3, carry_20_6)
    sum_21_7, cout_21_7 = FA(sum_21_4, sum_21_5, carry_20_7)
    sum_21_8, cout_21_8 = FA(sum_21_6, carry_20_8, carry_20_9)
    sum2Column[21][0] = sum_21_7
    sum2Column[21][1] = sum_21_8
    carry_21_0 = cout_21_0
    carry_21_1 = cout_21_1
    carry_21_2 = cout_21_2
    carry_21_3 = cout_21_3
    carry_21_4 = cout_21_4
    carry_21_5 = cout_21_5
    carry_21_6 = cout_21_6
    carry_21_7 = cout_21_7
    carry_21_8 = cout_21_8
    
    #column 22 - 9 dots + 9 carries = 18 → 2 dots (8 FA)
    sum_22_0, cout_22_0 = FA(partialProducts[7][15], partialProducts[15][7], carry_21_0)
    sum_22_1, cout_22_1 = FA(partialProducts[8][14], partialProducts[14][8], carry_21_1)
    sum_22_2, cout_22_2 = FA(partialProducts[9][13], partialProducts[13][9], carry_21_2)
    sum_22_3, cout_22_3 = FA(partialProducts[10][12], partialProducts[12][10], carry_21_3)
    sum_22_4, cout_22_4 = FA(partialProducts[11][11], sum_22_0, carry_21_4)
    sum_22_5, cout_22_5 = FA(sum_22_1, sum_22_2, carry_21_5)
    sum_22_6, cout_22_6 = FA(sum_22_3, sum_22_4, carry_21_6)
    sum_22_7, cout_22_7 = FA(sum_22_5, carry_21_7, carry_21_8)
    sum2Column[22][0] = sum_22_6
    sum2Column[22][1] = sum_22_7
    carry_22_0 = cout_22_0
    carry_22_1 = cout_22_1
    carry_22_2 = cout_22_2
    carry_22_3 = cout_22_3
    carry_22_4 = cout_22_4
    carry_22_5 = cout_22_5
    carry_22_6 = cout_22_6
    carry_22_7 = cout_22_7
    
    #column 23 - 8 dots + 8 carries = 16 → 2 dots (7 FA)
    sum_23_0, cout_23_0 = FA(partialProducts[8][15], partialProducts[15][8], carry_22_0)
    sum_23_1, cout_23_1 = FA(partialProducts[9][14], partialProducts[14][9], carry_22_1)
    sum_23_2, cout_23_2 = FA(partialProducts[10][13], partialProducts[13][10], carry_22_2)
    sum_23_3, cout_23_3 = FA(partialProducts[11][12], partialProducts[12][11], carry_22_3)
    sum_23_4, cout_23_4 = FA(sum_23_0, sum_23_1, carry_22_4)
    sum_23_5, cout_23_5 = FA(sum_23_2, sum_23_3, carry_22_5)
    sum_23_6, cout_23_6 = FA(sum_23_4, carry_22_6, carry_22_7)
    sum2Column[23][0] = sum_23_5
    sum2Column[23][1] = sum_23_6
    carry_23_0 = cout_23_0
    carry_23_1 = cout_23_1
    carry_23_2 = cout_23_2
    carry_23_3 = cout_23_3
    carry_23_4 = cout_23_4
    carry_23_5 = cout_23_5
    carry_23_6 = cout_23_6
    
    #column 24 - 7 dots + 7 carries = 14 → 2 dots (6 FA)
    sum_24_0, cout_24_0 = FA(partialProducts[9][15], partialProducts[15][9], carry_23_0)
    sum_24_1, cout_24_1 = FA(partialProducts[10][14], partialProducts[14][10], carry_23_1)
    sum_24_2, cout_24_2 = FA(partialProducts[11][13], partialProducts[13][11], carry_23_2)
    sum_24_3, cout_24_3 = FA(partialProducts[12][12], sum_24_0, carry_23_3)
    sum_24_4, cout_24_4 = FA(sum_24_1, sum_24_2, carry_23_4)
    sum_24_5, cout_24_5 = FA(sum_24_3, carry_23_5, carry_23_6)
    sum2Column[24][0] = sum_24_4
    sum2Column[24][1] = sum_24_5
    carry_24_0 = cout_24_0
    carry_24_1 = cout_24_1
    carry_24_2 = cout_24_2
    carry_24_3 = cout_24_3
    carry_24_4 = cout_24_4
    carry_24_5 = cout_24_5
    
    #column 25 - 6 dots + 6 carries = 12 → 2 dots (5 FA)
    sum_25_0, cout_25_0 = FA(partialProducts[10][15], partialProducts[15][10], carry_24_0)
    sum_25_1, cout_25_1 = FA(partialProducts[11][14], partialProducts[14][11], carry_24_1)
    sum_25_2, cout_25_2 = FA(partialProducts[12][13], partialProducts[13][12], carry_24_2)
    sum_25_3, cout_25_3 = FA(sum_25_0, sum_25_1, carry_24_3)
    sum_25_4, cout_25_4 = FA(sum_25_2, carry_24_4, carry_24_5)
    sum2Column[25][0] = sum_25_3
    sum2Column[25][1] = sum_25_4
    carry_25_0 = cout_25_0
    carry_25_1 = cout_25_1
    carry_25_2 = cout_25_2
    carry_25_3 = cout_25_3
    carry_25_4 = cout_25_4
    
    #column 26 - 5 dots + 5 carries = 10 → 2 dots (4 FA)
    sum_26_0, cout_26_0 = FA(partialProducts[11][15], partialProducts[15][11], carry_25_0)
    sum_26_1, cout_26_1 = FA(partialProducts[12][14], partialProducts[14][12], carry_25_1)
    sum_26_2, cout_26_2 = FA(partialProducts[13][13], sum_26_0, carry_25_2)
    sum_26_3, cout_26_3 = FA(sum_26_1, carry_25_3, carry_25_4)
    sum2Column[26][0] = sum_26_2
    sum2Column[26][1] = sum_26_3
    carry_26_0 = cout_26_0
    carry_26_1 = cout_26_1
    carry_26_2 = cout_26_2
    carry_26_3 = cout_26_3
    
    #column 27 - 4 dots + 4 carries = 8 → 2 dots (3 FA)
    sum_27_0, cout_27_0 = FA(partialProducts[12][15], partialProducts[15][12], carry_26_0)
    sum_27_1, cout_27_1 = FA(partialProducts[13][14], partialProducts[14][13], carry_26_1)
    sum_27_2, cout_27_2 = FA(sum_27_0, carry_26_2, carry_26_3)
    sum2Column[27][0] = sum_27_1
    sum2Column[27][1] = sum_27_2
    carry_27_0 = cout_27_0
    carry_27_1 = cout_27_1
    carry_27_2 = cout_27_2
    
    #column 28 - 3 dots + 3 carries = 6 → 2 dots (2 FA)
    sum_28_0, cout_28_0 = FA(partialProducts[13][15], partialProducts[15][13], carry_27_0)
    sum_28_1, cout_28_1 = FA(partialProducts[14][14], carry_27_1, carry_27_2)
    sum2Column[28][0] = sum_28_0
    sum2Column[28][1] = sum_28_1
    carry_28_0 = cout_28_0
    carry_28_1 = cout_28_1
    
    #column 29 - 2 dots + 2 carries = 4 → 2 dots (1 FA)
    sum_29_0, cout_29_0 = FA(partialProducts[14][15], partialProducts[15][14], carry_28_0)
    sum2Column[29][0] = sum_29_0
    sum2Column[29][1] = carry_28_1
    carry_29_0 = cout_29_0
    
    #column 30 - 1 dot + 1 carry = 2 dots
    sum2Column[30][0] = partialProducts[15][15]
    sum2Column[30][1] = carry_29_0
    
    #column 31 - just propagate if any final carry
    sum2Column[31][0] = False
    sum2Column[31][1] = False
    
    # Final ripple carry addition
    row0 = [sum2Column[i][0] for i in range(32)]
    row1 = [sum2Column[i][1] for i in range(32)]
    
    product = [False] * 32
    carry = False
    for i in range(32):
        product[i], carry = fullAdder(row0[i], row1[i], carry)
    
    return product
# # #16bit divider
# def bitDiv16(a, b):

# =====  tiny primitives  ==================================================
def HA(a, b):                               # half-adder
    return a ^ b, a & b

def FA(a, b, c):                            # full-adder
    s  = a ^ b ^ c
    co = (a & b) | (b & c) | (a & c)
    return s, co

def addBits(a, b, cin=False):               # n-bit adder
    out, c = [], cin
    for i in range(len(a)):
        s, c = FA(a[i], b[i], c)
        out.append(s)
    return out, c

def twoComp(v):                             # two’s-complement negate
    inv = [not b for b in v]
    one = [True] + [False]*(len(v)-1)
    return addBits(inv, one)[0]

def subBits(a, b):                          # a − b
    return addBits(a, twoComp(b))[0]

def shiftLeft(bits, in_bit):                # logical shift-left by 1
    return [in_bit] + bits[:-1]
# -------------------------------------------------------------------------

def _uDiv_nonrestoring(dividend, divisor):
    """Unsigned, non-restoring division (n-bit) → (Q, R)"""
    n   = len(dividend)
    Q   = [False]*n
    R   = [False]*(n+1)            # one extra sign bit
    D   = divisor + [False]        # align width

    for i in range(n-1, -1, -1):   # MSB → LSB
        R = shiftLeft(R, dividend[i])

        if not R[-1]:              # R ≥ 0 → subtract
            R = subBits(R, D)
        else:                      # R < 0 → add
            R, _ = addBits(R, D)

        Q[i] = not R[-1]           # quotient bit = ¬sign(R)

    if R[-1]:                      # final sign fix if negative
        R, _ = addBits(R, D)

    return Q, R[:-1]               # drop extra sign bit

# -------------------------------------------------------------------------
def bitDiv16_nonrestoring(a_bits, b_bits):
    """
    Gate-level 16-bit signed division (non-restoring).
    Returns  (quotient[16], remainder[16])  -- both LSB-first.
    Raises ZeroDivisionError on b == 0.
    """
    n = 16
    sign_a, sign_b = a_bits[15], b_bits[15]

    # magnitudes
    A = twoComp(a_bits) if sign_a else a_bits[:]
    B = twoComp(b_bits) if sign_b else b_bits[:]
    if B.count(True) == 0:
        raise ZeroDivisionError

    Qmag, Rmag = _uDiv_nonrestoring(A, B)

    # apply signs
    Q = twoComp(Qmag) if sign_a ^ sign_b else Qmag
    R = twoComp(Rmag) if sign_a         else Rmag

    return Q[:n], R[:n]




# def bitDiv4(A, B):
    
#     # a and b are lists of 4 bits: a[3] is MSB, a[0] is LSB
#     # Implements a 4-bit binary comparator for division (not a full divider)
#     # The logic is based on bitwise comparison, rewritten to use a/b indices

#     # Helper functions for logic
#     def xnor(x, y):
#         return (x and y) or (not x and not y)
#     def comparatorCircuit(A,B):
#         b1 = a[3] and not b[3]
#         b2 = xnor(a[3], b[3]) and (a[2] and not b[2])
#         b3 = xnor(a[3], b[3]) and xnor(a[2], b[2]) and (a[1] and not b[1])
#         b4 = xnor(a[3], b[3]) and xnor(a[2], b[2]) and xnor(a[1], b[1]) and (a[0] and not b[0])
#         b5 = xnor(a[3], b[3]) and xnor(a[2], b[2]) and xnor(a[1], b[1]) and xnor(a[0], b[0])
#         bitDec = b1 or b2 or b3 or b4 or b5
#         return bitDec
    

def bitAdd16(a, b, c_in):
    s = [False] * 16
    c = [False] * (16+1)
    c[0] = c_in
    for i in range(16):
        s[i], c[i + 1] = fullAdder(a[i], b[i], c[i])
    return s, c[16]

#should in theory work fine for both positive and negative in 2s complement
#might need to add zero and carry flags.
def bitAdd5(a, b, c_in):
    s = [False] * 5
    c = [False] * (5+1)
    c[0] = c_in
    for i in range(5):
        s[i], c[i + 1] = fullAdder(a[i], b[i], c[i])
    return s, c[5]

# def bitFPAdd32(a, b):

def bitMul16(a_bits, b_bits):
    n = 16
    # --- partial products -------------------------------------------------
    pp = [[a_bits[i] and b_bits[j] for j in range(n)] for i in range(n)]
    for j in range(n-1):               # invert MSB row
        pp[n-1][j] = not pp[n-1][j]
    for i in range(n-1):               # invert MSB col
        pp[i][n-1] = not pp[i][n-1]

    # --- bucket dots by column -------------------------------------------
    cols = [[] for _ in range(2*n)]
    for i in range(n):
        for j in range(n):
            cols[i+j].append(pp[i][j])
    cols[n].append(True)               # two Baugh-Wooley correction 1’s
    cols[2*n-1].append(True)

    # --- Dadda compression to 2 rows -------------------------------------
    sums  = [False]*(2*n)
    carys = [False]*(2*n)
    for k in range(2*n):
        while len(cols[k]) > 2:
            s,c = FA(cols[k].pop(), cols[k].pop(), cols[k].pop())
            cols[k].append(s)
            if k < 2*n-1:
                cols[k+1].append(c)
        if cols[k]: sums[k]  = cols[k].pop()
        if cols[k]: carys[k] = cols[k].pop()

    # --- final ripple-carry adder ----------------------------------------
    P   = [False]*(2*n)
    cin = False
    for k in range(2*n):
        P[k], cin = FA(sums[k], carys[k], cin)
    return P


# def bitFPSub32(a, b):


"""/****************************************************************************
 * DADDA REDUCTION ANALYSIS FOR 11-BIT MULTIPLIER
 *
 * Initial dot counts per column (partial products):
 * col  0:  1 dot   (weight 2^0)  – a[0]×b[0]
 * col  1:  2 dots  (weight 2^1)  – a[1]×b[0], a[0]×b[1]
 * col  2:  3 dots  (weight 2^2)  – a[2]×b[0], a[1]×b[1], a[0]×b[2]
 * col  3:  4 dots  (weight 2^3)  – a[3]×b[0], a[2]×b[1], a[1]×b[2], a[0]×b[3]
 * col  4:  5 dots  (weight 2^4)  – a[4]×b[0], a[3]×b[1], a[2]×b[2], a[1]×b[3], a[0]×b[4]
 * col  5:  6 dots  (weight 2^5)  – a[5]×b[0], a[4]×b[1], a[3]×b[2], a[2]×b[3], a[1]×b[4], a[0]×b[5]
 * col  6:  7 dots  (weight 2^6)  – a[6]×b[0], a[5]×b[1], a[4]×b[2], a[3]×b[3], a[2]×b[4], a[1]×b[5], a[0]×b[6]
 * col  7:  8 dots  (weight 2^7)  – a[7]×b[0], a[6]×b[1], a[5]×b[2], a[4]×b[3], a[3]×b[4], a[2]×b[5], a[1]×b[6], a[0]×b[7]
 * col  8:  9 dots  (weight 2^8)  – a[8]×b[0], a[7]×b[1], a[6]×b[2], a[5]×b[3], a[4]×b[4], a[3]×b[5], a[2]×b[6], a[1]×b[7], a[0]×b[8]
 * col  9: 10 dots  (weight 2^9)  – a[9]×b[0], a[8]×b[1], a[7]×b[2], a[6]×b[3], a[5]×b[4], a[4]×b[5], a[3]×b[6], a[2]×b[7], a[1]×b[8], a[0]×b[9]
 * col 10: 11 dots  (weight 2^10) – a[10]×b[0], a[9]×b[1], a[8]×b[2], a[7]×b[3], a[6]×b[4], a[5]×b[5], a[4]×b[6], a[3]×b[7], a[2]×b[8], a[1]×b[9], a[0]×b[10]
 * col 11: 10 dots  (weight 2^11) – a[10]×b[1], a[9]×b[2], a[8]×b[3], a[7]×b[4], a[6]×b[5], a[5]×b[6], a[4]×b[7], a[3]×b[8], a[2]×b[9], a[1]×b[10]
 * col 12:  9 dots  (weight 2^12) – a[10]×b[2], a[9]×b[3], a[8]×b[4], a[7]×b[5], a[6]×b[6], a[5]×b[7], a[4]×b[8], a[3]×b[9], a[2]×b[10]
 * col 13:  8 dots  (weight 2^13) – a[10]×b[3], a[9]×b[4], a[8]×b[5], a[7]×b[6], a[6]×b[7], a[5]×b[8], a[4]×b[9], a[3]×b[10]
 * col 14:  7 dots  (weight 2^14) – a[10]×b[4], a[9]×b[5], a[8]×b[6], a[7]×b[7], a[6]×b[8], a[5]×b[9], a[4]×b[10]
 * col 15:  6 dots  (weight 2^15) – a[10]×b[5], a[9]×b[6], a[8]×b[7], a[7]×b[8], a[6]×b[9], a[5]×b[10]
 * col 16:  5 dots  (weight 2^16) – a[10]×b[6], a[9]×b[7], a[8]×b[8], a[7]×b[9], a[6]×b[10]
 * col 17:  4 dots  (weight 2^17) – a[10]×b[7], a[9]×b[8], a[8]×b[9], a[7]×b[10]
 * col 18:  3 dots  (weight 2^18) – a[10]×b[8], a[9]×b[9], a[8]×b[10]
 * col 19:  2 dots  (weight 2^19) – a[10]×b[9], a[9]×b[10]
 * col 20:  1 dot   (weight 2^20) – a[10]×b[10]
 *
 * SEQUENCE REDUCTION: 2, 3, 4, 6, 9, 13, 19, 28, 42…
 *
 * DADDA REDUCTION STAGES:
 *   Stage 1: 11 → 9 dots
 *   Stage 2:  9 → 6 dots
 *   Stage 3:  6 → 4 dots
 *   Stage 4:  4 → 3 dots
 *   Stage 5:  3 → 2 dots (final)
 ****************************************************************************/

/*** STAGE 1: Reduction from 11 to 9 dots ***/
/*
 * Columns 0-8: already ≤ 9 dots – no reduction.
 *
 * Column 9 : 10 dots → 9 (1 HA)
 *            – take 2 dots, return 1 sum in col 9, send 1 carry to col 10.
 *
 * Column 10: 11 dots + 1 carry = 12 → 9
 *            – 1 FA: 12 → 10, carry → col 11
 *            – 1 HA: 10 → 9,  carry → col 11
 *
 * Column 11: 10 dots + 2 carries = 12 → 9
 *            – 1 FA: 12 → 10, carry → col 12
 *            – 1 HA: 10 → 9,  carry → col 12
 *
 * Column 12:  9 dots + 2 carries = 11 → 9
 *            – 1 FA: 11 → 9,  carry → col 13
 *
 * Column 13 reaches 9 dots after the incoming carry – no action.
 *
 * Stage 1 summary:
 *   Column 9 : 0 FA, 1 HA
 *   Column 10: 1 FA, 1 HA
 *   Column 11: 1 FA, 1 HA
 *   Column 12: 1 FA, 0 HA
 *   ----------------------
 *   **Total Stage 1:** 3 FA, 3 HA
 *

 */

/*** STAGE 2: Reduction from 9 to 6 dots ***/
/*
 * Column 0-5: Already ≤ 6 dots, no reduction needed
 *
 * Column 6: 7 dots → 6 dots (needs 1 HA)
 *   - Take 2 dots and replace with 1 dot in column 6, add 1 carry to column 7
 *   - Resulting column 6: 6 dots
 *   - HA count: 1
 *
 * Column 7: 8 dots + 1 carry = 9 dots → 6 dots (needs 1 FA, 1 HA)
 *   - FA: take 3 dots ⇒ 1 dot in col 7, 1 carry → col 8
 *   - HA: take 2 dots ⇒ 1 dot in col 7, 1 carry → col 8
 *   - Resulting column 7: 6 dots
 *   - FA count: 1, HA count: 1
 *
 * Column 8: 9 dots + 2 carries = 11 dots → 6 dots (needs 2 FA, 1 HA)
 *   - FA #1: 3 dots ⇒ 1 dot, 1 carry → col 9
 *   - FA #2: 3 dots ⇒ 1 dot, 1 carry → col 9
 *   - HA: 2 dots ⇒ 1 dot, 1 carry → col 9
 *   - Resulting column 8: 6 dots
 *   - FA count: 2, HA count: 1
 *
 * Column 9: 9 dots + 3 carries = 12 dots → 6 dots (needs 3 FA)
 *   - 3 FAs (each: 3 dots ⇒ 1 dot, 1 carry → col 10)
 *   - Resulting column 9: 6 dots
 *   - FA count: 3
 *
 * Column 10: 9 dots + 3 carries = 12 dots → 6 dots (needs 3 FA)
 *   - 3 FAs → 3 carries to column 11
 *   - Resulting column 10: 6 dots
 *   - FA count: 3
 *
 * Column 11: 9 dots + 3 carries = 12 dots → 6 dots (needs 3 FA)
 *   - 3 FAs → 3 carries to column 12
 *   - Resulting column 11: 6 dots
 *   - FA count: 3
 *
 * Column 12: 9 dots + 3 carries = 12 dots → 6 dots (needs 3 FA)
 *   - 3 FAs → 3 carries to column 13
 *   - Resulting column 12: 6 dots
 *   - FA count: 3
 *
 * Column 13: 9 dots + 3 carries = 12 dots → 6 dots (needs 3 FA)
 *   - 3 FAs → 3 carries to column 14
 *   - Resulting column 13: 6 dots
 *   - FA count: 3
 *
 * Column 14: 7 dots + 3 carries = 10 dots → 6 dots (needs 2 FA)
 *   - 2 FAs → 2 carries to column 15
 *   - Resulting column 14: 6 dots
 *   - FA count: 2
 *
 * Column 15: 6 dots + 2 carries = 8 dots → 6 dots (needs 1 FA)
 *   - 1 FA → 1 carry to column 16
 *   - Resulting column 15: 6 dots
 *   - FA count: 1
 *
 * Column 16: 5 dots + 1 carry = 6 dots – already at target, no reduction
 *
 * Columns 17-20: ≤ 6 dots, no reduction
 *
 * Stage 2 summary:
 *   FA: 21, HA: 3
 */

/*** STAGE 3: Reduction from 6 to 4 dots ***/
/*
 * Column 0-3: Already ≤ 4 dots, no reduction needed
 *
 * Column 4: 5 dots → 4 dots (needs 1 HA)
 *   - HA: 2 dots ⇒ 1 dot in col 4, 1 carry → col 5
 *   - Resulting column 4: 4 dots
 *   - HA count: 1
 *
 * Column 5: 6 dots + 1 carry = 7 dots → 4 dots (needs 1 FA, 1 HA)
 *   - FA: 3 dots ⇒ 1 dot, 1 carry → col 6
 *   - HA: 2 dots ⇒ 1 dot, 1 carry → col 6
 *   - Resulting column 5: 4 dots
 *   - FA count: 1, HA count: 1
 *
 * Column 6: 6 dots + 2 carries = 8 dots → 4 dots (needs 2 FA)
 *   - FA #1: 3 dots ⇒ 1 dot, 1 carry → col 7
 *   - FA #2: 3 dots ⇒ 1 dot, 1 carry → col 7
 *   - Resulting column 6: 4 dots
 *   - FA count: 2
 *
 * Column 7: 6 dots + 2 carries = 8 dots → 4 dots (needs 2 FA)
 *   - 2 FAs → 2 carries to column 8
 *   - Resulting column 7: 4 dots
 *   - FA count: 2
 *
 * Column 8: 6 dots + 2 carries = 8 dots → 4 dots (needs 2 FA)
 *   - 2 FAs → 2 carries to column 9
 *   - Resulting column 8: 4 dots
 *   - FA count: 2
 *
 * Column 9: 6 dots + 2 carries = 8 dots → 4 dots (needs 2 FA)
 *   - 2 FAs → 2 carries to column 10
 *   - Resulting column 9: 4 dots
 *   - FA count: 2
 *
 * Column 10: 6 dots + 2 carries = 8 dots → 4 dots (needs 2 FA)
 *   - 2 FAs → 2 carries to column 11
 *   - Resulting column 10: 4 dots
 *   - FA count: 2
 *
 * Column 11: 6 dots + 2 carries = 8 dots → 4 dots (needs 2 FA)
 *   - 2 FAs → 2 carries to column 12
 *   - Resulting column 11: 4 dots
 *   - FA count: 2
 *
 * Column 12: 6 dots + 2 carries = 8 dots → 4 dots (needs 2 FA)
 *   - 2 FAs → 2 carries to column 13
 *   - Resulting column 12: 4 dots
 *   - FA count: 2
 *
 * Column 13: 6 dots + 2 carries = 8 dots → 4 dots (needs 2 FA)
 *   - 2 FAs → 2 carries to column 14
 *   - Resulting column 13: 4 dots
 *   - FA count: 2
 *
 * Column 14: 6 dots + 2 carries = 8 dots → 4 dots (needs 2 FA)
 *   - 2 FAs → 2 carries to column 15
 *   - Resulting column 14: 4 dots
 *   - FA count: 2
 *
 * Column 15: 6 dots + 2 carries = 8 dots → 4 dots (needs 2 FA)
 *   - 2 FAs → 2 carries to column 16
 *   - Resulting column 15: 4 dots
 *   - FA count: 2
 *
 * Column 16: 6 dots + 2 carries = 8 dots → 4 dots (needs 2 FA)
 *   - 2 FAs → 2 carries to column 17
 *   - Resulting column 16: 4 dots
 *   - FA count: 2
 *
 * Column 17: 4 dots + 2 carries = 6 dots → 4 dots (needs 1 FA)
 *   - FA: 3 dots ⇒ 1 dot, 1 carry → col 18
 *   - Resulting column 17: 4 dots
 *   - FA count: 1
 *
 * Column 18: 3 dots + 1 carry = 4 dots – already at target, no reduction
 *
 * Columns 19-20: ≤ 4 dots, no reduction
 *
 * Stage 3 summary:
 *   FA: 24, HA: 2
 */

 /*** STAGE 4: Reduction from 4 to 3 dots ***/
/*
 * Target height = 3.  
 * Strategy:  
 *   • If a column has **4 dots** → use **1 HA** (net –1 dot, +1 carry).  
 *   • If a column has **≥5 dots** → use **1 FA** (pick 3 dots → 1 sum, +1 carry; net –2 dots)  
 *     until the height falls to 3, then finish with 1 HA if still 4.
 *
 * Columns 0-2: already ≤ 3 dots — no action.
 *
 * Column 3: 4 dots → 3 dots (1 HA)
 *   – HA: 2 dots ⇒ 1 sum in col 3, 1 carry → col 4
 *   – Result col 3: 3 dots
 *   – HA count: 1
 *
 * Column 4: 4 dots + 1 carry = 5 → 3 (1 FA)
 *   – FA: 3 dots ⇒ 1 sum in col 4, 1 carry → col 5
 *   – Result col 4: 3 dots
 *   – FA count: 1
 *
 * Column 5: 4 dots + 1 carry = 5 → 3 (1 FA)
 *   – FA → carry → col 6
 *   – Result col 5: 3 dots
 *   – FA count: 1
 *
 * Column 6: 4 dots + 1 carry = 5 → 3 (1 FA)
 *   – FA → carry → col 7
 *   – Result col 6: 3 dots
 *
 * Column 7: 4 dots + 1 carry = 5 → 3 (1 FA)
 *   – FA → carry → col 8
 *   – Result col 7: 3 dots
 *
 * Column 8: 4 dots + 1 carry = 5 → 3 (1 FA)
 *   – FA → carry → col 9
 *   – Result col 8: 3 dots
 *
 * Column 9: 4 dots + 1 carry = 5 → 3 (1 FA)
 *   – FA → carry → col 10
 *   – Result col 9: 3 dots
 *
 * Column 10: 4 dots + 1 carry = 5 → 3 (1 FA)
 *   – FA → carry → col 11
 *   – Result col 10: 3 dots
 *
 * Column 11: 4 dots + 1 carry = 5 → 3 (1 FA)
 *   – FA → carry → col 12
 *   – Result col 11: 3 dots
 *
 * Column 12: 4 dots + 1 carry = 5 → 3 (1 FA)
 *   – FA → carry → col 13
 *   – Result col 12: 3 dots
 *
 * Column 13: 4 dots + 1 carry = 5 → 3 (1 FA)
 *   – FA → carry → col 14
 *   – Result col 13: 3 dots
 *
 * Column 14: 4 dots + 1 carry = 5 → 3 (1 FA)
 *   – FA → carry → col 15
 *   – Result col 14: 3 dots
 *
 * Column 15: 4 dots + 1 carry = 5 → 3 (1 FA)
 *   – FA → carry → col 16
 *   – Result col 15: 3 dots
 *
 * Column 16: 4 dots + 1 carry = 5 → 3 (1 FA)
 *   – FA → carry → col 17
 *   – Result col 16: 3 dots
 *
 * Column 17: 4 dots + 1 carry = 5 → 3 (1 FA)
 *   – FA → carry → col 18
 *   – Result col 17: 3 dots
 *
 * Column 18: 4 dots + 1 carry = 5 → 3 (1 FA)
 *   – FA → carry → col 19
 *   – Result col 18: 3 dots
 *
 * Column 19: 2 dots + 1 carry = 3 dots — already at target, no action.
 *
 * Column 20: 1 dot — no action.
 *
 * Stage 4 summary (after all cascaded carries settle):
 *   Column 3 : 0 FA, 1 HA
 *   Columns 4-18: 1 FA each
 *   -------------------------
 *   **Total Stage 4:** 15 FA, 1 HA
 *
 *  (All columns are now ≤ 3 dots, ready for the final Stage 5 reduction
 *   from 3 to 2 dots.)
 */

/*** STAGE 5: Reduction from 3-dot columns → final 2-row array ***/
/*
 * Target: every column ≤ 2 dots before the closing ripple-carry adder (RCA).
 *
 *  Convention for this stage
 *      3 dots  → 1 HA   (3 → 2, +1 carry)
 *      4 dots  → 1 HA   (4 → 3, +1 carry)  THEN
 *                 1 FA   (3 → 1, +1 carry)      — keeps us safely ≤ 2
 *      5 dots  → 2 FA   (5 → 1, +2 carries)     — minimises local height fast
 *
 *  The RCA that follows will swallow up to two dots per column, so we stop
 *  compressing as soon as each column holds 1 or 2 dots.
 *
 * -------------------------------------------------------------------------
 *  COLUMN-BY-COLUMN WORK   (left-to-right, LSB first)
 * -------------------------------------------------------------------------
 *
 *  Column 0: 1 dot                                 – no action
 *
 *  Column 1: 2 dots                                – no action
 *
 *  Column 2: 3 dots  → 2 dots       (1 HA)
 *      • HA: take 2 dots ⇒ 1 sum left in col 2,
 *             1 carry → col 3
 *      → Result col 2: **2 dots**, 1 carry propagated
 *
 *  Column 3: 3 dots + 1 carry = 4 dots  (1 FA)
 *      • FA: take 2 dots + the carry ⇒ 1 sum in col 3, 1 carry → col 4   (4 → 2)
 *      → Result col 3: **2 dot**, 1 carries → col 4
 *
 *  Column 4: 3 dots + 1 carries = 4 dots  (1 FA)
 *      • FA#1: 3 dots ⇒ 1 sum, 1 carry → col 5   (4 → 2)
 *      → Result col 4: **2 dot**, 1 carries → col 5
 *
 *  Column 5: 3 dots + 1 carry = 4 dots  (1 FA)
 *      • FA: take 3 dots + 1 carry ⇒ 1 sum left in col 5,
 *             1 carry → col 6
 *      → Result col 5: **2 dots**
 *
 *  Column 6: 3 dots + 1 carry = 4 dots  (1 FA)
 *      • FA: take 3 dots + 1 carry ⇒ 1 sum left in col 6,
 *             1 carry → col 7
 *      → Result col 6: **2 dots**
 *
 *  Column 7: 3 dots + 1 carry = 4 dots  (1 FA)
 *      • FA: take 3 dots + 1 carry ⇒ 1 sum left in col 7,
 *             1 carry → col 8
 *      → Result col 7: **2 dots**
 *
 *  Column 8: 3 dots + 1 carry = 4 dots  (1 FA)
 *      • FA: take 3 dots + 1 carry ⇒ 1 sum left in col 8,
 *             1 carry → col 9
 *      → Result col 8: **2 dots**
 *
 *  Column 9: 3 dots + 1 carry = 4 dots  (1 FA)
 *      • FA: take 3 dots + 1 carry ⇒ 1 sum left in col 9,
 *             1 carry → col 10
 *      → Result col 9: **2 dots**
 *
 *  Column 10: 3 dots + 1 carry = 4 dots  (1 FA)
 *      • FA: take 3 dots + 1 carry ⇒ 1 sum left in col 10,
 *             1 carry → col 11
 *      → Result col 10: **2 dots**
 *
 *  Column 11: 3 dots + 1 carry = 4 dots  (1 FA)
 *      • FA: take 3 dots + 1 carry ⇒ 1 sum left in col 11,
 *             1 carry → col 12
 *      → Result col 11: **2 dots**
 *
 *  Column 12: 3 dots + 1 carry = 4 dots  (1 FA)
 *      • FA: take 3 dots + 1 carry ⇒ 1 sum left in col 12,
 *             1 carry → col 13
 *      → Result col 12: **2 dots**
 *
 *  Column 13: 3 dots + 1 carry = 4 dots  (1 FA)
 *      • FA: take 3 dots + 1 carry ⇒ 1 sum left in col 13,
 *             1 carry → col 14
 *      → Result col 13: **2 dots**
 *
 *  Column 14: 3 dots + 1 carry = 4 dots  (1 FA)
 *      • FA: take 3 dots + 1 carry ⇒ 1 sum left in col 14,
 *             1 carry → col 15
 *      → Result col 14: **2 dots**
 *
 *  Column 15: 3 dots + 1 carry = 4 dots  (1 FA)
 *      • FA: take 3 dots + 1 carry ⇒ 1 sum left in col 15,
 *             1 carry → col 16
 *      → Result col 15: **2 dots**
 *
 *  Column 16: 3 dots + 1 carry = 4 dots  (1 FA)
 *      • FA: take 3 dots + 1 carry ⇒ 1 sum left in col 16,
 *             1 carry → col 17
 *      → Result col 16: **2 dots**
 *
 *  Column 17: 3 dots + 1 carry = 4 dots  (1 FA)
 *      • FA: take 3 dots + 1 carry ⇒ 1 sum left in col 17,
 *             1 carry → col 18
 *      → Result col 17: **2 dots**
 *
 *  Column 18: 3 dots + 1 carry = 4 dots  (1 FA)
 *      • FA: take 3 dots + 1 carry ⇒ 1 sum left in col 18,
 *             1 carry → col 19
 *      → Result col 18: **2 dots**
 *
 *  Column 19: 3 dots + 1 carry = 4 dots  (1 FA)
 *      • FA: take 3 dots + 1 carry ⇒ 1 sum left in col 19,
 *             1 carry → col 20
 *      → Result col 19: **2 dots**
 *
 *  Column 20: 1 dot + 1 carry = 2 dots  
 *      → Result col 20: **2 dots**
 *
 *  Column 21 (new): 0 dots + 0 carries = 0 dot        – no action
 *
 * -------------------------------------------------------------------------
 *  STAGE-5  OPERATION  TALLY
 *      Column 2  : 1 HA
 *      Columns 3-19 : 17 FA  
 *  ------------------------------------------------
 *      **Total:** 17 FA, 1 HA
 *
 *  All columns now contain ≤ 2 dots.  These two rows (the “sum” and
 *  “carry” rows) feed directly into the final ripple-carry adder, which
 *  produces the 22-bit product P[21:0].
 */

### Aggregate adder count per column

*(summing all five “logical” stages — what finally gets instantiated in hardware)*

| Column (weight 2^k) | Full-adders (FA) | Half-adders (HA) |
| ------------------- | ---------------- | ---------------- |
| 0                   | 0                | 0                |
| 1                   | 0                | 0                |
| 2                   | 0                | 1                |
| 3                   | 1                | 1                |
| 4                   | 2                | 1                |
| 5                   | 3                | 1                |
| 6                   | 4                | 1                |
| 7                   | 5                | 1                |
| 8                   | 6                | 1                |
| 9                   | 7                | 1                |
| 10                  | 8                | 1                |
| 11                  | 8                | 1                |
| 12                  | 8                | 0                |
| 13                  | 7                | 0                |
| 14                  | 6                | 0                |
| 15                  | 5                | 0                |
| 16                  | 4                | 0                |
| 17                  | 3                | 0                |
| 18                  | 2                | 0                |
| 19                  | 1                | 0                |
| 20                  | 0                | 0                |


 
---

* Columns are accessed in the netlist as `output[k][0]` (sum row) and `output[k][1]` (carry row); after these compressors the 22-bit ripple-carry adder simply adds those two rows to produce the final product `P[21:0]`.

This is the actual gate budget the physical Dadda tree will instantiate — the “stages” above were only a design-time way to keep every column under the prescribed height limits (9, 6, 4, 3, 2).

(IMPORTANT) ***Final Product***:
cols0-21 (or 20 idk) are actually accessed via: output[i][0], output[i][1] throughout this process.

apply Final Ripple Carry Adder to output --> 22bit output product.


 

"""

def bitMul11(a_bits, b_bits):
    """
    11×11 unsigned multiplier
    • inputs : a_bits[0..10], b_bits[0..10]  (LSB-first, bools)
    • output : product[0..21]               (LSB-first, bools)
    """
    n = 11
    cols = [[] for _ in range(2*n)]          # bucket dots by weight

    # --- 1. partial products ------------------------------------------------
    for i in range(n):
        if not a_bits[i]:
            continue                         # skip zero rows early
        for j in range(n):
            if b_bits[j]:
                cols[i+j].append(True)       # only keep ‘1’ dots

    # --- 2. Dadda-style compression to 2 rows ------------------------------
    sums  = [False]*(2*n)
    carys = [False]*(2*n)

    for k in range(2*n):
        while len(cols[k]) > 2:              # keep height ≤ 2
            s, c = FA(cols[k].pop(),
                      cols[k].pop(),
                      cols[k].pop())
            cols[k].append(s)
            if k < 2*n-1:
                cols[k+1].append(c)
        if cols[k]:
            sums[k]  = cols[k].pop()
        if cols[k]:
            carys[k] = cols[k].pop()

    # --- 3. final ripple-carry adder ---------------------------------------
    product, cin = [False]*(2*n), False
    for k in range(2*n):
        product[k], cin = FA(sums[k], carys[k], cin)
    return product


def bitMul11Old(a,b):
    partialProducts = [[a[i] & b[j] for j in range(11)] for i in range(11)]
    sum2Column = [[False, False] for _ in range(22)]
    #print(partialProducts)
    #column 0
    sum2Column[0][0] = partialProducts[0][0]

    #column 1
    sum2Column[1][0] = partialProducts[0][1]
    sum2Column[1][1] = partialProducts[1][0]

    #column 2 - 0 FA, 1 HA
    sum_2_0, cout_2_0 = HA(partialProducts[0][2], partialProducts[1][1])  
    sum2Column[2][0] = sum_2_0
    sum2Column[2][1] = partialProducts[2][0]
    carry_2_0 = cout_2_0  # carry to col3

    #column 3 - 1 FA, 1 HA
    sum_3_0, cout_3_0 = HA(partialProducts[0][3], partialProducts[2][1]) 
    sum_3_1, cout_3_1 = FA(partialProducts[1][2], partialProducts[3][0], carry_2_0)
    sum2Column[3][0] = sum_3_0
    sum2Column[3][1] = sum_3_1
    carry_3_0 = cout_3_0
    carry_3_1 = cout_3_1

    #column 4 - 2 FA, 1 HA
    sum_4_0, cout_4_0 = HA(partialProducts[0][4], partialProducts[4][0]) 
    sum_4_1, cout_4_1 = FA(partialProducts[3][1], partialProducts[1][3], carry_3_0)
    sum_4_2, cout_4_2 = FA(sum_4_0, partialProducts[2][2], carry_3_1)
    sum2Column[4][0] = sum_4_1
    sum2Column[4][1] = sum_4_2
    carry_4_0 = cout_4_0
    carry_4_1 = cout_4_1
    carry_4_2 = cout_4_2

    #column 5 - 3 FA, 1 HA (6 initial dots + carries)
    sum_5_0, cout_5_0 = HA(partialProducts[0][5], partialProducts[5][0])
    sum_5_1, cout_5_1 = FA(partialProducts[1][4], partialProducts[4][1], carry_4_0)
    sum_5_2, cout_5_2 = FA(partialProducts[2][3], partialProducts[3][2], carry_4_1)
    sum_5_3, cout_5_3 = FA(sum_5_0, sum_5_1, carry_4_2)
    sum2Column[5][0] = sum_5_3
    sum2Column[5][1] = sum_5_2
    carry_5_0 = cout_5_0
    carry_5_1 = cout_5_1
    carry_5_2 = cout_5_2
    carry_5_3 = cout_5_3

    #column 6 - 4 FA, 1 HA (7 initial dots + carries)
    sum_6_0, cout_6_0 = HA(partialProducts[0][6], partialProducts[6][0])
    sum_6_1, cout_6_1 = FA(partialProducts[1][5], partialProducts[5][1], carry_5_0)
    sum_6_2, cout_6_2 = FA(partialProducts[2][4], partialProducts[4][2], carry_5_1)
    sum_6_3, cout_6_3 = FA(partialProducts[3][3], sum_6_0, carry_5_2)
    sum_6_4, cout_6_4 = FA(sum_6_1, sum_6_2, carry_5_3)
    sum2Column[6][0] = sum_6_4
    sum2Column[6][1] = sum_6_3
    carry_6_0 = cout_6_0
    carry_6_1 = cout_6_1
    carry_6_2 = cout_6_2
    carry_6_3 = cout_6_3
    carry_6_4 = cout_6_4

    #column 7 - 5 FA, 1 HA (8 initial dots + carries)
    sum_7_0, cout_7_0 = HA(partialProducts[0][7], partialProducts[7][0])
    sum_7_1, cout_7_1 = FA(partialProducts[1][6], partialProducts[6][1], carry_6_0)
    sum_7_2, cout_7_2 = FA(partialProducts[2][5], partialProducts[5][2], carry_6_1)
    sum_7_3, cout_7_3 = FA(partialProducts[3][4], partialProducts[4][3], carry_6_2)
    sum_7_4, cout_7_4 = FA(sum_7_0, sum_7_1, carry_6_3)
    sum_7_5, cout_7_5 = FA(sum_7_2, sum_7_3, carry_6_4)
    sum2Column[7][0] = sum_7_5
    sum2Column[7][1] = sum_7_4
    carry_7_0 = cout_7_0
    carry_7_1 = cout_7_1
    carry_7_2 = cout_7_2
    carry_7_3 = cout_7_3
    carry_7_4 = cout_7_4
    carry_7_5 = cout_7_5

    #column 8 - 6 FA, 1 HA (9 initial dots + carries)
    sum_8_0, cout_8_0 = HA(partialProducts[0][8], partialProducts[8][0])
    sum_8_1, cout_8_1 = FA(partialProducts[1][7], partialProducts[7][1], carry_7_0)
    sum_8_2, cout_8_2 = FA(partialProducts[2][6], partialProducts[6][2], carry_7_1)
    sum_8_3, cout_8_3 = FA(partialProducts[3][5], partialProducts[5][3], carry_7_2)
    sum_8_4, cout_8_4 = FA(partialProducts[4][4], sum_8_0, carry_7_3)
    sum_8_5, cout_8_5 = FA(sum_8_1, sum_8_2, carry_7_4)
    sum_8_6, cout_8_6 = FA(sum_8_3, sum_8_4, carry_7_5)
    sum2Column[8][0] = sum_8_6
    sum2Column[8][1] = sum_8_5
    carry_8_0 = cout_8_0
    carry_8_1 = cout_8_1
    carry_8_2 = cout_8_2
    carry_8_3 = cout_8_3
    carry_8_4 = cout_8_4
    carry_8_5 = cout_8_5
    carry_8_6 = cout_8_6

    #column 9 - 7 FA, 1 HA (10 initial dots + carries)
    sum_9_0, cout_9_0 = HA(partialProducts[0][9], partialProducts[9][0])
    sum_9_1, cout_9_1 = FA(partialProducts[1][8], partialProducts[8][1], carry_8_0)
    sum_9_2, cout_9_2 = FA(partialProducts[2][7], partialProducts[7][2], carry_8_1)
    sum_9_3, cout_9_3 = FA(partialProducts[3][6], partialProducts[6][3], carry_8_2)
    sum_9_4, cout_9_4 = FA(partialProducts[4][5], partialProducts[5][4], carry_8_3)
    sum_9_5, cout_9_5 = FA(sum_9_0, sum_9_1, carry_8_4)
    sum_9_6, cout_9_6 = FA(sum_9_2, sum_9_3, carry_8_5)
    sum_9_7, cout_9_7 = FA(sum_9_4, sum_9_5, carry_8_6)
    sum2Column[9][0] = sum_9_7
    sum2Column[9][1] = sum_9_6
    carry_9_0 = cout_9_0
    carry_9_1 = cout_9_1
    carry_9_2 = cout_9_2
    carry_9_3 = cout_9_3
    carry_9_4 = cout_9_4
    carry_9_5 = cout_9_5
    carry_9_6 = cout_9_6
    carry_9_7 = cout_9_7

    #column 10 - 8 FA, 1 HA (11 initial dots + carries)
    sum_10_0, cout_10_0 = HA(partialProducts[0][10], partialProducts[10][0])
    sum_10_1, cout_10_1 = FA(partialProducts[1][9], partialProducts[9][1], carry_9_0)
    sum_10_2, cout_10_2 = FA(partialProducts[2][8], partialProducts[8][2], carry_9_1)
    sum_10_3, cout_10_3 = FA(partialProducts[3][7], partialProducts[7][3], carry_9_2)
    sum_10_4, cout_10_4 = FA(partialProducts[4][6], partialProducts[6][4], carry_9_3)
    sum_10_5, cout_10_5 = FA(partialProducts[5][5], sum_10_0, carry_9_4)
    sum_10_6, cout_10_6 = FA(sum_10_1, sum_10_2, carry_9_5)
    sum_10_7, cout_10_7 = FA(sum_10_3, sum_10_4, carry_9_6)
    sum_10_8, cout_10_8 = FA(sum_10_5, sum_10_6, carry_9_7)
    sum2Column[10][0] = sum_10_8
    sum2Column[10][1] = sum_10_7
    carry_10_0 = cout_10_0
    carry_10_1 = cout_10_1
    carry_10_2 = cout_10_2
    carry_10_3 = cout_10_3
    carry_10_4 = cout_10_4
    carry_10_5 = cout_10_5
    carry_10_6 = cout_10_6
    carry_10_7 = cout_10_7
    carry_10_8 = cout_10_8

    #column 11 - 8 FA, 1 HA (10 initial dots + carries from col 10)
    #there clearly needs to be prev_column_carries+1 
    sum_11_0, cout_11_0 = FA(partialProducts[1][10], partialProducts[10][1], carry_10_0)
    sum_11_1, cout_11_1 = FA(partialProducts[2][9], partialProducts[9][2], carry_10_1)
    sum_11_2, cout_11_2 = FA(partialProducts[3][8], partialProducts[8][3], carry_10_2)
    sum_11_3, cout_11_3 = FA(partialProducts[4][7], partialProducts[7][4], carry_10_3)
    sum_11_4, cout_11_4 = FA(partialProducts[5][6], partialProducts[6][5], carry_10_4)
    sum_11_5, cout_11_5 = FA(carry_10_5, carry_10_6, carry_10_7)
    sum_11_6, cout_11_6 = FA(carry_10_8, sum_11_2, sum_11_3)
    sum_11_7, cout_11_7 = FA(sum_11_0, sum_11_1, sum_11_4)
    sum_11_8, cout_11_8 = HA(sum_11_5, sum_11_6)
    sum2Column[11][0] = sum_11_8
    sum2Column[11][1] = sum_11_7
    carry_11_0 = cout_11_0
    carry_11_1 = cout_11_1
    carry_11_2 = cout_11_2
    carry_11_3 = cout_11_3
    carry_11_4 = cout_11_4
    carry_11_5 = cout_11_5
    carry_11_6 = cout_11_6
    carry_11_7 = cout_11_7
    carry_11_8 = cout_11_8 

    #column 12 - 8 FA, 0 HA (9 initial dots + carries)
    sum_12_0, cout_12_0 = FA(partialProducts[2][10], partialProducts[10][2], carry_11_0)
    sum_12_1, cout_12_1 = FA(partialProducts[3][9], partialProducts[9][3], carry_11_1)
    sum_12_2, cout_12_2 = FA(partialProducts[4][8], partialProducts[8][4], carry_11_2)
    sum_12_3, cout_12_3 = FA(partialProducts[5][7], partialProducts[7][5], carry_11_3)
    sum_12_4, cout_12_4 = FA(partialProducts[6][6], sum_12_0, carry_11_4)
    sum_12_5, cout_12_5 = FA(carry_11_5, carry_11_6, carry_11_7)
    sum_12_6, cout_12_6 = FA(carry_11_8, sum_12_1, sum_12_2)
    sum_12_7, cout_12_7 = FA(sum_12_3, sum_12_4, sum_12_5)
    sum2Column[12][0] = sum_12_6
    sum2Column[12][1] = sum_12_7
    carry_12_0 = cout_12_0
    carry_12_1 = cout_12_1
    carry_12_2 = cout_12_2
    carry_12_3 = cout_12_3
    carry_12_4 = cout_12_4
    carry_12_5 = cout_12_5
    carry_12_6 = cout_12_6
    carry_12_7 = cout_12_7

    #column 13 - 7 FA, 0 HA (8 initial dots + carries)
    sum_13_0, cout_13_0 = FA(partialProducts[3][10], partialProducts[10][3], carry_12_0)
    sum_13_1, cout_13_1 = FA(partialProducts[4][9], partialProducts[9][4], carry_12_1)
    sum_13_2, cout_13_2 = FA(partialProducts[5][8], partialProducts[8][5], carry_12_2)
    sum_13_3, cout_13_3 = FA(partialProducts[6][7], partialProducts[7][6], carry_12_3)
    sum_13_4, cout_13_4 = FA(sum_13_0, sum_13_1, carry_12_4)
    sum_13_5, cout_13_5 = FA(sum_13_2, sum_13_3, carry_12_5)
    sum_13_6, cout_13_6 = FA(sum_13_4, carry_12_7, carry_12_6)
    sum2Column[13][0] = sum_13_5
    sum2Column[13][1] = sum_13_6 
    carry_13_0 = cout_13_0
    carry_13_1 = cout_13_1
    carry_13_2 = cout_13_2
    carry_13_3 = cout_13_3
    carry_13_4 = cout_13_4
    carry_13_5 = cout_13_5
    carry_13_6 = cout_13_6

    #column 14 - 6 FA, 0 HA (7 initial dots + carries)
    sum_14_0, cout_14_0 = FA(partialProducts[4][10], partialProducts[10][4], carry_13_0)
    sum_14_1, cout_14_1 = FA(partialProducts[5][9], partialProducts[9][5], carry_13_1)
    sum_14_2, cout_14_2 = FA(partialProducts[6][8], partialProducts[8][6], carry_13_2)
    sum_14_3, cout_14_3 = FA(partialProducts[7][7], sum_14_0, carry_13_3)
    sum_14_4, cout_14_4 = FA(sum_14_1, sum_14_2, carry_13_4)
    sum_14_5, cout_14_5 = FA(sum_14_3, carry_13_5, carry_13_6)
    sum2Column[14][0] = sum_14_4
    sum2Column[14][1] = sum_14_5 
    carry_14_0 = cout_14_0
    carry_14_1 = cout_14_1
    carry_14_2 = cout_14_2
    carry_14_3 = cout_14_3
    carry_14_4 = cout_14_4
    carry_14_5 = cout_14_5

    #column 15 - 5 FA, 0 HA (6 initial dots + carries)
    sum_15_0, cout_15_0 = FA(partialProducts[5][10], partialProducts[10][5], carry_14_0)
    sum_15_1, cout_15_1 = FA(partialProducts[6][9], partialProducts[9][6], carry_14_1)
    sum_15_2, cout_15_2 = FA(partialProducts[7][8], partialProducts[8][7], carry_14_2)
    sum_15_3, cout_15_3 = FA(sum_15_0, sum_15_1, carry_14_3)
    sum_15_4, cout_15_4 = FA(sum_15_2, carry_14_4, carry_14_5)
    sum2Column[15][0] = sum_15_3
    sum2Column[15][1] = sum_15_4
    carry_15_0 = cout_15_0
    carry_15_1 = cout_15_1
    carry_15_2 = cout_15_2
    carry_15_3 = cout_15_3
    carry_15_4 = cout_15_4

    #column 16 - 4 FA, 0 HA (5 initial dots + carries)
    sum_16_0, cout_16_0 = FA(partialProducts[6][10], partialProducts[10][6], carry_15_0)
    sum_16_1, cout_16_1 = FA(partialProducts[7][9], partialProducts[9][7], carry_15_1)
    sum_16_2, cout_16_2 = FA(partialProducts[8][8], sum_16_0, carry_15_2)
    sum_16_3, cout_16_3 = FA(sum_16_1, carry_15_4, carry_15_3)
    sum2Column[16][0] = sum_16_2
    sum2Column[16][1] = sum_16_3
    carry_16_0 = cout_16_0
    carry_16_1 = cout_16_1
    carry_16_2 = cout_16_2
    carry_16_3 = cout_16_3

    #column 17 - 3 FA, 0 HA (4 initial dots + carries)
    sum_17_0, cout_17_0 = FA(partialProducts[7][10], partialProducts[10][7], carry_16_0)
    sum_17_1, cout_17_1 = FA(partialProducts[8][9], partialProducts[9][8], carry_16_1)
    sum_17_2, cout_17_2 = FA(sum_17_0, carry_16_3, carry_16_2)
    sum2Column[17][0] = sum_17_1
    sum2Column[17][1] = sum_17_2
    carry_17_0 = cout_17_0
    carry_17_1 = cout_17_1
    carry_17_2 = cout_17_2

    #column 18 - 2 FA, 0 HA (3 initial dots + carries)
    sum_18_0, cout_18_0 = FA(partialProducts[8][10], partialProducts[10][8], carry_17_0)
    sum_18_1, cout_18_1 = FA(partialProducts[9][9], carry_17_2, carry_17_1)
    sum2Column[18][0] = sum_18_0
    sum2Column[18][1] = sum_18_1
    carry_18_0 = cout_18_0
    carry_18_1 = cout_18_1

    #column 19 - 1 FA, 0 HA (2 initial dots + carries)
    sum_19_0, cout_19_0 = FA(partialProducts[9][10], partialProducts[10][9], carry_18_0)
    sum2Column[19][0] = sum_19_0
    sum2Column[19][1] = carry_18_1
    carry_19_0 = cout_19_0

    #column 20 - 0 FA, 0 HA (1 initial dot + carry)
    sum2Column[20][0] = partialProducts[10][10]
    sum2Column[20][1] = carry_19_0

    #column 21 - just propagate final carry if any
    sum2Column[21][0] = False
    sum2Column[21][1] = False
    #for i in range(22):
        #print(f"first added vals: {sum2Column[i][0]}")
    #for i in range(22):
        #print(f"second added vals: {sum2Column[i][1]}")
    row0 = [sum2Column[i][0] for i in range(22)]
    row1 = [sum2Column[i][1] for i in range(22)]

    product = [False] * 22
    carry = False
    for i in range(22):
        product[i], carry = fullAdder(row0[i], row1[i], carry)
    print("product 22bit: ", product)
    return product

def bitFPMul16(a, b):
    signBit = a[15] ^ b[15]
    #a and b are 16bit floats
    #negate. We use -15? [True,False,False,False,True] (msb is last array index)
    bitNeg15 = [True,False,False,False,True] 
    bitPos15 = [True,True,True,True,False]
    print(f"a: {a}")
    print(f"b: {b}")
    print(f"bitNeg15: {bitNeg15}")
    print(f"bitPos15: {bitPos15}")
    # invertedB = ~(b[10:15])
    # print("invertedB:", invertedB)
    unbiasedA,cout_a = bitAdd5(a[10:15],bitNeg15,False) #carryin for adder matters in both these cases, its how we differentiate
    unbiasedB,cout_b = bitAdd5(b[10:15],bitNeg15,False)
    inverted_unbiasedB = [not bit for bit in unbiasedB] #turns 11011 (-5) into 00100 
    #print("unbiasedA",unbiasedA,"unbiasedB",unbiasedB,"inverted_unbiasedB",inverted_unbiasedB)
    #(with carry-->00101), that is, positive 5
    interimA, carry_out1 = bitAdd5(unbiasedA,unbiasedB,False)#subtract b from a
    #outExp, carry_out2 = bitAdd5(interimA,bitNeg15,True)#subtract 15 from b --> unbiased exponent
    #print(f"interimA: {interimA}")
    #print(f"outExp after subtracting 15: {outExp}")
    
    # outExp, carry_outexp2 = bitAdd5(outExp,bitPos15,False)#add 15 to bias the exponent

    #print("a[0:10]+[True]:",a[0:10]+[True])
    #multiply the 10bit mantissas (actually 11bit via implicit 1s) to get 22bit product
    bit22Mantissa = bitMul11(a[0:10]+[True],b[0:10]+[True]) #adding implicit leading 1s
    print(f"bit22Mantissa: {bit22Mantissa}")
    shifted22Mantissa = bit22Mantissa
    #handle shift logic
    if(bit22Mantissa[21] == True):
        #shift right
        shifted22Mantissa = bit22Mantissa[1:] + [False]
        interimA, carry_out2 = bitAdd5(interimA,[True,False,False,False,False],False)
        print("final interimA (it needed to be incremented by 1, before biasing):",interimA)
    else:
        pass
    print("final shifted22Mantissa:",shifted22Mantissa)
    biasedExp,cout = bitAdd5(interimA,bitPos15,False)
    print("biasedExp:",biasedExp)
    #last 2 msbs left out, the 2nd to last would be the implicit 1
    out = shifted22Mantissa[10:20]+biasedExp+ [signBit]  
    
    return out
    #specific 
    #multiplication

# def bitFPAdd16(a, b):




# def bitFPDiv16(a, b):




#     #normalization:
#     #GRS
#     #roundup = G & (output[lsb] | R | S) 




# # #32bit shifter
# def bitShifter32():

# def bitAND32(a, b):

# def bitOR32(a, b):

# def bitXOR32(a, b):

# def bitNOT32(a):

def convertToDecimalOnlyPositiveUnsigned(r):
    final = 0
    lengthM1 = len(r)
    for i in range(lengthM1):
        final += r[i] * (2 ** i)
        # print(f"i: {i}, final: {final}")
    return final

def convertToDecimal(r):
    final = 0
    lengthM1 = BIT_SIZE-1
    for i in range(lengthM1):
        final += r[i] * (2 ** i)
        # print(f"i: {i}, final: {final}")
    if r[lengthM1] == True:
        final -= 2 ** lengthM1
    return final

def convertFloatBinaryToDecimal(a): 
    bitNeg15 = [True,False,False,False,True]    
    unbiasedExp,cout = bitAdd5(a[10:15],bitNeg15,False)
    print("unbiasedExp:",unbiasedExp)
    b=unbiasedExp

    mantissaFrac = 0
    for j in range(0, 10):
        currentBit = 1 if a[j] else 0
        mantissaFrac += currentBit * 2 ** (j - 10)
    print("mantissaFrac:",mantissaFrac)
    mantissaFrac+=1
    expsum = 0
    for i in range(10, 15):
        currentBit = 1 if b[i-10] else 0
        #print(f"i: {i}, currentBit: {currentBit}")
        if i == 14:
            expsum += -16
        else:
            expsum += currentBit * 2 ** (i - 10)
        #print(f"i: {i}, expsum: {expsum}")
    print("expsum:",expsum)
    sign = -1 if a[15] else 1
    return mantissaFrac * 2**expsum * sign

def convert_bool_to_binary(bool_list):
    # Convert list of bools to list of 0s and 1s
    return [1 if value else 0 for value in bool_list]

# def convert_decimal_to_binary(decimal):
#     for i in range(32):

#just plain arr-->string
def convertToString(r):
    final = ""
    for i in range(len(r)):
        final += str(r[i])
    return final
#reverses array
def reverseArray(r):
    new_arr = []
    for i in reversed(range(len(r))):
        new_arr.append(r[i])
    return new_arr



def testTwoNums():
    
    # 11-bit value: alternating False/True
    # multt1 = [False]*3 + [True]*6 + [False]*2 #504
    # multt2 = [False]*3 + [True]*6 + [False]*2 #504
    multt1 = [False]*3 + [True]*4 + [False]*4 #8+16+32+64=120
    multt2 = [False]*5 + [True]*1 + [False]*5 #32

    # 16-bit value: 
    # Let's pick two random numbers between 0 and 65000 for demonstration
    # For example: 32745 and 49218

    # Helper to convert integer to 16-bit LSB-first boolean list
    def int_to_bool_list(n, bits=16):
        return [(n >> i) & 1 == 1 for i in range(bits)]

    multt3_val = 325
    multt4_val = 48
    multt3 = int_to_bool_list(multt3_val)
    multt4 = int_to_bool_list(multt4_val)
    print(f"multt3: {multt3}")
    print(f"multt4: {multt4}")
    #960*64=61440
    print(f"multt1 (decimal): {convertToDecimalOnlyPositiveUnsigned(convert_bool_to_binary(multt1))}")
    print(f"multt2 (decimal): {convertToDecimalOnlyPositiveUnsigned(convert_bool_to_binary(multt2))}")
    #calculate2
    result_mult = bitMul11(multt1, multt2)
    print(f"result_mult: {result_mult}")
    print(f"Binary product: {convertToDecimalOnlyPositiveUnsigned(convert_bool_to_binary(result_mult))}")
    print(f"bool to binary: {convert_bool_to_binary(result_mult)}")
    print(f"Human readable product: {convertToString(reverseArray(convert_bool_to_binary(result_mult)))}")
    
    result_mult2 = bitMul16(multt3, multt4)
    print(f"result_mult2: {result_mult2}")
    print(f"Binary product: {convertToDecimal(convert_bool_to_binary(result_mult2))}")
    print(f"bool to binary: {convert_bool_to_binary(result_mult2)}")
    print(f"Human readable product: {convertToString(reverseArray(convert_bool_to_binary(result_mult2)))}")
    
    # #floatingpoint
    # # fpa represents 12.0546875
    # fpa = [
    #     False,                   # sign bit = 0 → positive
    #     True, False, False,     # exponent bits [1,0,0]
    #     True, False,              #             [1,0] → unbiased exponent = 18 - bias = 3
    #     # implicit leading-1 + mantissa bits:
    #     True, False, False, False, False, False, False, True, True, True
    #     # mantissa (binary): 1.1000000111
    # ]
    # # this value = 1.1000000111 (binary) × 2³ = 1.53125 × 8 = 12.0546875


    # fpb represents 
    fpb = [
                           
        
        # implicit leading-1 + mantissa bits:
        # mantissa (binary): 1.1010000101 
        True, False, True, False, False, False, False, True, False, True,
        # exponent bits [1,0,1,1,1] (here its written in reverse, first element of array is lsb)
        #  → unbiased exponent = 15 − bias=0
        True, True, True, True, False, #exponent, stored as biased
        False # sign bit = 0 → positive
        
    ]
    # this value = 1.1010000101 (binary) × 2^0 = 1.6298828125 × 2^0 = 1.6298828125
    
    #'temporarily changing it to be smaller:
    #fpc represents...
    fpc = [
        # mantissa (binary): 1.1010100000
        
        
        
        # implicit leading-1 + mantissa bits:
        False, False, False, False, False, True, False, True, False, True,
        False, True, False, True, False, ## exponent bits [0,1,0,1,0] → 
        #biased exponent = 10 → unbiased = -5
        False, # sign bit = 0 → positive
        
    ]
    # this value = 1.1010100000 (binary) × 2^-5 = 1.65625 × 0.03125 = 0.05175781...
        
    result_fp = bitFPMul16(fpb, fpc)
    print(f"result_fp: {result_fp}")
    #print(f"Binary product: {convertToFloatingPoint(convert_bool_to_binary(result_fp))}")
    print(f"bool to binary: {convert_bool_to_binary(result_fp)}")
    print(f"Human readable product: {convertToString(reverseArray(convert_bool_to_binary(result_fp)))}")
    print(f"Decimal product: {convertFloatBinaryToDecimal(result_fp)}")

    #32-bit value: alternating False/True
    subtract1 = [True]*32 #-1
    subtract2 = [True]*1+[False]*28+[True]*3 #1
    print(f"subtract1 (decimal): {convertToDecimal(convert_bool_to_binary(subtract1))}")
    print(f"subtract2 (decimal): {convertToDecimal(convert_bool_to_binary(subtract2))}")
    #lets try subtracting 
    subtracted, cout = bitSub32(subtract1, subtract2)
    print("subtracted:", subtracted,"subtracted length:", len(subtracted))
    print(f"subtraction: {convertToDecimal(convert_bool_to_binary(subtracted))}")
    num1 = [False, True] * 15 + [False, False] # 32 bits: [F, T, F, T, ..., F, T]
    # 32-bit value: pattern of two True, two False
    num2 = ([True, True, False, False] * 8)  # 32 bits: [T, T, F, F, ..., T, T, F, F]
    #the four horsemen of readibility (decimal and binary)
    print(f"num1 (decimal): {convertToDecimal(convert_bool_to_binary(num1))}")
    print(f"num1: {convertToString(reverseArray(convert_bool_to_binary(num1)))}")
    print(f"num2 (decimal): {convertToDecimal(convert_bool_to_binary(num2))}")
    print(f"num2: {convertToString(reverseArray(convert_bool_to_binary(num2)))}")
    #calculate
    result_sum, carry_out = bitAdd32(num1, num2, False)
    #output
    print(f"Binary sum: {convertToDecimal(convert_bool_to_binary(result_sum))}, Carry out: {carry_out}")
    print(f"Human readable sum: {convertToString(reverseArray(convert_bool_to_binary(result_sum)))}")
    return result_sum

def testTwoEnteredNums():
    test = input("wanna try your own (skip if no, y if yes)")
    if test == 'y':
        num1 = input("enter first 32 bit number in decimal")
        num2 = input("enter second 32 bit number in decimal")
        result_sum, carry_out = bitAdd32(num1, num2, False)
        print(f"Binary sum: {convertToDecimal(convert_bool_to_binary(result_sum))}, Carry out: {carry_out}")
        print(f"Human readable sum: {convertToString(reverseArray(convert_bool_to_binary(result_sum)))}")

result_sum = testTwoNums()

print(list(reversed(range(len(result_sum)))))

#RAM32K = [False] * 32768


# # To create an integer array of a specific byte size in Python, you can use the 'array' module.
# # For example, to create an array of 32 bytes (8 integers of 4 bytes each, using 'i' for signed int):

# import array

# def int_array_of_byte_size(byte_size, int_type='i'):
#     """
#     Create an integer array of a specific byte size.
#     Args:
#         byte_size: Total size in bytes for the array.
#         int_type: Type code for the array module ('i' for signed int, 'I' for unsigned int, etc.)
#     Returns:
#         An array of the specified integer type and size.
#     """
#     int_size = array.array(int_type).itemsize
#     num_ints = byte_size // int_size
#     return array.array(int_type, [0] * num_ints)
# # No, an array of 8 Falses (e.g., [False, False, ..., False]) is not stored as a single byte in Python.
# # In Python, a list of booleans is an object with significant overhead—each boolean is a full Python object.
# # If you want to store 8 bits efficiently (as a single byte), use the 'bytes' type or the 'bitarray' module (external), or 'int' for bit manipulation.
# # Example of storing 8 bits in a single byte:
# byte_val = 0b00000000  # 8 bits, all zero (False)
# # To set the 3rd bit to True:
# # 1 << 2 means "bit-shift the number 1 left by 2 places", which gives 0b00000100 (decimal 4).
# # So, (1 << 2) is 4. This is a common way to set or check a specific bit in a byte or integer.
# byte_val |= (1 << 2)  # Sets the 3rd bit (counting from the right, 0-based) to 1 (True)
# # To check if the 3rd bit is set:
# third_bit = bool(byte_val & (1 << 2))
# # For efficient bit storage, consider using 'array' with type 'B' (unsigned char), or 'bytearray', or bit manipulation with integers.

# # Immediate action: If you want to store 8 booleans as a single byte:
# def bools_to_byte(bools):
#     """Convert list of 8 booleans to a single byte (int 0-255)."""
#     return sum((1 << i) if b else 0 for i, b in enumerate(reversed(bools)))

# def byte_to_bools(byte):
#     """Convert a single byte (int 0-255) to list of 8 booleans."""
#     return [bool((byte >> i) & 1) for i in reversed(range(8))]

# # Example usage:
# # packed = bools_to_byte([False]*8)  # packed == 0
# # unpacked = byte_to_bools(5)        # unpacked == [False, False, False, False, True, False, True, True]


# # Example usage:
# # arr = int_array_of_byte_size(32)  # Creates an array of 8 signed integers (4 bytes each)




