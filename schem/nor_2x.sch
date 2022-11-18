v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N 1590 -1390 1590 -1340 {
lab=#net1}
N 1590 -1280 1600 -1210 {
lab=#net2}
N 1400 -1210 1600 -1210 {
lab=#net2}
N 1400 -1150 1400 -1080 {
lab=VSS}
N 1400 -1085 1485 -1085 {
lab=VSS}
N 1485 -1085 1600 -1085 {
lab=VSS}
N 1600 -1150 1600 -1085 {
lab=VSS}
N 1600 -1090 1600 -1085 {
lab=VSS}
N 1600 -1210 1625 -1245 {
lab=#net2}
N 1590 -1490 1590 -1450 {
lab=#net3}
N 1590 -1310 1680 -1310 {
lab=#net3}
N 1680 -1465 1680 -1310 {
lab=#net3}
N 1585 -1420 1680 -1420 {
lab=#net3}
N 1590 -1465 1680 -1465 {
lab=#net3}
N 1210 -1285 1210 -1175 {
lab=#net4}
N 1210 -1180 1360 -1180 {
lab=#net4}
N 1300 -1310 1550 -1310 {
lab=#net4}
N 1300 -1310 1300 -1180 {
lab=#net4}
N 1510 -1420 1550 -1420 {
lab=A}
N 1510 -1420 1510 -1175 {
lab=A}
N 1510 -1180 1560 -1180 {
lab=A}
N 1210 -1340 1510 -1340 {
lab=A}
N 1400 -1180 1445 -1180 {
lab=VSS}
N 1445 -1180 1445 -1085 {
lab=VSS}
N 1600 -1180 1615 -1180 {
lab=VSS}
N 1615 -1180 1615 -1100 {
lab=VSS}
N 1600 -1100 1615 -1100 {
lab=VSS}
C {sky130_fd_pr/nfet_01v8_lvt.sym} 1380 -1180 0 0 {name=M1
L=0.15
W=1.2
nf=1
mult=2
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8_lvt
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8_lvt.sym} 1580 -1180 0 0 {name=M2
L=0.15
W=1.2
nf=1
mult=2
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8_lvt
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 1570 -1310 0 0 {name=M3
L=0.15
W=2.4
nf=1
mult=2
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 1570 -1420 0 0 {name=M4
L=0.15
W=2.4
nf=1
mult=2
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {ipin.sym} 1220 -1285 0 0 {name=p1 lab=B dir=in}
C {ipin.sym} 1220 -1340 0 0 {name=p2 lab=A dir=in}
C {iopin.sym} 1475 -1085 0 0 {name=p5 lab=VSS dir=inout}
C {iopin.sym} 1580 -1490 0 0 {name=p4 lab=VDD dir=inout}
C {opin.sym} 1620 -1245 0 0 {name=p3 lab=O dir=out}
