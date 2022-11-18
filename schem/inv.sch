v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N 100 -50 100 -20 {
lab=Y}
N 40 -80 60 -80 {
lab=X}
N 40 -80 40 10 {
lab=X}
N 40 10 60 10 {
lab=X}
N 100 -40 180 -40 {
lab=Y}
N 10 -40 40 -40 {
lab=X}
N 100 -150 100 -110 {
lab=VDD}
N 100 40 100 80 {
lab=VSS}
C {/usr/local/share/pdk/sky130A/libs.tech/xschem/sky130_fd_pr/nfet3_01v8_lvt.sym} 80 10 0 0 {name=M1
L=0.15
W=1.2
nf=1
mult=1
body=GND
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8_lvt
spiceprefix=X
}
C {/usr/local/share/pdk/sky130A/libs.tech/xschem/sky130_fd_pr/pfet3_01v8.sym} 80 -80 0 0 {name=M2
L=0.15
W=1.6
body=VDD
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
C {ipin.sym} 20 -40 0 0 {name=p1 lab=X}
C {opin.sym} 170 -40 0 0 {name=p2 lab=Y}
C {iopin.sym} 100 -140 3 0 {name=p3 lab=VDD}
C {iopin.sym} 100 70 1 0 {name=p4 lab=VSS}
