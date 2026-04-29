import os
import math
from lineDetApi import GetVisualInfo

# Tento skript bych rozsiril a pouzil na preciznejsi vypocet uhlu pro rotaci

def bufferCalculate() -> float:
        bufferlist: list[float] = []
        for i in range(0,10):
            bufferlist.append(GetVisualInfo()[1])
        sum: float = 0.0
        for j in range(0,10):
            sum += bufferlist[j]
        sum = sum / 10
        return sum