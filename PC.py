


#when building an interactive version, we may use AI to port it to C/C++...
#we should make it 'visualizeable, like logisim and those nice graphic little boxes that connect to each other, with a 'mini metro' game type style in terms of color and shapes
# - adder, decoder, 
# - FPU too
# 5 stage instruction pipeline, handling cache misses too
# l1 cache a few cycles, l2 cache maybe ~50, ram maybe hundreds
# memory bus that can be accessed by various system components
# interupts simulated from various input devices, IO devices as spaces in memory


# microkernel for process scheduling, timer interuppt for process switching
# syscalls & MMU (memory management unit)

#GPU - 32 cores, 8threads/core --> 32 warps, 256 threads?
# cpu sends instructions to gpu, and kernels..
# gpu instructions: vector add, vector multiply, matrix multiply, convolution, etc.
# gpu drivers as space in memory that cpu can call e.g gpu_launch(kernel_id, data_ptr, size)
# tensor core implementations
# simulate 'latency hiding' 
# gpu connects via simulated pcie (though understand and maybe implement SXM)

# visualizer allows for 'lighting up' follows paths through each gate, and zoom in or click on high level
# component to reveal its internal circuit makeup, and conversely zoom out and click again to collapse it.
# may implement as an interactive web app. 

#RULES:
#We use the 0th bit of the array as the lsb. Last bit is msb. 

current_cycle = 0
def tick_clock():
    global current_cycle

    current_cycle += 1

RAM32K = [False] * 32768

def reverseByte(lst):
    """
    Reverses a list in-place.
    
    Args:
        lst: The list to be reversed
        
    Returns:
        The reversed list (same object, modified in-place)
    """
    left = 0
    right = len(lst) - 1
    
    while left < right:
        # Swap elements at left and right indices
        lst[left], lst[right] = lst[right], lst[left]
        
        # Move indices toward the center
        left += 1
        right -= 1
        
    return lst

# Create an 8-bit binary number using True/False values
binary_list = [True, False, True, True, False, True, False, True]
# This binary number (10110101) represents the decimal value 181
# (128*1 + 64*0 + 32*1 + 16*1 + 8*0 + 4*1 + 2*0 + 1*1 = 181)
print(f"reversed: {reverseByte(binary_list)}")

def convert_bool_to_binary(bool_list):
    """
    Converts a list of boolean values (True/False) to a list of binary values (1/0).
    
    Args:
        bool_list: A list of boolean values (True/False)
        
    Returns:
        A list of binary values (1/0) corresponding to the input boolean values
    """
    return [1 if value else 0 for value in bool_list]

def convertToString(r):
    final = ""
    for i in range(len(r)):
        final += str(r[i])
    return final

print((f"converted: {reverseByte(convert_bool_to_binary(binary_list))}"))

def fullAdder(a,b,c):
    x1 = a ^ b
    s = x1 ^ c
    a1 = a & b
    a2 = c & x1
    cout = a1 | a2
    return s, cout

def bitAdder16(a, b, c_in):
    s = [False] * 16
    c = [False] * 17
    c[0] = c_in
    for i in range(16):
        s[i], c[i + 1] = fullAdder(a[i], b[i], c[i])
    return s, c[16]

def subTractor(a,b,c_in):
    na = [not a[i] for i in range(16)]
    na2 = bitAdder16(na, [False]*16, True)
    return na2

# Let's correct and complete your carryLookaheadAdder8 implementation.
# This version will use only True/False values and basic gates (AND, OR, XOR, NOT).

def AND(*args):
    result = True
    for a in args:
        result = result and a
    return result

def OR(*args):
    result = False
    for a in args:
        result = result or a
    return result

def NOT(a):
    return not a

def XOR(a, b):
    return a != b

def increment_by_one(bits):
    """Adds 1 to a bit array using our full adder"""
    result = [False] * len(bits)
    carry = True  # Starting with carry=1 to add 1
    
    for i in range(len(bits)):
        result[i], carry = fullAdder(bits[i], False, carry)
    
    return result, carry
def subtractor_nbits(a, b):
    """
    Subtracts b from a (a-b) using two's complement method
    All operations built from basic gates
    
    Args:
        a: Minuend (array of booleans)
        b: Subtrahend (array of booleans)
        
    Returns:
        result: Difference (array of booleans)
        borrow: Borrow out flag (boolean)
    """
    # Ensure a and b are the same length
    n = len(a)
    
    # Step 1: Invert all bits of b
    b_inverted = [NOT(b[i]) for i in range(n)]
    
    # Step 2: Add 1 to get two's complement of b
    neg_b, _ = increment_by_one(b_inverted)
    
    # Step 3: Add a + (-b)
    result = [False] * n
    carry = False
    
    for i in range(n):
        result[i], carry = fullAdder(a[i], neg_b[i], carry)
    
    # For subtraction, the final carry is inverted to get the borrow
    borrow = NOT(carry)
    
    return result, borrow
#subtraction,
#opcode deplexing via demuxes/muxes, encoders/decoders. 
#Stage 1: ALU that can be fed instructions and output data, which we view: add, sub, other gates, shift etc.
#Stage 2: Sequential logic, incorporating via registers and program counter and memory.
#Stage 3: ~Feeding sequences of instructions, learning and potentially implementing a full scale clock.
#Stage 4: assembler to turn assembly code into binary code that must, itself, run on the CPU!
#stage 5: Write higher level code, perhaps expand CPU, make writes/reads more true to what actually occurs even if
#its not exactly how it must be done (e.g simulated memory reads even if we can just index an array for what we want.)
#Tied ruthlessly to higher level goals. 
#stage 6: expand to GPU, other system components, more advanced and realistic hardware architecture, incorporate
# bios and on system instructions and ROM, make more realistic... then after that? Compiler for higher level code,
# Primitive OS, kernel, etc. 

# I'm trying to build a basic ALU. Lets see:
# Multiplexer.. made of:
# Goes to my adder, 

 
#test
num1 = [False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True]  # 16-bit value (alternating False/True)
num2 = [True, True, False, False, True, True, False, False, True, True, False, False, True, True, False, False]  # 16-bit value (pattern of two True, two False)
print(f"Human readable num1: {convertToString(convert_bool_to_binary(num1))}")

def convertToDecimal(r):
    final = 0
    for i in range(len(r)):
        final += r[i] * (2 ** i)
    return final

print(f"convertToDecimal(num1): {convertToDecimal(num1)}")
print(f"convertToDecimal(num2): {convertToDecimal(num2)}")


print(f"num1: {convertToDecimal(convert_bool_to_binary(num1))}")
f=0
for i in range(len(num1)):
    
    a=0
    if num1[i]==False:
        a=0
    elif num1[i]==True:
        a=2**i
    print(f"{f} + {a} = {f+a}")
    f+=a
        
result_sum, carry_out = bitAdder16(num1, num2, False)
print(f"Binary sum: {convertToDecimal(convert_bool_to_binary(result_sum))}, Carry out: {carry_out}")
print(f"Human readable sum: {convertToString(convert_bool_to_binary(result_sum))}")

def human_readable(bit_array):
    """
    Converts a boolean array to a human-readable string of 0s and 1s,
    with most significant bit (MSB) on the left.
    
    Args:
        bit_array: List of boolean values
        
    Returns:
        String of 0s and 1s with MSB on the left
    """
    return ''.join('1' if bit else '0' for bit in reversed(bit_array))

#takes in 3 ctrl bits and 8 data bits, returns the data bit that is selected by the ctrl bits
def mux8(ctrl, d):
    #this:
    a = ctrl[0]
    b = ctrl[1]
    c = ctrl[2]
    an = not ctrl[0]
    bn = not ctrl[1]
    cn = not ctrl[2]
    
    en0 = an and bn and cn
    en1 = a and bn and cn
    en2 = an and b and cn
    en3 = a and b and cn
    en4 = an and bn and c
    en5 = a and bn and c
    en6 = an and b and c
    en7 = a and b and c
    
    result = (en0 and d[0]) or (en1 and d[1]) or (en2 and d[2]) or (en3 and d[3]) or (en4 and d[4]) or (en5 and d[5]) or (en6 and d[6]) or (en7 and d[7])

    # #is equivalent to this:
    # result = False
    # if en0: result = d[0]
    # if en1: result = d[1]
    # if en2: result = d[2]
    # if en3: result = d[3]
    # if en4: result = d[4]
    # if en5: result = d[5]
    # if en6: result = d[6]
    # if en7: result = d[7]

    return result    

def final_16x8_Mux(a,b,c,d,e,f,g,h,ctrl):
    output = [False] * 16
    for i in range(16):
        output[i] = mux8(ctrl, [a[i],b[i],c[i],d[i],e[i],f[i],g[i],h[i]])
    return output

# def SHL16(a):
    



def ALU16(a, b, op_code):
    """
    16-bit ALU with hardware-realistic implementation
    Uses physical signal routing via control lines
    
    Args:
        a: 16-bit input A (boolean array)
        b: 16-bit input B (boolean array)
        op_code: 3-bit operation select (boolean array)
                [0,0,0] - ADD
                [0,0,1] - SUB
                [0,1,0] - AND
                [0,1,1] - OR
                [1,0,0] - XOR
                [1,0,1] - NOT (A)
                [1,1,0] - SHIFT LEFT
                [1,1,1] - SHIFT RIGHT
    
    Returns:
        result: 16-bit output (boolean array)
        flags: Dictionary with carry, zero, negative flags
    """
    # Preparation signals based on op_code
    invert_b = op_code[2]  # Activate for SUB operation
    use_carry_in = op_code[2]  # Activate for SUB operation
    
    # Output signals
    result = [False] * 16
    flags = {'carry': False, 'zero': False, 'negative': False}
    
    # ----- SUB Operation Prep -----
    # When doing subtraction, invert B and set carry_in to 1
    b_internal = [False] * 16
    for i in range(16):
        # This is a hardware MUX - selects either B or NOT(B) based on control signal
        b_internal[i] = b[i] if not invert_b else not b[i]
    #^^ this simply inverts it, and if its being subtracted its naturally inverted and the +1 is taken care 
    # of via the carry in.
    # ----- Main ALU Operations -----
    # Addition/Subtraction Path
    if not op_code[0] and not op_code[1]:  # ADD or SUB
        adder_result, flags['carry'] = bitAdder16(a, b_internal, use_carry_in)
        result = adder_result
        
    # Logic Operations Path    
    elif not op_code[0] and op_code[1]:  # AND or OR
        if not op_code[2]:  # AND
            for i in range(16):
                result[i] = a[i] and b[i]
        else:  # OR
            for i in range(16):
                result[i] = a[i] or b[i]
                
    elif op_code[0] and not op_code[1]:  # XOR or NOT
        if not op_code[2]:  # XOR
            for i in range(16):
                result[i] = (a[i] or b[i]) and not (a[i] and b[i])
        else:  # NOT A
            for i in range(16):
                result[i] = not a[i]
                
    # Shift Operations Path
    elif op_code[0] and op_code[1]:  # Shifts
        if not op_code[2]:  # SHIFT LEFT
            result = [False] + a[:-1]
        else:  # SHIFT RIGHT impl;ies shrinking it.
            result = a[1:] + [False]
    
    # ----- Set Flags -----
    # Zero flag - true if all result bits are 0
    flags['zero'] = all(not bit for bit in result)
    
    # Negative flag - true if MSB is 1 (in two's complement)
    flags['negative'] = result[15]
    
    # Note: Carry flag was already set by the adder
    
    return result, flags

