from ISA import instruction_map

keys_data = list(instruction_map.keys())
intr_data = list(instruction_map.values())
intr_data.sort( key=lambda a: len(a[1]))

directory = "CIRCUITOS_SEPARADOS"


# from page 397 from the book
control_codes = "Reg2Loc ALUOp1 ALUOp0 ALUSrc Branch MemRead MemWrite RegWrite MemtoReg SExt1 SExt0".split(" ")
R_fmt =    [0,1,0,0,0,0,0,1,0,0,0]
I_fmt =    [0,1,0,1,0,0,0,1,0,1,1]
LDUR_fmt = [0,0,0,1,0,1,0,1,1,0,0]
STUR_fmt = [1,0,0,1,0,0,1,0,0,0,0]
CBZ_fmt =  [1,0,1,0,1,0,0,0,0,1,0]
# B_fmt =    []
# MOVZ  =    []

dict_fmt = {
    "LDUR": LDUR_fmt,
    "STUR": STUR_fmt,
    "CBZ" : CBZ_fmt
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
        print(f"\t{ctrl} = false;",file=f)

def alu_control():
    out_file = f"{directory}/alu_control.m"
    alu_codes = "Op0 Op1 Ainv Binv".split(" ")
    with open(out_file, "w") as f:
        # header
        print_header(f, "alu_control", alu_codes, "ALUOp")
        print_base(f)

        print("end", file=f)


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
                    print(f"\t\t\t{code} = true;", file=f)
                continue
            if current_key == "I":
                for j, code in enumerate(control_codes):
                    if I_fmt[j] == 0: continue
                    print(f"\t\t\t{code} = true;", file=f)
                continue

            if keys_data[i] in dict_fmt:
                for j, code in enumerate(control_codes):
                    if dict_fmt[keys_data[i]][j] == 0: continue
                    print(f"\t\t\t{code} = true;", file=f)
                continue

        print("\tend", file=f)
        print("end", file=f)

    print(f"[INFO] We wrote the controls to {out_file} succesfully!")


if __name__ == "__main__":
    main_control()

