import struct, random
current_cycle = 0

BIT_SIZE = 32

def intToBoolList(value, width=32):
    """Convert integer to LSB-first boolean list"""
    return [bool((value >> i) & 1) for i in range(width)]
def signExtend(bits, targetWidth):
    """Sign extend boolean list to target width"""
    if len(bits) >= targetWidth:
        return bits[:targetWidth]

    signBit = bits[-1] if bits else False
    result = bits[:]
    while len(result) < targetWidth:
        result.append(signBit)
    return result
# Convert LSB→MSB bool array (unsigned) to decimal
def convertToDecimalUnsigned(r):
    final = 0
    lengthM1 = len(r)
    for i in range(lengthM1):
        final += r[i] * (2 ** i)
    return final

# Convert LSB→MSB bool array (signed, 2's comp, BIT_SIZE) to decimal
def convertToDecimal(r):
    final = 0
    lengthM1 = len(r)-1
    for i in range(lengthM1):
        final += r[i] * (2 ** i)
    if r[lengthM1] == True:
        final -= 2 ** lengthM1
    return final

def boolListToInt(boolList):
    """Convert LSB-first boolean list to integer"""
    return convertToDecimalUnsigned(boolList)

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

# Aliases for compatibility
HA = halfAdder
FA = fullAdder

def NOT(x):
    return not x

def AND(*inputs):
    if not inputs:
        return True
    result = True
    for inp in inputs:
        result = result and inp
    return result

def OR(*inputs):
    if not inputs:
        return False
    result = False
    for inp in inputs:
        result = result or inp
    return result


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


def twoComp(v):                             # two's-complement negate
    inv = [not b for b in v]
    one = [True] + [False]*(len(v)-1)
    return bitAdd(inv, one)[0]

def shiftLeftVal(inp,val):
    return inp[]


def shiftLeft(bits, in_bit):                # logical shift-left by 1
    return [in_bit] + bits[:-1]
# -------------1------------------------------------------------------------

def uDivNonrestoring(dividend, divisor):
    """Unsigned, non-restoring division (n-bit) → (Q, R)"""
    n   = len(dividend)
    Q   = [False]*n
    R   = [False]*(n+1)            # one extra sign bit
    D   = divisor + [False]        # align width

    for i in range(n-1, -1, -1):   # MSB → LSB
        R = shiftLeft(R, dividend[i])

        if not R[-1]:              # R ≥ 0 → subtract
            R, _ = bitSub(R, D)
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

    Qmag, Rmag = uDivNonrestoring(A, B)

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
    cols[n].append(True)               # two Baugh-Wooley correction 1's
    cols[2*n-1].append(True)

    # --- Dadda compression to 2 rows -------------------------------------
    sums  = [False]*(2*n)
    carys = [False]*(2*n)
    for k in range(2*n):
        while len(cols[k]) > 2:
            s,c = fullAdder(cols[k].pop(), cols[k].pop(), cols[k].pop())
            cols[k].append(s)
            if k < 2*n-1:
                cols[k+1].append(c)
        if cols[k]: sums[k]  = cols[k].pop()
        if cols[k]: carys[k] = cols[k].pop()

    # --- final ripple-carry adder ----------------------------------------
    P   = [False]*(2*n)
    cin = False
    for k in range(2*n):
        P[k], cin = fullAdder(sums[k], carys[k], cin)
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
                cols[i+j].append(True)       # only keep '1' dots

    # --- 2. Dadda-style compression to 2 rows ------------------------------
    sums  = [False]*(2*n)
    carys = [False]*(2*n)

    for k in range(2*n):
        while len(cols[k]) > 2:              # keep height ≤ 2
            s, c = fullAdder(cols[k].pop(),
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
        product[k], cin = fullAdder(sums[k], carys[k], cin)
    return product

# def mux(bitInput, bitSelect):



# def 5to32Decoder(bit5Input):
    #mux internals simply are:
    #n select bit lines and n inverted select bit lines and 2^n input bit lines both feed into
    #2^n n+1 input AND gates which feed into a 2^n input OR gate
MEMORY_SIZE=131072
memory=[False]*32*MEMORY_SIZE

rdReg = [False]*32
rs1Reg = [False]*32
rs2Reg = [False]*32

# class Register32:

def slice_instruction(instr_bits):
    """Extract all possible fields from 32-bit instruction"""
    return {
        'opcode': instr_bits[0:7],      # bits 6:0
        'rd':     instr_bits[7:12],     # bits 11:7  
        'funct3': instr_bits[12:15],    # bits 14:12
        'rs1':    instr_bits[15:20],    # bits 19:15
        'rs2':    instr_bits[20:25],    # bits 24:20
        'funct7': instr_bits[25:32],    # bits 31:25
    }

#want to be able to handle load, store, and add for now in RISC style.


#
def decoding(sliced_instructs):
    global rdReg, rs1Reg, rs2Reg
    if(sliced_instructs['opcode'] == '0110011'[::-1]):
        if(sliced_instructs['funct3'] == '000'):
            if(sliced_instructs['funct7'] == '0000000'):
                #add regs 1 & 2  into rd.   
                rdReg = ALU32(rs1Reg, rs2Reg, 'add')
                print("output of add part of ALU32:",)
    elif(sliced_instructs['opcode'] == '0000011'[::-1]):
        if(sliced_instructs['funct3'] == '010'):
            #lw rd, offset(targetMemAddr) --> rd = memory[targetMemAddr+offset]
            #load word from memory into rd.   
            print("hi!")
            # if(sliced_instructs['rd'] == '11110'):
            #     rs1Reg = memory[bits_to_int(sliced_instructs['rs1']+sliced_instructs['funct7']+sliced_instructs['rs2'])]
            # elif(sliced_instructs['rd'] == '11111'):
            temp = bits_to_int(sliced_instructs['rs1']+sliced_instructs['funct7']+sliced_instructs['rs2'])
            #deal with 11111 later
            print("temp:",temp)
            rs2Reg = memory[temp:temp+32]
            
# def decoder(insInp):
#     insInp[]

#5-->32 decoder 

def ALU32(a,b,instruction):
    if(instruction == 'add'):
        return bitAdd(a,b,False)[0]
    


# def FPU32(bit32Input):


# ───── helpers ────────────────────────────────────────────────────────────
def int_to_bits(val, n=32):
    return [(val >> i) & 1 == 1 for i in range(n)]
#print("int_to_bits(52)", int_to_bits(52))
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

# ───────── IEEE-754 binary32 multiply / divide  (True/False, LSB-first) ──
def bitFPMul32(a_bits, b_bits):
    """
    32-bit IEEE-754 multiply (round-to-nearest-even).
    Inputs / output = 32-element bool lists (LSB-first).
    """
    a = int_to_float32(bits_to_int(a_bits))
    b = int_to_float32(bits_to_int(b_bits))
    res = a * b                      # host FPU does 64-bit op
    return int_to_bits(float32_to_int(res), 32)

def bitFPDiv32(a_bits, b_bits):
    """
    32-bit IEEE-754 divide (round-to-nearest-even).
    Handles 0, ±inf, NaNs exactly like hardware.
    """
    a_int = bits_to_int(a_bits)
    b_int = bits_to_int(b_bits)

    # fast-detect zero divisor to avoid Python ZeroDivisionError
    if (b_int & 0x7FFF_FFFF) == 0:              # |b| == 0
        if (a_int & 0x7FFF_FFFF) == 0:          # 0/0 ➜ qNaN
            return int_to_bits(0x7FC0_0000, 32)
        else:                                   # x/0 ➜ ±inf
            sign = (a_int ^ b_int) & 0x8000_0000
            return int_to_bits(sign | 0x7F80_0000, 32)

    # use host FPU for normal path
    res = int_to_float32(a_int) / int_to_float32(b_int)
    return int_to_bits(float32_to_int(res), 32)


def mux(a=None, select=None):
    """
    Arbitrary-sized Multiplexer using only basic gates (AND, OR, NOT)
    
    Args:
        a: Data inputs array [d0, d1, ..., d(num_inputs-1)]
           Default: alternating True/False pattern
        select: Select bits array [s0, s1, ..., s(num_select_bits-1)] where s0 is LSB
                Default: all False (selects input 0)
        num_inputs: Number of data inputs (must equal 2^num_select_bits)
        num_select_bits: Number of select lines (log2 of num_inputs)
    
    Returns:
        Single output bit
        
    Note: If num_inputs and num_select_bits conflict, num_select_bits takes precedence
    """
    num_inputs = len(a)
    num_select_bits = len(select)
    # Basic gate implementations

    # ----------------------
    # Parameter resolution logic
    if num_select_bits is None and num_inputs is None:
        # Default to 4:16 MUX
        num_select_bits = 4
        num_inputs = 16
    elif num_select_bits is not None and num_inputs is None:
        # Calculate inputs from select bits
        num_inputs = 2 ** num_select_bits
    elif num_select_bits is None and num_inputs is not None:
        # Calculate select bits from inputs
        import math
        num_select_bits = int(math.log2(num_inputs))
        if 2 ** num_select_bits != num_inputs:
            raise ValueError(f"num_inputs ({num_inputs}) must be a power of 2")
    else:
        # Both specified - verify consistency
        expected_inputs = 2 ** num_select_bits
        if num_inputs != expected_inputs:
            print(f"Warning: num_inputs ({num_inputs}) != 2^num_select_bits ({expected_inputs})")
            print(f"Using num_select_bits={num_select_bits}, setting num_inputs={expected_inputs}")
            num_inputs = expected_inputs
    
    # Generate default inputs if not provided
    if a is None:
        a = [i % 2 == 0 for i in range(num_inputs)]  # Alternating pattern
    elif len(a) != num_inputs:
        raise ValueError(f"Input array length ({len(a)}) must equal num_inputs ({num_inputs})")
    
    # Generate default select if not provided  
    if select is None:
        select = [False] * num_select_bits  # All zeros - selects input 0
    elif len(select) != num_select_bits:
        raise ValueError(f"Select array length ({len(select)}) must equal num_select_bits ({num_select_bits})")
    # ----------------------


    # Edge case: single input (0 select bits)
    if num_select_bits == 0:
        return a[0]
    
    # Generate inverted select signals using NOT gates
    not_select = [NOT(s) for s in select]
    
    # Generate enable signal for each input
    enabled_outputs = []
    for input_index in range(num_inputs):
        # For each input, create enable signal that matches its binary representation
        enable_terms = []
        
        for bit_position in range(num_select_bits):
            # Check if bit_position bit of input_index is set
            bit_value = (input_index >> bit_position) & 1 #input_index[bit_position]
            #to replace this you'd need to manually create a bitarray of the current possibly select bits
            #we're at instead of easily shifting it to check. It's a quick solution that the llm was smart to implement.
            if bit_value == 1:
                # This bit should be 1, so use the select signal directly
                enable_terms.append(select[bit_position])
            else:
                # This bit should be 0, so use the inverted select signal
                enable_terms.append(not_select[bit_position])
        
        # Enable signal is AND of all required select bit conditions
        enable_signal = AND(*enable_terms)
        
        # Combine enable with data input
        enabled_output = AND(a[input_index], enable_signal)
        enabled_outputs.append(enabled_output)
    # Final OR gate combines all enabled outputs
    output = OR(*enabled_outputs)

    return output
class cpu_32:
#we interpret lsb as 1st element and msb as last, hence our ordering is 'reversed' from standard.
    def __init__(self):
        # Inherit register system from original cpu_32 class
        self.gRegs = [[False]*32 for _ in range(32)]
        self.memory = bytearray(4096)  # 4KB memory
        self.pc = 0
        
        # Control unit
        self.controlUnit = ControlUnit()
        
        # Register tag mapping (same as original)
        self.REG_TAGS = {
            0:  "zero",  1:  "ra",   2:  "sp",   3:  "gp",   4:  "tp",
            5:  "t0",    6:  "t1",   7:  "t2",
            8:  "s0",    9:  "s1", 
            10: "a0",   11: "a1",   12: "a2",   13: "a3",   14: "a4",   15: "a5",   16: "a6",   17: "a7",
            18: "s2",   19: "s3",   20: "s4",   21: "s5",   22: "s6",   23: "s7",   24: "s8",   25: "s9",   26: "s10",  27: "s11",
            28: "t3",   29: "t4",   30: "t5",   31: "t6"
        }
    
    def getReg(self, key):
        """Get register value (same as original)"""
        if isinstance(key, int):
            if 0 <= key < 32:
                return self.gRegs[key]
        return [False] * 32
    
    def setReg(self, key, value):
        """Set register value (same as original)"""
        if isinstance(key, int) and 0 < key < 32:  # x0 always zero
            if isinstance(value, list) and len(value) == 32:
                self.gRegs[key] = value.copy()

    def regTag(self, idx):
        """
        Get the canonical tag name for a register index.
        """
        return self.index_to_tag.get(idx, f"x{idx}")

    # Example: cpu.get_reg('a0'), cpu.get_reg(10), cpu.set_reg('sp', [False]*32)
    def decode(self, opcodeBits):
            """Returns dict of instruction type signals"""
            if len(opcodeBits) != 7:
                raise ValueError("Opcode must be 7 bits")
            
            # Create inverted signals
            opcodeNot = [NOT(bit) for bit in opcodeBits]
            b = opcodeBits  # shorthand
            n = opcodeNot   # shorthand
            
            # Gate count: 9 instruction types × 7 gates each = 63 AND gates + 7 NOT gates = 70 gates
            
            # R-type: 0110011 → LSB-first: 1100110
            rType = AND(b[0], b[1], n[2], n[3], b[4], b[5], n[6])
            
            # I-type ALU: 0010011 → LSB-first: 1100100
            iTypeAlu = AND(b[0], b[1], n[2], n[3], b[4], n[5], n[6])
            
            # Load: 0000011 → LSB-first: 1100000  
            load = AND(b[0], b[1], n[2], n[3], n[4], n[5], n[6])
            
            # Store: 0100011 → LSB-first: 1100010
            store = AND(b[0], b[1], n[2], n[3], n[4], b[5], n[6])
            
            # Branch: 1100011 → LSB-first: 1100011
            branch = AND(b[0], b[1], n[2], n[3], n[4], n[5], b[6])
            
            # JAL: 1101111 → LSB-first: 1111011
            jal = AND(b[0], b[1], b[2], b[3], n[4], b[5], b[6])
            
            # JALR: 1100111 → LSB-first: 1110011  
            jalr = AND(b[0], b[1], n[2], b[3], n[4], n[5], b[6])
            
            # LUI: 0110111 → LSB-first: 1110110
            lui = AND(b[0], b[1], n[2], b[3], b[4], b[5], n[6])
            
            # AUIPC: 0010111 → LSB-first: 1110100
            auipc = AND(b[0], b[1], n[2], b[3], n[4], b[5], n[6])
            
            return {
                'rType': rType,
                'iTypeAlu': iTypeAlu,
                'load': load, 
                'store': store,
                'branch': branch,
                'jal': jal,
                'jalr': jalr,
                'lui': lui,
                'auipc': auipc
            }

    def generateAluOp(self, opcodeSignals, funct3Bits, funct7Bits):
        """Generate 4-bit ALU control signal"""
        
        # ALU Operations (4-bit encoding):
        # 0000: ADD, 0001: SUB, 0010: AND, 0011: OR, 0100: XOR
        # 0101: SLL, 0110: SRL, 0111: SRA, 1000: SLT, 1001: SLTU
        # 1010-1111: Reserved for MUL/DIV etc.
        
        f3 = boolListToInt(funct3Bits)
        f7 = boolListToInt(funct7Bits)
        
        # Default: ADD (for loads, stores, branches address calc)
        aluOp = [False, False, False, False]  # 0000
        
        # R-type and I-type ALU operations
        if opcodeSignals['rType'] or opcodeSignals['iTypeAlu']:
            if f3 == 0:  # ADD/SUB
                if opcodeSignals['rType'] and f7 == 0x20:  # SUB
                    aluOp = [True, False, False, False]  # 0001: SUB
                # else ADD (default 0000)
            elif f3 == 1:  # SLL
                aluOp = [True, False, True, False]  # 0101: SLL
            elif f3 == 2:  # SLT  
                aluOp = [False, False, False, True]  # 1000: SLT
            elif f3 == 3:  # SLTU
                aluOp = [True, False, False, True]  # 1001: SLTU
            elif f3 == 4:  # XOR
                aluOp = [False, False, True, False]  # 0100: XOR
            elif f3 == 5:  # SRL/SRA
                if f7 == 0x20:  # SRA
                    aluOp = [True, True, True, False]  # 0111: SRA
                else:  # SRL
                    aluOp = [False, True, True, False]  # 0110: SRL
            elif f3 == 6:  # OR
                aluOp = [True, True, False, False]  # 0011: OR
            elif f3 == 7:  # AND
                aluOp = [False, True, False, False]  # 0010: AND
        
        return aluOp

    def generateImmediate(self, instrBits, opcodeSignals):
        """Generate 32-bit immediate based on instruction format"""
        
        # Extract raw immediate bits for each format
        iImm = self.extractIImmediate(instrBits)
        sImm = self.extractSImmediate(instrBits) 
        bImm = self.extractBImmediate(instrBits)
        uImm = self.extractUImmediate(instrBits)
        jImm = self.extractJImmediate(instrBits)
        
        # 5:1 mux to select appropriate immediate format
        # Mux select logic based on instruction type
        if opcodeSignals['iTypeAlu'] or opcodeSignals['load'] or opcodeSignals['jalr']:
            return iImm
        elif opcodeSignals['store']:
            return sImm 
        elif opcodeSignals['branch']:
            return bImm
        elif opcodeSignals['lui'] or opcodeSignals['auipc']:
            return uImm
        elif opcodeSignals['jal']:
            return jImm
        else:
            return [False] * 32  # Default zero immediate
    
    def extractIImmediate(self, instrBits):
        """I-type: bits[31:20] sign-extended"""
        immBits = instrBits[20:32]  # bits 31:20
        return signExtend(immBits, 32)
    
    def extractSImmediate(self, instrBits):
        """S-type: {bits[31:25], bits[11:7]} sign-extended"""
        immBits = instrBits[7:12] + instrBits[25:32]  # {11:7, 31:25}
        return signExtend(immBits, 32)
    
    def extractBImmediate(self, instrBits):
        """B-type: {bit[31], bit[7], bits[30:25], bits[11:8], 0} sign-extended"""
        # Assemble: {bit31, bit7, bits30:25, bits11:8, 0}
        immBits = ([False] +                           # bit 0 = 0 (branches are 2-byte aligned)
                  instrBits[8:12] +                    # bits 11:8 → positions 4:1
                  instrBits[25:31] +                   # bits 30:25 → positions 10:5  
                  [instrBits[7]] +                     # bit 7 → position 11
                  [instrBits[31]])                     # bit 31 → position 12 (sign)
        return signExtend(immBits, 32)
    
    def extractUImmediate(self, instrBits):
        """U-type: bits[31:12] in upper 20 bits, lower 12 bits = 0"""
        immBits = ([False] * 12 +                     # Lower 12 bits = 0
                  instrBits[12:32])                    # Upper 20 bits from instruction
        return immBits
    
    def extractJImmediate(self, instrBits):
        """J-type: {bit[31], bits[19:12], bit[20], bits[30:21], 0} sign-extended"""
        # Assemble: {bit31, bits19:12, bit20, bits30:21, 0}
        immBits = ([False] +                           # bit 0 = 0 (jumps are 2-byte aligned)
                  instrBits[21:31] +                   # bits 30:21 → positions 10:1
                  [instrBits[20]] +                    # bit 20 → position 11
                  instrBits[12:20] +                   # bits 19:12 → positions 19:12
                  [instrBits[31]])                     # bit 31 → position 20 (sign)
        return signExtend(immBits, 32)


    
    def executeInstruction(self, instrBits):
        """Execute single instruction using gate-level control"""
        
        # Generate control signals
        controls = self.controlUnit.generateControlSignals(instrBits)
        
        # Read source registers
        rs1Val = self.getReg(controls['rs1'])
        rs2Val = self.getReg(controls['rs2'])
        
        # ALU operand selection mux (2:1, 32-bit)
        # Mux gate count: 32 bits × 3 gates/bit = 96 gates
        aluOpB = mux2to1(rs2Val, controls['immediate'], controls['aluSrc'])
        
        # Execute ALU operation
        aluResult = self._executeAlu(rs1Val, aluOpB, controls['aluOp'])
        
        # Memory operations
        memData = [False] * 32
        if controls['memRead']:
            addr = boolListToInt(aluResult)
            memData = self._loadMemory(addr, controls['funct3'])
        elif controls['memWrite']:
            addr = boolListToInt(aluResult)
            self._storeMemory(addr, rs2Val, controls['funct3'])
        
        # Write-back result selection mux (4:1, 32-bit)
        # Mux gate count: 32 bits × (3+3+1) gates per 4:1 mux = 224 gates
        pcPlus4 = intToBoolList(self.pc + 4, 32)
        writeData = mux4to1(aluResult, memData, pcPlus4, controls['immediate'], 
                           controls['resultSel'])
        
        # Write to register file
        if controls['regWrite']:
            self.setReg(controls['rd'], writeData)
        
        # PC update logic
        self._updatePc(controls, aluResult, rs1Val, rs2Val)
        
        return controls  # Return for debugging
    
    def _executeAlu(self, opA, opB, aluOp):
        """Execute ALU operation based on 4-bit control"""
        # Import ALU functions from original coreALU0527.py
        from coreALU0527 import bitAdd, bitSub, AND as bitAND, OR as bitOR
        
        opCode = boolListToInt(aluOp)
        
        if opCode == 0:    # ADD
            result, _ = bitAdd(opA, opB, False)
            return result
        elif opCode == 1:  # SUB  
            result, _ = bitSub(opA, opB)
            return result
        elif opCode == 2:  # AND
            return [bitAND(opA[i], opB[i]) for i in range(32)]
        elif opCode == 3:  # OR
            return [bitOR(opA[i], opB[i]) for i in range(32)]
        elif opCode == 4:  # XOR
            return [AND(OR(opA[i], opB[i]), NOT(AND(opA[i], opB[i]))) for i in range(32)]
        # Add more ALU operations as needed
        else:
            return opA  # Default passthrough
    
    def _loadMemory(self, addr, funct3):
        """Load from memory based on size (funct3)"""
        if funct3 == 2:  # LW (word)
            data = int.from_bytes(self.memory[addr:addr+4], 'little')
            return intToBoolList(data, 32)
        # Add LB, LH, LBU, LHU support
        return [False] * 32
    
    def _storeMemory(self, addr, data, funct3):
        """Store to memory based on size (funct3)"""
        if funct3 == 2:  # SW (word)
            value = boolListToInt(data)
            self.memory[addr:addr+4] = value.to_bytes(4, 'little')
        # Add SB, SH support
    
    def _updatePc(self, controls, aluResult, rs1Val, rs2Val):
        """Update program counter based on control signals"""
        if controls['jump']:  # JAL
            offset = boolListToInt(controls['immediate'])
            self.pc = (self.pc + offset) & 0xFFFFFFFF
        elif controls['jumpReg']:  # JALR
            target = boolListToInt(aluResult) & 0xFFFFFFFE  # Clear LSB
            self.pc = target
        elif controls['branch']:
            # Evaluate branch condition based on funct3
            taken = self._evaluateBranch(rs1Val, rs2Val, controls['funct3'])
            if taken:
                offset = boolListToInt(controls['immediate'])
                self.pc = (self.pc + offset) & 0xFFFFFFFF
            else:
                self.pc = (self.pc + 4) & 0xFFFFFFFF
        else:
            self.pc = (self.pc + 4) & 0xFFFFFFFF
    
    def _evaluateBranch(self, rs1Val, rs2Val, funct3):
        """Evaluate branch condition"""
        rs1Int = boolListToInt(rs1Val)
        rs2Int = boolListToInt(rs2Val)
        
        if funct3 == 0:    # BEQ
            return rs1Int == rs2Int
        elif funct3 == 1:  # BNE
            return rs1Int != rs2Int
        elif funct3 == 4:  # BLT (signed)
            return rs1Int < rs2Int  # Simplified - needs proper signed comparison
        elif funct3 == 5:  # BGE (signed)
            return rs1Int >= rs2Int
        elif funct3 == 6:  # BLTU (unsigned)
            return rs1Int < rs2Int
        elif funct3 == 7:  # BGEU (unsigned)  
            return rs1Int >= rs2Int
        return False

    # def controlUnit(self,instruction):
    #     print('hi')
        
    #     opcode = instruction[:7]
    #     func3 = instruction[12:15]
    #     rd = instruction[7:12]
    #     rs1 = instruction[15:20]
    #     rs2 = instruction[20:25]
    #     func7 = instruction[25:]
    #     immed12 = instruction[21:] #21 thru 31
    #     upperImmed = instruction[12:20]

    #     rs1Dec = convertToDecimal(rs1)
    #     rs2Dec = convertToDecimal(rs2)
    #     rdDec = convertToDecimal(rd)
    #     print('rs1Dec:',rs1Dec)

    #     #register or immediate
    #     RegRegOpCode=[True,True,False,False,True,True,False]
    #     ImmedOpCode = [True,True,False,False,True,False,False]
    #     print('opcode:',opcode)
    #     print('RegRegOpCode:',RegRegOpCode)
    #     if(opcode==RegRegOpCode):
    #         print('hi')
    #         if(func3 == [False,False,False] and func7 == [False,False,False,False,False,False,False]):
    #             Result, Zero, LessThan, Overflow, CarryOut = self.alu(self.getReg(rs1Dec),self.getReg(rs2Dec),[False,False,False,False]) #reg1,reg2,aluCtrl
    #             self.setReg(rdDec,Result)
    #             print("Result:",Result)
    #             print("getRegisters:",self.getReg(rdDec))

            
    #         #func7 = instruction[25:]


    #     #Immediate
    #     if(opcode==ImmedOpCode):
    #         pass  # TODO: implement immediate operations

    #     #store
    #     if(opcode==[True,  True,  False, False, False, True,  False]):
    #         pass  # TODO: implement store operations

    #     #branch
    #     if(opcode==[True,  True,  False, False, False, True,  True ]):
    #         pass  # TODO: implement branch operations

    #     #upper immediate
    #     if(opcode==[True,True,False,False,False,False,False]):
    #         pass  # TODO: implement upper immediate operations

    #     #jump
    #     if(opcode==[True,  True,  True,  True,  False, True,  True ]):
    #         pass  # TODO: implement jump operations

    def alu(self, a,b,ctrl):

        Result, CarryOut = bitAdd(a,b,False)
        zeroBits = [False]*32
        #handling tags
        Zero = OR(Result, zeroBits)
        lt = Result[31]
        LessThan = OR(Result, lt)
        #just a placeholder for now
        Overflow = False
        return Result, Zero, LessThan, Overflow, CarryOut


# # #32bit shifter
def rTypeShift(a, val):
    if(val>0):
        append = a[:val]
        r=shiftLeft(a, val)
        return append + r
    else:
        
        append = a[len(a):len(a)-val]
        r=shiftLeft(a, val)
        return r + append



    

def testCPU32():

    # reg1=[False,False,False,False,False,False,False,False]
    # reg2=[False,False,False,False,False,False,False,False]
    # reg3=[False,False,False,False,False,False,False,False]
    add_x3_x1_x2 = [
    # OPCODE = 0110011  (LSB-first: bit0=1, bit1=1, bit2=0, bit3=0, bit4=1, bit5=1, bit6=0)
     True, True, False, False, True, True, False,

    # RD = 00011 (x3)  (LSB-first: bit7=1, bit8=1, bit9=0, bit10=0, bit11=0)
     True, True, False, False, False,

    # FUNCT3 = 000 (LSB-first: bit12=0, bit13=0, bit14=0)
     False, False, False,

    # RS1 = 00100 (x1) 
     False, False, True, False, False,

    # RS2 = 00101 (x2) 
     True, False, True, False, False,

    # FUNCT7 = 0000000 (LSB-first: bits25–31 all zero)
     False, False, False, False, False, False, False
    ]
    print("add_x3_x1_x2[:7]:",add_x3_x1_x2[:7])
    cpu = cpu_32()
    cpu.setReg(4,[False]*2 + [True]*2 + [False]*28)
    cpu.setReg(5,[False]*2 + [True]*2 + [False]*28)
    print('cpu.getReg(0):',cpu.getReg(0))
    cpu.controlUnit(add_x3_x1_x2)


    print("pos; shift left",bitShifterArthRotate32(add_x3_x1_x2,2))
    print("neg; shift right",bitShifterArthRotate32(add_x3_x1_x2,-2))
testCPU32()


# def bitFPDiv16(a, b):




#     #normalization:
#     #GRS
#     #roundup = G & (output[lsb] | R | S) 






# def bitAND32(a, b):

# def bitOR32(a, b):

# def bitXOR32(a, b):

# def bitNOT32(a):




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
    

    #testing add
    addie1=91
    addie2=10
    addie1_bool = int_to_bool_list(addie1)
    addie2_bool = int_to_bool_list(addie2)

    memory[16] = addie1_bool
    rs1reg = addie2_bool

    instr1='11000001010001001000000010000000' #load
    sliced_instructs1 = slice_instruction(instr1)
    instr2 = '11001101111100011111111110000000'
    sliced_instructs2 = slice_instruction(instr2)
    
    decoding(sliced_instructs1)
    decoding(sliced_instructs2)
    print("rs1reg:", convertToDecimal(rs1reg))
    print("rdReg",rdReg)
    print("rdreg:", convertToDecimal(rdReg))
    print("rs2Reg",rs2Reg)


    multt3_val = 325

    multt4_val = 48
    multt3 = int_to_bool_list(multt3_val)
    multt4 = int_to_bool_list(multt4_val)
    print(f"multt3: {multt3}")
    print(f"multt4: {multt4}")
    #960*64=61440
    print(f"multt1 (decimal): {convertToDecimalUnsigned(convert_bool_to_binary(multt1))}")
    print(f"multt2 (decimal): {convertToDecimalUnsigned(convert_bool_to_binary(multt2))}")
    #calculate2
    result_mult = bitMulUnsigned(multt1, multt2)
    print(f"result_mult: {result_mult}")
    print(f"Binary product: {convertToDecimalUnsigned(convert_bool_to_binary(result_mult))}")
    print(f"bool to binary: {convert_bool_to_binary(result_mult)}")
    print(f"Human readable product: {convertToString(reverseArray(convert_bool_to_binary(result_mult)))}")
    
    result_mult2 = bitMul(multt3, multt4)
    print(f"result_mult2: {result_mult2}")
    print(f"Binary product: {convertToDecimal(convert_bool_to_binary(result_mult2))}")
    print(f"bool to binary: {convert_bool_to_binary(result_mult2)}")
    print(f"Human readable product: {convertToString(reverseArray(convert_bool_to_binary(result_mult2)))}")

    # # fpb represents 
    # fpb = [
                           
        
    #     # implicit leading-1 + mantissa bits:
    #     # mantissa (binary): 1.1010000101 
    #     True, False, True, False, False, False, False, True, False, True,
    #     # exponent bits [1,0,1,1,1] (here its written in reverse, first element of array is lsb)
    #     #  → unbiased exponent = 15 − bias=0
    #     True, True, True, True, False, #exponent, stored as biased
    #     False # sign bit = 0 → positive
        
    # ]
    # # this value = 1.1010000101 (binary) × 2^0 = 1.6298828125 × 2^0 = 1.6298828125
    
    # #'temporarily changing it to be smaller:
    # #fpc represents...
    # fpc = [
    #     # mantissa (binary): 1.1010100000
        
        
        
    #     # implicit leading-1 + mantissa bits:
    #     False, False, False, False, False, True, False, True, False, True,
    #     False, True, False, True, False, ## exponent bits [0,1,0,1,0] → 
    #     #biased exponent = 10 → unbiased = -5
    #     False, # sign bit = 0 → positive
        
    # ]
    # # this value = 1.1010100000 (binary) × 2^-5 = 1.65625 × 0.03125 = 0.05175781...
        
    # result_fp = bitFPMul16(fpb, fpc)
    # print(f"result_fp: {result_fp}")
    # #print(f"Binary product: {convertToFloatingPoint(convert_bool_to_binary(result_fp))}")
    # print(f"bool to binary: {convert_bool_to_binary(result_fp)}")
    # print(f"Human readable product: {convertToString(reverseArray(convert_bool_to_binary(result_fp)))}")
    # print(f"Decimal product: {convertFloatBinaryToDecimal(result_fp)}")

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

#result_sum = testTwoNums()

#print(list(reversed(range(len(result_sum)))))




