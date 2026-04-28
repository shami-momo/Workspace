from astroquery.jplhorizons import Horizons

obj = Horizons(id='Hektor', location='@sun', epochs=2458400.5)
el = obj.elements()

a = el['a'][0]        # Semi-major axis (AU)
e = el['e'][0]        # Eccentricity
i = el['incl'][0]     # Inclination (deg)
w = el['w'][0]        # Argument of perihelion (deg)
node = el['Omega'][0] # Longitude of ascending node (deg)
M = el['M'][0]        # Mean anomaly (deg)

print(f" HEKTOR  ep=2458400.5d0")
print(f" {a:.16f}d0 {e:.16f}d0 {i:.16f}d0 {w:.16f}d0 {node:.16f}d0 {M:.16f}d0 0.d0 0.d0 0.d0")