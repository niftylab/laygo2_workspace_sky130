from PySpice.Spice.Netlist import Circuit, SubCircuit, SubCircuitFactory
from PySpice.Unit import *
import matplotlib.pyplot as plt
import numpy as np
import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()
import yaml
#open spice file and check whether VSS is before VDD or not
spec = "./laygo2_example/scan/scan_spec.yaml"
with open(spec, 'r') as stream:
   specdict = yaml.load(stream, Loader=yaml.FullLoader)
bit = specdict['bit']
_FIRST = 'VDD'
spice_file = "./scan_chain_%dbit.spice" %(bit)
f = open(spice_file,'r')
line = f.readline()
terms = line.split()
while 'VDD' not in terms and 'VSS' not in terms:
    line = f.readline()
    terms = line.split()
if 'VSS' not in terms:
    pass # VDD first
elif 'VDD' not in terms:
    _FIRST = 'VSS'
else:
    if terms.index('VSS') < terms.index('VDD'):
        _FIRST = 'VSS'
    else:
        pass # VDD first
f.close()
#set pin list of chain
pin_list = ['clk','clk_out']
for idx in range(bit):
    # pin_list.append('data_in<%d>'%(idx))
    pin_list.append('data_in')
for idx in range(bit):
    pin_list.append('data_out%d'%(idx))
pin_list.extend(['enable','reset'])
for idx in range(bit):
    # pin_list.append('reset_val<%d>'%(idx))
    pin_list.append('reset_val')
pin_list.extend(['shift_in','data_load','shift_out'])
if _FIRST == 'VSS':
    pin_list.extend(['0','VDD'])
else:
    pin_list.extend(['VDD','0'])

circuit = Circuit('tb_scan_chain_%dbit'%(bit))
circuit.lib('/usr/local/share/pdk/sky130A/libs.tech/ngspice/sky130.lib.spice', 'tt')
circuit.include(spice_file)
circuit.X('SCH','scan_chain_%dbit'%(bit),' '.join(pin_list))
circuit.V('power', 'VDD', circuit.gnd, 1.8)
circuit.V('dat', 'data_in', circuit.gnd, 1.8)
circuit.V('load', 'data_load', circuit.gnd, 0)
circuit.V('reset', 'reset', circuit.gnd, 0)
circuit.V('reset_val', 'reset_val', circuit.gnd, 1.8)
circuit.PulseVoltageSource('ser', 'shift_in', circuit.gnd,
                           initial_value=0@u_V, pulsed_value=1.8@u_V,
                           rise_time=0.01@u_ns, fall_time=0.01@u_ns,
                           pulse_width=6@u_ns, period=12@u_ns, delay_time=0@u_ns)
circuit.PulseVoltageSource('clk', 'clk', circuit.gnd,
                           initial_value=0@u_V, pulsed_value=1.8@u_V,
                           rise_time=0.01@u_ns, fall_time=0.01@u_ns,
                           pulse_width=3@u_ns, period=6@u_ns, delay_time=3@u_ns)
circuit.PulseVoltageSource('en', 'enable', circuit.gnd,
                           initial_value=0@u_V, pulsed_value=1.8@u_V,
                           rise_time=0.01@u_ns, fall_time=0.01@u_ns,
                           pulse_width=60@u_ns, period=63@u_ns, delay_time=0@u_ns)
print(circuit)
print('simulation start')
simulator = circuit.simulator()
analysis = simulator.transient(step_time=200@u_ps, end_time=63@u_ns)
print('done')
subplotNum = int(bit/2)+ + bit%2
rows = int(subplotNum/2)+1

plt.subplot(rows,2,1)
plt.plot(np.array(analysis.time), np.array(analysis['clk']))
plt.plot(np.array(analysis.time), np.array(analysis['shift_in']))
plt.legend(('clk', 'shift_in'))
# plt.subplot(rows,2,2)
# plt.plot(np.array(analysis.time), np.array(analysis['shift_in']))
# plt.plot(np.array(analysis.time), np.array(analysis['shift_out']))
# plt.legend(('shift_in', 'shift_out'))
for idx in range(subplotNum-1):
    plt.subplot(rows,2,idx+2)
    plt.plot(np.array(analysis.time), np.array(analysis['data_out%d'%(idx*2)]))
    plt.plot(np.array(analysis.time), np.array(analysis['data_out%d'%(idx*2+1)]))
    plt.legend(('data_out%d'%(idx*2), 'data_out%d'%(idx*2+1)))    
if bit%2 == 1:
    plt.subplot(rows,2,subplotNum+1)
    plt.plot(np.array(analysis.time), np.array(analysis['data_out%d'%(bit-1)]))
    plt.legend(('data_out%d'%(bit-1)))
else:
    plt.subplot(rows,2,subplotNum+1)
    plt.plot(np.array(analysis.time), np.array(analysis['data_out%d'%(bit-2)]))
    plt.plot(np.array(analysis.time), np.array(analysis['data_out%d'%(bit-1)]))
    plt.legend(('data_out%d'%(bit-2), 'data_out%d'%(bit-1)))    

# plt.subplot(rows,2,3)
# plt.plot(np.array(analysis.time), np.array(analysis['data_out0']))
# plt.plot(np.array(analysis.time), np.array(analysis['data_out1']))
# plt.legend(('data_out0', 'data_out1'))
# plt.subplot(rows,2,4)
# plt.plot(np.array(analysis.time), np.array(analysis['data_out2']))
# plt.plot(np.array(analysis.time), np.array(analysis['data_out3']))
# plt.legend(('data_out2', 'data_out3'))
plt.tight_layout()
plt.show()