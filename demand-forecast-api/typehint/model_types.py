
from typing import Callable, Type

from tensorflow.python.keras.models import Model


InputSize=int
ModelId=str
LR=float

KerasCreateModelCallback = Callable[[InputSize, ModelId, LR], Model]