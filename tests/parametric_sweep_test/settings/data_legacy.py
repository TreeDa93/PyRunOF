"""Settings retained for the historical parametric-sweep example."""

import os


L = 0.1
A = 0.01
B = 0.02
hx = 20
hy = 10
hz = 10

Uin = 1
nu = 3.7e-7
rho = 6440
startTime = 0
stopTime = 0.25

coreOF = 4
solverName = "pimpleFoam"
mode = "parallel"

dir_path = os.getcwd()
src_case = "base_case"

data = {
    "nu_var": nu,
    "rho_var": rho,
    "startTime_var": startTime,
    "endTime_var": stopTime,
    "Uin_var": Uin,
    "Lx_var": L,
    "A_var": A,
    "B_var": B,
    "hx_var": hx,
    "hy_var": hy,
    "hz_var": hz,
    "core_OF": coreOF,
}

ps_params = {
    "Uin_var": [3, 2, 5, 1],
    "nu_var": [1e-7, 2e-7, 5e-7, 8e-7],
    "rho_var": [6450, 6410, 6100, 6500],
}
