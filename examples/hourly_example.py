from pvgispy import Hourly

hourly = Hourly(lat=51, lon=9, pvcalculation=True, loss=20, peakpower=100,
                        angle=0, aspect=-180, startyear=2010, endyear=2012)

print(hourly.yearly_pv_production())