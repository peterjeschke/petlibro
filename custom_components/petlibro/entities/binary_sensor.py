from __future__ import annotations

import logging
from dataclasses import dataclass
from functools import cached_property
from typing import Callable, Optional

from homeassistant.components.binary_sensor import BinarySensorEntityDescription, BinarySensorDeviceClass, \
    BinarySensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .entity import PetLibroEntityDescription, _DeviceT, PetLibroEntity

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class PetLibroBinarySensorEntityDescription(BinarySensorEntityDescription, PetLibroEntityDescription[_DeviceT]):
    """A class that describes device binary sensor entities."""

    device_class_fn: Callable[[_DeviceT], BinarySensorDeviceClass | None] = lambda _: None
    should_report: Callable[[_DeviceT], bool] = lambda _: True
    device_class: Optional[BinarySensorDeviceClass] = None

class PetLibroBinarySensorEntity(PetLibroEntity[_DeviceT], BinarySensorEntity):
    def __init__(self, device: _DeviceT, coordinator: DataUpdateCoordinator, key: str):
        super().__init__(device, coordinator, key)

class PetLibroDescribedBinarySensorEntity(PetLibroBinarySensorEntity[_DeviceT]):

    entity_description: PetLibroBinarySensorEntityDescription[_DeviceT]

    def __init__(self, device: _DeviceT, coordinator: DataUpdateCoordinator, description: PetLibroBinarySensorEntityDescription[_DeviceT]):
        super().__init__(device, coordinator, description.key)
        self.entity_description = description

    @cached_property
    def device_class(self) -> BinarySensorDeviceClass | None:
        """Return the device class to use in the frontend, if any."""
        return self.entity_description.device_class

    @property
    def is_on(self) -> bool:
        """Return True if the binary sensor is on."""
        # Check if the binary sensor should report its state
        if not self.entity_description.should_report(self.device):
            return False

        # Retrieve the state using getattr, defaulting to None if the attribute is missing
        state = getattr(self.device, self.entity_description.key, None)

        # Check if this is the first time the sensor is being refreshed by checking if _last_state exists
        last_state = getattr(self, '_last_state', None)
        initial_log_done = getattr(self, '_initial_log_done', False)  # Track if we've logged the initial state

        # If this is the initial boot, don't log anything but track the state
        if not initial_log_done:
            # Mark the initial log as done without logging
            self._initial_log_done = True
        elif last_state != state:
            # Log state changes: log online with INFO and offline with WARNING
            if state:
                _LOGGER.info(f"Device {self.device.name} is online.")
            else:
                _LOGGER.warning(f"Device {self.device.name} is offline.")

        # Store the last state for future comparisons
        self._last_state = state

        # Return the state, ensuring it's a boolean
        return bool(state)
