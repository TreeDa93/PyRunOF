"""Input data for the parametric-sweep integration example."""

DUCT_LENGTH = 0.1
DUCT_HEIGHT = 0.01
DUCT_WIDTH = 0.02

OF_CORES = 4
SOLVER = "pimpleFoam"

BASE_PARAMETERS = {
    "nu_var": 3.7e-7,
    "rho_var": 6440,
    "startTime_var": 0,
    "endTime_var": 0.25,
    "Uin_var": 1,
    "Lx_var": DUCT_LENGTH,
    "A_var": DUCT_HEIGHT,
    "B_var": DUCT_WIDTH,
    "hx_var": 20,
    "hy_var": 10,
    "hz_var": 10,
    "core_OF": OF_CORES,
}

SWEEP_PARAMETERS = {
    "Uin_var": [3, 2, 5, 1],
    "nu_var": [1e-7, 2e-7, 5e-7, 8e-7],
    "rho_var": [6450, 6410, 6100, 6500],
}
