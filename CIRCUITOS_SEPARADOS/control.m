function [Reg2Loc, ALUOp1, ALUOp0, ALUSrc, Branch, MemRead, MemWrite, RegWrite, MemtoReg] = control_block(opcode)
    Reg2Loc = false;
    ALUOp0 = false;
    ALUOp1 = false;
    ALUSrc = false;
    Branch = false;
    MemRead = false;
    MemWrite = false;
    RegWrite = false;
    MemtoReg = false;

    % Formato B
    temp = xl_slice(opcode, 31, 26);
    switch temp
        case 5 % B
    end

    % Formato CB
    temp = xl_slice(opcode, 31, 24);
    switch temp
        case 84 % B.LT
        case 180 % CBZ
            Reg2Loc = true;
            ALUOp0 = true;
            Branch = true;
    end

    % Formato I - ignore for now
    % temp = xl_slice(opcode, 31, 22);
    % switch temp
    %     case 576 % ADDI
    %     case 576 % ANDI
    %     case 576 % ORRI
    %     case 576 % XORI
    %     case 576 % SUBI
    % end

    % Formato D
    temp = xl_slice(opcode, 31, 21);
    switch temp
        case 1986 % LDUR
            ALUSrc = true;
            MemRead = true;
            RegWrite = true;
            MemtoReg = true;
        case 1984 % STUR
            Reg2Loc = true;
            ALUSrc = true;
            MemWrite = true;
    end

    % Formato R
    temp = xl_slice(opcode, 31, 21);
    switch temp
        case 1088 % ADD
            ALUOp1 = true;
            RegWrite = true;
        case 1089 % AND
            ALUOp1 = true;
            RegWrite = true;
        case 1090 % ORR
            ALUOp1 = true;
            RegWrite = true;
        case 1091 % XOR
            ALUOp1 = true;
            RegWrite = true;
        case 1092 % SUB
            ALUOp1 = true;
            RegWrite = true;
        case 1093 % LSR
            ALUOp1 = true;
            RegWrite = true;
        case 1094 % LSL
            ALUOp1 = true;
            RegWrite = true;
    end

    % Formato IW
    temp = xl_slice(opcode, 31, 21);
    switch temp
        case 1280 % MOVZ
        case 1281 % MOVK
    end
end
