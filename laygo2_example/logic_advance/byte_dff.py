###########################################
#                                         #
#     DFF driven byte Layout Generator    #
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
cell_type = 'byte_dff'
nf=2
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
ref_dir_template = './laygo2_example/' #export this layout's information into the yaml in this dir 
ref_dir_export = './laygo2_example/logic_advance/'
ref_dir_MAG_exported = './laygo2_example/logic_advance/TCL/'
ref_dir_layout = './magic_layout'
# End of parameter definitions ######

# Generation start ##################
# 1. Load templates and grids.
print("Load templates")
templates = tech.load_templates()
tpmos, tnmos = templates[tpmos_name], templates[tnmos_name]
tlogic_prim = laygo2.interface.yaml.import_template(filename=ref_dir_template+'logic/logic_generated_templates.yaml')
tlogic_adv = laygo2.interface.yaml.import_template(filename=ref_dir_template+'logic_advance/logic_advanced_templates.yaml')

print("Load grids")
grids = tech.load_grids(templates=templates)
pg, r12, r23_cmos, r23, r34 = grids[pg_name], grids[r12_name], grids[r23_cmos_name], grids[r23_basic_name], grids[r34_name]

cellname = cell_type+'_'+str(nf)+'x'
print('--------------------')
print('Now Creating '+cellname)

# 2. Create a design hierarchy
lib = laygo2.object.database.Library(name=libname)
dsn = laygo2.object.database.Design(name=cellname, libname=libname)
lib.append(dsn)

# 3. Create istances.
print("Create instances")
inv_sel = tlogic_prim['inv_'+str(nf)+'x'].generate(name='inv_sel')
inv_and = tlogic_prim['inv_'+str(nf)+'x'].generate(name='inv_and')
nand = tlogic_prim['nand_'+str(nf)+'x'].generate(name='nand')
cgate = tlogic_adv['cgate_'+str(nf)+'x'].generate(name='cgate0')
cells=list()
for i in range(8):
    cells.append(tlogic_prim['dff_'+str(nf)+'x'].generate(name='dff_'+str(i)))
    cells.append(tlogic_prim['inv_'+str(nf)+'x'].generate(name='inv'+str(i)))
    cells.append(tlogic_prim['tinv_'+str(nf)+'x'].generate(name='tinv'+str(i)))

# 4. Place instances.
dsn.place(grid=pg, inst=nand, mn=[0,0])
dsn.place(grid=pg, inst=inv_and, mn=pg.mn.bottom_right(nand))
dsn.place(grid=pg, inst=inv_sel, mn=pg.mn.bottom_right(inv_and))
dsn.place(grid=pg, inst=cgate, mn=pg.mn.bottom_right(inv_sel))
dsn.place(grid=pg, inst=cells, mn=pg.mn.bottom_right(cgate))

# 5. Create and place wires.
print("Create wires")
# sel
mn_list = [r34.mn(nand.pins['B'])[0], r34.mn(inv_sel.pins['I'])[0]]
for i in range(8):
    mn_list.append(r34.mn(cells[3*i+2].pins['EN'])[0]) # ~= cells[i].tinv.pins[EN]
_track = [None, r34.mn(inv_sel.pins['O'])[0,1]-1]
rsel = dsn.route_via_track(grid=r34, mn=mn_list, track=_track)

# sel_bar
mn_list = [r34.mn(inv_sel.pins['O'])[0]]
for i in range(8):
    mn_list.append(r34.mn(cells[3*i+2].pins['ENB'])[0]) # ~= cells[i].tinv.pins[ENB]
_track = [None, r34.mn(inv_sel.pins['O'])[0,1]+1]
dsn.route_via_track(grid=r34, mn=mn_list, track=_track)

# Nand_inv
mn_list = [ r23.mn(nand.pins['OUT'])[0], r23.mn(inv_and.pins['I'])[0] ]
_track = [None, (r23.mn(inv_and.pins['I'])[0,1]+r23.mn(inv_and.pins['I'])[1,1])/2]
dsn.route_via_track(grid=r23, mn=mn_list, track=_track)

# clock en
mn_list = [r23.mn(inv_and.pins['O'])[0], r23.mn(cgate.pins['EN'])[0] ]
_track = [None,(r23.mn(cgate.pins['EN'])[0,1]+r23.mn(cgate.pins['EN'])[1,1])/2]
dsn.route_via_track(grid=r23, mn=mn_list, track=_track)

# clk flip flop
mn_list = [r34.mn(cgate.pins['CK_O'])[0]]
for i in range(8):
    mn_list.append(r34.mn(cells[3*i].pins['CLK'])[0])
_track = [None, r34.mn(cgate.pins['CK_O'])[0,1]]
dsn.route_via_track(grid=r34, mn=mn_list, track=_track)

# cell internal
for i in range(8):
    # dff_out <--> inv_in
    mn_list = [r23.mn(cells[3*i].pins['O'])[0], r23.mn(cells[3*i+1].pins['I'])[0]]
    _track = [None, (r23.mn(cells[3*i+1].pins['I'])[0,1] + r23.mn(cells[3*i+1].pins['I'])[1,1])/2]
    dsn.route_via_track(grid=r23, mn=mn_list, track=_track)
    # inv_out <--> tinv_in
    mn_list = [r23.mn(cells[3*i+1].pins['O'])[0], r23.mn(cells[3*i+2].pins['I'])[0]]
    _track = [None, (r23.mn(cells[3*i+2].pins['I'])[0,1] + r23.mn(cells[3*i+2].pins['I'])[1,1])/2]
    dsn.route_via_track(grid=r23, mn=mn_list, track=_track)

# VSS
rvss0 = dsn.route(grid=r12, mn=[r12.mn.bottom_left(nand), r12.mn.bottom_right(cells[3*8-1])])

# VDD
rvdd0 = dsn.route(grid=r12, mn=[r12.mn.top_left(nand), r12.mn.top_right(cells[3*8-1])])

# 6. Create pins.
psel =  dsn.pin(name='SEL', grid=r34, mn=r34.mn.bbox(rsel[-1]))
pwe = dsn.pin(name='WE', grid=r23_cmos, mn=r23_cmos.mn.bbox(nand.pins['A']))
pclk = dsn.pin(name='CLK', grid=r23_cmos, mn=r23_cmos.mn.bbox(cgate.pins['CK_I']))
pDo = list()
pDi = list()
for i in range(8):
    pDo.append(dsn.pin(name='Do<'+str(7-i)+'>', grid=r23_cmos, mn=r23_cmos.mn.bbox(cells[3*(7-i)+2].pins['O'])))
    pDi.append(dsn.pin(name='Di<'+str(7-i)+'>', grid=r23_cmos, mn=r23_cmos.mn.bbox(cells[3*(7-i)].pins['I'])))
# pA2bar = dsn.pin(name='A2bar', grid=r23_cmos, mn=r23_cmos.mn.bbox(inv0.pins['O']))

pvss0 = dsn.pin(name='VSS', grid=r12, mn=r12.mn.bbox(rvss0))
pvdd0 = dsn.pin(name='VDD', grid=r12, mn=r12.mn.bbox(rvdd0))

# 7. Export to physical database.
print("Export design")

# Uncomment for BAG export
laygo2.interface.magic.export(lib, filename=ref_dir_MAG_exported +libname+'_'+cellname+'.tcl', cellname=None, libpath=ref_dir_layout, scale=1, reset_library=False, tech_library='sky130A')

# 8. Export to a template database file.
nat_temp = dsn.export_to_template()
laygo2.interface.yaml.export_template(nat_temp, filename=ref_dir_export+libname+'_templates.yaml', mode='append')