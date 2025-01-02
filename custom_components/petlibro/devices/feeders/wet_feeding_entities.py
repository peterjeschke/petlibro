from datetime import datetime, date
from decimal import Decimal
from enum import Enum
from logging import getLogger
from typing import Any
from zoneinfo import ZoneInfo

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .. import Device
from ...entity import _DeviceT
from ...sensor import PetLibroSensorEntity

type NativeValueType = StateType | date | datetime | Decimal

_LOGGER = getLogger(__name__)


# The value is how the API defines the state
class PlateState(Enum):
    WAITING = 1
    DONE = 2
    ACTIVE = 3


class WetFeedingPlanPlateSensorEntity(PetLibroSensorEntity[_DeviceT]):
    def __init__(self,
                 device: Device,
                 coordinator: DataUpdateCoordinator,
                 plate_index: int,
                 plate: dict[str, Any] | None):
        super().__init__(device, coordinator, str(plate_index))
        self._plate = plate
        self._attr_translation_placeholders = {"plate": self.label if self.label is not None else str(plate_index)}
        self._attr_has_entity_name = True
        self._attr_device_class = SensorDeviceClass.ENUM
        self._attr_options = [e.name for e in PlateState]

    @property
    def translation_key(self):
        return f"wet_feeding_plan_element"

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
    def native_value(self) -> str | None:
        if self._plate is None:
            return None
        state = self._plate.get("state")
        try:
            return PlateState(state).name
        except ValueError as err:
            _LOGGER.error("Unexpected plate state received: %s", state, err)
            return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "label": self.label,
            "cancel_state": self.cancel_state
        }
