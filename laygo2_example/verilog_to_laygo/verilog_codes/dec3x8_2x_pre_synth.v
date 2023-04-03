////////////////////////////////////////////
//                                        //
//         decoder3x8 verilog code        //
//            pre yosys synthesis         //
//           Created by S.Y. LEE          //
//                                        //
////////////////////////////////////////////

module dec3x8_2x(A0, A1, A2, EN, O);
    input A0, A1, A2, EN;
    output wire [7:0] O;
    
    always @(*) begin
        case({EN,A2,A1,A0})
            4'b1000 : O = 8'b00000001;
            4'b1001 : O = 8'b00000010;
            4'b1010 : O = 8'b00000100;
            4'b1011 : O = 8'b00001000;
            4'b1100 : O = 8'b00010000;
            4'b1101 : O = 8'b00100000;
            4'b1110 : O = 8'b01000000;
            4'b1111 : O = 8'b10000000;
            default : O = 8'b00000000;
        endcase
    end

endmodule