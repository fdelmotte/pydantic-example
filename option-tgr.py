#!/usr/bin/python
# coding: utf-8 -*-

import sys
import json
import logging
from rich import print
from rich.pretty import pprint
from typing import List, Optional
from pydantic import BaseModel

def load_json_file(file_path: str):
    with open(file_path) as json_file:
        return json.load(json_file)

class TempSensor(BaseModel):
    name: Optional[str]
    status: str
    temperature: str

# To be added later
class Fan(BaseModel):
    name: Optional[str]
    status: str
    speed: int

class PowerSupply(BaseModel):
    id: int
    outputPower: float
    modelName: str
    capacity: int
    tempSensors: List[TempSensor]
    state: str
    inputCurrent: float
    dominant: bool
    inputVoltage: float
    outputCurrent: float
    managed: bool

class PowerSupplies():

    def __init__(self) -> None:
        self.power_supplies = []

    def _load_json_file(self, file_path: str):
        with open(file_path) as json_file:
            return json.load(json_file)

    def load_psus_from_file(self, json_file: str):
        for k,entry in self._load_json_file(json_file)['powerSupplies'].items():
            entry['id'] = int(k)
            if 'tempSensors' in entry:
                temp_sensors_list = []
                for ct, sensor in entry["tempSensors"].items():
                    sensor['name'] = ct
                    temp_sensors_list.append(sensor)
                entry['tempSensors'] = temp_sensors_list
            self.power_supplies.append(PowerSupply(**entry))



if __name__ == '__main__':

    power_supplies = PowerSupplies()
    power_supplies.load_psus_from_file(json_file='files/power_supply_result.json')

    for psu in power_supplies.power_supplies:
        pprint(psu.dict())

    sys.exit(0)