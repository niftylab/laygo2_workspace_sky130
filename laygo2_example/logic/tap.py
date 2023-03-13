import numpy as np
import pprint
import laygo2
import laygo2.interface
import laygo2_tech as tech

tptap_name = 'ptap_sky'
tntap_name = 'ntap_sky'
cell_type = 'TAP'

pg_name = 'placement_basic'
r12_name = 'routing_12_cmos'

libname = 'logic_generated'
ref_dir_template = './laygo2_example/logic/' #export this layout's information into the yaml in this dir 
ref_dir_MAG_exported = './laygo2_example/logic/TCL/'
ref_dir_layout = './magic_layout'

templates = tech.load_templates()
tptap, tntap = templates[tptap_name], templates[tntap_name]

grids = tech.load_grids(templates=templates)
pg, r12 = grids[pg_name], grids[r12_name]

lib = laygo2.object.database.Library(name=libname)

cellname = cell_type
dsn = laygo2.object.database.Design(name=cellname, libname=libname)
lib.append(dsn)
      
# 3. Create instances.
print("Create instances")
int0 = tntap.generate(name='MNT0', params={'nf': 2, 'tie': 'TAP0'})
ipt0 = tptap.generate(name='MPT0', transform='MX', params={'nf': 2,'tie': 'TAP0'})
      
dsn.place(grid=pg, inst=int0, mn=[0,0])
dsn.place(grid=pg, inst=ipt0, mn=pg.mn.top_left(int0) + pg.mn.height_vec(ipt0))

print("Export design")
print("")

laygo2.interface.magic.export(lib, filename=ref_dir_MAG_exported +libname+'_'+cellname+'.tcl', cellname=None, libpath=ref_dir_layout, scale=1, reset_library=False, tech_library='sky130A')

nat_temp = dsn.export_to_template()
laygo2.interface.yaml.export_template(nat_temp, filename=ref_dir_template+libname+'_templates.yaml', mode='append')
