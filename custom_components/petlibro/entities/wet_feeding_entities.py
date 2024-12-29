from datetime import datetime, date
from decimal import Decimal
from logging import getLogger
from typing import Any
from zoneinfo import ZoneInfo

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .entity import _DeviceT
from .sensor import PetLibroSensorEntity
from ..core import Device

type NativeValueType = StateType | date | datetime | Decimal

_LOGGER = getLogger(__name__)


class WetFeedingPlanSensorEntity(PetLibroSensorEntity[_DeviceT]):
    def __init__(self, device: Device, coordinator: DataUpdateCoordinator, plan: dict[str, Any],
                 provider_property: property):
        try:
            _LOGGER.debug(
                f"Setting up wet feeding plan sensor. Plate: {plan.get("plate")} Property: {provider_property}")
            super().__init__(device, coordinator, f"{plan.get("plate")}_{provider_property.__name__}")
        except Exception as err:
            _LOGGER.error(f"Error logging the setup:", err)
            raise err
        self._plan = plan
        self._property = provider_property
        self._attr_translation_placeholders = {"plate": plan.get("plate")}

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
    def native_value(self) -> NativeValueType:
        return self._property.__get__(self)

    @property
    def start_time(self) -> datetime | None:
        return datetime.strptime(self._plan.get("executionStartTime"), "%Y-%m-%d %H:%M").astimezone(
            ZoneInfo(self._plan.get("timezone")))

    @property
    def end_time(self) -> datetime | None:
        return datetime.strptime(self._plan.get("executionEndTime"), "%Y-%m-%d %H:%M").astimezone(
            ZoneInfo(self._plan.get("timezone")))

    @property
    def label(self) -> str | None:
        return self._plan.get("label")

    @property
    def cancel_state(self) -> bool | None:
        return self._plan.get("cancelState")

    @staticmethod
    def build_sensors(device: Device, coordinator: DataUpdateCoordinator, plan: dict[str, Any]) -> list[
        PetLibroSensorEntity[_DeviceT]]:
        built_sensors = [WetFeedingPlanSensorEntity(device, coordinator, plan, prop) for prop in
                         [WetFeedingPlanSensorEntity.start_time,
                          WetFeedingPlanSensorEntity.end_time,
                          WetFeedingPlanSensorEntity.label,
                          WetFeedingPlanSensorEntity.cancel_state,
                          ]
                         ]
        _LOGGER.info(f"built sensors: {built_sensors}")
        return built_sensors
