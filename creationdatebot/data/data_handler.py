from json import load
from pathlib import Path
from numpy import polyfit, poly1d
import numpy as np

class IDData:
    def __init__(self,
                 folder: str = "creationdatebot/data",
                 file: str = "dates.json"):
        self.iddata_path = Path.cwd().joinpath(folder, file)

        self.x, self.y = self._unpack_iddata()
        self.fitted_function = self._fit_data()


    def _unpack_iddata(self):
        with open(self.iddata_path) as string_data:
            iddata = load(string_data)

        # json doesn't allow keys to be stored as integers
        # therefore conversion
        iddata = {int(k):v for k,v in iddata.items()}

        iddata_x = np.array(list(iddata.keys()))
        iddata_y = np.array(list(iddata.values()))

        return iddata_x, iddata_y


    def _fit_data(self, order=6):
        fitted = np.polyfit(self.x, self.y, order)
        fitted_function = np.poly1d(fitted)

        return fitted_function
