from datetime import datetime, date
from decimal import Decimal
from typing import Callable, Self

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.helpers.typing import StateType

from custom_components.petlibro import PetLibroHub, Device
from custom_components.petlibro.sensor import PetLibroSensorEntity
from custom_components.petlibro.entity import _DeviceT

type native_value_type = StateType | date | datetime | Decimal

class WetFeedingPlanSensorEntity(PetLibroSensorEntity[_DeviceT]):
    def __init__(self, device: Device, hub: PetLibroHub, plan, provider_property: property):
        super().__init__(device, hub, f"{plan.plate}_{provider_property.__name__}")
        self._plan = plan
        self._property = provider_property

    @property
    def device_class(self) -> SensorDeviceClass | None:
        match self.native_value:
            case datetime():
                return SensorDeviceClass.TIMESTAMP
            case _:
                return None

    @property
    def translation_key(self):
        return f"wet_feeding_plan_{self._property.__name__}"

    @property
    def native_value(self) -> native_value_type:
        return self._property.__get__(self)

    @property
    def start_time(self) -> datetime:
        return self._plan.executionStartTime

    @property
    def end_time(self) -> datetime:
        return self._plan.executionEndTime

    @property
    def label(self) -> str:
        return self._plan.label

    @property
    def cancel_state(self) -> bool:
        return self._plan.cancelState


    @staticmethod
    def build_sensors(device: Device, hub: PetLibroHub, plan) -> list[PetLibroSensorEntity[_DeviceT]]:
        return [
            WetFeedingPlanSensorEntity(device, hub, plan, prop)
            for prop in [
                WetFeedingPlanSensorEntity.start_time,
                WetFeedingPlanSensorEntity.end_time,
                WetFeedingPlanSensorEntity.label,
                WetFeedingPlanSensorEntity.cancel_state,
            ]
        ]
