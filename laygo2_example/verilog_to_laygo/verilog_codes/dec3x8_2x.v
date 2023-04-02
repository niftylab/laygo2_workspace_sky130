////////////////////////////////////////////
//                                        //
//         decoder3x8 verilog code        //
//          Created by S.Y. LEE           //
//                                        //
////////////////////////////////////////////

module dec3x8_2x(A0, A1, A2, EN, Y0, Y1, Y2, Y3, Y4, Y5, Y6, Y7);
    input A0, A1, A2, EN;
    output Y0, Y1, Y2, Y3, Y4, Y5, Y6, Y7;
    
    wire A0bar;
    wire A1bar;
    wire A1bar;

    inv_2x inv0(.O(A0bar), .I(A0));
    inv_2x inv1(.O(A1bar), .I(A1));
    inv_2x inv2(.O(A2bar), .I(A2));

    and4_2x and4_0(.A(A0bar), .B(A1bar), .C(A2bar), .D(EN), .Y(Y0));
    and4_2x and4_1(.A(A0), .B(A1bar), .C(A2bar), .D(EN), .Y(Y1));
    and4_2x and4_2(.A(A0bar), .B(A1), .C(A2bar), .D(EN), .Y(Y2));
    and4_2x and4_3(.A(A0), .B(A1), .C(A2bar), .D(EN), .Y(Y3));
    and4_2x and4_4(.A(A0bar), .B(A1bar), .C(A2), .D(EN), .Y(Y4));
    and4_2x and4_5(.A(A0), .B(A1bar), .C(A2), .D(EN), .Y(Y5));
    and4_2x and4_6(.A(A0bar), .B(A1), .C(A2), .D(EN), .Y(Y6));
    and4_2x and4_7(.A(A0), .B(A1), .C(A2), .D(EN), .Y(Y7));

endmodule