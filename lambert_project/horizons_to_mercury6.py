from astroquery.jplhorizons import Horizons

START = 2461350.5638184664
DAYS_PER_JULIAN_YEAR = 365.25

BIG = {
    'MERCURY':  {'id': '1',   'm': '1.6601367952719304D-07', 'r': '20.D0', 'd': '5.43D0'},
    'VENUS':    {'id': '2',   'm': '2.4478383396645443D-06', 'r': '20.D0', 'd': '5.24D0'},
    'MARS':     {'id': '4',   'm': '3.2271514450538653D-07', 'r': '20.D0', 'd': '3.93D0'},
    'JUPITER':  {'id': '5',   'm': '9.5479193842432660D-04', 'r': '20.D0', 'd': '1.33D0'},
    'SATURN':   {'id': '6',   'm': '2.8588598066613081D-04', 'r': '20.D0', 'd': '0.69D0'},
    'URANUS':   {'id': '7',   'm': '4.3662440433515630D-05', 'r': '20.D0', 'd': '1.27D0'},
    'NEPTUNE':  {'id': '8',   'm': '5.1513890204661145D-05', 'r': '20.D0', 'd': '1.64D0'},
    'EARTH':    {'id': '399', 'm': '3.0034895963248533D-06', 'r': '20.D0', 'd': '5.51D0'},
    'MOON':     {'id': '301', 'm': '3.694873455835E-08',     'r': '20.D0', 'd': '3.34D0'},
}

SMALL = {
    '2002AA29': {'id': '2002 AA29'}
}

# Cartesian
print("=== big.in ===")
for name, info in BIG.items():
    obj = Horizons(id=info['id'], location='@sun', epochs=START)
    vec = obj.vectors()

    x, y, z = vec['x'][0], vec['y'][0], vec['z'][0]
    vx, vy, vz = vec['vx'][0], vec['vy'][0], vec['vz'][0]

    def to_d_format(val):

        return f"{val: .16E}".replace('E', 'D')

    print(f" {name:<10} m={info['m']} r={info['r']} d={info['d']}")
    print(f"  {to_d_format(x)} {to_d_format(y)} {to_d_format(z)}")
    print(f"  {to_d_format(vx)} {to_d_format(vy)} {to_d_format(vz)}")
    print("  0.D0 0.D0 0.D0")

print("=== small.in ===")
for name, info in SMALL.items():
    obj = Horizons(id=info['id'], location='@sun', epochs=START)
    vec = obj.vectors()

    x, y, z = vec['x'][0], vec['y'][0], vec['z'][0]
    vx, vy, vz = vec['vx'][0], vec['vy'][0], vec['vz'][0]

    def to_d_format(val):

        return f"{val: .16E}".replace('E', 'D')

    print(f" {name:<10} ep={START:.1f}d0")
    print(f"  {to_d_format(x)} {to_d_format(y)} {to_d_format(z)} {to_d_format(vx)} {to_d_format(vy)} {to_d_format(vz)}")