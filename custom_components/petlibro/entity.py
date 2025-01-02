"""PETLIBRO entities for common data and methods."""

from __future__ import annotations

from functools import cached_property
from typing import Generic, TypeVar

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator

from .const import DOMAIN
from .devices import Device
from .devices.event import EVENT_UPDATE

_DeviceT = TypeVar("_DeviceT", bound=Device)


class PetLibroEntity(
    CoordinatorEntity[DataUpdateCoordinator[bool]], Generic[_DeviceT]
):
    """Generic PETLIBRO entity representing common data and methods."""

    _attr_has_entity_name = True

    def __init__(
            self, device: _DeviceT, coordinator: DataUpdateCoordinator[bool], key: str
    ) -> None:
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self.device = device
        self._attr_unique_id = f"{self.device.serial}-{key}"

    @cached_property
    def device_info(self) -> DeviceInfo | None:
        """Return the device information for a PETLIBRO."""
        assert self.device.serial
        return DeviceInfo(
            identifiers={(DOMAIN, self.device.serial)},
            manufacturer="PETLIBRO",
            model=self.device.model,
            name=self.device.name,
            sw_version=self.device.software_version,
            hw_version=self.device.hardware_version
        )

    async def async_added_to_hass(self) -> None:
        """Set up a listener for the entity."""
        await super().async_added_to_hass()
        self.async_on_remove(self.device.on(EVENT_UPDATE, self.async_write_ha_state))

class PetLibroEntityDescription(EntityDescription, Generic[_DeviceT]):
    """PETLIBRO Entity description"""
