current_cycle = 0

BIT_SIZE = 32

def tick_clock():
    global current_cycle

    current_cycle += 1

def halfAdder(a, b):
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

fpa = [False,False,False,False,True,True,True,False,False,False,False,False,False,True,True,True] 
#0 is sign bit, 00011 (exponnent), #(implicit 1 is added here)11000000111 is mantissa.
#this value is 1.1000000111 * 2^3 = 12.0546875...
fpb = [False,True,False,True,True,True,True,False,True,False,False,False,False,True,False,True]
#0 is sign bit, 10111 (exponent), #(implicit 1 is added here)1010000101 is mantissa. 
#this value is 1.1010000101 * 2^8 = 417.25
#output should be ~4900-5000

def bitMul11(a, b):
    
    partialProducts = [[False for _ in range(11)] for _ in range(11)]
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
    phase=1
    if(phase==1):#0-1
        sum2Column[0][0] = a[0] & b[0] #lsbs
    elif(phase==2):#0/2
        sum2Column[1][0],sum2Column[1][1] = (a[1]&b[0]),(a[0]&b[1])
    elif(phase==3):#0/4
        sum1,cout1 = halfAdder((a[2]&b[0]),(a[1]&b[1]))
        sum2Column[2][0],sum2Column[2][1] = sum1,(a[0]&b[2])
    elif(phase==4):#0/8
        sum2,cout2 = halfAdder((a[3]&b[0]),(a[1]&b[2]))
        sum3,cout3 = fullAdder((a[2]&b[1]),(a[0]&b[3]),cout1)
        sum2Column[3][0],sum2Column[3][1] = sum2,sum3
    elif(phase==5):#0/16 --> 2 FAs and 1 HA
        sum4,cout4 = 
    elif(phase==6):#0/32 --> 3 FAs and 1 HA
    
    elif(phase==7):#0/64 --> 4 FAs and 1 HA

    elif(phase==8):#0/128 --> 5 FAs and 1 HA

    elif(phase==9):#0/256 --> 

def bitFPMul16(a, b):
    #a and b are 16bit floats
    partialProducts = [[False for _ in range(10)] for _ in range(10)]
    #negate. We use -15? [True,False,False,False,True] (msb is last array index)
    bitNeg15 = [True,False,False,False,True]
    interimA = bitAdd5(a,bitNeg15,True)
    interimB = bitAdd5(b,bitNeg15,True)
    outB = bitAdd5(interimA,interimB,False)

    #multiply the 10bit mantissas (actually 11bit via implicit 1s) to get 22bit product


    return outB
    #specific 
    #multiplication





# def bitFPDiv32(a, b):

# # #32bit shifter
# def bitShifter32():

# def bitAND32(a, b):

# def bitOR32(a, b):

# def bitXOR32(a, b):

# def bitNOT32(a):



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
    
    # 32-bit value: alternating False/True
    multt1 = [False]*3 + [True]*6 + [False]*23 #504
    multt2 = [False]*3 + [True]*6 + [False]*23 #504
    print(f"multt1 (decimal): {convertToDecimal(convert_bool_to_binary(multt1))}")
    print(f"multt2 (decimal): {convertToDecimal(convert_bool_to_binary(multt2))}")
    #calculate
    # result_mult = bitMul32(multt1, multt2)
    # print(f"Binary product: {convertToDecimal(convert_bool_to_binary(result_mult))}")
    # print(f"Human readable product: {convertToString(reverseArray(convert_bool_to_binary(result_mult)))}")
    # 32-bit value: alternating False/True
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




