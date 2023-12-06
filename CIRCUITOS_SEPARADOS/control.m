function [Reg2Loc, ALUOp, ALUSrc, Branch, MemRead, MemWrite, RegWrite, MemtoReg, SExt, UBranch, EsEstoUnMOV] = control_block(opcode)
	Reg2Loc = 0;
	ALUOp = 0;
	ALUSrc = 0;
	Branch = 0;
	MemRead = 0;
	MemWrite = 0;
	RegWrite = 0;
	MemtoReg = 0;
	SExt = 0;
	UBranch = 0;
	EsEstoUnMOV = 0;
	% Formato B
	temp = xl_slice(opcode, 31, 26);
	switch temp
		case 5 % B
			Reg2Loc = 1;
			ALUOp = 1;
			Branch = 1;
			SExt = 1;
			UBranch = 1;
	end

	% Formato CB
	temp = xl_slice(opcode, 31, 24);
	switch temp
		case 180 % CBZ
			Reg2Loc = 1;
			ALUOp = 1;
			Branch = 1;
			SExt = 2;
	end

	% Formato IW
	temp = xl_slice(opcode, 31, 23);
	switch temp
		case 320 % MOVZ
			RegWrite = 1;
			EsEstoUnMOV = 1;
		case 321 % MOVK
			RegWrite = 1;
			EsEstoUnMOV = 1;
	end

	% Formato I
	temp = xl_slice(opcode, 31, 22);
	switch temp
		case 576 % ADDI
			ALUOp = 2;
			ALUSrc = 1;
			RegWrite = 1;
			SExt = 3;
		case 577 % ANDI
			ALUOp = 2;
			ALUSrc = 1;
			RegWrite = 1;
			SExt = 3;
		case 578 % ORRI
			ALUOp = 2;
			ALUSrc = 1;
			RegWrite = 1;
			SExt = 3;
		case 579 % XORI
			ALUOp = 2;
			ALUSrc = 1;
			RegWrite = 1;
			SExt = 3;
		case 580 % SUBI
			ALUOp = 2;
			ALUSrc = 1;
			RegWrite = 1;
			SExt = 3;
		case 581 % NORI
			ALUOp = 2;
			ALUSrc = 1;
			RegWrite = 1;
			SExt = 3;
	end

	% Formato D
	temp = xl_slice(opcode, 31, 21);
	switch temp
		case 1986 % LDUR
			ALUSrc = 1;
			MemRead = 1;
			RegWrite = 1;
			MemtoReg = 1;
		case 1984 % STUR
			Reg2Loc = 1;
			ALUSrc = 1;
			MemWrite = 1;
	end

	% Formato R
	temp = xl_slice(opcode, 31, 21);
	switch temp
		case 1088 % ADD
			ALUOp = 2;
			RegWrite = 1;
		case 1089 % AND
			ALUOp = 2;
			RegWrite = 1;
		case 1090 % ORR
			ALUOp = 2;
			RegWrite = 1;
		case 1091 % XOR
			ALUOp = 2;
			RegWrite = 1;
		case 1092 % NOR
			ALUOp = 2;
			RegWrite = 1;
		case 1093 % SUB
			ALUOp = 2;
			RegWrite = 1;
		case 1125 % LSR
			ALUOp = 2;
			RegWrite = 1;
		case 1126 % LSL
			ALUOp = 2;
			RegWrite = 1;
	end
end
