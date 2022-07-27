#!/usr/bin/python
# coding: utf-8 -*-

import sys
import json
import logging
from rich import print
from rich.pretty import pprint
from typing import List, Optional, Dict
from pydantic import BaseModel

def load_json_file(file_path: str):
    with open(file_path) as json_file:
        return json.load(json_file)

class TempSensor(BaseModel):
    name: Optional[str]
    status: str
    temperature: str

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
    fans: List[Fan]
    state: str
    inputCurrent: float
    dominant: bool
    inputVoltage: float
    outputCurrent: float
    managed: bool

    def get_sensor(self, sensor_name: str) -> TempSensor:
        if len([sensor for sensor in self.tempSensors if str(sensor.name) == sensor_name]) == 1:
            return [sensor for sensor in self.tempSensors if str(sensor.name) == sensor_name][0]
        return None

    def get_fan(self, fan_name: str) -> TempSensor:
        if len([sensor for sensor in self.fans if str(sensor.name) == fan_name]) == 1:
            return [sensor for sensor in self.fans if str(sensor.name) == fan_name][0]
        return None

class DeviceModel():

    def __init__(self, hostname: str = 'demo.lab') -> None:
        self.psus = []
        self.hostname = hostname

    def __repr__(self):
        return f'"{self.hostname}": {self.psus}'

    def _load_json_file(self, file_path: str):
        with open(file_path) as json_file:
            return json.load(json_file)

    def _dict_to_list(self, entry: Dict, key: str):
        if key in entry:
            temp_list = []
            for ct, sensor in entry[key].items():
                sensor['name'] = ct
                temp_list.append(sensor)
            entry[key] = temp_list
        return entry

    def load_json_psus(self, json_file: str):
        for k,entry in self._load_json_file(json_file)['powerSupplies'].items():
            entry['id'] = int(k)
            entry = self._dict_to_list(entry=entry, key='tempSensors')
            entry = self._dict_to_list(entry=entry, key='fans')
            self.psus.append(PowerSupply(**entry))

    def get_psu(self, psu_id: int):
        if len([sensor for sensor in self.psus if int(sensor.id) == psu_id]) == 1:
            return [sensor for sensor in self.psus if int(sensor.id) == psu_id][0]
        return None


if __name__ == '__main__':

    eos = DeviceModel()
    eos.load_psus_from_file(json_file='files/power_supply_result.json')

    for psu in eos.psus:
        pprint(psu.dict(), expand_all=False)

    print('Getting information for PSU 2 sensor 2/3')
    pprint(eos.get_psu(2).get_sensor(sensor_name='TempSensorP2/3').dict())

    sys.exit(0)
