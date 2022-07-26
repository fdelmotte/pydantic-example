import json
from pydantic import BaseModel
from typing import Optional, List, Union


class TempSensor(BaseModel):
    status: Optional[str]
    temperature: Optional[str]


class Definition3(BaseModel):
    deviceName: str
    modelName: Optional[str]
    # tempSensors = list[TempSensor]
    tempSensors: List[TempSensor] = None


def read_files(file_name):
    with open(f'files/{file_name}') as file:
        result = json.load(file)
        return result


def restructuration_sh_env_power(records):
    power_supply_convert = {}
    power_supply_convert.update({"deviceName": records[0]})
    power_supply_ids = records[1][0]['powerSupplies'].keys()

    for power_supply_id in power_supply_ids:
        for key, value in records[1][0]['powerSupplies'][power_supply_id].items():
            power_supply_convert.update({key: value})
            # if type(value) != dict:
            #     power_supply_convert.update({key: value})
            # else:
            #     [power_supply_convert.update({(key1.replace("/", "_"))[0].lower()+(key1.replace("/", "_"))[1:]: value1}) for key1, value1 in value.items()]
    return power_supply_convert


if __name__ == '__main__':
    power_supply_result = []
    data = read_files('show_env_power.json')
    for item in data:
        power_supply_result.append(restructuration_sh_env_power(item))

    print(power_supply_result)

    titi = [Definition3(**item) for item in power_supply_result]
    print(titi)

