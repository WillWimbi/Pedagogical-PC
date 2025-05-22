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



# # #32bit divider
# def bitDiv32(a, b):



def bitAdd16(a, b, c_in):
    s = [False] * 16
    c = [False] * (16+1)
    c[0] = c_in
    for i in range(16):
        s[i], c[i + 1] = fullAdder(a[i], b[i], c[i])
    return s, c[16]

def bitAdd5(a, b, c_in):
    s = [False] * 5
    c = [False] * (5+1)
    c[0] = c_in
    for i in range(5):
        s[i], c[i + 1] = fullAdder(a[i], b[i], c[i])
    return s, c[5]

# def bitFPAdd32(a, b):

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



# fpa represents 12.0546875
fpa = [
    False,                   # sign bit = 0 → positive
    True, False, False,     # exponent bits [1,0,0]
    True, False,              #             [1,0] → unbiased exponent = 18 - bias = 3
    # implicit leading-1 + mantissa bits:
    True, False, False, False, False, False, False, True, True, True
    # mantissa (binary): 1.1000000111
]
# this value = 1.1000000111 (binary) × 2³ = 1.53125 × 8 = 12.0546875


# fpb represents 417.25
fpb = [
    False,                   # sign bit = 0 → positive
    True, False, True, True, True,
    # exponent bits [1,0,1,1,1] → unbiased exponent = 23 − bias=8
    # implicit leading-1 + mantissa bits:
    True, False, True, False, False, False, False, True, False, True
    # mantissa (binary): 1.1010000101
]
# this value = 1.1010000101 (binary) × 2⁸ = 1.6298828125 × 256 = 417.25


def bitFPMul16(a, b):
    #a and b are 16bit floats
    partialProducts = [[False for _ in range(10)] for _ in range(10)]
    #negate. We use -15? [True,False,False,False,True] (msb is last array index)
    bitNeg15 = [True,False,False,False,True]
    interimA = bitAdd5(a,bitNeg15,True)
    interimB = bitAdd5(b,bitNeg15,True)
    outB = bitAdd5(interimA,interimB,False)

    #multiply the 10bit mantissas (actually 11bit via implicit 1s) to get 22bit product
    bit22Mantissa = bitMul11(a[5:],b[5:])

    return outB
    #specific 
    #multiplication


###################################################
# DADDA MULTIPLIER FOR 11×11 BITS
# "SIMPLE, MANUAL WAY" EXACTLY IN YOUR STYLE
# 
# We implement all 22 columns of partial-product 
# combination, using only halfAdder(...) and 
# fullAdder(...). Each column is handled by 
# enumerating the bits and leftover carries, 
# storing results in sum2Column[col][0..1].
# 
# This matches the 5-stage Dadda plan from your 
# massive comment, but unrolled line by line.
# 
# Because we do so many columns, the code is long. 
# Please note: We keep the same variable naming 
# style you started: sumX, coutX, etc. 
# 
# After bitMul11(a,b) finishes, you have 
# sum2Column[22], each = [bit0, bit1], 
# which you feed into a 22-bit ripple-carry adder 
# for the final product.
###################################################


def myBitMul11(a,b):
    partialProducts = [[a[j] & b[i] for j in range(11)] for i in range(11)]
    sum2Column = [[False, False] for _ in range(22)]
    #column 0
    sum2Column[0][0] = partialProducts[0][0]

    #column 1
    sum2Column[1][0] = partialProducts[0][1]
    sum2Column[1][1] = partialProducts[1][0]

    #column 2
    sum_2_0, cout_2_0 = HA(partialProducts[0][2], partialProducts[1][1])  
    sum2Column[2][0] = sum_2_0
    sum2Column[2][1] = partialProducts[2][0]
    carry_2_0 = cout_2_0  # carry to col3

    #column 3
    sum2Column[3][0], cout_3_0 = HA(partialProducts[0][3], partialProducts[2][1]) 
    sum2Column[3][1], cout_3_1 = FA(partialProducts[1][2], partialProducts[3][0], carry_2_0)
    carry_3_0 = cout_3_0
    carry_3_1 = cout_3_1

    #column 4
    sum_4_0, cout_4_0 = HA(partialProducts[0][4], partialProducts[4][0]) 
    sum2Column[4][0], cout_4_1 = FA(partialProducts[3][1], partialProducts[1][3], carry_3_0)
    sum2Column[4][1], cout_4_2 = FA(sum_4_0, partialProducts[2][2], carry_3_1)

    #column 5

def halfAdder(a, b):
    s = a ^ b
    cout = a & b
    return s, cout

def fullAdder(a, b, cin):
    x1 = a ^ b
    s  = x1 ^ cin
    a1 = a & b
    a2 = cin & x1
    cout = a1 | a2
    return s, cout



# def bitFPDiv32(a, b):

# # #32bit shifter
# def bitShifter32():

# def bitAND32(a, b):

# def bitOR32(a, b):

# def bitXOR32(a, b):

# def bitNOT32(a):

def convertToDecimal11(r):
    final = 0
    lengthM1 = 11
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
    multt1 = [False]*3 + [True]*6 + [False]*2 #504
    multt2 = [False]*3 + [True]*6 + [False]*2 #504
    print(f"multt1 (decimal): {convertToDecimal11(convert_bool_to_binary(multt1))}")
    print(f"multt2 (decimal): {convertToDecimal11(convert_bool_to_binary(multt2))}")
    #calculate
    result_mult = bitMul11(multt1, multt2)
    print(f"Binary product: {convertToDecimal11(convert_bool_to_binary(result_mult))}")
    print(f"Human readable product: {convertToString(reverseArray(convert_bool_to_binary(result_mult)))}")
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




