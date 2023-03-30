////////////////////////////////////////////
//                                        //
//           buffer verilog code          //
//          Created by J.Y. PARK          //
//                                        //
////////////////////////////////////////////

module buffer_24x(I, O);
    input I;
    output wire O;

    wire w1;

    inv_24x inv0(.I(I), .O(w1));
    inv_24x inv1(.I(w1), .O(O));
endmodule