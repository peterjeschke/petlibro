"""Support for PETLIBRO numbers."""
from __future__ import annotations

from logging import getLogger

from homeassistant.config_entries import ConfigEntry  # Added ConfigEntry import
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import PetLibroHub
from .core import DOMAIN, Device
from .devices.feeders.feeder import Feeder
from .devices.feeders.one_rfid_smart_feeder import OneRFIDSmartFeeder
from .entities import PetLibroNumberEntityDescription, PetLibroDescribedNumberEntity

_LOGGER = getLogger(__name__)

DEVICE_NUMBER_MAP: dict[type[Device], list[PetLibroNumberEntityDescription]] = {
    Feeder: [
    ],
    OneRFIDSmartFeeder: [
        PetLibroNumberEntityDescription[OneRFIDSmartFeeder](
            key="desiccant_frequency",
            translation_key="desiccant_frequency",
            icon="mdi:calendar-alert",
            native_unit_of_measurement="Days",
            mode="box",
            native_max_value=60,
            native_min_value=1,
            native_step=1,
            value=lambda device: device.desiccant_frequency,
            method=lambda device, value: device.set_desiccant_frequency(value),
            name="Desiccant Frequency"
        ),
        PetLibroNumberEntityDescription[OneRFIDSmartFeeder](
            key="sound_level",
            translation_key="sound_level",
            icon="mdi:volume-high",
            native_unit_of_measurement="%",
            native_max_value=100,
            native_min_value=1,
            native_step=1,
            value=lambda device: device.sound_level,
            method=lambda device, value: device.set_sound_level(value),
            name="Sound Level"
        )
    ]
}

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,  # Use ConfigEntry
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up PETLIBRO number using config entry."""
    # Retrieve the hub from hass.data that was set up in __init__.py
    hub: PetLibroHub = hass.data[DOMAIN].get(entry.entry_id)

    if not hub:
        _LOGGER.error("Hub not found for entry: %s", entry.entry_id)
        return

    # Ensure that the devices are loaded (if load_devices is not already called elsewhere)
    if not hub.devices:
        _LOGGER.warning("No devices found in hub during number setup.")
        return

    # Log the contents of the hub data for debugging
    _LOGGER.debug("Hub data: %s", hub)

    devices = hub.devices  # Devices should already be loaded in the hub
    _LOGGER.debug("Devices in hub: %s", devices)

    # Create number entities for each device based on the number map
    entities = [
        PetLibroDescribedNumberEntity(device, hub.coordinator, description)
        for device in devices  # Iterate through devices from the hub
        for device_type, entity_descriptions in DEVICE_NUMBER_MAP.items()
        if isinstance(device, device_type)
        for description in entity_descriptions
    ]

    if not entities:
        _LOGGER.warning("No number entities added, entities list is empty!")
    else:
        # Log the number of entities and their details
        _LOGGER.debug("Adding %d PetLibro number entities", len(entities))
        for entity in entities:
            _LOGGER.debug("Adding number entity: %s for device %s", entity.entity_description.name, entity.device.name)

        # Add number entities to Home Assistant
        async_add_entities(entities)

