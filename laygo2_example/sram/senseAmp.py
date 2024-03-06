#####################################################################
#                                                                   #
#             SRAM Sense Amplifier Layout Gernerator                #
#                    Created by Hyungjoo Park                       #
#                                                                   #
#####################################################################

import numpy as np
import pprint
import laygo2
import laygo2.interface
import laygo2_tech as tech
import laygo2.object.physical as phy

# Parameter definitions #############
# Variables
cell_type = 'senseAmp'
nf = 1
nf_space = 2
# Templates
tpmos_name = 'pmos'
tnmos_name = 'nmos'
# Grids
pg_name = 'placement_basic'
r12_name = 'routing_12_cmos'
r23_name = 'routing_23_cmos'
r34_name = 'routing_34_basic'
# Design hierarchy
libname = 'sram'
cellname = cell_type+'_'+str(nf)+'x'
ref_dir_template = './laygo2_example/sram/' #export this layout's information into the yaml in this dir 
ref_dir_MAG_exported = ref_dir_template+'TCL/'
ref_dir_layout = './magic_layout'
# End of parameter definitions ######

# Generation start ##################
# 1. Load templates and grids.
print("Load templates")
templates_tech = tech.load_templates()
tpmos, tnmos = templates_tech[tpmos_name], templates_tech[tnmos_name]
templates = laygo2.interface.yaml.import_template(filename=ref_dir_template+'sram_templates.yaml')
tlib = laygo2.interface.yaml.import_template(filename='./laygo2_example/logic_ver2/logic_ver2_templates.yaml')

print("Load grids")
grids = tech.load_grids(templates=templates_tech)
pg, r12, r23, r34 = grids[pg_name], grids[r12_name], grids[r23_name], grids[r34_name]

# 2. Create a design hierarchy
lib = laygo2.object.database.Library(name=libname)
dsn = laygo2.object.database.Design(name=cellname, libname=libname)
lib.append(dsn)

# 3. Create istances.
print("Create instances")
nstack0 = templates['nmos130_2stack'].generate(name='nstack0')
nstack1 = templates['nmos130_2stack'].generate(name='nstack1', transform='MY')
nbndl = templates['nmos130_boundary'].generate(name='nbndl')
nbndr = templates['nmos130_boundary'].generate(name='nbndr')
nspace0 = templates['nmos130_space'].generate(name='nspace0')
nspace1 = templates['nmos130_space'].generate(name='nspace1')
pstack0 = templates['pmos130_2stack'].generate(name='pstack0', transform='MX')
pstack1 = templates['pmos130_2stack'].generate(name='pstack1', transform='MX')
pspace0 = templates['pmos130_space'].generate(name='pspace0',shape=[nf_space, 1], transform='MX')
pbndl = templates['pmos130_boundary'].generate(name='pbndl', transform='MX')
pbndr = templates['pmos130_boundary'].generate(name='pbndr', transform='MX')

inv0 = tlib['inv_2x'].generate(name='inv0')
inv1 = tlib['inv_2x'].generate(name='inv1')
# 4. Place instances.
pg_list = [0]*2
pg_list[1] = [None,pbndl,pstack0,pspace0,pstack1,pbndr,None,None]
pg_list[0] = [inv0,nbndl,nspace0,nstack0,nstack1,nspace1,nbndr,inv1]
dsn.place(grid=pg, inst=pg_list,mn=[0,0])

# 5. routing
# Enable
mn_list = [r12.mn(pstack0.pins['G0'])[0], r12.mn(pstack1.pins['G1'])[0], r12.mn(nstack0.pins['G1'])[1]]
_track = [None,int(np.mean([mn_list[0][1],mn_list[-1][1]]))]
dsn.route_via_track(grid=r12,mn=mn_list,track=_track)

# cross-couple
_mn = [r23.mn(nstack0.pins['G0'])[0], r23.mn(pstack0.pins['G1'])[1]]
_mn = [_mn[0],[_mn[1][0],_mn[0][1]],_mn[1]]
_cpl = dsn.route(grid=r23, mn=_mn, via_tag = [False, True, True])
rcpl0 = _cpl[-2] # last rect element
_mn = [r23.mn(nstack1.pins['G0'])[0], r23.mn(pstack1.pins['G0'])[1]]
_mn = [_mn[0],[_mn[1][0],_mn[0][1]],_mn[1]]
_cpl = dsn.route(grid=r23, mn=_mn, via_tag = [False, True, True])
rcpl1 = _cpl[-2] # last rect element

# 7. Export to physical database.
print("Export design")

# Uncomment for BAG export
laygo2.interface.magic.export(lib, filename=ref_dir_MAG_exported +libname+'_'+cellname+'.tcl', cellname=None, libpath=ref_dir_layout, scale=0.5, reset_library=False, tech_library='sky130A')

# 8. Export to a template database file.
nat_temp = dsn.export_to_template()
laygo2.interface.yaml.export_template(nat_temp, filename=ref_dir_template+libname+'_templates.yaml', mode='append')
