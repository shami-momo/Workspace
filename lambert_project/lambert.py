from dataclasses import dataclass

import numpy as np
import pandas as pd
from astroquery.jplhorizons import Horizons
from lamberthub import gooding1990


AU_KM = 149_597_870.7
DAY_S = 86_400.0

MU_SUN = 2.959122082855911e-4 # AU^3 / day^2

def au_per_day_to_km_per_s(value):
    return np.asarray(value) * AU_KM / DAY_S


# Horizons data import
epochs = {
    "start": "2027-01-01",
    "stop": "2038-01-01",
    "step": "1d",
}

earth_hor = Horizons(
    id="399",             # Earth center
    location="@sun",
    epochs=epochs,
)
earth_vec = earth_hor.vectors(refplane="ecliptic")

aa29_hor = Horizons(
    id="2002 AA29",
    id_type="smallbody",
    location="@sun",
    epochs=epochs,
)
aa29_vec = aa29_hor.vectors(refplane="ecliptic")


@dataclass(frozen=True)
class StateVector:
    r: np.ndarray  # position [AU], shape=(3,)
    v: np.ndarray  # velocity [AU/day], shape=(3,)


@dataclass(frozen=True)
class TransferResult:
    v_dep: np.ndarray  # heliocentric departure velocity [AU/day]
    v_arr: np.ndarray  # heliocentric arrival velocity [AU/day]
    vinf_dep: float    # Earth-relative departure v-infinity [km/s]
    vinf_arr: float    # AA29-relative arrival v-infinity [km/s]
    c3: float          # Earth departure C3 [km^2/s^2]
    tof_days: float    # flight time [day]


def state_from_horizons(table, index):
    return StateVector(
        r=np.array(
            [table["x"][index], table["y"][index], table["z"][index]],
            dtype=float,
        ),
        v=np.array(
            [table["vx"][index], table["vy"][index], table["vz"][index]],
            dtype=float,
        ),
    )


def solve_lambert(
    earth_dep: StateVector,
    target_arr: StateVector,
    dep_jd: float,
    arr_jd: float,
    *,
    mu: float = MU_SUN,
) -> TransferResult:
    tof_days = float(arr_jd - dep_jd)

    v_sc_departure, v_sc_arrival = gooding1990(
        mu,
        earth_dep.r,
        target_arr.r,
        tof_days,
        M=0,
        prograde=True,
        low_path=True,
    )

    vinf_dep_au_day = np.linalg.norm(v_sc_departure - earth_dep.v)
    vinf_arr_au_day = np.linalg.norm(v_sc_arrival - target_arr.v)

    vinf_dep_km_s = float(au_per_day_to_km_per_s(vinf_dep_au_day))
    vinf_arr_km_s = float(au_per_day_to_km_per_s(vinf_arr_au_day))

    return TransferResult(
        v_dep=v_sc_departure,
        v_arr=v_sc_arrival,
        vinf_dep=vinf_dep_km_s,
        vinf_arr=vinf_arr_km_s,
        c3=vinf_dep_km_s**2,
        tof_days=tof_days,
    )

DEP_START_INDEX = 0
DEP_STOP_INDEX = 9 * 365       # 2027-01-01 ~ 2035년 말 부근

TOF_MIN_DAYS = 30
TOF_MAX_DAYS = 730

DATE_STEP_DAYS = 5
TOF_STEP_DAYS = 5

results = []

for dep_index in range(
    DEP_START_INDEX,
    DEP_STOP_INDEX + 1,
    DATE_STEP_DAYS,
):
    for tof_days in range(
        TOF_MIN_DAYS,
        TOF_MAX_DAYS + 1,
        TOF_STEP_DAYS,
    ):
        arr_index = dep_index + tof_days

        # Horizons 데이터 범위를 벗어나는 조합 제외
        if arr_index >= len(aa29_vec):
            continue

        try:
            result = solve_lambert(
                state_from_horizons(earth_vec, dep_index),
                state_from_horizons(aa29_vec, arr_index),
                earth_vec["datetime_jd"][dep_index],
                aa29_vec["datetime_jd"][arr_index],
            )
        except ValueError:
            continue

        results.append({
            "dep_jd": earth_vec["datetime_jd"][dep_index],
            "arr_jd": aa29_vec["datetime_jd"][arr_index],
            "tof_days": result.tof_days,
            "c3_km2_s2": result.c3,
            "vinf_dep_km_s": result.vinf_dep,
            "vinf_arr_km_s": result.vinf_arr,
            "revolutions": 0,
        })

results_df = pd.DataFrame(results)
results_df.to_csv(
    "aa29_lambert_m0_coarse.csv",
    index=False,
)