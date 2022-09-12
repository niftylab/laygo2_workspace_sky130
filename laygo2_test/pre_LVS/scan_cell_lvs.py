##############################################
#                                            #
#       PROJECT: SCAN CHAIN AUTOMATION       #
#       SCAN CELL LAYOUT GENERATOR           #
#       CREATED BY TAEHO SHIN                #
#                                            #
##############################################

import numpy as np
import pprint
import laygo2
import laygo2.interface
import laygo2_tech as tech
import netmap_template as nMap
### PARAMETER DEFINITION
# Templates
tpmos_name = 'pmos_sky'
tnmos_name = 'nmos_sky'
tntap_name = 'ntap_sky'
tptap_name = 'ptap_sky'
# Grids
pg_name  = 'placement_basic'
r12_name = 'routing_12_cmos'
r23_name = 'routing_23_cmos'
r23_basic_name = 'routing_23_basic'
r34_name = 'routing_34_basic'

# Design hierarchy
libname  = 'scan_generated'
cellname = 'scan_cell_modified'
ref_dir_template = './laygo2_test/scan/'
ref_dir_MAG_exported = './laygo2_test/scan/TCL/'
yaml_import_path = './laygo2_test/logic/' #logic_generated.yaml path
# End of parameter definitions ######

### GENERATION START
# 1. Load templates and grids.
print("Load templates")
templates = tech.load_templates()
tpmos, tnmos = templates[tpmos_name], templates[tnmos_name]
tptap, tntap = templates[tptap_name], templates[tntap_name]
tlib = laygo2.interface.yaml.import_template(filename=yaml_import_path+'logic_generated_templates.yaml')
tlib_reduce = laygo2.interface.yaml.import_template(filename=yaml_import_path+'logic_reduced_templates.yaml')
# Filename Example: ./laygo2_generators_private/scan/scan_generated_templates.yaml

print("Load grids")
grids = tech.load_grids(templates=templates)
pg, r12, r23, r34 = grids[pg_name], grids[r12_name], grids[r23_name], grids[r34_name]
r23_basic = grids[r23_basic_name]
# 2. Create a design hierarchy
lib = laygo2.object.database.Library(name=libname)
dsn = laygo2.object.database.Design(name=cellname, libname=libname)
lib.append(dsn)

# 3. Create istances.
print("Create instances")
# BOTTOM INSTANCES
inv_load      = tlib['inv_2x'    ].generate(name='I0', transform='MX', netname={'I':"SCAN_LOAD",'O':'SCAN_LOAD_BAR','VSS':'VSS','VDD':'VDD:'})
mux_in        = tlib['mux2to1_2x'].generate(name='I1', transform='MX', netname={'EN0':'SCAN_LOAD_BAR','EN1':'SCAN_LOAD','I0':'SCAN_IN','I1':'SCAN_DATA_IN','O':'MUX_IN/O','VSS':'VSS','VDD':'VDD:'})
dff_out       = tlib_reduce['dff_2x'    ].generate(name='I2', transform='MX', netname={'CLK':'SCAN_CLK','I':'MUX_IN/O','O':'DFF_OUT/O','VSS':'VSS','VDD':'VDD:'})

inv_out0      = tlib['inv_2x'    ].generate(name='I4', transform='MX', netname={'I':'DFF_OUT/O','O':'INV_OUT0/O','VSS':'VSS','VDD':'VDD:'})
inv_out1      = tlib['inv_2x'    ].generate(name='I5', transform='MX', netname={'I':'INV_OUT0/O','O':'INV_OUT1/O','VSS':'VSS','VDD':'VDD:'})
inv_out2      = tlib['inv_2x'    ].generate(name='I6', transform='MX', netname={'I':'INV_OUT1/O','O':'INV_OUT2/O','VSS':'VSS','VDD':'VDD:'})
inv_out3      = tlib['inv_2x'    ].generate(name='I7', transform='MX', netname={'I':'INV_OUT2/O','O':'SCAN_OUT','VSS':'VSS','VDD':'VDD:'})

inv_data_out0 = tlib['inv_2x'    ].generate(name='I22', transform='R180', netname={'I':'MUX_DAT/O','O':'INV_DAT0/O','VSS':'VSS','VDD':'VDD:'})
inv_data_out1 = tlib['inv_4x'    ].generate(name='I23', transform='MX', netname={'I':'INV_DAT0/O','O':'INV_DAT1/O','VSS':'VSS','VDD':'VDD:'})
inv_data_out2 = tlib['inv_24x'   ].generate(name='I24', transform='MX', netname={'I':'INV_DAT1/O','O':'INV_DAT2/O','VSS':'VSS','VDD':'VDD:'})

# TOP INSTANCES
inv_clk0      = tlib['inv_2x'    ].generate(name='I15', transform='MY', netname={'I':'INV_CLK1/O','O':'SCAN_CLK_OUT','VSS':'VSS','VDD':'VDD:'})
inv_clk1      = tlib['inv_2x'    ].generate(name='I16', transform='MY', netname={'I':'INV_CLK2/O','O':'INV_CLK1/O','VSS':'VSS','VDD':'VDD:'})
inv_clk2      = tlib['inv_2x'    ].generate(name='I17', transform='MY', netname={'I':'INV_CLK3/O','O':'INV_CLK2/O','VSS':'VSS','VDD':'VDD:'})
inv_clk3      = tlib['inv_2x'    ].generate(name='I18', transform='MY', netname={'I':'SCAN_CLK','O':'INV_CLK3/O','VSS':'VSS','VDD':'VDD:'})

inv_en        = tlib['inv_2x'    ].generate(name='I19', netname={'I':'SCAN_EN','O':'INV_EN/O','VSS':'VSS','VDD':'VDD:'})
dff_data_out  = tlib_reduce['dff_2x'    ].generate(name='I20', netname={'CLK':'INV_EN/O','I':'DFF_OUT/O','O':'DFF_DAT/O','VSS':'VSS','VDD':'VDD:'})

inv_scan_gate = tlib['inv_2x'    ].generate(name='I3', netname={'I':'SCAN_GATE','O':'INV_GATE/O','VSS':'VSS','VDD':'VDD:'})
mux_data_out  = tlib['mux2to1_2x'].generate(name='I21', netname={'I0':'SCAN_GATE_VALUE','I1':'DFF_DAT/O','EN0':'SCAN_GATE','EN1':'INV_GATE/O','O':'MUX_DAT/O','VSS':'VSS','VDD':'VDD:'})
inv_data_out3 = tlib['inv_24x'   ].generate(name='I14', transform='MY', netname={'I':'INV_DAT2/O','O':'SCAN_DATA_OUT','VSS':'VSS','VDD':'VDD:'})

# TAP for DRC
# CAN BE DELETED
# tap_bot_left  = tlib['tap'       ].generate(name='TAP0', transform='MX')
# tap_bot_right = tlib['tap'       ].generate(name='TAP1', transform='MX')
# tap_top_left  = tlib['tap'       ].generate(name='TAP2')
# tap_top_right = tlib['tap'       ].generate(name='TAP3')

# 4. Place instances.
pg_list = [0]*2
pg_list[1] = [inv_clk0, inv_clk1, inv_clk2, inv_clk3, inv_en,   dff_data_out, inv_scan_gate, mux_data_out,  inv_data_out3, None]
pg_list[0] = [inv_load, mux_in,   dff_out,  inv_out0, inv_out1, inv_out2,     inv_out3,      inv_data_out0, inv_data_out1, inv_data_out2]

############################ FILLING FUNCTION ####################################
nf_space = np.zeros((len(pg_list), len(pg_list)), dtype=int)
for i in range(len(pg_list)):
   for j in range(len(pg_list[i])):
      if pg_list[i][j] == None:
         pass
      else:
         nf_space[i] = nf_space[i] + pg.mn.bbox(pg_list[i][j])[:,0]
nf_space = sum(abs(nf_space[0]))-sum(abs(nf_space[1]))
######################### FILLING FUNCTION END ###################################

_num=0
for i in range(len(pg_list[1])):
   if pg_list[1][i] == None:
      pg_list[1][i] = tlib['space_1x'].generate(name='SPACE'+str(_num), shape=[nf_space, 1])
      _num+=1

dsn.place(grid=pg, inst=pg_list, mn=[0,0])

# 5. Create and place wires.
print("Create wires")
############################# BOTTOM INSTANCES ##########################
track_ref_bot = [None, np.mean(r34.mn(inv_load.pins['I'])[:,1], dtype=int)]

# SCAN_LOAD signal to MUX
_mn = [r34.mn(inv_load.pins['I'])[0], r34.mn(mux_in.pins['EN1'])[0]]
dsn.route_via_track(grid=r34, mn=_mn, track=[None, track_ref_bot[1]+2])

_mn = [r34.mn(inv_load.pins['O'])[0], r34.mn(mux_in.pins['EN0'])[0]]
dsn.route_via_track(grid=r34, mn=_mn, track=[None, track_ref_bot[1]+3])

# MUX to DFF
_mn = [r34.mn(mux_in.pins['O'])[0], r34.mn(dff_out.pins['I'])[0]]
dsn.route_via_track(grid=r34, mn=_mn, track=[None, track_ref_bot[1]+2])

# SCAN_CLK to DFF
_mn = [r34.mn(inv_clk3.pins['I'])[0], r34.mn(dff_out.pins['CLK'])[1]]
_track = [None, track_ref_bot[1]+5]
dsn.route_via_track(grid=r34, mn=_mn, track=_track)

# DFF to INV chain for SCAN_OUT signal
_mn = [r34.mn(dff_out.pins['O'])[0], r34.mn(inv_out0.pins['I'])[0]]
_track = [None, track_ref_bot[1]+2]
dsn.route_via_track(grid=r34, mn=_mn, track=_track)

_mn = [r34.mn(inv_out0.pins['O'])[0], r34.mn(inv_out1.pins['I'])[0]]
_track = [None, track_ref_bot[1]+1]
dsn.route_via_track(grid=r34, mn=_mn, track=_track)

_mn = [r34.mn(inv_out1.pins['O'])[0], r34.mn(inv_out2.pins['I'])[0]]
_track = [None, track_ref_bot[1]+2]
dsn.route_via_track(grid=r34, mn=_mn, track=_track)

_mn = [r34.mn(inv_out2.pins['O'])[0], r34.mn(inv_out3.pins['I'])[0]]
_track = [None, track_ref_bot[1]+1]
dsn.route_via_track(grid=r34, mn=_mn, track=_track)
############################ BOTTOM INSTANCES END #######################

############################ TOP INSTANCES START ########################
track_ref_top = [None, np.mean(r34.mn(inv_clk0.pins['I'])[:,1], dtype=int)]

# INV chain for SCAN_CLK signal
_mn = [r34.mn(inv_clk3.pins['O'])[0], r34.mn(inv_clk2.pins['I'])[0]]
_track = [None, track_ref_top[1]-2]
dsn.route_via_track(grid=r34, mn=_mn, track=_track)

_mn = [r34.mn(inv_clk2.pins['O'])[0], r34.mn(inv_clk1.pins['I'])[0]]
_track = [None, track_ref_top[1]-1]
dsn.route_via_track(grid=r34, mn=_mn, track=_track)

_mn = [r34.mn(inv_clk1.pins['O'])[0], r34.mn(inv_clk0.pins['I'])[0]]
_track = [None, track_ref_top[1]-2]
dsn.route_via_track(grid=r34, mn=_mn, track=_track)

# SCAN_EN signal to DFF
_mn = [r34.mn(inv_en.pins['O'])[0], r34.mn(dff_data_out.pins['CLK'])[0]]
_track = [None, track_ref_top[1]-2]
dsn.route_via_track(grid=r34, mn=_mn, track=_track)

# DFF for SCAN_DATA_OUT signal
_mn = [r34.mn(dff_data_out.pins['I'])[0], r34.mn(dff_out.pins['O'])[0]]
_track = [r34.mn(dff_out.pins['O'])[0,0]-2, None]
dsn.route_via_track(grid=r34, mn=_mn, track=_track)
dsn.via(grid=r34, mn=r34.mn(dff_out.pins['O'])[0])
dsn.via(grid=r34, mn=r34.mn(dff_data_out.pins['I'])[0])

# SCAN_GATE signal
_mn = [r34.mn(inv_scan_gate.pins['I'])[1], r34.mn(mux_data_out.pins['EN0'])[1]]
dsn.route(grid=r34, mn=_mn, via_tag=[True, True])

_mn = [r34.mn(inv_scan_gate.pins['O'])[0], r34.mn(mux_data_out.pins['EN1'])[0]]
# _track = [None, track_ref_top[1]+2] -> short error due to basic routing grid difference: (y/x)TSMC:(y/x)SKY = 7:9)
_track = [None, track_ref_top[1]+1]
dsn.route_via_track(grid=r34, mn=_mn, track=_track)

# INV chain for SCAN_DATA_OUT signal
_mn = [r34.mn(dff_data_out.pins['O'])[0], r34.mn(mux_data_out.pins['I1'])[0]]
#_track = [None, track_ref_top[1]-2] -> short error due to basic routing grid difference: (y/x)TSMC:(y/x)SKY = 7:9)
_track = [None, track_ref_top[1]-1] 
dsn.route_via_track(grid=r34, mn=_mn, track=_track)

_mn = [r34.mn(mux_data_out.pins['O'])[0]-[0,2], r34.mn(mux_data_out.pins['O'])[0]]
dsn.route(grid=r34, mn=_mn)

#_mn = [_mn[0], r34.mn(inv_data_out0.pins['I'])[1]+[0,1]] -> open with sky130 implementation
_mn = [_mn[0], r34.mn(inv_data_out0.pins['I'])[1]]
_track = [r34.mn(mux_data_out.pins['O'])[0,0]-2, None]
dsn.route_via_track(grid=r34, mn=_mn, track=_track)
dsn.via(grid=r34, mn=_mn[0])
dsn.via(grid=r34, mn=_mn[1])

_mn = [r34.mn(inv_data_out0.pins['O'])[0], r34.mn(inv_data_out1.pins['I'])[0]]
_track = [None, track_ref_bot[1]+1]
dsn.route_via_track(grid=r34, mn=_mn, track=_track)

_mn = [r34.mn(inv_data_out1.pins['O'])[0], r34.mn(inv_data_out2.pins['I'])[0]]
_track = [None, track_ref_bot[1]+2]
dsn.route_via_track(grid=r34, mn=_mn, track=_track)

_mn = [r34.mn(inv_data_out2.pins['O'])[0], r34.mn(inv_data_out3.pins['I'])[0]]
_track = [None, track_ref_top[1]-3]
dsn.route_via_track(grid=r34, mn=_mn, track=_track)
############################### TOP INSTANCES END ################################

# VSS
rvss0 = dsn.route(grid=r12, mn=[r12.mn.top_left(pg_list[0][0]), r12.mn.top_right(pg_list[0][-1])])

# VDD
rvdd0 = dsn.route(grid=r12, mn=[r12.mn.bottom_left(pg_list[0][0]), r12.mn.bottom_right(pg_list[0][-1])])
rvdd1 = dsn.route(grid=r12, mn=[r12.mn.top_left(pg_list[-1][0]), r12.mn.top_right(pg_list[-1][-1])])


# 6. Create pins.
pSCAN_IN         = dsn.pin(name='SCAN_IN',         grid=r23, mn=r23.mn.bbox(mux_in.pins['I0']))
pSCAN_DATA_IN    = dsn.pin(name='SCAN_DATA_IN',    grid=r23, mn=r23.mn.bbox(mux_in.pins['I1']))
pSCAN_OUT        = dsn.pin(name='SCAN_OUT',        grid=r23, mn=r23.mn.bbox(inv_out3.pins['O']))
pSCAN_DATA_OUT   = dsn.pin(name='SCAN_DATA_OUT',   grid=r23, mn=r23.mn.bbox(inv_data_out3.pins['O']))

pSCAN_GATE       = dsn.pin(name='SCAN_GATE',       grid=r23, mn=r23.mn.bbox(mux_data_out.pins['EN0']))
pSCAN_GATE_VALUE = dsn.pin(name='SCAN_GATE_VALUE', grid=r23, mn=r23.mn.bbox(mux_data_out.pins['I0']))

pSCAN_CLK        = dsn.pin(name='SCAN_CLK',        grid=r23, mn=r23.mn.bbox(inv_clk3.pins['I']))
pSCAN_CLK_OUT    = dsn.pin(name='SCAN_CLK_OUT',    grid=r23, mn=r23.mn.bbox(inv_clk0.pins['O']))

pSCAN_EN         = dsn.pin(name='SCAN_EN',         grid=r23, mn=r23.mn.bbox(inv_en.pins['I']))
pSCAN_LOAD       = dsn.pin(name='SCAN_LOAD',       grid=r23, mn=r23.mn.bbox(inv_load.pins['I']))

pvss0            = dsn.pin(name='VSS',             grid=r12, mn=r12.mn.bbox(rvss0))
pvdd0            = dsn.pin(name='VDD0',            grid=r12, mn=r12.mn.bbox(rvdd0), netname='VDD:')
pvdd1            = dsn.pin(name='VDD1',            grid=r12, mn=r12.mn.bbox(rvdd1), netname='VDD:')

via_table = dict()
via_table["via_M1_M2_0"] = ('M1','M2')
via_table["via_M1_M2_1"] = ('M1','M2')
via_table["via_M2_M3_0"] = ('M2','M3')
via_table["via_M2_M3_1"] = ('M2','M3')
via_table["via_M3_M4_0"] = ('M3','M4')
via_table["via_M4_M5_0"] = ('M4','M5')
nMap.netMap.lvs_check(dsn, r34, via_table)
# 7. Export to physical database.
print("Export design")
### EXPORT TO BAG
# SKILL script for load in Virtuoso
laygo2.interface.magic.export(lib, filename=ref_dir_MAG_exported+libname+'_'+cellname+'.tcl', libpath = './magic_layout', cellname=None, scale=1, reset_library=False, tech_library=tech.name)

# 8. Export to a template database file.
nat_temp = dsn.export_to_template()
laygo2.interface.yaml.export_template(nat_temp, filename=ref_dir_template+libname+'_templates.yaml', mode='append')
# Filename example: ./laygo2_generators_private/scan/scan_generated_templates.yaml 
