import csv
import os

t = inputs[0].GetInformation().Get(inputs[0].DATA_TIME_STEP())

volData = inputs[0]
inletData = inputs[1]
outletData = inputs[2]

#FilePath = "C:\\Users\\Ivan\science\\works\\2021_PVpython\\data\\dataOutput.csv"
txtPath = 'C:\\Users\\Ivan\science\\works\\2021_PVpython\\pathes.txt'
with open(txtPath) as file:
    FilePath = file.read()
rho = 1500

volData = inputs[0]
inletData = inputs[1]
outletData = inputs[2]

JxB_int = volData.CellData['JxB'].GetValue(0)

area = inletData.CellData['Area']
Umag_in = mag(inletData.CellData['U'])
p_kietic_in = inletData.CellData['p']
p_static_in = rho *p_kietic_in
p_total_in = p_static_in + 0.5* rho * Umag_in**2
C_fric_in = p_static_in/(0.5*rho*Umag_in**2)

Umag_out = mag(outletData.CellData['U'])
p_kietic_out = outletData.CellData['p']
p_static_out = rho *p_kietic_out
p_total_out = p_static_out + 0.5* rho * Umag_out**2
C_fric_out = p_static_out/(0.5*rho*Umag_out**2)

#output.GetInformation().Set(output.DATA_TIME_STEP(), 0.16)

output.CellData.append(p_static_in, 'p_s_in')
output.CellData.append(Umag_in, 'Umag_in')
output.CellData.append(p_total_in, 'p_t_in')
output.CellData.append(p_kietic_in, 'p_k_in')
output.CellData.append(C_fric_in, 'C_fric_in')

output.CellData.append(p_static_in, 'p_s_out')
output.CellData.append(Umag_in, 'Umag_out')
output.CellData.append(p_total_in, 'p_t_out')
output.CellData.append(p_kietic_in, 'p_k_out')
output.CellData.append(C_fric_in, 'C_fric_out')

output.CellData.append(area, 'area')
output.CellData.append(JxB_int, 'JxB')


keys = output.GetCellData().keys()
FieldData = []
for key in keys:
    FieldData.append(output.GetCellData().GetArray(key)[0])

if os.path.exists(FilePath) == False:
    with open(FilePath, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',')
        filewriter.writerow(keys)

with open(FilePath, 'a') as csvfile:
    filewriter = csv.writer(csvfile,lineterminator='\n')
    filewriter.writerow(FieldData)