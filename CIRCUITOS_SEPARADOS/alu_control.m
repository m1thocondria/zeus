function [Op1, Op0, Ainv, Binv] = alu_control(ALUOp, opcode)
	Op1 = 0;
	Op0 = 0;
	Ainv = 0;
	Binv = 0;
	opcode_R = xl_slice(opcode, 31, 21);
	opcode_I = xl_slice(opcode, 31, 22);
	switch ALUOp
		case 0 % LDUR y STUR
			Op1 = 1;
		case 1 % CBZ
		case 2 % Formato R e I
			switch opcode_R
				case 1088 % ADD
					Op1 = 1;
				case 1089 % AND
				case 1090 % ORR
					Op0 = 1;
				case 1091 % XOR
					Op1 = 1;
					Op0 = 1;
				case 1092 % NOR
					Ainv = 1;
					Binv = 1;
				case 1093 % SUB
					Op1 = 1;
					Binv = 1;
			end
			switch opcode_I
				case 576 % ADDI
					Op1 = 1;
				case 577 % ANDI
				case 578 % ORRI
					Op0 = 1;
				case 579 % XORI
					Op1 = 1;
					Op0 = 1;
				case 580 % SUBI
					Op1 = 1;
					Binv = 1;
				case 581 % NORI
					Ainv = 1;
					Binv = 1;
			end
	end
end
