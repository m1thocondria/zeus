function [ForwardA, ForwardB] = control_block(Rn, Rm, EX_MEM_Rd, MEM_WB_Rd)
    % pag 318
	ForwardA = 0;
	ForwardB = 0;
    if Rn == EX_MEM_Rd
        ForwardA = 1;
    end
    if Rm == EX_MEM_Rd
        ForwardB = 1;
    end
    if Rn == MEM_WB_Rd
        ForwardA = 2;
    end
    if Rm == MEM_WB_Rd
        ForwardB = 2;
    end
end
