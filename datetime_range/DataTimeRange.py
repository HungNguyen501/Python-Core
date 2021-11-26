from datetime import datetime, timedelta
from math import ceil
from typing import Iterable


class DateTimeRange:
    def __init__(self, start: str, end: str, step: timedelta = timedelta(seconds=5)):
        self._start = start
        self._end = end
        self._step = step

    def __iter__(self) -> Iterable[datetime]:
        point = self._start
        while point <= self._end:
            yield point
            point += self._step

    def __len__(self) -> int:
        return ceil((self._end-self._start)/self._step)

    def __contains__(self, item: datetime) -> bool:
        if item < self._start or item > self._end:
            return False
        return divmod(item-self._start, self._step)[1]==timedelta(seconds=0)

    def __getitem__(self, index: int) -> datetime:
        n_steps = index if index >= 0 else len(self) + index
        return_value = self._start + n_steps*self._step

        if return_value not in self:
            raise IndexError()

        return return_value

    def __str__(self):
        return f"DateTimeRange [{self._start}, {self._end}] with step {self._step}"


if __name__=="__main__":
    my_range = DateTimeRange(start=datetime(2021,11,1), end=datetime(2021,11,30), step=timedelta(days=3))
    print(my_range)
    assert len(my_range)==len(list(my_range)), "error"
    print(my_range[-2] in my_range)
    print(my_range[5] in my_range)

    for i in my_range:
        print(i)