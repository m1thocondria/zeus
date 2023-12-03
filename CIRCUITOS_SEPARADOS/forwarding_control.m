function [ForwardA, ForwardB] = control_block(Rn, Rm, EX_MEM_Rd, MEM_WB_Rd)
    % pag 318
	ForwardA = xfix({xlUnsigned, 2, 0}, 0);
	ForwardB = xfix({xlUnsigned, 2, 0}, 0);
    if Rn == EX_MEM_Rd
        ForwardA = xfix({xlUnsigned, 2, 0}, 1);
    end
    if Rm == EX_MEM_Rd
        ForwardB = xfix({xlUnsigned, 2, 0}, 1);
    end
    if Rn == MEM_WB_Rd
        ForwardA = xfix({xlUnsigned, 2, 0}, 2);
    end
    if Rm == MEM_WB_Rd
        ForwardA = xfix({xlUnsigned, 2, 0}, 2);
    end
end
