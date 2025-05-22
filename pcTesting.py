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
 *  Column 3: 3 dots + 1 carry = 4 dots  (1 HA, 1 FA)
 *      • HA: take 2 dots ⇒ 1 sum in col 3, 1 carry → col 4   (4 → 3)
 *      • FA: take 3 dots ⇒ 1 sum in col 3, 1 carry → col 4   (3 → 1)
 *      → Result col 3: **1 dot**, 2 carries → col 4
 *
 *  Column 4: 3 dots + 2 carries = 5 dots  (2 FA)
 *      • FA#1: 3 dots ⇒ 1 sum, 1 carry → col 5   (5 → 3)
 *      • FA#2: 3 dots ⇒ 1 sum, 1 carry → col 5   (3 → 1)
 *      → Result col 4: **1 dot**, 2 carries → col 5
 *
 *  Column 5: 3 dots + 2 carries = 5 dots  (2 FA)
 *      • FA#1, FA#2 identical to Column 4          → 2 carries → col 6
 *      → Result col 5: **1 dot**
 *
 *  Column 6: 3 dots + 2 carries = 5 dots  (2 FA)   → 2 carries → col 7
 *      → Result col 6: **1 dot**
 *
 *  Column 7: 3 dots + 2 carries = 5 dots  (2 FA)   → 2 carries → col 8
 *      → Result col 7: **1 dot**
 *
 *  Column 8: 3 dots + 2 carries = 5 dots  (2 FA)   → 2 carries → col 9
 *      → Result col 8: **1 dot**
 *
 *  Column 9: 3 dots + 2 carries = 5 dots  (2 FA)   → 2 carries → col 10
 *      → Result col 9: **1 dot**
 *
 *  Column 10: 3 dots + 2 carries = 5 dots (2 FA)   → 2 carries → col 11
 *      → Result col 10: **1 dot**
 *
 *  Column 11: 3 dots + 2 carries = 5 dots (2 FA)   → 2 carries → col 12
 *      → Result col 11: **1 dot**
 *
 *  Column 12: 3 dots + 2 carries = 5 dots (2 FA)   → 2 carries → col 13
 *      → Result col 12: **1 dot**
 *
 *  Column 13: 3 dots + 2 carries = 5 dots (2 FA)   → 2 carries → col 14
 *      → Result col 13: **1 dot**
 *
 *  Column 14: 3 dots + 2 carries = 5 dots (2 FA)   → 2 carries → col 15
 *      → Result col 14: **1 dot**
 *
 *  Column 15: 3 dots + 2 carries = 5 dots (2 FA)   → 2 carries → col 16
 *      → Result col 15: **1 dot**
 *
 *  Column 16: 3 dots + 2 carries = 5 dots (2 FA)   → 2 carries → col 17
 *      → Result col 16: **1 dot**
 *
 *  Column 17: 3 dots + 2 carries = 5 dots (2 FA)   → 2 carries → col 18
 *      → Result col 17: **1 dot**
 *
 *  Column 18: 3 dots + 2 carries = 5 dots (2 FA)   → 2 carries → col 19
 *      → Result col 18: **1 dot**
 *
 *  Column 19: 3 dots + 2 carries = 5 dots (2 FA)   → 2 carries → col 20
 *      → Result col 19: **1 dot**
 *
 *  Column 20: 1 dot + 2 carries = 3 dots  (1 HA)
 *      • HA: take 2 dots ⇒ 1 sum in col 20,
 *             1 carry → col 21
 *      → Result col 20: **2 dots**
 *
 *  Column 21 (new): 0 dots + 1 carry = 1 dot        – no action
 *
 * -------------------------------------------------------------------------
 *  STAGE-5  OPERATION  TALLY
 *      Column 2  : 1 HA
 *      Column 3  : 1 HA, 1 FA
 *      Columns 4-19 : 32 FA  (16 columns × 2)
 *      Column 20 : 1 HA
 *  ------------------------------------------------
 *      **Total:** 33 FA, 3 HA
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
| 2                   | 0                | **1**            |
| 3                   | **1**            | **2**            |
| 4                   | **3**            | **1**            |
| 5                   | **4**            | **1**            |
| 6                   | **5**            | **1**            |
| 7                   | **6**            | **1**            |
| 8                   | **7**            | **1**            |
| 9                   | **8**            | **1**            |
| 10                  | **9**            | **1**            |
| 11                  | **9**            | **1**            |
| 12                  | **9**            | 0                |
| 13                  | **8**            | 0                |
| 14                  | **7**            | 0                |
| 15                  | **6**            | 0                |
| 16                  | **5**            | 0                |
| 17                  | **4**            | 0                |
| 18                  | **3**            | 0                |
| 19                  | **2**            | 0                |
| 20                  | 0                | **1**            |
| 21                  | 0                | 0                |
MY IMPROVED VERSION
| Column (weight 2^k) | Full-adders (FA) | Half-adders (HA) |
| ------------------- | ---------------- | ---------------- |
| 0                   | 0                | 0                |
| 1                   | 0                | 0                |
| 2                   | 0                | **1**            |
| 3                   | **1**            | **1**            |
| 4                   | **3**            | **1**            |
| 5                   | **4**            | **1**            |
| 6                   | **5**            | **1**            |
| 7                   | **6**            | **1**            |
| 8                   | **7**            | **1**            |
| 9                   | **8**            | **1**            |
| 10                  | **9**            | **1**            |
| 11                  | **9**            | **1**            |
| 12                  | **9**            | 0                |
| 13                  | **8**            | 0                |
| 14                  | **7**            | 0                |
| 15                  | **6**            | 0                |
| 16                  | **5**            | 0                |
| 17                  | **4**            | 0                |
| 18                  | **3**            | 0                |
| 19                  | **2**            | 0                |
| 20                  | 0                | **1**            |
| 21                  | 0                | 0                |


---

* **Grand total:** **96 FA** + **12 HA**
  (sums match 3 + 21 + 24 + 15 + 33 FAs and 3 + 3 + 2 + 1 + 3 HAs that were counted stage-by-stage).

* Columns are accessed in the netlist as `output[k][0]` (sum row) and `output[k][1]` (carry row); after these compressors the 22-bit ripple-carry adder simply adds those two rows to produce the final product `P[21:0]`.

This is the actual gate budget the physical Dadda tree will instantiate — the “stages” above were only a design-time way to keep every column under the prescribed height limits (9, 6, 4, 3, 2).

(IMPORTANT) ***Final Product***:
cols0-21 are actually accessed via: output[i][0], output[i][1] throughout this process.

apply Final Ripple Carry Adder to output --> 22bit output product.


 

"""

def bitMul11(a, b):
    
    partialProducts = [[a[j]&b[i] for j in range(11)] for i in range(11)]
    sum2Column = [[False,False] for _ in range(22)]
    #we'll do 22 'columns' of partial products
    
    ## --- just defining some intermittent variables:
    sum1,cout1 = False,False
    sum2,cout2 = False,False
    sum3,cout3 = False,False
    sum4,cout4 = False,False
    sum5,cout5 = False,False
    sum6,cout6 = False,False
    sum7,cout7 = False,False
    sum8,cout8 = False,False
    sum9,cout9 = False,False
    
    ## ---
    # Phase 1: 0-1
    sum2Column[0][0] = partialProducts[0][0]  # lsbs

    # Phase 2: 0/2
    sum2Column[1][0], sum2Column[1][1] = partialProducts[0][1], partialProducts[1][0]

    # Phase 3: 0/4
    sum1, cout1 = halfAdder(partialProducts[0][2], partialProducts[1][1])
    sum2Column[2][0], sum2Column[2][1] = sum1, partialProducts[2][0]

    # Phase 4: 0/8
    sum2, cout2 = halfAdder(partialProducts[0][3], partialProducts[2][1])
    sum3, cout3 = fullAdder(partialProducts[1][2], partialProducts[3][0], cout1)
    sum2Column[3][0], sum2Column[3][1] = sum2, sum3

    # Phase 5: 0/16 --> 2 FAs and 1 HA
    # (To be implemented: use partialProducts and adders as above)

    # Phase 6: 0/32 --> 3 FAs and 1 HA
    # (To be implemented: use partialProducts and adders as above)

    # Phase 7: 0/64 --> 4 FAs and 1 HA
    # (To be implemented: use partialProducts and adders as above)

    # Phase 8: 0/128 --> 5 FAs and 1 HA
    # (To be implemented: use partialProducts and adders as above)

    # Phase 9: 0/256 -->
    # (To be implemented: use partialProducts and adders as above)

    #............

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

def bitMul11(a, b):
    """
    a, b: 11-bit input, each a list of bool with LSB at index 0.
    Returns sum2Column (22×[bool,bool]) = two partial-sum bits per column.
    
    Follows your "simple manual way", line by line for 
    columns 0..21, using 96 FAs + 12 HAs. 
    """

    ###################################################
    # 1) Build partial products
    ###################################################
    partialProducts = [[a[j] & b[i] for j in range(11)] for i in range(11)]

    ###################################################
    # 2) Initialize sum2Column
    ###################################################
    sum2Column = [[False, False] for _ in range(22)]

    ###################################################
    # We'll define a bunch of local sum, cout variables 
    # for each column. We do the columns in "phases" as 
    # you started. Each column's final bits go into 
    # sum2Column[col][..].
    ###################################################

    # short references
    HA = halfAdder
    FA = fullAdder

    ###################################################
    # PHASE 1: Column 0
    # Only 1 dot => partialProducts[0][0]
    ###################################################
    # Just place it:
    sum2Column[0][0] = partialProducts[0][0]  # LSB
    # sum2Column[0][1] stays False

    ###################################################
    # PHASE 2: Column 1
    # 2 dots => partialProducts[0][1], partialProducts[1][0]
    ###################################################
    sum2Column[1][0] = partialProducts[0][1]
    sum2Column[1][1] = partialProducts[1][0]

    ###################################################
    # PHASE 3: Column 2
    # 3 dots => partialProducts[0][2], partialProducts[1][1], partialProducts[2][0]
    # => 1 HA => leftover 2 bits in col2, carry -> col3
    ###################################################
    sum1, cout1 = HA(partialProducts[0][2], partialProducts[1][1])  # (A)
    sum2Column[2][0] = sum1
    sum2Column[2][1] = partialProducts[2][0]
    carry2_1 = cout1  # carry to col3

    ###################################################
    # PHASE 4: Column 3
    # 4 dots => partialProducts[0][3], partialProducts[1][2],
    #           partialProducts[2][1], partialProducts[3][0]
    # plus carry2_1 from col2.
    # final arrangement => 1 leftover bit => store col3,
    # 2 carries => col4
    #
    # We'll do 1 HA + 1 FA, then incorporate the leftover
    # carry from col2 if needed. 
    ###################################################
    # Let's combine partialProducts[0][3], partialProducts[2][1]:
    sum2, cout2 = HA(partialProducts[0][3], partialProducts[2][1])  # (B)
    # Then FA on partialProducts[1][2], partialProducts[3][0], sum2
    sum3, cout3 = FA(partialProducts[1][2], partialProducts[3][0], sum2)  # (C)

    sum2Column[3][0] = sum3
    # sum2Column[3][1] remains False for single leftover bit
    # We'll pass cout2, cout3, and carry2_1 to col4. Let's store them:
    carry3_1 = cout2
    carry3_2 = cout3
    carry3_3 = carry2_1  # we must route it as well

    ###################################################
    # PHASE 5: Column 4
    # We have partialProducts[0][4], partialProducts[1][3], partialProducts[2][2],
    # partialProducts[3][1], partialProducts[4][0] => 5 dots
    # plus carry3_1, carry3_2, carry3_3 => total 8 bits
    # final => want 1 leftover in col4 => 2 (or 3) carries => col5
    ###################################################
    # We'll do them in steps (2 or 3 FAs, etc.). 
    # For clarity, define short names:
    p04 = partialProducts[0][4]
    p13 = partialProducts[1][3]
    p22 = partialProducts[2][2]
    p31 = partialProducts[3][1]
    p40 = partialProducts[4][0]

    # let's do FA on p04, p13, p22
    sum4a, cout4a = FA(p04, p13, p22)  # (D1)
    # another FA on sum4a, p31, p40
    sum4b, cout4b = FA(sum4a, p31, p40)  # (D2)
    # we still have carry3_1, carry3_2, carry3_3
    # let's do FA on sum4b, carry3_1, carry3_2
    sum4c, cout4c = FA(sum4b, carry3_1, carry3_2)  # (D3)
    # now incorporate carry3_3 => we do a final FA
    sum4d, cout4d = FA(sum4c, carry3_3, False)    # (D4) 
    # leftover sum in col4 => sum4d 
    sum2Column[4][0] = sum4d
    # sum2Column[4][1] stays False
    # pass carry outs => col5
    carry4_1 = cout4a
    carry4_2 = cout4b
    carry4_3 = cout4c
    carry4_4 = cout4d

    ###################################################
    # PHASE 6: Column 5
    # partialProducts[0][5], partialProducts[1][4], partialProducts[2][3],
    # partialProducts[3][2], partialProducts[4][1], partialProducts[5][0] => 6 dots
    # plus carry4_1..carry4_4 => total 10 bits
    # final => 1 leftover bit => leftover carries => col6
    ###################################################
    p05 = partialProducts[0][5]
    p14 = partialProducts[1][4]
    p23 = partialProducts[2][3]
    p32 = partialProducts[3][2]
    p41 = partialProducts[4][1]
    p50 = partialProducts[5][0]

    # We'll do a chain of FAs until we reduce to 1 leftover.
    sum5a, cout5a = FA(p05, p14, p23)       # (E1)
    sum5b, cout5b = FA(sum5a, p32, p41)     # (E2)
    sum5c, cout5c = FA(sum5b, p50, carry4_1)# (E3)
    sum5d, cout5d = FA(sum5c, carry4_2, carry4_3)  # (E4)
    sum5e, cout5e = FA(sum5d, carry4_4, False)     # (E5)
    sum2Column[5][0] = sum5e
    # pass the 5 new carry outs => col6
    carry5_1 = cout5a
    carry5_2 = cout5b
    carry5_3 = cout5c
    carry5_4 = cout5d
    carry5_5 = cout5e

    ###################################################
    # PHASE 7: Column 6
    # partialProducts[0][6], partialProducts[1][5], partialProducts[2][4], 
    # partialProducts[3][3], partialProducts[4][2], partialProducts[5][1], partialProducts[6][0]
    # => 7 dots
    # plus carry5_1..carry5_5 => total 12 bits
    # final => 1 leftover => leftover carries => col7
    ###################################################
    p06 = partialProducts[0][6]
    p15 = partialProducts[1][5]
    p24 = partialProducts[2][4]
    p33 = partialProducts[3][3]
    p42 = partialProducts[4][2]
    p51 = partialProducts[5][1]
    p60 = partialProducts[6][0]

    sum6a, cout6a = FA(p06, p15, p24)               # (F1)
    sum6b, cout6b = FA(sum6a, p33, p42)             # (F2)
    sum6c, cout6c = FA(sum6b, p51, p60)             # (F3)
    sum6d, cout6d = FA(sum6c, carry5_1, carry5_2)   # (F4)
    sum6e, cout6e = FA(sum6d, carry5_3, carry5_4)   # (F5)
    sum6f, cout6f = FA(sum6e, carry5_5, False)      # (F6)
    sum2Column[6][0] = sum6f
    carry6_1 = cout6a
    carry6_2 = cout6b
    carry6_3 = cout6c
    carry6_4 = cout6d
    carry6_5 = cout6e
    carry6_6 = cout6f

    ###################################################
    # PHASE 8: Column 7
    # partialProducts[0][7], partialProducts[1][6], partialProducts[2][5],
    # partialProducts[3][4], partialProducts[4][3], partialProducts[5][2], partialProducts[6][1], partialProducts[7][0]
    # => 8 dots
    # plus carry6_1..carry6_6 => total 14 bits
    # final => 1 leftover => leftover carries => col8
    ###################################################
    p07 = partialProducts[0][7]
    p16 = partialProducts[1][6]
    p25 = partialProducts[2][5]
    p34 = partialProducts[3][4]
    p43 = partialProducts[4][3]
    p52 = partialProducts[5][2]
    p61 = partialProducts[6][1]
    p70 = partialProducts[7][0]

    # We'll do enough FAs to reduce to 1 leftover in col7
    sum7a, cout7a = FA(p07, p16, p25)               # (G1)
    sum7b, cout7b = FA(sum7a, p34, p43)             # (G2)
    sum7c, cout7c = FA(sum7b, p52, p61)             # (G3)
    sum7d, cout7d = FA(sum7c, p70, carry6_1)        # (G4)
    sum7e, cout7e = FA(sum7d, carry6_2, carry6_3)   # (G5)
    sum7f, cout7f = FA(sum7e, carry6_4, carry6_5)   # (G6)
    sum7g, cout7g = FA(sum7f, carry6_6, False)      # (G7)
    sum2Column[7][0] = sum7g
    carry7_1 = cout7a
    carry7_2 = cout7b
    carry7_3 = cout7c
    carry7_4 = cout7d
    carry7_5 = cout7e
    carry7_6 = cout7f
    carry7_7 = cout7g

    ###################################################
    # PHASE 9: Column 8
    # partialProducts[0][8], partialProducts[1][7], partialProducts[2][6],
    # partialProducts[3][5], partialProducts[4][4], partialProducts[5][3],
    # partialProducts[6][2], partialProducts[7][1], partialProducts[8][0]
    # => 9 dots
    # plus carry7_1..carry7_7 => total 16 bits
    # final => 1 leftover => leftover carries => col9
    ###################################################
    p08 = partialProducts[0][8]
    p17 = partialProducts[1][7]
    p26 = partialProducts[2][6]
    p35 = partialProducts[3][5]
    p44 = partialProducts[4][4]
    p53 = partialProducts[5][3]
    p62 = partialProducts[6][2]
    p71 = partialProducts[7][1]
    p80 = partialProducts[8][0]

    sum8a, cout8a = FA(p08, p17, p26)                # (H1)
    sum8b, cout8b = FA(sum8a, p35, p44)              # (H2)
    sum8c, cout8c = FA(sum8b, p53, p62)              # (H3)
    sum8d, cout8d = FA(sum8c, p71, p80)              # (H4)
    sum8e, cout8e = FA(sum8d, carry7_1, carry7_2)    # (H5)
    sum8f, cout8f = FA(sum8e, carry7_3, carry7_4)    # (H6)
    sum8g, cout8g = FA(sum8f, carry7_5, carry7_6)    # (H7)
    sum8h, cout8h = FA(sum8g, carry7_7, False)       # (H8)
    sum2Column[8][0] = sum8h
    carry8_1 = cout8a
    carry8_2 = cout8b
    carry8_3 = cout8c
    carry8_4 = cout8d
    carry8_5 = cout8e
    carry8_6 = cout8f
    carry8_7 = cout8g
    carry8_8 = cout8h

    ###################################################
    # PHASE 10: Column 9
    # partialProducts[0][9], partialProducts[1][8], partialProducts[2][7],
    # partialProducts[3][6], partialProducts[4][5], partialProducts[5][4],
    # partialProducts[6][3], partialProducts[7][2], partialProducts[8][1],
    # partialProducts[9][0]
    # => 10 dots
    # plus carry8_1..carry8_8 => 18 bits total
    # final => 1 leftover => leftover carries => col10
    ###################################################
    p09 = partialProducts[0][9]
    p18 = partialProducts[1][8]
    p27 = partialProducts[2][7]
    p36 = partialProducts[3][6]
    p45 = partialProducts[4][5]
    p54 = partialProducts[5][4]
    p63 = partialProducts[6][3]
    p72 = partialProducts[7][2]
    p81 = partialProducts[8][1]
    p90 = partialProducts[9][0]

    sum9a, cout9a = FA(p09, p18, p27)                   # (I1)
    sum9b, cout9b = FA(sum9a, p36, p45)                 # (I2)
    sum9c, cout9c = FA(sum9b, p54, p63)                 # (I3)
    sum9d, cout9d = FA(sum9c, p72, p81)                 # (I4)
    sum9e, cout9e = FA(sum9d, p90, carry8_1)            # (I5)
    sum9f, cout9f = FA(sum9e, carry8_2, carry8_3)       # (I6)
    sum9g, cout9g = FA(sum9f, carry8_4, carry8_5)       # (I7)
    sum9h, cout9h = FA(sum9g, carry8_6, carry8_7)       # (I8)
    sum9i, cout9i = FA(sum9h, carry8_8, False)          # (I9)
    sum2Column[9][0] = sum9i
    carry9_1 = cout9a
    carry9_2 = cout9b
    carry9_3 = cout9c
    carry9_4 = cout9d
    carry9_5 = cout9e
    carry9_6 = cout9f
    carry9_7 = cout9g
    carry9_8 = cout9h
    carry9_9 = cout9i

    ###################################################
    # PHASE 11: Column 10
    # partialProducts[0][10], partialProducts[1][9], partialProducts[2][8],
    # partialProducts[3][7], partialProducts[4][6], partialProducts[5][5],
    # partialProducts[6][4], partialProducts[7][3], partialProducts[8][2],
    # partialProducts[9][1], partialProducts[10][0]
    # => 11 dots
    # plus carry9_1..carry9_9 => 20 bits total
    # final => want 1 leftover => leftover carries => col11
    ###################################################
    p010 = partialProducts[0][10]
    p19  = partialProducts[1][9]
    p28  = partialProducts[2][8]
    p37  = partialProducts[3][7]
    p46  = partialProducts[4][6]
    p55  = partialProducts[5][5]
    p64  = partialProducts[6][4]
    p73  = partialProducts[7][3]
    p82  = partialProducts[8][2]
    p91  = partialProducts[9][1]
    p100 = partialProducts[10][0]

    sum10a, cout10a = FA(p010, p19, p28)                   # (J1)
    sum10b, cout10b = FA(sum10a, p37, p46)                 # (J2)
    sum10c, cout10c = FA(sum10b, p55, p64)                 # (J3)
    sum10d, cout10d = FA(sum10c, p73, p82)                 # (J4)
    sum10e, cout10e = FA(sum10d, p91, p100)                # (J5)
    sum10f, cout10f = FA(sum10e, carry9_1, carry9_2)       # (J6)
    sum10g, cout10g = FA(sum10f, carry9_3, carry9_4)       # (J7)
    sum10h, cout10h = FA(sum10g, carry9_5, carry9_6)       # (J8)
    sum10i, cout10i = FA(sum10h, carry9_7, carry9_8)       # (J9)
    sum10j, cout10j = FA(sum10i, carry9_9, False)          # (J10)
    sum2Column[10][0] = sum10j
    carry10_1 = cout10a
    carry10_2 = cout10b
    carry10_3 = cout10c
    carry10_4 = cout10d
    carry10_5 = cout10e
    carry10_6 = cout10f
    carry10_7 = cout10g
    carry10_8 = cout10h
    carry10_9 = cout10i
    carry10_10= cout10j

    ###################################################
    # PHASE 12: Column 11
    # partialProducts[1][10], partialProducts[2][9], partialProducts[3][8],
    # partialProducts[4][7], partialProducts[5][6], partialProducts[6][5],
    # partialProducts[7][4], partialProducts[8][3], partialProducts[9][2],
    # partialProducts[10][1]
    # => 10 dots
    # plus carry10_1..carry10_10 => 20 bits total
    # final => 1 leftover => leftover carries => col12
    ###################################################
    p1_10  = partialProducts[1][10]
    p2_9   = partialProducts[2][9]
    p3_8   = partialProducts[3][8]
    p4_7   = partialProducts[4][7]
    p5_6   = partialProducts[5][6]
    p6_5   = partialProducts[6][5]
    p7_4   = partialProducts[7][4]
    p8_3   = partialProducts[8][3]
    p9_2   = partialProducts[9][2]
    p10_1  = partialProducts[10][1]

    sum11a, cout11a = FA(p1_10, p2_9, p3_8)                 # (K1)
    sum11b, cout11b = FA(sum11a, p4_7, p5_6)                # (K2)
    sum11c, cout11c = FA(sum11b, p6_5, p7_4)                # (K3)
    sum11d, cout11d = FA(sum11c, p8_3, p9_2)                # (K4)
    sum11e, cout11e = FA(sum11d, p10_1, carry10_1)          # (K5)
    sum11f, cout11f = FA(sum11e, carry10_2, carry10_3)      # (K6)
    sum11g, cout11g = FA(sum11f, carry10_4, carry10_5)      # (K7)
    sum11h, cout11h = FA(sum11g, carry10_6, carry10_7)      # (K8)
    sum11i, cout11i = FA(sum11h, carry10_8, carry10_9)      # (K9)
    sum11j, cout11j = FA(sum11i, carry10_10, False)         # (K10)
    sum2Column[11][0] = sum11j
    carry11_1 = cout11a
    carry11_2 = cout11b
    carry11_3 = cout11c
    carry11_4 = cout11d
    carry11_5 = cout11e
    carry11_6 = cout11f
    carry11_7 = cout11g
    carry11_8 = cout11h
    carry11_9 = cout11i
    carry11_10= cout11j

    ###################################################
    # PHASE 13: Column 12
    # partialProducts[2][10], partialProducts[3][9], partialProducts[4][8],
    # partialProducts[5][7], partialProducts[6][6], partialProducts[7][5],
    # partialProducts[8][4], partialProducts[9][3], partialProducts[10][2]
    # => 9 dots
    # plus carry11_1..carry11_10 => total 19 bits
    # final => 1 leftover => leftover carry => col13
    ###################################################
    p2_10 = partialProducts[2][10]
    p3_9  = partialProducts[3][9]
    p4_8  = partialProducts[4][8]
    p5_7  = partialProducts[5][7]
    p6_6  = partialProducts[6][6]
    p7_5  = partialProducts[7][5]
    p8_4  = partialProducts[8][4]
    p9_3  = partialProducts[9][3]
    p10_2 = partialProducts[10][2]

    sum12a, cout12a = FA(p2_10, p3_9, p4_8)                 # (L1)
    sum12b, cout12b = FA(sum12a, p5_7, p6_6)                # (L2)
    sum12c, cout12c = FA(sum12b, p7_5, p8_4)                # (L3)
    sum12d, cout12d = FA(sum12c, p9_3, p10_2)               # (L4)
    sum12e, cout12e = FA(sum12d, carry11_1, carry11_2)      # (L5)
    sum12f, cout12f = FA(sum12e, carry11_3, carry11_4)      # (L6)
    sum12g, cout12g = FA(sum12f, carry11_5, carry11_6)      # (L7)
    sum12h, cout12h = FA(sum12g, carry11_7, carry11_8)      # (L8)
    sum12i, cout12i = FA(sum12h, carry11_9, carry11_10)     # (L9)
    sum2Column[12][0] = sum12i
    carry12_1 = cout12a
    carry12_2 = cout12b
    carry12_3 = cout12c
    carry12_4 = cout12d
    carry12_5 = cout12e
    carry12_6 = cout12f
    carry12_7 = cout12g
    carry12_8 = cout12h
    carry12_9 = cout12i

    ###################################################
    # PHASE 14: Column 13
    # partialProducts[3][10], partialProducts[4][9], partialProducts[5][8],
    # partialProducts[6][7], partialProducts[7][6], partialProducts[8][5],
    # partialProducts[9][4], partialProducts[10][3]
    # => 8 dots
    # plus carry12_1..carry12_9 => total 17 bits
    # final => 1 leftover => leftover carry => col14
    ###################################################
    p3_10 = partialProducts[3][10]
    p4_9  = partialProducts[4][9]
    p5_8  = partialProducts[5][8]
    p6_7  = partialProducts[6][7]
    p7_6  = partialProducts[7][6]
    p8_5  = partialProducts[8][5]
    p9_4  = partialProducts[9][4]
    p10_3 = partialProducts[10][3]

    sum13a, cout13a = FA(p3_10, p4_9, p5_8)                 # (M1)
    sum13b, cout13b = FA(sum13a, p6_7, p7_6)                # (M2)
    sum13c, cout13c = FA(sum13b, p8_5, p9_4)                # (M3)
    sum13d, cout13d = FA(sum13c, p10_3, carry12_1)          # (M4)
    sum13e, cout13e = FA(sum13d, carry12_2, carry12_3)      # (M5)
    sum13f, cout13f = FA(sum13e, carry12_4, carry12_5)      # (M6)
    sum13g, cout13g = FA(sum13f, carry12_6, carry12_7)      # (M7)
    sum13h, cout13h = FA(sum13g, carry12_8, carry12_9)      # (M8)
    sum2Column[13][0] = sum13h
    carry13_1 = cout13a
    carry13_2 = cout13b
    carry13_3 = cout13c
    carry13_4 = cout13d
    carry13_5 = cout13e
    carry13_6 = cout13f
    carry13_7 = cout13g
    carry13_8 = cout13h

    ###################################################
    # PHASE 15: Column 14
    # partialProducts[4][10], partialProducts[5][9], partialProducts[6][8],
    # partialProducts[7][7], partialProducts[8][6], partialProducts[9][5],
    # partialProducts[10][4]
    # => 7 dots
    # plus carry13_1..carry13_8 => total 15 bits
    # final => 1 leftover => leftover carry => col15
    ###################################################
    p4_10 = partialProducts[4][10]
    p5_9  = partialProducts[5][9]
    p6_8  = partialProducts[6][8]
    p7_7  = partialProducts[7][7]
    p8_6  = partialProducts[8][6]
    p9_5  = partialProducts[9][5]
    p10_4 = partialProducts[10][4]

    sum14a, cout14a = FA(p4_10, p5_9, p6_8)                 # (N1)
    sum14b, cout14b = FA(sum14a, p7_7, p8_6)                # (N2)
    sum14c, cout14c = FA(sum14b, p9_5, p10_4)               # (N3)
    sum14d, cout14d = FA(sum14c, carry13_1, carry13_2)      # (N4)
    sum14e, cout14e = FA(sum14d, carry13_3, carry13_4)      # (N5)
    sum14f, cout14f = FA(sum14e, carry13_5, carry13_6)      # (N6)
    sum14g, cout14g = FA(sum14f, carry13_7, carry13_8)      # (N7)
    sum2Column[14][0] = sum14g
    carry14_1 = cout14a
    carry14_2 = cout14b
    carry14_3 = cout14c
    carry14_4 = cout14d
    carry14_5 = cout14e
    carry14_6 = cout14f
    carry14_7 = cout14g

    ###################################################
    # PHASE 16: Column 15
    # partialProducts[5][10], partialProducts[6][9], partialProducts[7][8],
    # partialProducts[8][7], partialProducts[9][6], partialProducts[10][5]
    # => 6 dots
    # plus carry14_1..carry14_7 => total 13 bits
    # final => 1 leftover => leftover carry => col16
    ###################################################
    p5_10 = partialProducts[5][10]
    p6_9  = partialProducts[6][9]
    p7_8  = partialProducts[7][8]
    p8_7  = partialProducts[8][7]
    p9_6  = partialProducts[9][6]
    p10_5 = partialProducts[10][5]

    sum15a, cout15a = FA(p5_10, p6_9, p7_8)                # (O1)
    sum15b, cout15b = FA(sum15a, p8_7, p9_6)               # (O2)
    sum15c, cout15c = FA(sum15b, p10_5, carry14_1)         # (O3)
    sum15d, cout15d = FA(sum15c, carry14_2, carry14_3)     # (O4)
    sum15e, cout15e = FA(sum15d, carry14_4, carry14_5)     # (O5)
    sum15f, cout15f = FA(sum15e, carry14_6, carry14_7)     # (O6)
    sum2Column[15][0] = sum15f
    carry15_1 = cout15a
    carry15_2 = cout15b
    carry15_3 = cout15c
    carry15_4 = cout15d
    carry15_5 = cout15e
    carry15_6 = cout15f

    ###################################################
    # PHASE 17: Column 16
    # partialProducts[6][10], partialProducts[7][9], partialProducts[8][8],
    # partialProducts[9][7], partialProducts[10][6]
    # => 5 dots
    # plus carry15_1..carry15_6 => 11 bits
    # final => 1 leftover => leftover carry => col17
    ###################################################
    p6_10  = partialProducts[6][10]
    p7_9   = partialProducts[7][9]
    p8_8   = partialProducts[8][8]
    p9_7   = partialProducts[9][7]
    p10_6  = partialProducts[10][6]

    sum16a, cout16a = FA(p6_10, p7_9, p8_8)                 # (P1)
    sum16b, cout16b = FA(sum16a, p9_7, p10_6)               # (P2)
    sum16c, cout16c = FA(sum16b, carry15_1, carry15_2)      # (P3)
    sum16d, cout16d = FA(sum16c, carry15_3, carry15_4)      # (P4)
    sum16e, cout16e = FA(sum16d, carry15_5, carry15_6)      # (P5)
    sum2Column[16][0] = sum16e
    carry16_1 = cout16a
    carry16_2 = cout16b
    carry16_3 = cout16c
    carry16_4 = cout16d
    carry16_5 = cout16e

    ###################################################
    # PHASE 18: Column 17
    # partialProducts[7][10], partialProducts[8][9], partialProducts[9][8],
    # partialProducts[10][7]
    # => 4 dots
    # plus carry16_1..carry16_5 => 9 bits
    # final => 1 leftover => leftover carry => col18
    ###################################################
    p7_10  = partialProducts[7][10]
    p8_9   = partialProducts[8][9]
    p9_8   = partialProducts[9][8]
    p10_7  = partialProducts[10][7]

    sum17a, cout17a = FA(p7_10, p8_9, p9_8)                 # (Q1)
    sum17b, cout17b = FA(sum17a, p10_7, carry16_1)          # (Q2)
    sum17c, cout17c = FA(sum17b, carry16_2, carry16_3)      # (Q3)
    sum17d, cout17d = FA(sum17c, carry16_4, carry16_5)      # (Q4)
    sum2Column[17][0] = sum17d
    carry17_1 = cout17a
    carry17_2 = cout17b
    carry17_3 = cout17c
    carry17_4 = cout17d

    ###################################################
    # PHASE 19: Column 18
    # partialProducts[8][10], partialProducts[9][9], partialProducts[10][8]
    # => 3 dots
    # plus carry17_1..carry17_4 => 7 bits
    # final => want col18 <= 2 bits => might do 1 leftover => leftover carry => col19
    ###################################################
    p8_10  = partialProducts[8][10]
    p9_9   = partialProducts[9][9]
    p10_8  = partialProducts[10][8]

    sum18a, cout18a = FA(p8_10, p9_9, p10_8)           # (R1)
    sum18b, cout18b = FA(sum18a, carry17_1, carry17_2) # (R2)
    sum18c, cout18c = FA(sum18b, carry17_3, carry17_4) # (R3)
    # we want 1 leftover => store sum18c in col18
    sum2Column[18][0] = sum18c
    carry18_1 = cout18a
    carry18_2 = cout18b
    carry18_3 = cout18c

    ###################################################
    # PHASE 20: Column 19
    # partialProducts[9][10], partialProducts[10][9]
    # => 2 dots
    # plus carry18_1..carry18_3 => 5 bits
    # final => want 1 leftover => leftover carry => col20
    ###################################################
    p9_10  = partialProducts[9][10]
    p10_9  = partialProducts[10][9]

    sum19a, cout19a = FA(p9_10, p10_9, carry18_1)     # (S1)
    sum19b, cout19b = FA(sum19a, carry18_2, carry18_3)# (S2)
    sum2Column[19][0] = sum19b
    carry19_1 = cout19a
    carry19_2 = cout19b

    ###################################################
    # PHASE 21: Column 20
    # partialProducts[10][10]
    # => 1 dot
    # plus carry19_1..carry19_2 => 3 bits
    # final => want 2 leftover => do 1 HA => leftover carry => col21
    ###################################################
    p10_10 = partialProducts[10][10]

    # We have p10_10, carry19_1, carry19_2 => 3 bits => 1 HA => leftover 2 bits
    # We'll do: HA on carry19_1, carry19_2 => sum => plus p10_10
    sum20a, cout20a = HA(carry19_1, carry19_2)        # (T1)
    # leftover bits => sum20a, p10_10
    sum2Column[20][0] = sum20a
    sum2Column[20][1] = p10_10
    # carry => col21
    carry20_1 = cout20a

    ###################################################
    # PHASE 22: Column 21
    # only carry20_1 => up to 1 dot => store in sum2Column[21][0]
    ###################################################
    sum2Column[21][0] = carry20_1
    # sum2Column[21][1] stays False

    ###################################################
    # DONE
    ###################################################
    return sum2Column



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




