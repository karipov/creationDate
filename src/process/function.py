import json, pathlib  # noqa: E401
from typing import Callable
import time

import numpy as np


class Function:
    def __init__(self, order: int = 3):
        self.order = 3
        self.data_path = pathlib.Path.cwd().joinpath("src/data/dates.json")

        self.x, self.y = self._unpack_data()
        self._func = self._fit_data()

    def _unpack_data(self) -> (list, list):
        with open(self.data_path) as string_data:
            data = json.load(string_data)

        x_data = np.array(list(map(int, data.keys())))
        y_data = np.array(list(data.values()))

        return (x_data, y_data)

    def _fit_data(self) -> Callable[[int], int]:
        fitted = np.polyfit(self.x, self.y, self.order)
        func = np.poly1d(fitted)

        return func

    def add_datapoint(self, pair: tuple):
        pair[0] = str(pair[0])

        with open(self.data_path) as string_data:
            data = json.load(string_data)

        data.update([pair])

        with open(self.data_path, "w") as string_data:
            json.dump(data, string_data)

        # update the model with new data
        self.x, self.y = self._unpack_data()
        self._func = self._fit_data()

    def func(self, tg_id: int) -> int:
        value = self._func(tg_id)
        current = time.time()

        if value > current:
            value = current

        return value


if __name__ == "__main__":
    # import matplotlib.pyplot as plt
    from datetime import datetime

    f = Function(6)

    a = f.func(1_300_200_300)
    print(datetime.utcfromtimestamp(a).strftime("%Y-%m-%d"))  # example interpolation

    # plot scatter data + line of best fit
    # plt.scatter(f.x, f.y)
    # plt.plot(f.x, [f.func(x) for x in f.x])
    # plt.show()
