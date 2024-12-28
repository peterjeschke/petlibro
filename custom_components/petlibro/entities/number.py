from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from logging import getLogger
from typing import Callable, Optional

from homeassistant.components.number import NumberEntityDescription, NumberDeviceClass, NumberEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .entity import PetLibroEntityDescription, _DeviceT, PetLibroEntity

_LOGGER = getLogger(__name__)

@dataclass(frozen=True)
class PetLibroNumberEntityDescription(NumberEntityDescription, PetLibroEntityDescription[_DeviceT]):
    """A class that describes device number entities."""

    device_class_fn: Callable[[_DeviceT], NumberDeviceClass | None] = lambda _: None
    value: Callable[[_DeviceT], float] = lambda _: True
    method: Callable[[_DeviceT], float] = lambda _: True
    device_class: Optional[NumberDeviceClass] = None


class PetLibroDescribedNumberEntity(PetLibroEntity[_DeviceT], NumberEntity):
    """PETLIBRO sensor entity."""

    entity_description: PetLibroNumberEntityDescription[_DeviceT]

    def __init__(self, device: _DeviceT, coordinator: DataUpdateCoordinator, description: PetLibroNumberEntityDescription[_DeviceT]):
        super().__init__(device, coordinator, description.key)

    @cached_property
    def device_class(self) -> NumberDeviceClass | None:
        """Return the device class to use in the frontend, if any."""
        return self.entity_description.device_class

    @property
    def native_value(self) -> float | None:
        """Return the current state."""
        state = getattr(self.device, self.entity_description.key, None)
        if state is None:
            _LOGGER.warning(f"Value '{self.entity_description.key}' is None for device {self.device.name}")
            return None
        _LOGGER.debug(f"Retrieved value for '{self.entity_description.key}', {self.device.name}: {state}")
        return float(state)

    async def async_set_native_value(self, value: float) -> None:
        """Set the value of the number."""
        _LOGGER.debug(f"Setting value {value} for {self.device.name}")
        try:
            # Regular case for sound_level or other methods that only need a value
            _LOGGER.debug(f"Calling method with value={value} for {self.device.name}")
            await self.entity_description.method(self.device, value)
            _LOGGER.debug(f"Value {value} set successfully for {self.device.name}")
        except Exception as e:
            _LOGGER.error(f"Error setting value {value} for {self.device.name}: {e}")
