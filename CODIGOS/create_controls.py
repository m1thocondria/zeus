from ISA import instruction_map

keys_data = list(instruction_map.keys())
intr_data = list(instruction_map.values())
intr_data.sort( key=lambda a: len(a[1]))

directory = "CIRCUITOS_SEPARADOS"


# from page 397 from the book
control_codes = "Reg2Loc ALUOp ALUSrc Branch MemRead MemWrite RegWrite MemtoReg SExt UBranch EsEstoUnMOV".split(" ")
R_fmt =    [0,2,0,0,0,0,1,0,0,0,0]
I_fmt =    [0,2,1,0,0,0,1,0,3,0,0]
IW_fmt =   [0,0,0,0,0,0,1,0,0,0,1]
LDUR_fmt = [0,0,1,0,1,0,1,1,0,0,0]
STUR_fmt = [1,0,1,0,0,1,0,0,0,0,0]
CBZ_fmt =  [1,1,0,1,0,0,0,0,2,0,0]
B_fmt =    [1,1,0,1,0,0,0,0,1,1,0]
# B_fmt =    []
# MOVZ  =    []

dict_fmt = {
    "LDUR": LDUR_fmt,
    "STUR": STUR_fmt,
    "CBZ" : CBZ_fmt,
    "B" : B_fmt
}

alu_codes = "Ainv Binv Op1 Op0".split(" ")
dict_ALOps = {
    "LDUR": [0,0,1,0],
    "STUR": [0,0,1,0],
    "CBZ" : [0,1,1,1],
}
dict_ALOps_R = {
    "AND" : [0,0,0,0],
    "ORR" : [0,0,0,1],
    "ADD" : [0,0,1,0],
    "SUB" : [0,1,1,0],
    "XOR" : [0,0,1,1],
    "NOR" : [1,1,0,0]
}

def print_header(f, name:str, ccodes=control_codes, args="opcode"):
    print("function [", end="", file=f)
    for j, ctrl in enumerate(ccodes):
        if j == len(ccodes)-1:
            print(f"{ctrl}] = {name}({args})", file=f)
        else:
            print(f"{ctrl}, ", end="", file=f)

def print_base(f, ccodes=control_codes):
    for ctrl in ccodes:
        print(f"\t{ctrl} = 0;",file=f)

def print_iftrue(f, names, values, prefix="\t\t"):
    for i,val in enumerate(values):
        if val == 0: continue
        print(f"{prefix}{names[i]} = {val};", file=f)

def is_not_inside(outer, inner) -> bool:
    if len(inner) == 1: return True
    if outer == "LSL": return True
    if outer == "LSR": return True
    res = (inner in outer)
    return not res

def alu_control():
    out_file = f"{directory}/alu_control.m"
    with open(out_file, "w") as f:
        # header
        print_header(f, "alu_control", alu_codes, "ALUOp, opcode")
        print_base(f, ccodes=alu_codes)

        print("\topcode_R = xl_slice(opcode, 31, 21);", file=f)
        print("\topcode_I = xl_slice(opcode, 31, 22);", file=f)

        # poner los codes apropiados
        print("\tswitch (ALUOp)", file=f)
        print("\t\tcase 0: % LDUR y STUR", file=f)
        print_iftrue(f, alu_codes, dict_ALOps["LDUR"], prefix="\t\t\t")
        print("\t\tcase 1: % CBZ", file=f)
        print_iftrue(f, alu_codes, dict_ALOps["CBZ"], prefix="\t\t\t")
        print("\t\tcase 2: % Formato R e I", file=f)
        # checar por toda la ISA
        print("\t\t\tswitch (opcode_R)", file=f)
        for name in instruction_map.keys():
            for alu_name in dict_ALOps_R.keys(): # checar por si se parece algun op
                if is_not_inside(name, alu_name): continue
                if instruction_map[name][0] == "I": continue
                print(f"\t\t\t\tcase {int(instruction_map[name][1],2)}: % {name}", file=f)
                print_iftrue(f, alu_codes, dict_ALOps_R[alu_name], prefix="\t\t\t\t\t")
        print("\t\t\tswitch (opcode_I)", file=f)
        for name in instruction_map.keys():
            for alu_name in dict_ALOps_R.keys(): # checar por si se parece algun op
                if is_not_inside(name, alu_name): continue
                if instruction_map[name][0] == "R": continue
                print(f"\t\t\t\tcase {int(instruction_map[name][1],2)}: % {name}", file=f)
                print_iftrue(f, alu_codes, dict_ALOps_R[alu_name], prefix="\t\t\t\t\t")

        print("end", file=f)
        print(f"[INFO] We wrote the alu controls to '{out_file}' succesfully!")


def main_control():
    first = True
    out_file = f"{directory}/control.m"
    current_key = ""
    with open(out_file, "w") as f:
        # header
        print_header(f, "control_block")
        print_base(f)

        for i,el in enumerate(intr_data):
            # start switch case
            if el[0] != current_key:
                if not first:
                    print("\tend\n", file=f) # end del switch
                else:
                    first = False
                current_key = el[0]
                print(f"\t% Formato {current_key}", file=f)
                print(f"\ttemp = xl_slice(opcode, 31, {31-len(el[1])+1});", file=f)
                print(f"\tswitch temp", file=f)
            print(f"\t\tcase {int(el[1],2)} % {keys_data[i]}", file=f)

            # flags
            if current_key == "R":
                for j, code in enumerate(control_codes):
                    if R_fmt[j] == 0: continue
                    print(f"\t\t\t{code} = {R_fmt[j]};", file=f)
                continue
            if current_key == "I":
                for j, code in enumerate(control_codes):
                    if I_fmt[j] == 0: continue
                    print(f"\t\t\t{code} = {I_fmt[j]};", file=f)
                continue
            if current_key == "IW":
                for j, code in enumerate(control_codes):
                    if IW_fmt[j] == 0: continue
                    print(f"\t\t\t{code} = {IW_fmt[j]};", file=f)
                continue

            if keys_data[i] in dict_fmt:
                for j, code in enumerate(control_codes):
                    if dict_fmt[keys_data[i]][j] == 0: continue
                    print(f"\t\t\t{code} = {dict_fmt[keys_data[i]][j]};", file=f)
                continue

        print("\tend", file=f)
        print("end", file=f)

    print(f"[INFO] We wrote the controls to {out_file} succesfully!")


if __name__ == "__main__":
    alu_control()

