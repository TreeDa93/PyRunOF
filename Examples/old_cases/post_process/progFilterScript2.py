rho = 1500

volData = inputs[0]
inletData = inputs[2]
outletData = inputs[1]

JxB_int = volData.CellData['JxB'].GetValue(0)
area = inletData.CellData['Area']
p_m = JxB_int/area

Umag_in = mag(inletData.CellData['U']/area)
Q_in = Umag_in/area
p_kietic_in = inletData.CellData['p']/area
p_static_in = rho *p_kietic_in
p_total_in = p_static_in + 0.5 * rho * Umag_in**2
C_fric_in = p_static_in/(0.5*rho*Umag_in**2)

Umag_out = mag(outletData.CellData['U']/area)
Q_out = Umag_out/area
p_kietic_out = outletData.CellData['p']/area
p_static_out = rho * p_kietic_out
p_total_out = p_static_out + 0.5 * rho * Umag_out**2
C_fric_out = p_static_out/(0.5*rho*Umag_out**2)

p_kinetic = p_kietic_in - p_kietic_out
p_static = p_static_in - p_static_out
p_total = p_total_in - p_total_out

output.CellData.append(Umag_in, 'Umag_in')
output.CellData.append(Q_in, 'Q_in')
output.CellData.append(p_static_in, 'p_s_in')
output.CellData.append(p_total_in, 'p_t_in')
output.CellData.append(p_kietic_in, 'p_k_in')
output.CellData.append(C_fric_in, 'C_fric_in')

output.CellData.append(Umag_out, 'Umag_out')
output.CellData.append(Q_out, 'Q_out')
output.CellData.append(p_static_out, 'p_s_out')
output.CellData.append(p_total_out, 'p_t_out')
output.CellData.append(p_kietic_out, 'p_k_out')
output.CellData.append(C_fric_out, 'C_fric_out')

output.CellData.append(p_m, 'p_m')
output.CellData.append(p_total, 'p_t')
output.CellData.append(p_kinetic, 'p_k')
output.CellData.append(p_static, 'p_s')
output.CellData.append(area, 'area')
output.CellData.append(JxB_int, 'JxB')