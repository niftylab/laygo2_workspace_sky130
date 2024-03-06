###########################################
#                                         #
#      D-Flip Flop Layout Generator       #
#         Created by Taeho Shin           #   
#                                         #
###########################################


import numpy as np
import pprint
import laygo2
import laygo2.interface
import laygo2_tech as tech

# Parameter definitions #############
# Variables
cell_type = 'grid_test'
nf_list = [2]
# Templates
tpmos_name = 'pmos'
tnmos_name = 'nmos'
# Grids
pg_name = 'placement_basic'
r12_name = 'routing_12_cmos'
r23_name = 'routing_23_cmos'
r34_name = 'routing_34_basic'
r45_name = 'routing_45_basic'
# Design hierarchy
libname = 'logic_ver2'
ref_dir_template = './laygo2_example/logic_ver2/' #export this layout's information into the yaml in this dir 
ref_dir_MAG_exported = './laygo2_example/logic_ver2/TCL/'
ref_dir_layout = './magic_layout'
# End of parameter definitions ######

# Generation start ##################
# 1. Load templates and grids.
print("Load templates")
templates = tech.load_templates()
tpmos, tnmos = templates[tpmos_name], templates[tnmos_name]
tlib = laygo2.interface.yaml.import_template(filename=ref_dir_template+'logic_ver2_templates.yaml')
print(templates[tpmos_name], templates[tnmos_name], sep="\n")

print("Load grids")
grids = tech.load_grids(templates=templates)
pg, r12, r23, r34 ,r45= grids[pg_name], grids[r12_name], grids[r23_name], grids[r34_name], grids[r45_name]

for nf in nf_list:
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
    inv1 = tlib['inv_'+str(nf)+'x'].generate(name='inv1')
    inv2 = tlib['inv_'+str(nf)+'x'].generate(name='inv2', transform='MX')
    inv3 = tlib['inv_'+str(nf)+'x'].generate(name='inv3', transform='MX') 

    tinv0 = tlib['tinv_'+str(nf)+'x'].generate(name='tinv0')
    tinv1 = tlib['tinv_'+str(nf)+'x'].generate(name='tinv1', transform='MX')

    tinv_small0 = tlib['tinv_small_1x'].generate(name='tinv_small0')
    tinv_small1 = tlib['tinv_small_1x'].generate(name='tinv_small1', transform='MX')

    # 4. Place instances.
    pg_list = [0]*2
    pg_list[1] = [inv2,inv3,tinv1,tinv_small1]
    pg_list[0] = [inv0,inv1,tinv0,tinv_small0]

    dsn.place(grid=pg, inst=pg_list,mn=[0,0])

    # 5. Create and place wires.
    print("Create wires")

    # 1st M4

    _mn = [r45.mn(inv0.pins['I'])[1], r45.mn(inv2.pins['O'])[0]]
    _track = [None, r45.mn(inv2.pins['O'])[0,1]-2]
    dsn.route_via_track(grid=r45, mn=_mn, track=_track)

    _mn = [r45.mn(inv0.pins['I'])[1],r45.mn(inv2.pins['I'])[1]]
    for i in range(5):
        _mn.append(_mn[-2]+[1,0])
        _mn.append(_mn[-2]+[1,0])
    dsn.route_via_track(grid=r45, mn=_mn, track=_track)
    # # VSS
    # rvss0 = dsn.route(grid=r12, mn=[r12.mn.bottom_left(inv0), r12.mn.bottom_right(inv3)])

    # # VDD
    # rvdd0 = dsn.route(grid=r12, mn=[r12.mn.top_left(inv0), r12.mn.top_right(inv3)])

    # 6. Create pins.
    pin0 = dsn.pin(name='I', grid=r23, mn=r23.mn.bbox(tinv0.pins['I']))
    pclk0 = dsn.pin(name='CLK', grid=r23, mn=r23.mn.bbox(inv0.pins['I']))
    pout0 = dsn.pin(name='O', grid=r23, mn=r23.mn.bbox(inv3.pins['O']))
    # pvss0 = dsn.pin(name='VSS', grid=r12, mn=r12.mn.bbox(rvss0))
    # pvdd0 = dsn.pin(name='VDD', grid=r12, mn=r12.mn.bbox(rvdd0))

    # 7. Export to physical database.
    print("Export design")
    # Uncomment for BAG export
    laygo2.interface.magic.export(lib, filename=ref_dir_MAG_exported +libname+'_'+cellname+'.tcl', cellname=None, libpath=ref_dir_layout, scale=0.5, reset_library=False, tech_library=tech.name)
    # 8. Export to a template database file.
    nat_temp = dsn.export_to_template()
    laygo2.interface.yaml.export_template(nat_temp, filename=ref_dir_template+libname+'_templates.yaml', mode='append')
