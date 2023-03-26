v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N 740 -670 740 -590 {
lab=A0}
N 390 -670 390 -590 {
lab=A1}
N 50 -670 50 -590 {
lab=A2}
N 50 -630 210 -630 {
lab=A2}
N 390 -630 560 -630 {
lab=A1}
N 740 -630 920 -630 {
lab=A0}
N 920 770 1010 770 {
lab=#net1}
N 740 950 1010 950 {
lab=A0}
N 560 -490 560 570 {
lab=#net2}
N 560 570 1010 570 {
lab=#net2}
N 390 -490 390 930 {
lab=A1}
N 390 930 1010 930 {
lab=A1}
N 50 -490 50 900 {
lab=A2}
N 50 900 50 910 {
lab=A2}
N 50 910 50 920 {
lab=A2}
N 50 920 1010 920 {
lab=A2}
N 210 -490 210 200 {
lab=#net3}
N 210 200 1010 200 {
lab=#net3}
N 390 750 1010 750 {
lab=A1}
N 50 740 1010 740 {
lab=A2}
N 740 590 1010 590 {
lab=A0}
N 50 560 1010 560 {
lab=A2}
N 920 420 1010 420 {
lab=#net1}
N 560 400 1010 400 {
lab=#net2}
N 740 230 1010 230 {
lab=A0}
N 390 210 1010 210 {
lab=A1}
N 920 40 1010 40 {
lab=#net1}
N 390 20 1010 20 {
lab=A1}
N 210 10 1010 10 {
lab=#net3}
N 50 390 1010 390 {
lab=A2}
N 740 -160 1010 -160 {
lab=A0}
N 560 -180 1010 -180 {
lab=#net2}
N 210 -190 1010 -190 {
lab=#net3}
N 920 -350 1010 -350 {
lab=#net1}
N 560 -370 1010 -370 {
lab=#net2}
N 210 -380 1010 -380 {
lab=#net3}
N 1080 -410 1100 -410 {
lab=VDD}
N 1080 -220 1100 -220 {
lab=VDD}
N 1080 -20 1100 -20 {
lab=VDD}
N 1080 170 1100 170 {
lab=VDD}
N 1080 360 1100 360 {
lab=VDD}
N 1080 530 1100 530 {
lab=VDD}
N 1080 710 1100 710 {
lab=VDD}
N 1080 890 1100 890 {
lab=VDD}
N 1080 -310 1100 -310 {
lab=VSS}
N 1080 -120 1100 -120 {
lab=VSS}
N 1080 80 1100 80 {
lab=VSS}
N 1080 270 1100 270 {
lab=VSS}
N 1080 460 1100 460 {
lab=VSS}
N 1080 630 1100 630 {
lab=VSS}
N 1080 810 1100 810 {
lab=VSS}
N 1080 990 1100 990 {
lab=VSS}
N 250 -570 270 -570 {
lab=VDD}
N 600 -570 620 -570 {
lab=VDD}
N 960 -570 980 -570 {
lab=VDD}
N 860 -570 880 -570 {
lab=VSS}
N 500 -570 520 -570 {
lab=VSS}
N 150 -570 170 -570 {
lab=VSS}
N 1160 -360 1180 -360 {
lab=Y0}
N 1160 -170 1180 -170 {
lab=Y1}
N 1160 30 1180 30 {
lab=Y2}
N 1160 220 1180 220 {
lab=Y3}
N 1160 410 1180 410 {
lab=Y4}
N 1160 580 1180 580 {
lab=Y5}
N 1160 760 1180 760 {
lab=Y6}
N 1160 940 1180 940 {
lab=Y7}
N 50 -590 50 -490 {
lab=A2}
N 390 -590 390 -490 {
lab=A1}
N 740 -590 740 -490 {
lab=A0}
N -110 -670 -110 960 {
lab=EN}
N -110 960 1010 960 {
lab=EN}
N 740 -490 740 950 {
lab=A0}
N -110 780 1010 780 {
lab=EN}
N -110 600 1010 600 {
lab=EN}
N -110 430 1010 430 {
lab=EN}
N -110 240 1010 240 {
lab=EN}
N -110 50 1010 50 {
lab=EN}
N -110 -150 1010 -150 {
lab=EN}
N 920 -490 920 -350 {
lab=#net1}
N 920 -350 920 770 {
lab=#net1}
N -110 -340 1010 -340 {
lab=EN}
C {xschem_lib/inv.sym} 170 -630 1 0 {name=X_inv7 NF=4}
C {xschem_lib/inv.sym} 520 -630 1 0 {name=X_inv8 NF=4}
C {xschem_lib/inv.sym} 880 -630 1 0 {name=X_inv9 NF=4}
C {ipin.sym} 50 -660 1 0 {name=p1 lab=A2}
C {ipin.sym} 390 -660 1 0 {name=p2 lab=A1}
C {ipin.sym} 740 -660 1 0 {name=p3 lab=A0}
C {iopin.sym} 1090 -410 0 0 {name=p4 lab=VDD}
C {iopin.sym} 1090 -220 0 0 {name=p5 lab=VDD}
C {iopin.sym} 1090 -20 0 0 {name=p6 lab=VDD}
C {iopin.sym} 1090 170 0 0 {name=p7 lab=VDD}
C {iopin.sym} 1090 360 0 0 {name=p8 lab=VDD}
C {iopin.sym} 1090 530 0 0 {name=p9 lab=VDD}
C {iopin.sym} 1090 710 0 0 {name=p10 lab=VDD}
C {iopin.sym} 1090 890 0 0 {name=p11 lab=VDD}
C {iopin.sym} 1090 -310 0 0 {name=p12 lab=VSS}
C {iopin.sym} 1090 -120 0 0 {name=p13 lab=VSS}
C {iopin.sym} 1090 80 0 0 {name=p14 lab=VSS}
C {iopin.sym} 1090 270 0 0 {name=p15 lab=VSS}
C {iopin.sym} 1090 460 0 0 {name=p16 lab=VSS}
C {iopin.sym} 1090 630 0 0 {name=p17 lab=VSS}
C {iopin.sym} 1090 810 0 0 {name=p18 lab=VSS}
C {iopin.sym} 1090 990 0 0 {name=p19 lab=VSS}
C {iopin.sym} 270 -570 1 0 {name=p24 lab=VDD}
C {iopin.sym} 620 -570 1 0 {name=p26 lab=VDD}
C {iopin.sym} 980 -570 1 0 {name=p28 lab=VDD}
C {iopin.sym} 860 -570 1 0 {name=p32 lab=VSS}
C {iopin.sym} 500 -570 1 0 {name=p34 lab=VSS}
C {iopin.sym} 150 -570 1 0 {name=p36 lab=VSS}
C {opin.sym} 1180 -360 0 0 {name=p38 lab=Y0}
C {opin.sym} 1180 -170 0 0 {name=p39 lab=Y1}
C {opin.sym} 1180 30 0 0 {name=p40 lab=Y2
}
C {opin.sym} 1180 220 0 0 {name=p41 lab=Y3
}
C {opin.sym} 1180 410 0 0 {name=p42 lab=Y4
}
C {opin.sym} 1180 580 0 0 {name=p43 lab=Y5
}
C {opin.sym} 1180 760 0 0 {name=p44 lab=Y6
}
C {opin.sym} 1180 940 0 0 {name=p45 lab=Y7
}
C {xschem_lib/and_4in.sym} 1090 -360 0 0 {name=x_AndF1 NF=2}
C {xschem_lib/and_4in.sym} 1090 -170 0 0 {name=x_AndF2 NF=2}
C {xschem_lib/and_4in.sym} 1090 30 0 0 {name=x_AndF3 NF=2}
C {xschem_lib/and_4in.sym} 1090 220 0 0 {name=x_AndF4 NF=2}
C {xschem_lib/and_4in.sym} 1090 410 0 0 {name=x_AndF5 NF=2}
C {xschem_lib/and_4in.sym} 1090 580 0 0 {name=x_AndF6 NF=2}
C {xschem_lib/and_4in.sym} 1090 760 0 0 {name=x_AndF7 NF=2}
C {xschem_lib/and_4in.sym} 1090 940 0 0 {name=x_AndF8 NF=2}
C {ipin.sym} -110 -660 1 0 {name=p20 lab=EN}
