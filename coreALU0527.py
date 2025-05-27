import struct, random
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


def bitAdd(a, b, c_in):
    bitSize2 = len(a)
    s = [False] * bitSize2
    c = [False] * (bitSize2+1)
    c[0] = c_in
    for i in range(bitSize2):
        s[i], c[i + 1] = fullAdder(a[i], b[i], c[i])
    return s, c[bitSize2]

def bitSub(a, b):
    # Two's complement subtraction: a - b = a + (~b + 1)
    nb = [not b[i] for i in range(len(b))]
    s, cout = bitAdd(a, nb, True)
    return s, cout

# # #16bit divider
# def bitDiv16(a, b):

# =====  tiny primitives  ==================================================


def twoComp(v):                             # two’s-complement negate
    inv = [not b for b in v]
    one = [True] + [False]*(len(v)-1)
    return bitAdd(inv, one)[0]

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
            R = bitSub(R, D)
        else:                      # R < 0 → add
            R, _ = bitAdd(R, D)

        Q[i] = not R[-1]           # quotient bit = ¬sign(R)

    if R[-1]:                      # final sign fix if negative
        R, _ = bitAdd(R, D)

    return Q, R[:-1]               # drop extra sign bit

# -------------------------------------------------------------------------
def bitDiv(a_bits, b_bits):
    """
    Gate-level n-bit signed division (non-restoring).
    Returns  (quotient[n], remainder[n])  -- both LSB-first.
    Raises ZeroDivisionError on b == 0.
    """
    n = len(a_bits)
    sign_a, sign_b = a_bits[n-1], b_bits[n-1]

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


def bitMul(a_bits, b_bits):
    n = len(a_bits)
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

def bitMulUnsigned(a_bits, b_bits):
    """
    n×n unsigned multiplier
    • inputs : a_bits[0..n-1], b_bits[0..n-1]  (LSB-first, bools)
    • output : product[0..2n-1]               (LSB-first, bools)
    """
    n = len(a_bits)
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



# ───── helpers ────────────────────────────────────────────────────────────
def int_to_bits(val, n=32):
    return [(val >> i) & 1 == 1 for i in range(n)]

def bits_to_int(bits):
    return sum((1 << i) for i, b in enumerate(bits) if b) & 0xFFFFFFFF

def int_to_float32(i):
    return struct.unpack('>f', struct.pack('>I', i & 0xFFFFFFFF))[0]

def float32_to_int(f):
    return struct.unpack('>I', struct.pack('>f', f))[0]

# ───── core FP32 adder/subtractor ────────────────────────────────────────
def bitFPAdd32(a_bits, b_bits, subtract=False):
    """
    IEEE-754 binary32 adder (subtract if subtract=True)

    a_bits, b_bits : 32-element bool lists (LSB-first)
    returns        : 32-element bool list (LSB-first)
    """
    a_int = bits_to_int(a_bits)
    b_int = bits_to_int(b_bits)
    if subtract:                       # invert sign-bit of B for a–b
        b_int ^= 0x8000_0000

    # host FPU does exact IEEE rounding to nearest-even in 32-bit
    res_float = int_to_float32(a_int) + int_to_float32(b_int)
    res_int   = float32_to_int(res_float)
    return int_to_bits(res_int, 32)

def bitFPSub32(a_bits, b_bits):
    return bitFPAdd32(a_bits, b_bits, subtract=True)

# def bitFPMul32()




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
    unbiasedA,cout_a = bitAdd(a[10:15],bitNeg15,False) #carryin for adder matters in both these cases, its how we differentiate
    unbiasedB,cout_b = bitAdd(b[10:15],bitNeg15,False)
    inverted_unbiasedB = [not bit for bit in unbiasedB] #turns 11011 (-5) into 00100 
    #print("unbiasedA",unbiasedA,"unbiasedB",unbiasedB,"inverted_unbiasedB",inverted_unbiasedB)
    #(with carry-->00101), that is, positive 5
    interimA, carry_out1 = bitAdd(unbiasedA,unbiasedB,False)#subtract b from a
    #outExp, carry_out2 = bitAdd(interimA,bitNeg15,True)#subtract 15 from b --> unbiased exponent
    #print(f"interimA: {interimA}")
    #print(f"outExp after subtracting 15: {outExp}")
    
    # outExp, carry_outexp2 = bitAdd(outExp,bitPos15,False)#add 15 to bias the exponent

    #print("a[0:10]+[True]:",a[0:10]+[True])
    #multiply the 10bit mantissas (actually 11bit via implicit 1s) to get 22bit product
    bit22Mantissa = bitMulUnsigned(a[0:10]+[True],b[0:10]+[True]) #adding implicit leading 1s
    print(f"bit22Mantissa: {bit22Mantissa}")
    shifted22Mantissa = bit22Mantissa
    #handle shift logic
    if(bit22Mantissa[21] == True):
        #shift right
        shifted22Mantissa = bit22Mantissa[1:] + [False]
        interimA, carry_out2 = bitAdd(interimA,[True,False,False,False,False],False)
        print("final interimA (it needed to be incremented by 1, before biasing):",interimA)
    else:
        pass
    print("final shifted22Mantissa:",shifted22Mantissa)
    biasedExp,cout = bitAdd(interimA,bitPos15,False)
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

# Convert LSB→MSB bool array (unsigned) to decimal
def convertToDecimalOnlyPositiveUnsigned(r):
    final = 0
    lengthM1 = len(r)
    for i in range(lengthM1):
        final += r[i] * (2 ** i)
    return final

# Convert LSB→MSB bool array (signed, 2's comp, BIT_SIZE) to decimal
def convertToDecimal(r):
    final = 0
    lengthM1 = BIT_SIZE-1
    for i in range(lengthM1):
        final += r[i] * (2 ** i)
    if r[lengthM1] == True:
        final -= 2 ** lengthM1
    return final

# Convert N-bit float (bool array) to decimal (supports 16, 32, 64, etc.)
def convertFloatBinaryToDecimal(a, exp_bits=None, mantissa_bits=None):
    """
    Converts a binary float (as LSB-first bool array) to decimal.
    Supports 16, 32, 64, etc. bit widths.
    If exp_bits and mantissa_bits are not provided, tries to infer from length.
    """
    n = len(a)
    # Default IEEE-like layouts
    if exp_bits is None or mantissa_bits is None:
        if n == 16:
            exp_bits = 5
            mantissa_bits = 10
        elif n == 32:
            exp_bits = 8
            mantissa_bits = 23
        elif n == 64:
            exp_bits = 11
            mantissa_bits = 52
        else:
            raise ValueError("Unknown float width, please specify exp_bits and mantissa_bits.")

    sign_bit = n - 1
    exp_start = mantissa_bits
    exp_end = mantissa_bits + exp_bits

    # Calculate exponent bias
    bias = (2 ** (exp_bits - 1)) - 1

    # Extract sign
    sign = -1 if a[sign_bit] else 1

    # Extract exponent bits (LSB-first)
    exp_bits_arr = a[exp_start:exp_end]
    exponent = 0
    for i, bit in enumerate(exp_bits_arr):
        exponent += (1 if bit else 0) * (2 ** i)
    unbiased_exp = exponent - bias

    # Extract mantissa bits (LSB-first)
    mantissaFrac = 0.0
    for j in range(mantissa_bits):
        currentBit = 1 if a[j] else 0
        mantissaFrac += currentBit * 2 ** (j - mantissa_bits)
    mantissaFrac += 1.0  # Add implicit leading 1 for normalized numbers

    # Handle special cases (Inf, NaN, subnormals)
    all_exp_ones = all(a[exp_start:exp_end])
    all_exp_zeros = not any(a[exp_start:exp_end])
    if all_exp_ones:
        if any(a[0:mantissa_bits]):
            return float('nan')
        else:
            return float('inf') * sign
    elif all_exp_zeros:
        # Subnormal number (no implicit leading 1)
        mantissaFrac -= 1.0
        unbiased_exp = 1 - bias

    return sign * mantissaFrac * (2 ** unbiased_exp)

# Convert bool list to 0/1 list
def convert_bool_to_binary(bool_list):
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
    result_mult = bitMulUnsigned(multt1, multt2)
    print(f"result_mult: {result_mult}")
    print(f"Binary product: {convertToDecimalOnlyPositiveUnsigned(convert_bool_to_binary(result_mult))}")
    print(f"bool to binary: {convert_bool_to_binary(result_mult)}")
    print(f"Human readable product: {convertToString(reverseArray(convert_bool_to_binary(result_mult)))}")
    
    result_mult2 = bitMul(multt3, multt4)
    print(f"result_mult2: {result_mult2}")
    print(f"Binary product: {convertToDecimal(convert_bool_to_binary(result_mult2))}")
    print(f"bool to binary: {convert_bool_to_binary(result_mult2)}")
    print(f"Human readable product: {convertToString(reverseArray(convert_bool_to_binary(result_mult2)))}")

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
    subtracted, cout = bitSub(subtract1, subtract2)
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
    result_sum, carry_out = bitAdd(num1, num2, False)
    #output
    print(f"Binary sum: {convertToDecimal(convert_bool_to_binary(result_sum))}, Carry out: {carry_out}")
    print(f"Human readable sum: {convertToString(reverseArray(convert_bool_to_binary(result_sum)))}")
    return result_sum

def testTwoEnteredNums():
    test = input("wanna try your own (skip if no, y if yes)")
    if test == 'y':
        num1 = input("enter first 32 bit number in decimal")
        num2 = input("enter second 32 bit number in decimal")
        result_sum, carry_out = bitAdd(num1, num2, False)
        print(f"Binary sum: {convertToDecimal(convert_bool_to_binary(result_sum))}, Carry out: {carry_out}")
        print(f"Human readable sum: {convertToString(reverseArray(convert_bool_to_binary(result_sum)))}")

result_sum = testTwoNums()

print(list(reversed(range(len(result_sum)))))




