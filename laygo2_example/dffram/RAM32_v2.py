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
cell_type = 'ram32_v2'
nf = 1
nf_inv = 2
words_num = 32 # must be an even number
buffer_num = 40 # number of buffers
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
libname = 'dffram'
ref_dir_template = './laygo2_example/' #export this layout's information into the yaml in this dir 
ref_dir_export = './laygo2_example/dffram/'
ref_dir_MAG_exported = './laygo2_example/dffram/TCL/'
ref_dir_layout = './magic_layout'
# End of parameter definitions ######

# Generation start ##################
# 1. Load templates and grids.
print("Load templates")
templates = tech.load_templates()
tpmos, tnmos = templates[tpmos_name], templates[tnmos_name]
tlogic_prim = laygo2.interface.yaml.import_template(filename=ref_dir_template+'logic_ver2/logic_ver2_templates.yaml')
tlogic_adv = laygo2.interface.yaml.import_template(filename=ref_dir_template+'dffram/dffram_templates.yaml')

print("Load grids")
grids = tech.load_grids(templates=templates)
pg, r12, r23, r34, r45 = grids[pg_name], grids[r12_name], grids[r23_name], grids[r34_name], grids[r45_name]

cellname = cell_type+'_'+str(nf)+'x'
print('--------------------')
print('Now Creating '+cellname)

# 2. Create a design hierarchy
lib = laygo2.object.database.Library(name=libname)
dsn = laygo2.object.database.Design(name=cellname, libname=libname)
lib.append(dsn)

print("Create instances")
rams=list()
muxs = list()
dffs = list()
buf_in = list()
buf_we = list()
buf_sel = list()

buf_clk = tlogic_prim['ck_buf_4x'].generate(name='buf_ck')

ck_gate = dict()
ck_gate['gate'] = tlogic_adv['cgate_2x'].generate(name='ckg_gate', transform='MX')
ck_gate['inv0'] = tlogic_prim['inv_12x'].generate(name='ckg_inv0', transform='MX')
ck_gate['inv1'] = tlogic_prim['inv_36x'].generate(name='ckg_inv1', transform='MY')

dec8 = list()
for i in range(2):
    dec8.append(tlogic_adv['dec3x8_'+str(nf_inv)+'x'].generate(name='dec3x8_'+str(i), transform='R180'))
for i in range(2,4):
    dec8.append(tlogic_adv['dec3x8_'+str(nf_inv)+'x'].generate(name='dec3x8_'+str(i), transform='MX'))
for i in range(2):
    rams.append(tlogic_adv['ram8_v2_'+str(nf)+'x'].generate(name='ram8_'+str(i*2)))
    rams.append(tlogic_adv['ram8_v2_'+str(nf)+'x'].generate(name='ram8_'+str(i*2+1), transform='MX'))
# for i in range(words_num):
#     buf_sel.append(tlogic_prim['ck_buf_'+str(nf*2)+'x'].generate(name='buf_sel'+str(i+1)))
for i in range(32):
    buf_in.append(tlogic_prim['ck_buf_'+str(nf_inv*2)+'x'].generate(name='buf_in'+str(i+1)))
    dffs.append(tlogic_prim['dff_'+str(nf)+'x'].generate(name='dff'+str(i+1), transform='MX'))
    muxs.append(tlogic_prim['mux4to1_'+str(nf_inv)+'x'].generate(name='mux'+str(i+1)))
#     buf_out.append(tlogic_prim['ck_buf_'+str(nf)+'x'].generate(name='buf_out'+str(i+1),transform='MY'))   
for i in range(4):
    buf_we.append(tlogic_prim['ck_buf_'+str(nf_inv)+'x'].generate(name='buf_we'+str(i+1)))  

#dec4 = tlogic_adv['dec2x4_'+str(nf_inv)+'x'].generate(name='dec4', transform='MX')

# 4. Place instances.
_height_rail = pg.mn.height_vec(buf_in[0])
# RAM8
mn_ref = [0,0]
for i in range(2):
    dsn.place(grid=pg, inst=rams[i*2], mn=mn_ref)
    mn_ref = pg.mn.top_left(rams[i*2]) + pg.mn.height_vec(rams[0])
    dsn.place(grid=pg, inst=rams[2*i+1], mn=mn_ref)
    mn_ref = pg.mn.top_left(rams[i*2+1]) # + pg.mn.height_vec(dec8.inv0)*2
_maxwidth = np.maximum(pg.mn.width_vec(muxs[0]), np.maximum(pg.mn.width_vec(dffs[0]), pg.mn.width_vec(dffs[0])))
# # MUX - 4to1
mn_ref = pg.mn.top_left(rams[3])
_offset = pg.mn.bbox(rams[0].pins['Di31'])[0][0]
for i in range(2):
    _mn = mn_ref + [pg.mn.bbox(rams[3].pins['Di'+str(31 - i*8)])[0][0], 0] - [_offset,0]  
    for j in range(8):
        dsn.place(grid=pg, inst=muxs[8*(3-i)+(7-j)], mn=_mn)
        _mn = _mn + _maxwidth
_offset = pg.mn.top_right(rams[3])[0] - pg.mn.bbox(rams[0].pins['Di0'])[0][0]
for i in range(2):
    _mn = mn_ref + [pg.mn.bbox(rams[3].pins['Di'+str(i*8)])[0][0], 0] - pg.mn.width_vec(muxs[0]) + [_offset,0]   
    for j in range(8):
        dsn.place(grid=pg, inst=muxs[8*i+j], mn=_mn)
        _mn = _mn - _maxwidth
# DFF
mn_ref += _height_rail*2
_offset = pg.mn.bbox(rams[0].pins['Di31'])[0][0]
for i in range(2):
    _mn = mn_ref + [pg.mn.bbox(rams[3].pins['Di'+str(31 - i*8)])[0][0], 0] - [_offset,0]  
    for j in range(8):
        dsn.place(grid=pg, inst=dffs[8*(3-i)+(7-j)], mn=_mn)
        _mn = _mn + _maxwidth
_offset = pg.mn.top_right(rams[3])[0] - pg.mn.bbox(rams[0].pins['Di0'])[0][0]
for i in range(2):
    _mn = mn_ref + [pg.mn.bbox(rams[3].pins['Di'+str(i*8)])[0][0], 0] - pg.mn.width_vec(dffs[0]) + [_offset,0]   
    for j in range(8):
        dsn.place(grid=pg, inst=dffs[8*i+j], mn=_mn)
        _mn = _mn - _maxwidth

# Input Buffer
mn_ref += [0,0]
_offset = pg.mn.bbox(rams[0].pins['Di31'])[0][0]
for i in range(2):
    _mn = mn_ref + [pg.mn.bbox(rams[3].pins['Di'+str(31 - i*8)])[0][0], 0] - [_offset,0]  
    for j in range(8):
        dsn.place(grid=pg, inst=buf_in[8*(3-i)+(7-j)], mn=_mn)
        _mn = _mn + _maxwidth # pg.mn.width_vec(buf_in[8*(3-i)+(7-j)])
_offset = pg.mn.top_right(rams[3])[0] - pg.mn.bbox(rams[0].pins['Di0'])[0][0]
for i in range(2):
    _mn = mn_ref + [pg.mn.bbox(rams[3].pins['Di'+str(i*8)])[0][0], 0] - pg.mn.width_vec(buf_in[0]) + [_offset,0]   
    for j in range(8):
        dsn.place(grid=pg, inst=buf_in[8*i+j], mn=_mn)
        _mn = _mn - _maxwidth # pg.mn.width_vec(buf_in[8*i+j])
# dec8
mn_ref += _height_rail*2
_offset = pg.mn.bbox(rams[0].pins['Di31'])[0][0]
for i in range(2):
    _mn = mn_ref + [pg.mn.bbox(rams[3].pins['Di'+str(31 - i*8)])[0][0], 0] - [_offset,0]
    dsn.place(grid=pg, inst=dec8[3-i], mn=_mn)
_offset = pg.mn.top_right(rams[3])[0] - pg.mn.bbox(rams[0].pins['Di0'])[0][0]
for i in range(2):
    _mn = mn_ref + [pg.mn.bbox(rams[3].pins['Di'+str(i*8)])[0][0], 0] + [_offset,0]
    dsn.place(grid=pg, inst=dec8[i], mn=_mn)
# clk buffer
mn_cursor = pg.mn.bottom_right(muxs[16]) + pg.mn.width_vec(ck_gate['inv1'])
dsn.place(grid=pg, inst=ck_gate['inv1'], mn=mn_cursor)
mn_cursor = pg.mn.top_left(ck_gate['inv1']) + pg.mn.height_vec(ck_gate['gate'])
dsn.place(grid=pg, inst=ck_gate['gate'], mn=mn_cursor)
mn_cursor += pg.mn.width_vec(ck_gate['gate'])
dsn.place(grid=pg, inst=ck_gate['inv0'], mn=mn_cursor)
# 5. Create and place wires.
print("Create wires")

# 7. Export to physical database.
print("Export design")

# Uncomment for BAG export
laygo2.interface.magic.export(lib, filename=ref_dir_MAG_exported +libname+'_'+cellname+'.tcl', cellname=None, libpath=ref_dir_layout, scale=0.5, reset_library=False, tech_library='sky130A')

# 8. Export to a template database file.
nat_temp = dsn.export_to_template()
laygo2.interface.yaml.export_template(nat_temp, filename=ref_dir_export+libname+'_templates.yaml', mode='append')
