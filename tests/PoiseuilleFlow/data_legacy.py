"""Settings retained for the historical Poiseuille-flow example."""

base_case = "PoiseuilleFlow"

L = 0.1
A = 0.01
B = 0.02
hx = 40
hy = 30
hz = 30

Uin = 1
nu = 3.7e-7
rho = 6440
startTime = 0
stopTime = 0.25

data = {
    "L_var": L,
    "A_var": A,
    "B_var": B,
    "hx_var": hx,
    "hy_var": hy,
    "hz_var": hz,
    "Uin_var": Uin,
    "startTime_var": startTime,
    "endTime_var": stopTime,
    "nu_var": nu,
    "rho_var": rho,
}

turbulence_model = "kOmegaSST"
