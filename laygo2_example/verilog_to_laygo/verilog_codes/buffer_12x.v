////////////////////////////////////////////
//                                        //
//           buffer verilog code          //
//          Created by J.Y. PARK          //
//                                        //
////////////////////////////////////////////

module buffer_12x(I, O);
    input I;
    output wire O;

    wire w1;

    inv_12x inv0(.I(I), .O(w1));
    inv_12x inv1(.I(w1), .O(O));
endmodule