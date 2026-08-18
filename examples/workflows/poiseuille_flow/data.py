"""Configuration for the current Poiseuille-flow example."""

BASE_CASE_NAME = "PoiseuilleFlow"
SOLVER = "pimpleFoam"
TURBULENCE_MODEL = "kEpsilon"

PARAMETERS = {
    "L_var": 0.1,
    "A_var": 0.01,
    "B_var": 0.02,
    "hx_var": 40,
    "hy_var": 30,
    "hz_var": 30,
    "Uin_var": 1,
    "startTime_var": 0,
    "endTime_var": 0.25,
    "nu_var": 3.7e-7,
    "rho_var": 6440,
}
