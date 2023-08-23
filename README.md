# pvgispy

This package aims to provide a clean, performant and barrier-free interface to the PVGIS API by the EU Science Hub.

More info about the PVGIS API: https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis/getting-started-pvgis/api-non-interactive-service_en

## Disclaimer

This project is **not an official project from the EU Science Hub**. 

## Installation

Install from the Python Package Index (PyPI) using `pip`:
```
pip install pvgispy
```

## Basic Usage

The interface was designed to be simple and intuitive. Basic usage follows these steps:
- Choose an endpoint (Hourly, Daily, Monthly, TMY, Off-Grid, Grid-Connected)
- Get the raw data or use functionalities to calculate certain values

A basic example looks like this:

```python
from pvgispy import Daily

daily = Daily(lat=48, lon=9, month=1)

print(daily.irradiance(as_list=True))

# Raw data
print(daily.data)
```

Another example to get the pv solar production over a year:

```python
from pvgispy import Hourly

hourly = Hourly(lat=51, lon=9, pvcalculation=True, loss=20, peakpower=100,
                        angle=0, aspect=-180, startyear=2010, endyear=2010)

print(hourly.yearly_pv_production())
```