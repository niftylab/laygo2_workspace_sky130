v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N 200 -290 240 -290 {
lab=#net1}
N 200 -100 240 -100 {
lab=#net2}
N 200 90 240 90 {
lab=#net3}
N 200 280 240 280 {
lab=#net4}
N -40 -420 -40 -310 {
lab=#net5}
N -40 -310 70 -310 {
lab=#net5}
N -40 -310 -40 70 {
lab=#net5}
N -40 70 70 70 {
lab=#net5}
N -140 -600 -140 -120 {
lab=A0}
N -140 -120 70 -120 {
lab=A0}
N -140 -120 -140 260 {
lab=A0}
N -140 260 70 260 {
lab=A0}
N -140 -560 -40 -560 {
lab=A0}
N -310 -420 -310 -290 {
lab=#net6}
N -310 -290 70 -290 {
lab=#net6}
N -310 -290 -310 90 {
lab=#net6}
N -310 90 70 90 {
lab=#net6}
N -440 -600 -440 -100 {
lab=A1}
N -440 -100 70 -100 {
lab=A1}
N -440 280 70 280 {
lab=A1}
N -440 -100 -440 280 {
lab=A1}
N -440 -560 -310 -560 {
lab=A1}
N -270 -500 -250 -500 {
lab=VDD}
N -370 -500 -350 -500 {
lab=VSS}
N -100 -500 -80 -500 {
lab=VSS}
N 0 -500 20 -500 {
lab=VDD}
N 120 -360 120 -340 {
lab=VDD}
N 120 -360 200 -360 {
lab=VDD}
N 300 -360 300 -330 {
lab=VDD}
N 200 -360 300 -360 {
lab=VDD}
N 120 -170 120 -150 {
lab=VDD}
N 120 -170 200 -170 {
lab=VDD}
N 300 -170 300 -140 {
lab=VDD}
N 200 -170 300 -170 {
lab=VDD}
N 120 20 120 40 {
lab=VDD}
N 120 20 200 20 {
lab=VDD}
N 300 20 300 50 {
lab=VDD}
N 200 20 300 20 {
lab=VDD}
N 120 -240 120 -220 {
lab=VSS}
N 120 -220 220 -220 {
lab=VSS}
N 300 -250 300 -220 {
lab=VSS}
N 220 -220 300 -220 {
lab=VSS}
N 120 -50 120 -30 {
lab=VSS}
N 120 -30 220 -30 {
lab=VSS}
N 300 -60 300 -30 {
lab=VSS}
N 220 -30 300 -30 {
lab=VSS}
N 120 140 120 160 {
lab=VSS}
N 120 160 220 160 {
lab=VSS}
N 300 130 300 160 {
lab=VSS}
N 220 160 300 160 {
lab=VSS}
N 120 330 120 350 {
lab=VSS}
N 120 350 220 350 {
lab=VSS}
N 300 320 300 350 {
lab=VSS}
N 220 350 300 350 {
lab=VSS}
N 120 210 120 230 {
lab=VDD}
N 120 210 200 210 {
lab=VDD}
N 300 210 300 240 {
lab=VDD}
N 200 210 300 210 {
lab=VDD}
N -560 -270 70 -270 {
lab=EN}
N -560 -600 -560 -270 {
lab=EN}
N -560 -270 -560 -80 {
lab=EN}
N -560 -80 70 -80 {
lab=EN}
N -560 -80 -560 110 {
lab=EN}
N -560 110 70 110 {
lab=EN}
N -560 110 -560 300 {
lab=EN}
N -560 300 70 300 {
lab=EN}
N 380 -290 400 -290 {}
N 380 -100 400 -100 {}
N 380 90 400 90 {}
N 380 280 400 280 {}
C {xschem_lib/nand_3in.sym} 90 -260 0 0 {name=X_nand1}
C {xschem_lib/inv.sym} 240 -250 0 0 {name=X_inv1 NF=2}
C {xschem_lib/nand_3in.sym} 90 -70 0 0 {name=X_nand2}
C {xschem_lib/inv.sym} 240 -60 0 0 {name=X_inv3 NF=2}
C {xschem_lib/nand_3in.sym} 90 120 0 0 {name=X_nand3}
C {xschem_lib/inv.sym} 240 130 0 0 {name=X_inv4 NF=2}
C {xschem_lib/nand_3in.sym} 90 310 0 0 {name=X_nand5}
C {xschem_lib/inv.sym} 240 320 0 0 {name=X_inv6 NF=2}
C {xschem_lib/inv.sym} -80 -560 1 0 {name=X_inv2 NF=2}
C {xschem_lib/inv.sym} -350 -560 1 0 {name=X_inv5 NF=2}
C {ipin.sym} -140 -600 1 0 {name=p1 lab=A0}
C {ipin.sym} -440 -600 1 0 {name=p3 lab=A1}
C {iopin.sym} -250 -500 0 0 {name=p2 lab=VDD}
C {iopin.sym} -370 -500 2 0 {name=p4 lab=VSS}
C {lab_wire.sym} -100 -500 0 0 {name=l1 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 20 -500 2 0 {name=l2 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 200 -360 2 0 {name=l3 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 200 -170 2 0 {name=l4 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 200 20 2 0 {name=l5 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 220 -220 0 0 {name=l6 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 220 -30 0 0 {name=l7 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 220 160 0 0 {name=l8 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 220 350 0 0 {name=l9 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 200 210 2 0 {name=l10 sig_type=std_logic lab=VDD}
C {ipin.sym} -560 -600 1 0 {name=p5 lab=EN}
C {opin.sym} 400 -290 0 0 {name=p6 lab=Y0}
C {opin.sym} 400 -100 0 0 {name=p7 lab=Y1}
C {opin.sym} 400 90 0 0 {name=p8 lab=Y2}
C {opin.sym} 400 280 0 0 {name=p9 lab=Y3}
