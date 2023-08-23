import json
import requests


class BaseAPI:
    BASE_URL = "https://re.jrc.ec.europa.eu/api/v5_2/"
    BASE_URL_V1 = "https://re.jrc.ec.europa.eu/api/v5_1/"

    def __init__(self, lat: float, lon: float,  **kwargs):
        """
        Constructor to initialize any common parameters for API calls.
        """
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            self.lat = lat
            self.lon = lon
        else:
            raise ValueError("Incorrect Latitude or Longitude.")

        self._params = kwargs
        self.data = None

    @property
    def params(self):
        print(self._params)
        return self._params

    @params.setter
    def params(self, value):
        self._params = value

    def _get_endpoint(self):
        """
        Returns the endpoint URL for the specific API. 
        This should be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def fetch_data(self):
        """
        Fetch data from the API.
        """
        print("---> FETCHING...")
        response = requests.get(self._get_endpoint(), params=self.params)
        self.data = self._handle_response(response)

    def _handle_response(self, response):
        """
        Handle the API response. Can be extended to handle errors, 
        convert formats, etc.
        """
        if response.status_code != 200:
            # Handle error
            self._handle_error(response)

        # Always use json, only let user decide for export
        if self._params["outputformat"] == "csv":
            return response.text
        elif self._params["outputformat"] == "json":
            return response.json()
        elif self._params["outputformat"] == "basic":
            return response.json()
        else:
            raise Exception(f"Invalid Outputformat.")

    def _handle_error(self, response):
        """
        Handle errors from the API response.
        This can be extended to raise custom exceptions based on the error type.
        """
        raise Exception(f"API Error {response.status_code}: {response.text}")

    def export(self, filename):
        file = open(filename, "w")
        json.dump(self.data, file)
