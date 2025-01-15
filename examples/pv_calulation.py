from pvgispy import Hourly

hourly = Hourly(
    lat=51.0,
    lon=9.0,
    angle=0, # inclination angle from horizontal plane
    aspect=-180, # Orientation (azimuth) angle of the (fixed) plane, 0=south, 90=west, -90=east. Not relevant for tracking planes.
    startyear=2020,
    endyear=2023,
    pvcalculation=True, # enable pv calulations
    peakpower=1000.0,
    loss=20.0
)


print(hourly.irradiance(as_list=True))