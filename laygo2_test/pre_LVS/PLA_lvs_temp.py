###########################################
#                                         #
#          PLA Layout Generator           #
#        Created by HyungJoo Park         #   
#                                         #
###########################################


import numpy as np
import random
import pprint
import laygo2
import laygo2.interface
import laygo2_tech as tech
#import netmap_template as nMap
import pre_lvs_module_test as nMap
# Parameter definitions #############
# Variables
cell_type = 'PLA'
nf_list = [2]
inv_num = 600
nand_num = 600
# Templates
tpmos_name = 'pmos_sky'
tnmos_name = 'nmos_sky'
# Grids
pg_name = 'placement_basic'
r12_name = 'routing_12_cmos'
r23_name = 'routing_23_cmos'
r34_name = 'routing_34_basic'
# Design hierarchy
libname = 'logic_generated'
ref_dir_template = './laygo2_test/logic/' #export this layout's information into the yaml in this dir 
ref_dir_MAG_exported = './laygo2_test/logic/TCL/'
# End of parameter definitions ######

# define via_table for pre-lvs
via_table = dict()
via_table["via_M1_M2_0"] = ('M1','M2')
via_table["via_M1_M2_1"] = ('M1','M2')
via_table["via_M2_M3_0"] = ('M2','M3')
via_table["via_M2_M3_1"] = ('M2','M3')
via_table["via_M3_M4_0"] = ('M3','M4')
via_table["via_M4_M5_0"] = ('M4','M5')

#define macro functions for this topology
def gen_place_inv(dsn, grid, tlib, num, nf):
    inverters = list()
    for idx in range (num):
        _name = "in" + str(idx)
        if idx % 4 < 2:
            inverters.append(tlib['inv_'+str(nf)+'x'].generate(name=_name, netname={'I':"dat_in"+str(idx),'O':'dat_in'+str(idx)+'_bar','VSS':'VSS','VDD':'VDD'}))
        else:
            inverters.append(tlib['inv_'+str(nf)+'x'].generate(name=_name, transform = 'MX', netname={'I':"dat_in"+str(idx),'O':'dat_in'+str(idx)+'_bar','VSS':'VSS','VDD':'VDD'}))

    dsn.place(grid=pg, inst=inverters[0], mn=pg.mn.top_left(space2_0))

    for idx in range (1, num):
        if idx % 4 == 0:
            dsn.place(grid=grid, inst=inverters[idx], mn=pg.mn.top_left(inverters[idx-2]))
        elif idx % 4 == 1:
            dsn.place(grid=grid, inst=inverters[idx], mn=pg.mn.bottom_right(inverters[idx-1]))
        elif idx % 4 == 2:
            dsn.place(grid=grid, inst=inverters[idx], mn=pg.mn.top_left(inverters[idx-2]) + pg.mn.height_vec(inverters[idx]))
        else:
            dsn.place(grid=grid, inst=inverters[idx], mn=pg.mn.top_right(inverters[idx-1]))
    return inverters

def gen_place_nand(dsn, grid, tlib, num):
    nand_lower = list()
    nand_upper = list()
    space0_0 = tlib['space_4x'].generate(name='space0_0', netname={'VSS':'VSS','VDD':'VDD'})
    space0_1 = tlib['space_4x'].generate(name='space0_1', netname={'VSS':'VSS','VDD':'VDD'})
    space1 = tlib['space_2x'].generate(name='space1', netname={'VSS':'VSS','VDD':'VDD'})
    space2_0 = tlib['space_4x'].generate(name='space2_0', transform='MX', netname={'VSS':'VSS','VDD':'VDD'})
    space2_1 = tlib['space_4x'].generate(name='space2_1', transform='MX', netname={'VSS':'VSS','VDD':'VDD'})
    space3 = tlib['space_2x'].generate(name='space3', transform='MX', netname={'VSS':'VSS','VDD':'VDD'})
    for idx in range(num):
        _name = 'nand_lower_'+str(idx)
        nand_lower.append(tlib['nand_2x'].generate(name=_name,netname={'VSS':'VSS','VDD':'VDD'}))
    for idx in range(num):
        _name = 'nand_upper_'+str(idx)
        nand_upper.append(tlib['nand_2x'].generate(name=_name,transform='MX',netname={'VSS':'VSS','VDD':'VDD'}))    

    dsn.place(grid=grid, inst=space0_0, mn=[0,0])
    dsn.place(grid=grid, inst=space0_1, mn=pg.mn.bottom_right(space0_0))
    dsn.place(grid=grid, inst=space1, mn=pg.mn.bottom_right(space0_1))
    dsn.place(grid=grid, inst=nand_lower[0],mn=pg.mn.bottom_right(space1))
    dsn.place(grid=grid, inst=space2_0, mn=pg.mn.top_left(space0_0) + pg.mn.height_vec(space1))
    dsn.place(grid=grid, inst=space2_1, mn=pg.mn.top_right(space2_0))
    dsn.place(grid=grid, inst=nand_upper[0], mn=pg.mn.top_right(space2_1))
    for idx in range(num-1):
        dsn.place(grid=grid, inst=nand_lower[idx+1],mn=pg.mn.bottom_right(nand_lower[idx]))
        dsn.place(grid=grid, inst=nand_upper[idx+1], mn=pg.mn.top_right(nand_upper[idx]))
    dsn.place(grid=pg, inst=space3, mn=pg.mn.top_right(nand_upper[num-1]))
    return space2_0, nand_lower, nand_upper

def route_nand(dsn, grid, nand, input, input_name):
    _mn = [grid.mn(nand.pins['A'])[1], [grid.mn(nand.pins['A'])[1][0],input[0][1]], input[0]]
    dsn.route(grid=grid, mn=_mn, via_tag=[False, True, True])
    nand.pins['A'].netname = input_name[0]

    _mn = [grid.mn(nand.pins['B'])[1], [grid.mn(nand.pins['B'])[1][0],input[1][1]], input[1]]
    dsn.route(grid=grid, mn=_mn, via_tag=[False, True, True])
    nand.pins['B'].netname = input_name[1]

# Generation start ##################
# 1. Load templates and grids.
print("Load templates")
templates = tech.load_templates()
tpmos, tnmos = templates[tpmos_name], templates[tnmos_name]
tlib = laygo2.interface.yaml.import_template(filename=ref_dir_template+'logic_generated_templates.yaml')
#print(templates[tpmos_name], templates[tnmos_name], sep="\n")

print("Load grids")
grids = tech.load_grids(templates=templates)
pg, r12, r23, r34 = grids[pg_name], grids[r12_name], grids[r23_name], grids[r34_name]
#print(grids[pg_name], grids[r12_name], grids[r23_name], grids[r34_name], sep="\n")

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
# 4. Place instances.
#Nands
    space2_0, nand_lower, nand_upper = gen_place_nand(dsn, pg, tlib, nand_num)
#Inverters
    inverters = gen_place_inv(dsn, pg, tlib, inv_num, nf)
    #dsn.place(grid=pg, inst=inv0, mn=pg.mn.top_left(space2_0))
    #dsn.place(grid=pg, inst=inv1, mn=pg.mn.bottom_right(inv0))
    #dsn.place(grid=pg, inst=inv2, mn=pg.mn.top_left(inv0) + pg.mn.height_vec(inv2))
    #dsn.place(grid=pg, inst=inv3, mn=pg.mn.top_right(inv2))
# 5. Create and place wires.
    print("Create wires")
   
   # 1st M4
    '''mn_A_bar = r34.mn(inv0.pins['O'])[0]
    mn_A = r34.mn(inv0.pins['I'])[0]
    mn_B = r34.mn(inv1.pins['I'])[1]
    mn_B_bar = r34.mn(inv1.pins['O'])[1]

    mn_C_bar = r34.mn(inv2.pins['O'])[0]
    mn_C = r34.mn(inv2.pins['I'])[0]
    mn_D = r34.mn(inv3.pins['I'])[1] 
    mn_D_bar = r34.mn(inv3.pins['O'])[1]'''

    inputs = list()
    input_names = list()
    for idx in range (inv_num):
        if idx % 2 == 0:
            inputs.append(r34.mn(inverters[idx].pins['O'])[0])
            input_names.append('dat_'+inverters[idx].name+'_bar')
            inputs.append(r34.mn(inverters[idx].pins['I'])[0])
            input_names.append('dat_'+inverters[idx].name)
        else:
            inputs.append(r34.mn(inverters[idx].pins['O'])[1])
            input_names.append('dat_'+inverters[idx].name+'_bar')
            inputs.append(r34.mn(inverters[idx].pins['I'])[1])
            input_names.append('dat_'+inverters[idx].name)

    for idx in range (nand_num):
        rand1 = random.randrange(0, 2*inv_num-1)
        rand2 = random.randrange(0, 2*inv_num-1)
        route_nand(dsn, r34, nand_lower[idx], [inputs[rand1], inputs[rand2]],[input_names[rand1],input_names[rand2]])
        rand1 = random.randrange(0, 2*inv_num-1)
        rand2 = random.randrange(0, 2*inv_num-1)
        route_nand(dsn, r34, nand_upper[idx], [inputs[rand1], inputs[rand2]],[input_names[rand1],input_names[rand2]])


    '''route_nand(dsn, r34, nand_lower[0], [mn_B, mn_A_bar],['dat_B','dat_A_bar'])
    route_nand(dsn, r34, nand_lower[1], [mn_A, mn_B_bar],['dat_A','dat_B_bar'])
    route_nand(dsn, r34, nand_lower[2], [mn_C, mn_D],['dat_C','dat_D'])
    route_nand(dsn, r34, nand_lower[3], [mn_C_bar, mn_D_bar],['dat_C_bar','dat_D_bar'])

    route_nand(dsn, r34, nand_lower[4], [mn_C_bar, mn_A_bar],['dat_C_bar','dat_A_bar'])
    route_nand(dsn, r34, nand_lower[5], [mn_D_bar, mn_B_bar],['dat_D_bar','dat_B_bar'])
    route_nand(dsn, r34, nand_lower[6], [mn_A, mn_C],['dat_A','dat_C'])
    route_nand(dsn, r34, nand_lower[7], [mn_B, mn_D],['dat_B','dat_D'])

    route_nand(dsn, r34, nand_upper[0], [mn_A, mn_C],['dat_A','dat_C'])
    route_nand(dsn, r34, nand_upper[1], [mn_B, mn_D],['dat_B','dat_D'])
    route_nand(dsn, r34, nand_upper[2], [mn_C_bar, mn_A_bar],['dat_C_bar','dat_A_bar'])
    route_nand(dsn, r34, nand_upper[3], [mn_D_bar, mn_B_bar],['dat_D_bar','dat_B_bar'])
    
    route_nand(dsn, r34, nand_upper[4], [mn_C, mn_D],['dat_C','dat_D'])
    route_nand(dsn, r34, nand_upper[5], [mn_C_bar, mn_D_bar],['dat_C_bar','dat_D_bar'])
    route_nand(dsn, r34, nand_upper[6], [mn_B, mn_A_bar],['dat_B','dat_A_bar'])
    route_nand(dsn, r34, nand_upper[7], [mn_A, mn_B_bar],['dat_A','dat_B_bar'])'''
    # _mn = [mn_A, r34.mn(nand1.pins['A'])[1], r34.mn(nand4.pins['A'])[1]]
    # _track = [None, mn_A[1]]
    # rA = dsn.route_via_track(grid=r34, mn=_mn, track=_track)

    # _mn = [mn_A_bar, r34.mn(nand0.pins['B'])[1], r34.mn(nand6.pins['B'])[1]]
    # _track = [None, mn_A_bar[1]]
    # rA_bar = dsn.route_via_track(grid=r34, mn=_mn, track=_track)   

    # _mn = [mn_B, r34.mn(nand0.pins['A'])[1], r34.mn(nand5.pins['A'])[1]]
    # _track = [None, mn_B[1]]
    # rB = dsn.route_via_track(grid=r34, mn=_mn, track=_track)

    # _mn = [mn_B_bar, r34.mn(nand1.pins['B'])[1], r34.mn(nand7.pins['B'])[1]]
    # _track = [None, mn_B_bar[1]]
    # rB_bar = dsn.route_via_track(grid=r34, mn=_mn, track=_track)

    # _mn = [mn_C, r34.mn(nand2.pins['A'])[1], r34.mn(nand4.pins['B'])[1]]
    # _track = [None, mn_C[1]]
    # rC = dsn.route_via_track(grid=r34, mn=_mn, track=_track)

    # _mn = [mn_C_bar, r34.mn(nand3.pins['A'])[1], r34.mn(nand6.pins['A'])[1]]
    # _track = [None, mn_C_bar[1]]
    # rC_bar = dsn.route_via_track(grid=r34, mn=_mn, track=_track)  

    # _mn = [mn_D, r34.mn(nand2.pins['B'])[1], r34.mn(nand5.pins['B'])[1]]
    # _track = [None, mn_D[1]]
    # rD = dsn.route_via_track(grid=r34, mn=_mn, track=_track) 

    # _mn = [mn_D_bar, r34.mn(nand3.pins['B'])[1], r34.mn(nand7.pins['A'])[1]]
    # _track = [None, mn_D_bar[1]]
    # rD_bar = dsn.route_via_track(grid=r34, mn=_mn, track=_track)
#    # VSS
#     rvss0 = dsn.route(grid=r12, mn=[r12.mn.bottom_left(inv0), r12.mn.bottom_right(inv3)],netname='VSS')
   
#    # VDD
#     rvdd0 = dsn.route(grid=r12, mn=[r12.mn.top_left(inv0), r12.mn.top_right(inv3)],netname='VDD')
   
#    # 6. Create pins.

   

    nMap.netMap.lvs_check(dsn, r34, via_table)
   # # 7. Export to physical database.
   # print("Export design")
   
   # Uncomment for BAG export
    laygo2.interface.magic.export(lib, filename=ref_dir_MAG_exported +libname+'_'+cellname+'.tcl', cellname=None, libpath='./magic_layout', scale=1, reset_library=False, tech_library=tech.name)
   
   # 8. Export to a template database file.
    nat_temp = dsn.export_to_template()
    laygo2.interface.yaml.export_template(nat_temp, filename=ref_dir_template+libname+'_templates.yaml', mode='append')