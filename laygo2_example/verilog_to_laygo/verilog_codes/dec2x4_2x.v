////////////////////////////////////////////
//                                        //
//         decoder2x4 verilog code        //
//          Created by S.Y. LEE           //
//                                        //
////////////////////////////////////////////

module dec2x4_2x(A0, A1, EN, Y0, Y1, Y2, Y3);
    input A0, A1, EN;
    output Y0, Y1, Y2, Y3;
    
    wire A0bar;
    wire A1bar;
    wire w0, w1, w2, w3;

    inv_2x inv0(.O(A0bar), .I(A0));
    inv_2x inv1(.O(A1bar), .I(A1));
    
    nand3_2x nand3_0(.A(A0bar), .B(A1bar), .C(EN), .Y(w0));
    inv_2x inv_0(.I(w0), .O(Y0));
    nand3_2x nand3_1(.A(A0), .B(A1bar), .C(EN), .Y(w1));
    inv_2x inv_1(.I(w1), .O(Y1));
    nand3_2x nand3_2(.A(A0bar), .B(A1), .C(EN), .Y(w2));
    inv_2x inv_2(.I(w2), .O(Y2));
    nand3_2x nand3_3(.A(A0), .B(A1), .C(EN), .Y(w3));
    inv_2x inv_3(.I(w3), .O(Y3));

endmodule