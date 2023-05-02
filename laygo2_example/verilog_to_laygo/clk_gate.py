###########################################
#                                         #
#      clock gate Layout Generator        #
#        Created by HyungJoo Park         #   
#                                         #
###########################################


import numpy as np
import pprint
import laygo2
import laygo2.interface
import laygo2_tech as tech
# Parameter definitions #############
# Variables
cell_type = 'cgate'
# Templates
tpmos_name = 'pmos_sky'
tnmos_name = 'nmos_sky'
tptap_name = 'ptap_sky'
tntap_name = 'ntap_sky'
# Grids
pg_name = 'placement_basic'
r12_name = 'routing_12_cmos'
r23_basic_name = 'routing_23_basic'
r23_cmos_name = 'routing_23_cmos'
r34_name = 'routing_34_basic'
# Design hierarchy
libname = 'logic_advanced'
ref_dir_template = './laygo2_example/logic/' #export this layout's information into the yaml in this dir 
ref_dir_export = './laygo2_example/logic_advance/'
ref_dir_MAG_exported = './laygo2_example/logic_advance/TCL/'
ref_dir_layout = './magic_layout'
# End of parameter definitions ######

# Generation start ##################
# 1. Load templates and grids.
print("Load templates")
templates = tech.load_templates()
tpmos, tnmos = templates[tpmos_name], templates[tnmos_name]
tlib = laygo2.interface.yaml.import_template(filename=ref_dir_template+'logic_generated_templates.yaml')
#print(templates[tpmos_name], templates[tnmos_name], sep="\n")

print("Load grids")
grids = tech.load_grids(templates=templates)
pg, r12, r23_cmos, r23, r34 = grids[pg_name], grids[r12_name], grids[r23_cmos_name], grids[r23_basic_name], grids[r34_name]
#print(grids[pg_name], grids[r12_name], grids[r23_basic_name], grids[r34_name], sep="\n")

nf=2
cellname = cell_type+'_'+str(nf)+'x'
print('--------------------')
print('Now Creating '+cellname)

# 2. Create a design hierarchy
lib = laygo2.object.database.Library(name=libname)
dsn = laygo2.object.database.Design(name=cellname, libname=libname)
lib.append(dsn)

# 3. Create istances.
print("Create instances")
inv0 = tlib['inv_'+str(nf)+'x'].generate(name='inv0')
inv1 = tlib['inv_'+str(12)+'x'].generate(name='inv1')
latch0 = tlib['latch_2ck_'+str(nf)+'x'].generate(name='latch0')
nand0 = tlib['nand_'+str(nf)+'x'].generate(name='nand0')

NTAP0 = templates[tntap_name].generate(name='MNT0', params={'nf':2, 'tie':'TAP0'})
PTAP0 = templates[tptap_name].generate(name='MPT0', transform='MX',params={'nf':2, 'tie':'TAP0'})

# 4. Place instances.
dsn.place(grid=pg, inst=inv0, mn=[0,0])
dsn.place(grid=pg, inst=latch0, mn=pg.mn.bottom_right(inv0))
dsn.place(grid=pg, inst=NTAP0, mn=pg.mn.bottom_right(latch0))
dsn.place(grid=pg, inst=PTAP0, mn=pg.mn.top_left(NTAP0) + pg.mn.height_vec(PTAP0))
dsn.place(grid=pg, inst=nand0, mn=pg.mn.bottom_right(NTAP0))
dsn.place(grid=pg, inst=inv1, mn=pg.mn.bottom_right(nand0))

# 5. Create and place wires.
print("Create wires")

# clk
mn_list = [r34.mn(inv0.pins['I'])[0], r34.mn(latch0.pins['CLKB'])[0],r34.mn(nand0.pins['B'])[0]]
_track = [None, r34.mn(inv1.pins['O'])[0,1]]
dsn.route_via_track(grid=r34, mn=mn_list, track=_track)

# clk_bar
mn_list = [r34.mn(inv0.pins['O'])[1], r34.mn(latch0.pins['CLK'])[1]]
_track = [None, r34.mn(inv0.pins['O'])[1,1] - 5]
dsn.route_via_track(grid=r34, mn=mn_list, track=_track)

#latch out
mn_list = [r34.mn(latch0.pins['O'])[1], r34.mn(nand0.pins['A'])[1]]
_track = [None, r34.mn(latch0.pins['O'])[1,1] - 5]
dsn.route_via_track(grid=r34, mn=mn_list, track=_track)

#internal
mn_list = [r23.mn(nand0.pins['OUT'])[0], r23.mn(inv1.pins['I'])[0]]
_track = [None, (r23.mn(nand0.pins['OUT'])[0,1]+r23.mn(nand0.pins['OUT'])[1,1])/2]
dsn.route_via_track(grid=r23, mn=mn_list, track=_track)

# VSS
rvss0 = dsn.route(grid=r12, mn=[r12.mn.bottom_left(inv0), r12.mn.bottom_right(inv1)])
# VDD
rvdd0 = dsn.route(grid=r12, mn=[r12.mn.top_left(inv0), r12.mn.top_right(inv1)])

# 6. Create pins.
pCLK_in = dsn.pin(name='CK_I', grid=r23_cmos, mn=r23_cmos.mn.bbox(inv0.pins['I']))
pEN = dsn.pin(name='EN', grid=r23_cmos, mn=r23_cmos.mn.bbox(latch0.pins['I']))
pCLK_out = dsn.pin(name='CK_O', grid=r23_cmos, mn=r23_cmos.mn.bbox(inv1.pins['O']))
pvss0 = dsn.pin(name='VSS', grid=r12, mn=r12.mn.bbox(rvss0))
pvdd0 = dsn.pin(name='VDD', grid=r12, mn=r12.mn.bbox(rvdd0))

# 7. Export to physical database.
print("Export design")

# Uncomment for BAG export
laygo2.interface.magic.export(lib, filename=ref_dir_MAG_exported +libname+'_'+cellname+'.tcl', cellname=None, libpath=ref_dir_layout, scale=1, reset_library=False, tech_library='sky130A')

# 8. Export to a template database file.
nat_temp = dsn.export_to_template()
laygo2.interface.yaml.export_template(nat_temp, filename=ref_dir_export+libname+'_templates.yaml', mode='append')