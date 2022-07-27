import json
from pydantic import BaseModel
from typing import Optional, List, Dict


class TempSensor(BaseModel):
    name: Optional[str]
    status: str
    temperature: str


class Fan(BaseModel):
    name: Optional[str]
    status: str
    speed: int


class PowerSupply(BaseModel):
    hostName: str
    id: int
    outputPower: Optional[float]
    modelName: Optional[str]
    capacity: Optional[int]
    tempSensors: Optional[List[TempSensor]]
    fans: Optional[List[Fan]]
    state: Optional[str]
    inputCurrent: Optional[float]
    dominant: Optional[bool]
    inputVoltage: Optional[float]
    outputCurrent: Optional[float]
    managed: Optional[bool]


class DeviceModel():
    def __init__(self) -> None:
        self.psus = []


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
        print(type(self._load_json_file(json_file)))
        for device_hostname, value in self._load_json_file(json_file):
            for k, entry in value[0]['powerSupplies'].items():
                entry['hostName'] = device_hostname
                entry['id'] = int(k)
                entry = self._dict_to_list(entry=entry, key='tempSensors')
                entry = self._dict_to_list(entry=entry, key='fans')
                self.psus.append(PowerSupply(**entry))


if __name__ == '__main__':
    eos = DeviceModel()
    eos.load_json_psus(json_file='files/show_env_power.json')
    for psu in eos.psus:
        print(psu.dict(), expand_all=False)

