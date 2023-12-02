from ISA import instruction_map

keys_data = list(instruction_map.keys())
intr_data = list(instruction_map.values())
intr_data.sort( key=lambda a: len(a[1]))

current_key = ""

# from page 397 from the book
control_codes = "Reg2Loc ALUOp1 ALUOp0 ALUSrc Branch MemRead MemWrite RegWrite MemtoReg".split(" ")
R_fmt =    [0,1,0,0,0,0,0,1,0]
LDUR_fmt = [0,0,0,1,0,1,0,1,1]
STUR_fmt = [1,0,0,1,0,0,1,0,0]
CBZ_fmt =  [1,0,1,0,1,0,0,0,0]

dict_fmt = {
    "LDUR": LDUR_fmt,
    "STUR": STUR_fmt,
    "CBZ" : CBZ_fmt
}

out_file = "control.m"
with open(out_file, "w") as f:
    for i,el in enumerate(intr_data):
        if el[0] != current_key:
            current_key = el[0]
            print(f"end\n\n% Formato {current_key}", file=f)
            print(f"temp = xl_slice(opcode, 31, {31-len(el[1])+1});", file=f)
            print(f"switch temp", file=f)
        print(f"\tcase {int(el[1],2)} % {keys_data[i]}", file=f)

        if current_key == "R":
            for j, code in enumerate(control_codes):
                if R_fmt[j] == 0: continue
                print(f"\t\t{code} = true;", file=f)

        if keys_data[i] in dict_fmt:
            for j, code in enumerate(control_codes):
                if dict_fmt[keys_data[i]][j] == 0: continue
                print(f"\t\t{code} = true;", file=f)

print(f"[INFO] We wrote the controls to {out_file} succesfully!")




