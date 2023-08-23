from .base import BaseAPI


class Daily(BaseAPI):
    ENDPOINT = "DRcalc"

    def __init__(self, lat, lon, month, **kwargs):
        """
        Daily radiation for one day in a specific month.
        Calculated in a TMY.

        Obligatory parameters:
        :param lat: Latitude in decimal degrees (south is negative).
        :param lon: Longitude in decimal degrees (west is negative).
        :param month: The number of the month, starting at 1 for January. A value of 0 indicates data for all months.


        Optional parameters:
        :param usehorizon: (Optional) Calculate considering shadows from a high horizon. Default is 1 for "yes".
        :param userhorizon: (Optional) Height of the horizon at equidistant directions around the point of interest, in degrees. Starting at north and moving clockwise. The series '0,10,20,30,40,15,25,5' would mean the horizon height is 0° due north, 10° for north-east, 20° for east, 30° for south-east, etc.
        :param raddatabase
        :param angle
        :param aspect
        :param global
        :param glob_2axis
        :param clearsky
        :param clearsky_2axis
        :param showtemperatures
        :param localtime
        :param outputformat
        :param browser

        API return values:
        :var G(i): [W/m2] Global irradiance on a fixed plane.
        :var Gb(i): [W/m2] Direct irradiance on a fixed plane.
        :var Gd(i): [W/m2] Diffuse irradiance on a fixed plane.
        :var time: [xx:00] Time in hours. Starting at 00:00.
        """
        self.month = month
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
            "month": self.month,
            "usehorizon": self._params.get("usehorizon", 1),
            "raddatabase": self._params.get("raddatabase", "PVGIS-SARAH2"),
            "angle": self._params.get("angle", 0),
            "aspect": self._params.get("aspect", 0),
            "global": self._params.get("global", 1),
            "glob_2axis": self._params.get("glob_2axis", 0),
            "clearsky": self._params.get("clearsky", 0),
            "clearsky_2axis": self._params.get("clearsky_2axis", 0),
            "showtemperatures": self._params.get("showtemperatures", 0),
            "localtime": self._params.get("localtime", 0),
            "outputformat": self._params.get("outputformat", 0),
            "browser": self._params.get("browser", 0)
        }

        # Remove any parameters set to None
        return {k: v for k, v in parameters.items() if v is not None}

    def total_irradiance(self, irradiance_type: str = "global"):
        """
        Returns the total irradiance during one day.

        :param irradiance_type: Type of irradiance to compute. Choices are 'global', 'direct', and 'diffuse'.
                                'global' is the sum of 'direct' and 'diffuse'.
        :return: irradiance [W/m2] on a fixed plane.
        """
        if self.data is None:
            self.fetch_data()

        total_irradiance = 0
        for hour in self.data["outputs"]["daily_profile"]:
            # Make sure that param global=1, else the api doesnt return irradiance.
            if irradiance_type == "global":
                total_irradiance += hour.get("G(i)", 0)
            elif irradiance_type == "direct":
                total_irradiance += hour.get("Gb(i)", 0)
            elif irradiance_type == "diffuse":
                total_irradiance += hour.get("Gd(i)", 0)
            else:
                raise ValueError("Invalid irradiance_type. Choose from 'global', 'direct', or 'diffuse'.")

        return total_irradiance

    def irradiance(self, as_list: bool = False):
        """
        Returns the total irradiance during one day. All types.
        """
        if self.data is None:
            self.fetch_data()

        if as_list:
            irradiance = {"G(i)": [], "Gb(i)": [], "Gd(i)": []}
        else:
            irradiance = {"G(i)": 0, "Gb(i)": 0, "Gd(i)": 0}

        for hour in self.data["outputs"]["daily_profile"]:
            # Make sure that param global=1, else the api doesnt return irradiance.
            if as_list:
                irradiance["G(i)"].append(hour.get("G(i)", 0))
                irradiance["Gb(i)"].append(hour.get("Gb(i)", 0))
                irradiance["Gd(i)"].append(hour.get("Gd(i)", 0))
            else:
                irradiance["G(i)"] += hour.get("G(i)", 0)
                irradiance["Gb(i)"] += hour.get("Gb(i)", 0)
                irradiance["Gd(i)"] += hour.get("Gd(i)", 0)

        return irradiance
