"""Plain Python class loaded by the SDK PythonFile importer."""
class TemperatureDevice:
    def __init__(self, start=20.0, increment=0.5):
        self._temperature_c = start
        self.increment = increment

    @property
    def temperature_c(self):
        return self._temperature_c

    @temperature_c.setter
    def temperature_c(self, value):
        self._temperature_c = float(value)

    def tick(self):
        self.temperature_c += self.increment
