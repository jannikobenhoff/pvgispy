from pvgispy import Hourly, TMY
import pandas as pd

hourly = Hourly(
    lat=51.0,
    lon=9.0,
    angle=0, # inclination angle from horizontal plane
    aspect=-180, # Orientation (azimuth) angle of the (fixed) plane, 0=south, 90=west, -90=east. Not relevant for tracking planes.
    startyear=2020,
    endyear=2023,
    pvcalculation=False, # disable pv claulations, we only want radiation data
)

df_hourly = pd.json_normalize(hourly.hourly())

print(df_hourly.head())

# uncomment the line below to safe the DAtaFrame as a CSV fiel
# df.to_csv("hourly.csv")

tmy = TMY(
    lat=51.0,
    lon=9.0,
)

df_tmy = pd.json_normalize(tmy.hourly())

print(df_tmy.head())