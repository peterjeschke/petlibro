from datetime import datetime, date
from decimal import Decimal
from logging import getLogger
from typing import Any
from zoneinfo import ZoneInfo

from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .binary_sensor import PetLibroBinarySensorEntity
from .entity import _DeviceT
from ..core import Device

type NativeValueType = StateType | date | datetime | Decimal

_LOGGER = getLogger(__name__)


class WetFeedingPlanElementSensorEntity(PetLibroBinarySensorEntity[_DeviceT]):
    def __init__(self,
                 device: Device,
                 coordinator: DataUpdateCoordinator,
                 plan: dict[str, Any]):
        super().__init__(device, coordinator, f"{plan.get("plate")}")
        self._plan = plan
        self._attr_translation_placeholders = {"plate": plan.get("plate")}

    @property
    def translation_key(self):
        return f"wet_feeding_plan_element"

    @property
    def is_on(self) -> bool:
        return True

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

    @property
    def state_attributes(self) -> dict[str, Any]:
        return {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "label": self.label,
            "cancel_state": self.cancel_state
        }