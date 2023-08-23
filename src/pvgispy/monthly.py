from .base import BaseAPI


class Monthly(BaseAPI):
    ENDPOINT = "tmy"

    def __init__(self, lat, lon, **kwargs):
        """
        Typical meteorological year.

        Obligatory parameters:
        :param lat: Latitude in decimal degrees (south is negative).
        :param lon: Longitude in decimal degrees (west is negative).

        Describes the various output variables from the API call:

        - `G(h)`: Global irradiance on the horizontal plane (units: W/m2).
        - `Gb(n)`: Beam/direct irradiance on a plane always normal to sun rays (units: W/m2).
        - `Gd(h)`: Diffuse irradiance on the horizontal plane (units: W/m2).
        - `IR(h)`: Surface infrared (thermal) irradiance on a horizontal plane (units: W/m2).
        - `RH`: Relative humidity (units: %).
        - `SP`: Surface (air) pressure (units: Pa).
        - `T2m`: 2-m air temperature (units: degree Celsius).
        - `WD10m`: 10-m wind direction (0 = N, 90 = E) (units: degree).
        - `WS10m`: 10-m total wind speed (units: m/s).
        """
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
        Construct and return parameters for the API call.
        """
        parameters = {
            "lat": self.lat,
            "lon": self.lon,
            "usehorizon": self._params.get("usehorizon", 1),
            "startyear": self._params.get("startyear", None),
            "endyear": self._params.get("endyear", None),
            "outputformat": self._params.get("outputformat", 0),
            "browser": self._params.get("browser", 0)
        }

        # Remove any parameters set to None
        return {k: v for k, v in parameters.items() if v is not None}