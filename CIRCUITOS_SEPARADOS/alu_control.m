function [Op0, Op1, Ainv, Binv] = alu_control(ALUOp, opcode)
	Op1 = false;
	Op0 = false;
	Ainv = false;
	Binv = false;

    % pag 272 del libro
    switch ALUOp
        case 0 % LD y STR
            Op1 = true;
        case 1 % CBZ
            Op0 = true;
            Op1 = true;
            Binv = true;
        case 2 % R
            % pag 356 del libro
            switch opcode
                case 1088 % ADD
                    Op1 = true;
                case 1092 % SUB
                    Binv = true;
                    Op1 = true;
                case 1090 % ORR
                    Op0 = true;
                case 1089 % AND
            end
    end
end
