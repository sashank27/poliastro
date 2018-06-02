import numpy as np
from scipy.interpolate import interp1d
from astropy import units as u
from astropy.time import Time
from poliastro.twobody.orbit import Orbit
from poliastro.coordinates import transform
from astropy.coordinates import ICRS, GCRS


def build_ephem_interpolant(body, t_span, rtol=1e-5):
    T_approx = 2 * np.pi * np.sqrt(body.R ** 3 / body.k)
    h = 0.25  # (T_approx * rtol ** (1.0 / 4.0)).to(u.day).value

    t_values = np.linspace(t_span[0], t_span[1], int((t_span[1] - t_span[0]) / h))
    r_values = np.zeros((t_values.shape[0], 3))

    for i, t in enumerate(t_values):
        epoch = Time(t, format='jd', scale='tdb')
        body_t = Orbit.from_body_ephem(body, epoch)
        body_t = transform(body_t, ICRS, GCRS)
        r_values[i] = body_t.r

    t_values = ((t_values - t_span[0]) * u.day).to(u.s).value
    return interp1d(t_values, r_values, kind='cubic', axis=0, assume_sorted=True)
