from __future__ import annotations

from dataclasses import dataclass
from logging import getLogger
from typing import Generic, Callable, Coroutine, Any

from homeassistant.components.button import ButtonEntityDescription, ButtonEntity
from homeassistant.const import EntityCategory
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .entity import _DeviceT, PetLibroEntityDescription, PetLibroEntity

_LOGGER = getLogger(__name__)


@dataclass(frozen=True)
class RequiredKeysMixin(Generic[_DeviceT]):
    """A class that describes devices button entity required keys."""
    set_fn: Callable[[_DeviceT], Coroutine[Any, Any, None]]


@dataclass(frozen=True)
class PetLibroButtonEntityDescription(ButtonEntityDescription, PetLibroEntityDescription[_DeviceT], RequiredKeysMixin[_DeviceT]):
    """A class that describes device button entities."""
    entity_category: EntityCategory = EntityCategory.CONFIG


class PetLibroDescribedButtonEntity(PetLibroEntity[_DeviceT], ButtonEntity):
    """PETLIBRO button entity."""
    entity_description: PetLibroButtonEntityDescription[_DeviceT]

    def __init__(self, device: _DeviceT, coordinator: DataUpdateCoordinator,
                 description: PetLibroButtonEntityDescription[_DeviceT]):
        super().__init__(device, coordinator, description.key)

    @property
    def available(self) -> bool:
        """Check if the device is available."""
        return getattr(self.device, 'online', False)

    async def async_press(self) -> None:
        """Handle the button press."""
        _LOGGER.debug("Pressing button: %s for device %s", self.entity_description.name, self.device.name)

        # Log available methods for debugging
        _LOGGER.debug("Available methods for device %s: %s", self.device.name, dir(self.device))

        try:
            await self.entity_description.set_fn(self.device)
            await self.device.refresh()  # Refresh the device state after the button press
            _LOGGER.debug("Successfully pressed button: %s", self.entity_description.name)
        except Exception as e:
            _LOGGER.error(
                f"Error pressing button {self.entity_description.name} for device {self.device.name}: {e}",
                exc_info=True  # Log full traceback for better debugging
            )
