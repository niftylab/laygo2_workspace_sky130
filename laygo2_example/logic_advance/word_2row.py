###########################################
#                                         #
#       32bit WORD Layout Generator       #
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
cell_type = 'word_2row'
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

cells=list()
for i in range(2):
    cells.append(tlogic_adv['byte_dff_'+str(nf)+'x'].generate(name='byte_dff'+str(i*2)))
    cells.append(tlogic_adv['byte_dff_'+str(nf)+'x'].generate(name='byte_dff'+str(i*2+1), transform='MX'))
buf_sel=[]
buf_sel.append(tlogic_prim['inv_'+str(36)+'x'].generate(name='inv_sel0', transform='MX'))
buf_sel.append(tlogic_prim['inv_'+str(36)+'x'].generate(name='inv_sel1', transform='MY'))
tgate0 = tlogic_prim['tgate_'+str(nf)+'x'].generate(name='gate_clk')
NTAP1 = templates[tntap_name].generate(name='MNT1', transform='MX', params={'nf':4, 'tie':'TAP0'})
PTAP1 = templates[tptap_name].generate(name='MPT1', params={'nf':4, 'tie':'TAP0'})

# 4. Place instances.
_TAP = [0]*2
_TAP[1] = [NTAP1]
_TAP[0] = [PTAP1]

mn_ref = [0,0]
dsn.place(grid=pg, inst=cells[0], mn=mn_ref)
mn_ref = pg.mn.top_left(cells[0]) + pg.mn.height_vec(cells[1])
dsn.place(grid=pg, inst=cells[1], mn=mn_ref)
mn_ref = pg.mn.bottom_right(cells[0]) + pg.mn.width_vec(buf_sel[1])
dsn.place(grid=pg, inst=buf_sel[1], mn=mn_ref)
mn_ref = pg.mn.top_left(buf_sel[1]) + pg.mn.height_vec(buf_sel[0])
dsn.place(grid=pg, inst=buf_sel[0], mn=mn_ref)
mn_ref = pg.mn.bottom_right(buf_sel[1])
dsn.place(grid=pg, inst=tgate0, mn=mn_ref)
mn_ref = pg.mn.top_left(tgate0)
dsn.place(grid=pg, inst=_TAP, mn=mn_ref)
mn_ref = pg.mn.bottom_right(tgate0)
dsn.place(grid=pg, inst=cells[2], mn=mn_ref)
mn_ref = pg.mn.top_left(cells[2]) + pg.mn.height_vec(cells[3])
dsn.place(grid=pg, inst=cells[3], mn=mn_ref)
# 5. Create and place wires.
print("Create wires")
## input sig == sel_bar(dec outputs are inverted) -> inv_sel out == sel
# sel
mn_list = [r23.mn(buf_sel[0].pins['O'])[0], r23.mn(buf_sel[1].pins['I'])[1]]
_track = [None, r23.mn(buf_sel[1].pins['I'])[1,1]]
dsn.route_via_track(grid=r23, mn=mn_list, track=_track)

mn_list = [r34.mn(cells[0].pins['SEL'])[1], r34.mn(buf_sel[1].pins['O'])[0], r34.mn(cells[2].pins['SEL'])[0]]
_track = [None, r34.mn(cells[0].pins['SEL'])[1,1]]
rsel = dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
mn_list = [r34.mn(cells[1].pins['SEL'])[1], r34.mn(buf_sel[1].pins['O'])[1], r34.mn(cells[3].pins['SEL'])[0]]
_track = [None, r34.mn(cells[1].pins['SEL'])[1,1]]
dsn.route_via_track(grid=r34, mn=mn_list, track=_track)
mn_list = [r23.mn(buf_sel[1].pins['I'])[1], r23.mn(tgate0.pins['ENB'])[1]]
dsn.route(grid=r23, mn=mn_list, via_tag=[False, False])
mn_list = [r23.mn(buf_sel[1].pins['O'])[1], r23.mn(tgate0.pins['EN'])[0]]
_track = [None, r23.mn(buf_sel[1].pins['O'])[1,1]]
dsn.route_via_track(grid=r23, mn=mn_list, track=_track)

# clk
mn_list = [r34.mn(cells[0].pins['CLK'])[0],r34.mn(cells[1].pins['CLK'])[1]]
rclk0 = dsn.route(grid=r34, mn=mn_list, via_tag=[False, False])
mn_list = [r34.mn(cells[2].pins['CLK'])[0],r34.mn(cells[3].pins['CLK'])[1]]
rclk1 = dsn.route(grid=r34, mn=mn_list, via_tag=[False, False])
_mid = int((r34.mn(rclk0)[0,1]+r34.mn(rclk0)[1,1])/2)
mn_list = [ [r34.mn(rclk0)[0,0],_mid],[r34.mn(rclk1)[0,0],_mid] ]
vclk0, rclk2, vclk1 = dsn.route(grid=r34, mn=mn_list, via_tag=[True, True])
mn_list = [r34.mn(tgate0.pins['O'])[1], [ r34.mn(tgate0.pins['O'])[1,0], _mid] ]
dsn.route(grid=r34, mn=mn_list, via_tag=[False, True])
# VSS
rvss0 = dsn.route(grid=r12, mn=[r12.mn.top_left(cells[1]), r12.mn.top_right(cells[3])])
rvss1 = dsn.route(grid=r12, mn=[r12.mn.bottom_left(cells[0]), r12.mn.bottom_right(cells[2])])
# VDD
rvdd0 = dsn.route(grid=r12, mn=[r12.mn.top_left(cells[0]), r12.mn.top_right(cells[2])])

# 6. Create pins.
# psel_bar = dsn.pin(name='SelBar', grid=r23_cmos, mn=r23_cmos.mn.bbox(cells[0].pins['SelBar']))
psel = dsn.pin(name='SEL', grid=r34, mn=r34.mn.bbox(buf_sel[0].pins['I']))
pwe = list()
for i in range(4):
    pwe.append(dsn.pin(name='WE<'+str(3-i)+'>', grid=r23_cmos, mn=r23_cmos.mn.bbox(cells[i].pins['WE'])))
pclk = dsn.pin(name='CLK', grid=r34, mn=r34.mn.bbox(tgate0.pins['I']))
pDo = list()
pDi = list()
for i in range(4):
    for j in range(8):
        pDo.append(dsn.pin(name='Do<'+str(8*(3-i)+(7-j))+'>', grid=r23_cmos, mn=r23_cmos.mn.bbox(cells[i].pins['Do<'+str(j)+'>'])))
        pDi.append(dsn.pin(name='Di<'+str(8*(3-i)+(7-j))+'>', grid=r23_cmos, mn=r23_cmos.mn.bbox(cells[i].pins['Di<'+str(j)+'>'])))
pvss0 = dsn.pin(name='VSS', grid=r12, mn=r12.mn.bbox(rvss0))
pvdd0 = dsn.pin(name='VDD', grid=r12, mn=r12.mn.bbox(rvdd0))

# 7. Export to physical database.
print("Export design")

# Uncomment for BAG export
laygo2.interface.magic.export(lib, filename=ref_dir_MAG_exported +libname+'_'+cellname+'.tcl', cellname=None, libpath=ref_dir_layout, scale=1, reset_library=False, tech_library='sky130A')

# 8. Export to a template database file.
nat_temp = dsn.export_to_template()
laygo2.interface.yaml.export_template(nat_temp, filename=ref_dir_export+libname+'_templates.yaml', mode='append')