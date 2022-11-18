v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
N 110 -30 110 0 {
lab=Y}
N -10 -80 -10 10 {
lab=X}
N 110 -20 190 -20 {
lab=Y}
N -40 -40 -10 -40 {
lab=X}
N 110 -260 110 -220 {
lab=VDD}
N 110 150 110 190 {
lab=VSS}
N 110 -160 110 -140 {
lab=#net1}
N -10 -190 20 -190 {
lab=X}
N -10 -190 -10 -80 {
lab=X}
N 110 70 110 90 {
lab=#net2}
N 110 -80 110 -30 {
lab=Y}
N 110 -0 110 10 {
lab=Y}
N 20 -190 70 -190 {
lab=X}
N -10 120 70 120 {
lab=X}
N -10 10 -10 120 {
lab=X}
N 50 40 70 40 {
lab=EN}
N 50 -110 70 -110 {
lab=ENB}
C {/usr/local/share/pdk/sky130A/libs.tech/xschem/sky130_fd_pr/nfet3_01v8_lvt.sym} 90 120 0 0 {name=M1
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
C {/usr/local/share/pdk/sky130A/libs.tech/xschem/sky130_fd_pr/pfet3_01v8.sym} 90 -190 0 0 {name=M2
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
C {ipin.sym} -30 -40 0 0 {name=p1 lab=X}
C {opin.sym} 180 -20 0 0 {name=p2 lab=Y}
C {iopin.sym} 110 -250 3 0 {name=p3 lab=VDD}
C {iopin.sym} 110 180 1 0 {name=p4 lab=VSS}
C {/usr/local/share/pdk/sky130A/libs.tech/xschem/sky130_fd_pr/pfet3_01v8.sym} 90 -110 0 0 {name=M3
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
C {/usr/local/share/pdk/sky130A/libs.tech/xschem/sky130_fd_pr/nfet3_01v8_lvt.sym} 90 40 0 0 {name=M4
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
C {iopin.sym} 60 40 2 0 {name=p5 lab=EN}
C {iopin.sym} 60 -110 2 0 {name=p6 lab=ENB}
