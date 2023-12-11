from ISA import instruction_map

out_file = "ISA.txt"

fmt = "| {:<6} | {:<8} | {:<16} |"

MAX_LEN = 11

with open(out_file, "w") as f:
    header = fmt.format("INST","DEC","BIN")
    print(header, file=f)
    print("+"*len(header), file=f)
    for keys, vals in instruction_map.items():
        new_bin = vals[1] + "0"*(MAX_LEN - len(vals[1]))
        print(fmt.format(keys, int(new_bin, 2), new_bin), file=f)


