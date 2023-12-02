#!/usr/bin/python3
from enum import Enum
from pathlib import Path
import argparse

suffix = "\t | "
instruction_map = {
        "B"   :("B", "000101"),
        "B.LT":("CB","01010100"),
        "CBZ" :("CB","10110100"),
        "LDUR":("D", "11111000010"),
        "STUR":("D", "11111000000"),
        "ADD" :("R", "10001000000"),
        "AND" :("R", "10001000001"),
        "ORR" :("R", "10001000010"),
        "XOR" :("R", "10001000011"),
        "SUB" :("R", "10001000100"),
        "LSR" :("R", "10001000101"),
        "LSL" :("R", "10001000110"),
        "ADDI":("I", "1001000000"),
        "ANDI":("I", "1001000000"),
        "ORRI":("I", "1001000000"),
        "XORI":("I", "1001000000"),
        "SUBI":("I", "1001000000"),
        "MOVZ":("IW","10100000000"),
        "MOVK":("IW","10100000001"),
        }

class lType(Enum):
    VACIO = 0
    COMENTARIO = 1
    TAG = 2
    INSTRUCTION = 3

def print_list(data:list, name="data"):
    endstr = ", \n"
    startstr = f"[DEBUG] {name} = ["
    for i,el in enumerate(data):
        if i == len(data)-1:
            endstr = "]\n"
        print(startstr, el, end=endstr)
        if i == 0:
            startstr = "            " + " "*len(name)

def dump_code(data:list, file:str|None = None, binary=True):
    if file is None:
        print_list(data)
        return
    if binary:
        with open(file, "w") as f:
            for line in data:
                print(line, file=f)
    else:
        with open(file, "w") as f:
            print([int(a,2) for a in data], file=f)
            # for line in data:
            #     print(int(line, 2), file=f)

def parse_line(line:str) -> (lType, tuple[str]):
    """
    Se devuelve (tipo:lType, argumentos:str)
    No hace analisis semantico
    """
    line = line.strip()
    if line == "": return (lType.VACIO, (""))
    # Ignorar comentarios
    com = line.find(";")
    if com != -1:
        comentario = line[com:]
        line = line[:com]
    if line == "": return (lType.COMENTARIO, (comentario))
    # Checar si es una etiqueta
    tag = line.find(":")
    if tag != -1: return (lType.TAG, (line[:tag]))
    # Entonces es un posible comando
    line = line.lstrip()
    ws = line.find(" ")
    cmd = line[:ws]
    line = line[ws:]
    args = [arg.strip() for arg in line.split(",")]
    args.insert(0, cmd)
    return (lType.INSTRUCTION, args)

def to2comp(num:int, size:int):
    num = int(num)
    signed = num < 0
    if signed:
        if abs(num) > 2**(size-1):
            raise ValueError(f"Num '{num}' is too small to be represented by {size} bits")
        b = bin(num + 1)
        bnum = b[3:]
    else:
        if abs(num) > 2**(size-1) - 1:
            raise ValueError(f"Num '{num}' is too big to be represented by {size} bits")
        b = bin(num)
        bnum = b[2:]

    diff = size - len(bnum)
    if diff > 0:
        bnum = "0"*diff + bnum

    if signed:
        bnum = bnum.replace("0", "2")
        bnum = bnum.replace("1", "0")
        bnum = bnum.replace("2", "1")

    return bnum

def tobits(num:int, size:int) -> str:
    b = bin(num)[2:]
    diff = size - len(b)
    if diff > 0:
        res = "0"*diff + b
    if diff < 0:
        raise ValueError(f"'{num}' can't be represented in a unsigned {size} bit number.")
    return res

def reg_to_bits(reg:str):
    # Assumes reg is 2 char long, of the format xn
    if reg[0].lower() != "x":
        raise ValueError(f"Registros tienen nombre XN, no {reg[0]}.")
    try:
        num = int(reg[1:])
    except Exception as e:
        raise ValueError(f"{num} no es un numero")
    if num < 0 or num > 31:
        raise ValueError(f"No tenemos registro X{num}, el rango de registros es de X0 a X31.")
    return tobits(num, 5)

def parse_args(tipo:str, args:list[str], noLine:int, tags:dict[str, int]) -> list[str]:
    def check_argument_len(nargs:int, desired:int, itype:str):
        if nargs > desired:
            raise ValueError(f"Too many arguments ({args = }) for {itype} type instruction, expected {desired}.")
        if nargs < desired:
            raise ValueError(f"Too few arguments ({args = }) for {itype} type instruction, expected {desired}.")

    result = []
    # Se asume que args tiene tamaño >= 1
    match tipo:
        case "B":
            check_argument_len(len(args), 1, "B")
            tag = args[0].strip()
            if not tag in tags:
                raise ValueError(f"There is no tag '{tag}' in source.")
            offset = tags[tag] - noLine
            result.append( to2comp(offset, 26) )
        case "CB":
            check_argument_len(len(args), 2, "B")
            # offset
            tag = args[1].strip()
            if not tag in tags:
                raise ValueError(f"There is no tag '{tag}' in source.")
            offset = tags[tag] - noLine
            result.append( to2comp(offset, 19) )
            # register
            result.append( reg_to_bits(args[0].strip()) )
        case "D":
            check_argument_len(len(args), 3, "D")
            # address
            addr = args[2].replace("]","").replace("#","").strip()
            result.append( tobits(int(addr), 9) )
            # op
            result.append( tobits(0, 2) )
            # Rn
            reg = args[1].replace("[","").strip()
            result.append( reg_to_bits(reg) )
            # Rt
            result.append( reg_to_bits(args[0].strip()) )
        case "R":
            check_argument_len(len(args), 3, "R")
            # Rm
            result.append( reg_to_bits(args[1].strip()) )
            # shamt
            result.append( tobits(0, 6) )
            # Rn
            result.append( reg_to_bits(args[2].strip()) )
            # Rd
            result.append( reg_to_bits(args[0].strip()) )
        case "I":
            check_argument_len(len(args), 3, "I")
            # inmmediate
            result.append( to2comp( int(args[2].replace("#","").strip()), 12) )
            # Rn
            result.append( reg_to_bits( args[1].strip()) )
            # Rd
            result.append( reg_to_bits( args[0].strip()) )
        case "IW":
            check_argument_len(len(args), 2, "IW")
            # mov inmmediate
            result.append( to2comp( int(args[1].replace("#","").strip()), 16) )
            # Rd
            result.append( reg_to_bits( args[0].strip()) )
        case _:
            raise NotImplementedError(f"Tipo de instruccion \"{tipo}\" no implementado.")
    return result


def main(file, dump = None):
    tags = dict()
    instructions = []
    for_later = []
    lines = []
    with open(file, "r") as f:
        for i,line in enumerate(f):
            res = parse_line(line)
            if res[0] == lType.VACIO or res[0] == lType.COMENTARIO:
                continue
            if res[0] == lType.TAG:
                tags[res[1]] = i
            if res[0] == lType.INSTRUCTION:
                for_later.append((i,res[1]))
                lines.append(line)

    # Ahora que ya sabemos todas las tags podemos trabajar
    for i,inst in enumerate(for_later):
        noLine = inst[0]
        cmd = inst[1][0]
        args = inst[1][1:]

        if not cmd in instruction_map:
            raise ValueError(f"[ERROR] {file}:{noLine}. {cmd} no es una instruccion soportada.")
        if len(args) == 0:
            raise ValueError(f"[ERROR] {file}:{noLine}. {cmd} no tiene suficientes argumentos.")

        inst_type, opcode = instruction_map[cmd]

        try:
            args_list = parse_args(inst_type, args, noLine, tags)
        except Exception as e:
            print(f"[ERROR] {file}:{noLine}. Couldn't parse instruction:")
            print(f"{suffix}{e}")
            print(f"{suffix}{noLine} > '{lines[i][:-1]}'")
            break

        args_list.insert(0, opcode )
        code = "".join(args_list)
        instructions.append( code )

    if dump is None:
        dump = f"{file.stem}.out"
    dump_code(instructions, dump, binary=False)
    print(f"[INFO] '{file}' was assemble successfully!")
    # print_list([len(ins) for ins in instructions])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Assemble assembly code.')
    parser.add_argument('filename', type=str, nargs="+",
                        help='ARM(legv8) assembly code to assemble.')
    parser.add_argument("-o",'--out', type=str, nargs="*", help='Output file to dump native code. (default="filename".out)')
    args = parser.parse_args()

    if args.out is not None:
        if len(args.out) != len(args.filename):
            print(f"[ERROR] The outfile parameters(size={len(args.out)}) doesn't have the same size as the infile parameters(size={len(args.filename)}).")
            exit(1)
        outs = args.out
    else:
        outs = [None]*len(args.filename)
    # print(args.out, args.filename, sep="\n")
    # exit(69)
    for i,file in enumerate(args.filename):
        main(Path(file), outs[i])
