current_cycle = 0

BIT_SIZE = 32

def tick_clock():
    global current_cycle

    current_cycle += 1

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

def bitSub32(a, b):
    # Two's complement subtraction: a - b = a + (~b + 1)
    nb = [not b[i] for i in range(BIT_SIZE)]
    s, cout = bitAdd32(a, nb, True)
    return s, cout

#32bit multiplier
def bitMul32(a, b):
    



#32bit divider
def bitDiv32(a, b):




def bitFPAdd32(a, b):

def bitFPSub32(a, b):

def bitFPMul32(a, b):

def bitFPDiv32(a, b):

# #32bit shifter
def bitShifter32():

def bitAND32(a, b):

def bitOR32(a, b):

def bitXOR32(a, b):

def bitNOT32(a):



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
        result_sum, carry_out = bitAdder32(num1, num2, False)
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




