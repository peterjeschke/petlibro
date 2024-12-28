"""Support for PETLIBRO switches."""
from __future__ import annotations

from logging import getLogger

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import PetLibroHub
from .core import DOMAIN, Device
from .devices.feeders.air_smart_feeder import AirSmartFeeder
from .devices.feeders.feeder import Feeder
from .devices.feeders.granary_smart_camera_feeder import GranarySmartCameraFeeder
from .devices.feeders.granary_smart_feeder import GranarySmartFeeder
from .devices.feeders.one_rfid_smart_feeder import OneRFIDSmartFeeder
from .devices.feeders.polar_wet_food_feeder import PolarWetFoodFeeder
from .devices.fountains.dockstream_smart_fountain import DockstreamSmartFountain
from .devices.fountains.dockstream_smart_rfid_fountain import DockstreamSmartRFIDFountain
from .entities import PetLibroSwitchEntityDescription, PetLibroDescribedSwitchEntity

_LOGGER = getLogger(__name__)

DEVICE_SWITCH_MAP: dict[type[Device], list[PetLibroSwitchEntityDescription]] = {
    Feeder: [
    ],
    AirSmartFeeder: [
    ],
    GranarySmartFeeder: [
    ],
    GranarySmartCameraFeeder: [
    ],
    OneRFIDSmartFeeder: [
    ],
    PolarWetFoodFeeder: [
    ],
    DockstreamSmartFountain: [
    ],
    DockstreamSmartRFIDFountain: [
    ],
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up PETLIBRO switches using config entry."""
    # Retrieve the hub from hass.data that was set up in __init__.py
    hub: PetLibroHub = hass.data[DOMAIN].get(entry.entry_id)

    if not hub:
        _LOGGER.error("Hub not found for entry: %s", entry.entry_id)
        return

    # Ensure that the devices are loaded
    if not hub.devices:
        _LOGGER.warning("No devices found in hub during switch setup.")
        return

    # Log the contents of the hub data for debugging
    _LOGGER.debug("Hub data: %s", hub)

    devices = hub.devices  # Devices should already be loaded in the hub
    _LOGGER.debug("Devices in hub: %s", devices)

    # Create switch entities for each device based on the switch map
    entities = [
        PetLibroDescribedSwitchEntity(device, hub.coordinator, description)
        for device in devices  # Iterate through devices from the hub
        for device_type, entity_descriptions in DEVICE_SWITCH_MAP.items()
        if isinstance(device, device_type)
        for description in entity_descriptions
    ]

    if not entities:
        _LOGGER.warning("No switches added, entities list is empty!")
    else:
        # Log the number of entities and their details
        _LOGGER.debug("Adding %d PetLibro switches", len(entities))
        for entity in entities:
            _LOGGER.debug("Adding switch entity: %s for device %s", entity.entity_description.name, entity.device.name)

        # Add switch entities to Home Assistant
        async_add_entities(entities)

