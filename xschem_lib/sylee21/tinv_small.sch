v {xschem version=3.1.0 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 1030 -1680 1030 -1500 {
lab=X}
N 1030 -1680 1130 -1680 {
lab=X}
N 1030 -1500 1030 -1330 {
lab=X}
N 1030 -1330 1130 -1330 {
lab=X}
N 1090 -1450 1130 -1450 {
lab=#net1}
N 1090 -1570 1130 -1570 {
lab=ENB}
N 1170 -1540 1170 -1480 {
lab=Y}
N 1170 -1420 1170 -1360 {
lab=#net2}
N 1170 -1650 1170 -1600 {
lab=#net3}
N 1170 -1500 1210 -1500 {
lab=Y}
N 1170 -1760 1170 -1710 {
lab=VDD}
N 1170 -1680 1200 -1680 {
lab=VDD}
N 1200 -1730 1200 -1680 {
lab=VDD}
N 1170 -1730 1200 -1730 {
lab=VDD}
N 1170 -1570 1200 -1570 {
lab=VDD}
N 1200 -1680 1200 -1570 {
lab=VDD}
N 1170 -1300 1170 -1240 {
lab=VSS}
N 1170 -1330 1210 -1330 {
lab=VSS}
N 1210 -1330 1210 -1270 {
lab=VSS}
N 1170 -1270 1210 -1270 {
lab=VSS}
N 1170 -1450 1210 -1450 {
lab=VSS}
N 1210 -1450 1210 -1330 {
lab=VSS}
N 980 -1500 1030 -1500 {
lab=X}
C {sky130_fd_pr/pfet_01v8.sym} 1150 -1680 0 0 {name=M1
L=0.15
W=2.4
nf=1
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 1150 -1570 0 0 {name=M2
L=0.15
W=2.4
nf=1
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8_lvt.sym} 1150 -1450 0 0 {name=M3
L=0.15
W=1.2
nf=1
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8_lvt
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8_lvt.sym} 1150 -1330 0 0 {name=M4
L=0.15
W=1.2
nf=1
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8_lvt
spiceprefix=X
}
C {devices/ipin.sym} 990 -1500 0 0 {name=p1 lab=X}
C {devices/ipin.sym} 1100 -1570 0 0 {name=p2 lab=ENB}
C {devices/ipin.sym} 1100 -1450 0 0 {name=p3 lab=EN}
C {devices/opin.sym} 1200 -1500 0 0 {name=p4 lab=Y}
C {devices/iopin.sym} 1170 -1750 3 0 {name=p5 lab=VDD}
C {devices/iopin.sym} 1170 -1250 1 0 {name=p6 lab=VSS}
