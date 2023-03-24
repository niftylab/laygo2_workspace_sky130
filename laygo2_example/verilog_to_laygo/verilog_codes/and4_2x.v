////////////////////////////////////////////
//                                        //
//            AND4 verilog code           //
//          Created by J.Y. PARK          //
//                                        //
////////////////////////////////////////////

module and4_2x(A, B, C, D, Y);
    input A, B, C, D;
    output wire Y;

    wire w1;
    wire w2;
    
    nand_2x nand0(.A(C), .B(D), .OUT(w1));
    nand_2x nand1(.A(A), .B(B), .OUT(w2));
    nor_2x nor0(.A(w2), .B(w1), .OUT(Y));
endmodule