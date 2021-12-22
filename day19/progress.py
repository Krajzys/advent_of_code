from time import time
from statistics import mean
from math import inf

class Progress:
    def __init__(self, curr_val=0, max_val=1, bars=30, unit='s', avg_list_len=40):
        self.curr_val = curr_val
        self.max_val = max_val
        self.bars = bars
        self.eta = inf
        self.last_update_time = 0
        self.init_time = time()
        self.time_passed = []
        self.avg_time_passed = 0
        self.avg_list_len = avg_list_len
        self.unit = unit
        self._progress_str = f'[{" "*self.bars}] {round(self.curr_val/self.max_val)}% ETA: {self.eta}{self.unit}'
        self.max_len = len(self._progress_str)

    def update(self, curr_val):
        time_passed = 0
        if self.last_update_time != 0:
            time_passed = time() - self.last_update_time
        else:
            time_passed = time() - self.init_time
        self.time_passed = [time_passed] + self.time_passed[:self.avg_list_len-1]
        self.last_update_time = time()
        self.curr_val = curr_val
        self.eta = round((self.max_val - self.curr_val) * mean(self.time_passed), 2)
        percentage_completed = round((self.curr_val/self.max_val) * 100)
        self._progress_str = f'[{round(percentage_completed*self.bars/100)*"=" + " "*round((1-(percentage_completed/100))*self.bars)}] {percentage_completed}% ETA: {self.eta}{self.unit}'
        self.max_len = max(len(self._progress_str), self.max_len)

    def get_max_len(self):
        return self.max_len

    def reset(self):
        self.curr_val = 0
        self.eta = inf
        self.last_update_time = 0
        self.init_time = time()
        self.time_passed = []
        self.avg_time_passed = 0
        self._progress_str = f'[{" "*self.bars}] {round(self.curr_val/self.max_val)}% ETA: {self.eta}{self.unit}'
        self.max_len = len(self._progress_str)

    def __repr__(self):
        return self._progress_str

    def print(self):
        end_str = " "*(self.get_max_len() - len(self._progress_str)) + self.get_max_len()*"\b"
        print(self, end=end_str, flush=True)
        if self.curr_val == self.max_val:
            print()
            print("Completed")