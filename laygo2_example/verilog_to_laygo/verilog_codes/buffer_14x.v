////////////////////////////////////////////
//                                        //
//           buffer verilog code          //
//          Created by S.Y. LEE           //
//                                        //
////////////////////////////////////////////

module buffer_14x(I, O);
    input I;
    output wire O;

    wire w1;

    inv_14x inv0(.I(I), .O(w1));
    inv_14x inv1(.I(w1), .O(O));
endmodule