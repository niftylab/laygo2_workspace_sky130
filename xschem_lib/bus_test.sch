v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N 360 -280 360 -100 {bus=true
lab=#net1}
N -40 -260 -40 -80 {bus=true
lab=Di[7:0]}
N 0 -250 60 -250 {
lab=Di[0]}
N 0 -230 60 -230 {
lab=Di[1]}
N 0 -210 60 -210 {
lab=Di[2]}
N -0 -190 60 -190 {
lab=Di[3]}
N 0 -170 60 -170 {
lab=Di[4]}
N 0 -150 60 -150 {
lab=Di[5]}
N 0 -130 60 -130 {
lab=Di[6]}
N 0 -110 60 -110 {
lab=Di[7]}
N 280 -270 360 -270 {
lab=#net1}
N 280 -250 360 -250 {
lab=#net1}
N 280 -230 360 -230 {
lab=#net1}
N 280 -210 360 -210 {
lab=#net1}
N 280 -190 360 -190 {
lab=#net1}
N 280 -170 360 -170 {
lab=#net1}
N 280 -150 360 -150 {
lab=#net1}
N 280 -130 360 -130 {
lab=#net1}
N 280 -310 300 -310 {
lab=VDD}
N 280 -290 330 -290 {
lab=VSS}
N 330 -310 330 -290 {
lab=VSS}
N 0 -270 60 -270 {
lab=CLK}
N 0 -300 0 -270 {
lab=CLK}
N 10 -290 60 -290 {
lab=SEL}
N 10 -330 10 -290 {
lab=SEL}
N 0 -330 10 -330 {
lab=SEL}
N 20 -310 60 -310 {
lab=WE}
N 20 -360 20 -310 {
lab=WE}
N -0 -360 20 -360 {
lab=WE}
N -30 -110 -0 -110 {
lab=Di[7]}
N -30 -250 -0 -250 {
lab=Di[0]}
N -30 -230 -0 -230 {
lab=Di[1]}
N -30 -210 -0 -210 {
lab=Di[2]}
N -30 -190 -0 -190 {
lab=Di[3]}
N -30 -170 -0 -170 {
lab=Di[4]}
N -30 -150 -0 -150 {
lab=Di[5]}
N -30 -130 -0 -130 {
lab=Di[6]}
C {xschem_lib/byte_dff.sym} 170 -210 0 0 {name=xByte_1 NF=2}
C {bus_connect.sym} 360 -110 1 0 {name=l2 lab=Do[7:0]}
C {iopin.sym} 230 -400 0 0 {name=p1 lab=VDD}
C {iopin.sym} 230 -370 0 0 {name=p2 lab=VSS}
C {lab_wire.sym} 300 -310 1 0 {name=l3 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 330 -310 1 0 {name=l4 sig_type=std_logic lab=VSS}
C {ipin.sym} 0 -360 0 0 {name=p3 lab=WE}
C {ipin.sym} 0 -330 0 0 {name=p4 lab=SEL}
C {ipin.sym} 0 -300 0 0 {name=p5 lab=CLK}
C {lab_pin.sym} -40 -260 0 0 {name=l1 sig_type=std_logic lab=Di[7:0]}
C {bus_connect_nolab.sym} -30 -110 2 0 {name=r1}
C {bus_connect_nolab.sym} -30 -130 2 0 {name=r2}
C {bus_connect_nolab.sym} -30 -150 2 0 {name=r3}
C {bus_connect_nolab.sym} -30 -170 2 0 {name=r4}
C {bus_connect_nolab.sym} -30 -190 2 0 {name=r5}
C {bus_connect_nolab.sym} -30 -210 2 0 {name=r6}
C {bus_connect_nolab.sym} -30 -230 2 0 {name=r7}
C {bus_connect_nolab.sym} -30 -250 2 0 {name=r8}
C {lab_wire.sym} 30 -110 0 0 {name=l5 sig_type=std_logic lab=Di[7]}
C {lab_wire.sym} 30 -130 0 0 {name=l6 sig_type=std_logic lab=Di[6]}
C {lab_wire.sym} 30 -150 0 0 {name=l7 sig_type=std_logic lab=Di[5]}
C {lab_wire.sym} 30 -170 0 0 {name=l8 sig_type=std_logic lab=Di[4]}
C {lab_wire.sym} 30 -190 0 0 {name=l9 sig_type=std_logic lab=Di[3]}
C {lab_wire.sym} 30 -210 0 0 {name=l10 sig_type=std_logic lab=Di[2]}
C {lab_wire.sym} 30 -230 0 0 {name=l11 sig_type=std_logic lab=Di[1]}
C {lab_wire.sym} 30 -250 0 0 {name=l12 sig_type=std_logic lab=Di[0]}
