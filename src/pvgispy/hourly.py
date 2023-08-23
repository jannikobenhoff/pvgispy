from .base import BaseAPI


class Hourly(BaseAPI):
    ENDPOINT = "seriescalc"

    def __init__(self, lat, lon, pvcalculation: bool, angle: float = 0, aspect: float = 0, peakpower: float = None,
                 loss: float = None,
                 startyear: int = None, endyear: int = None, pvtech: str = "crystSi", **kwargs):
        """
        Hourly averages data.

        :param lat: Latitude in decimal degrees (south is negative).
        :param lon: Longitude in decimal degrees (west is negative).
        :param pvcalculation: If False outputs only solar radiation calculations.
                              If True outputs the estimation of hourly PV production as well.
        :param peakpower: Nominal power of the PV system, in kW.
        :param loss: Sum of system losses, in percent. E.g. 20% -> loss=20
        :param pvtech: (Default: 'crystSi') PV technology.{"crystSi", "CIS", "CdTe", "Unknown"}
        :param angle: (Default: 0) Inclination angle from horizontal plane. Not relevant for 2-axis tracking.
        :param aspect: (Default: 0) Orientation (azimuth) angle of the (fixed) plane.
                       0=south, 90=west, -90=east. Not relevant for tracking planes.

        Describes the various output variables from the API call:

        - `G(i)`: Global irradiance on the inclined plane (plane of the array) (units: W/m2).
        - `H_sun`: Sun height (units: degree).
        - `Int`: Indicates solar radiation values; 1 means values are reconstructed.
        - `P`: PV system power (units: W).
        - `T2m`: 2-m air temperature (units: degree Celsius).
        - `WS10m`: 10-m total wind speed (units: m/s).
        """
        self.pvcalculation = pvcalculation

        if endyear < startyear:
            raise ValueError("Incorrect time period. The calculation period for this app should be at least 1 years.")
        if startyear not in range(2005, 2020):
            raise ValueError("Incorrect start year. Please, enter an integer between 2005 and 2016.")
        self.startyear = startyear
        if endyear not in range(2005, 2020):
            raise ValueError("Incorrect end year. Please, enter an integer between 2005 and 2016.")
        self.endyear = endyear

        if pvcalculation and peakpower is None:
            raise ValueError("Invalid peak-power. If pvcalculation set True, peakpower can't be None.")
        self.peakpower = peakpower

        if pvcalculation and loss is None:
            raise ValueError("Invalid loss. If pvcalculation set True, loss can't be None.")
        if int(loss) not in range(0, 100):
            raise ValueError("Invalid loss value. Please, enter a float between 0 and 100.")
        self.loss = loss

        if pvtech not in ["crystSi", "CIS", "CdTe", "Unknown"]:
            raise ValueError("Invalid PV Technology. Valid technologies are 'crystSi', 'CIS', 'CdTe', 'Unknown'")
        self.pvtech = pvtech

        if int(angle) not in range(0, 91):
            raise ValueError("Invalid angle. Please, enter a float between 0 and 90.")
        self.angle = angle

        if int(aspect) not in range(-180, 181):
            raise ValueError("Invalid aspect / azimuth. Please, enter a float between -180 and 180.")
        self.aspect = aspect

        super().__init__(lat, lon, **kwargs)

    def _get_endpoint(self):
        """
        Returns the endpoint URL for the Daily Radiation API call.
        """
        return self.BASE_URL + self.ENDPOINT

    def set_params(self, **kwargs):
        """
        Update or set parameters.
        """
        self.params.update(kwargs)

    @property
    def params(self):
        """
        Construct parameters for the API call.
        """
        parameters = {
            "lat": self.lat,
            "lon": self.lon,
            "usehorizon": self._params.get("usehorizon", 1),
            "raddatabase": self._params.get("raddatabase", "PVGIS-SARAH2"),
            "startyear": self.startyear,
            "endyear": self.endyear,
            "pvcalculation": 1 if self.pvcalculation else 0,
            "peakpower": self.peakpower,
            "pvtechchoice": self.pvtech,
            "mountingplace": self._params.get("mountingplace", None),
            "loss": self.loss,
            "trackingtype": self._params.get("trackingtype", None),
            "angle": self.angle,
            "aspect": self.aspect,
            "optimalinclination": self._params.get("optimalinclination", None),
            "optimalangles": self._params.get("optimalangles", None),
            "components": self._params.get("components", None),
            "outputformat": self._params.get("outputformat", 0),
            "browser": self._params.get("browser", 0)
        }

        # Remove any parameters set to None
        return {k: v for k, v in parameters.items() if v is not None}

    def fetch_data(self):
        """
        Fetch data and change start and endyear if set to None before.
        """
        super().fetch_data()

        self.startyear = self.data["inputs"]["meteo_data"]["year_min"]
        self.endyear = self.data["inputs"]["meteo_data"]["year_max"]

    def hourly(self):
        if self.data is None:
            self.fetch_data()

        hourly = self.data["outputs"]["hourly"]

        return hourly

    def yearly_pv_production(self):
        """
        Calculates the total pv power production in W over a year.

        :return: p in W
        """
        if self.data is None:
            self.fetch_data()

        hourly = self.data["outputs"]["hourly"]

        p = 0
        for hour in hourly:
            p += hour.get("P", 0)

        return p

    def monthly_pv_production(self):
        """
        Calculates the total pv power production in W over a month for a year.

        :return: p in W
        """
        if self.data is None:
            self.fetch_data()

        hourly = self.data["outputs"]["hourly"]

        p = 0
        for hour in hourly:
            p += hour.get("P", 0)

        return p
