import os
import sys
import configs.settings

def as_dict():
   res = {}
   for atr in [f for f in dir(configs.settings) if not '__' in f]:
       val = getattr(configs.settings, atr)
       res[atr] = val
   return res