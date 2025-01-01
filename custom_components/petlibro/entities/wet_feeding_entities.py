from datetime import datetime, date
from decimal import Decimal
from enum import Enum
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

# The value is how the API defines the state
class PlateState(Enum):
    WAITING = 1,
    DONE = 2,
    ACTIVE = 3

class WetFeedingPlanPlateSensorEntity(PetLibroBinarySensorEntity[_DeviceT]):
    def __init__(self,
                 device: Device,
                 coordinator: DataUpdateCoordinator,
                 plate_index: int,
                 plate: dict[str, Any] | None):
        super().__init__(device, coordinator, str(plate_index))
        self._plate = plate
        self._attr_translation_placeholders = {"plate": str(plate_index)}
        self._attr_has_entity_name = True

    @property
    def translation_key(self):
        return f"wet_feeding_plan_element"

    @property
    def is_on(self) -> bool:
        return self.plate_state == PlateState.ACTIVE

    @property
    def start_time(self) -> datetime | None:
        if self._plate is None:
            return None
        return datetime.strptime(self._plate.get("executionStartTime"), "%Y-%m-%d %H:%M").astimezone(
            ZoneInfo(self._plate.get("timezone")))

    @property
    def end_time(self) -> datetime | None:
        if self._plate is None:
            return None
        return datetime.strptime(self._plate.get("executionEndTime"), "%Y-%m-%d %H:%M").astimezone(
            ZoneInfo(self._plate.get("timezone")))

    @property
    def label(self) -> str | None:
        if self._plate is None:
            return None
        return self._plate.get("label")

    @property
    def cancel_state(self) -> bool | None:
        if self._plate is None:
            return None
        return self._plate.get("cancelState")

    @property
    def plate_state(self) -> PlateState | None:
        if self._plate is None:
            _LOGGER.debug("Polar: self._plate is none!")
            return None
        try:
            _LOGGER.debug("Polar: platestate %s (%s): %s", self._plate.get("state"), type(self._plate.get("state")), PlateState(self._plate.get("state")))
            return PlateState(self._plate.get("state"))
        except ValueError as err:
            _LOGGER.warning("Unexpected plate state received: %s", self._plate.get("state"), err)
            return None

    @property
    def state_attributes(self) -> dict[str, Any]:
        return {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "label": self.label,
            "cancel_state": self.cancel_state,
            "plate_state": self.plate_state
        }