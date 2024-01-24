import parselef
import yaml
from parselef import lef_parser

lef_osu = lef_parser.LefParser("./sky130_osu_sc_t12/12T_hs/lef/sky130_osu_sc_12T_hs.lef")
lef_osu.parse()

scale = 100
export_path = 'laygo2_example/osu_12t/'
lib_name = 'sky130_osu_sc_12T_hs'

templates = dict()
for cellname, cell in lef_osu.macro_dict.items():
    cellname_real = cellname.replace(lib_name+'__','')
    _info = dict()
    _info['bbox'] = [tuple(int(elem) for elem in cell.info['ORIGIN']), tuple(int(scale*elem) for elem in cell.info['SIZE'])]
    _info['cellname'] = cellname_real
    _info['libname'] = lib_name
    _info['pins']=dict()
    for pin in cell.info['PIN']:
        if pin.name == 'vdd':
            pinname = 'VDD'
        elif pin.name == 'vss' or pin.name == 'gnd' or pin.name == 'GND':
            pinname = 'VSS'
        else:
            pinname = pin.name
        _info['pins'][pinname] = dict()
        _pin = _info['pins'][pinname]
        port = pin.info['PORT']
        for layer in port.info['LAYER']:
            _pin['layer'] = layer.name.replace('met','M')
            _pin['name'] = pinname
            _pin['netname'] = pinname
            area_max = 0
            bbox = list()
            for shape in layer.shapes:
                _bbox = shape.points
                area = (_bbox[1][0] - _bbox[0][0])*(_bbox[1][1] - _bbox[0][1])
                if area > area_max:
                    bbox = _bbox
            _xy = list()
            _xy.append(tuple(int(scale*elem) for elem in bbox[0]))
            _xy.append(tuple(int(scale*elem) for elem in bbox[1]))
            _pin['xy'] = _xy
    templates[cellname_real] = _info

lib = {lib_name:templates}
with open(export_path+lib_name+'.yaml', 'w') as f:
    yaml.safe_dump(lib, f)
"""
for pin in lef_osu.macro_dict['sky130_osu_sc_12T_hs__nand2_1'].info['PIN']:
    print("Pin:", pin.name)
    print("Property:",pin.info['USE'], pin.info['DIRECTION'])
    port = pin.info['PORT']
    print('   port: ')
    for layer in port.info['LAYER']:
        print("   ",layer.name)
        for shape in layer.shapes:
            print("      ",shape.points)
"""