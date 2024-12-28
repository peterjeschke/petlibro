"""Support for PETLIBRO buttons."""
from __future__ import annotations

from logging import getLogger

from homeassistant.config_entries import ConfigEntry  # Added ConfigEntry import
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
from .entities import PetLibroButtonEntityDescription, PetLibroDescribedButtonEntity

_LOGGER = getLogger(__name__)

# Map buttons to their respective device types
DEVICE_BUTTON_MAP: dict[type[Device], list[PetLibroButtonEntityDescription]] = {
    Feeder: [
    ],
    AirSmartFeeder: [
        PetLibroButtonEntityDescription[AirSmartFeeder](
            key="manual_feed",
            translation_key="manual_feed",
            set_fn=lambda device: device.set_manual_feed(),
            name="Manual Feed"
        ),
        PetLibroButtonEntityDescription[AirSmartFeeder](
            key="enable_feeding_plan",
            translation_key="enable_feeding_plan",
            set_fn=lambda device: device.set_feeding_plan(True),
            name="Enable Feeding Plan"
        ),
        PetLibroButtonEntityDescription[AirSmartFeeder](
            key="disable_feeding_plan",
            translation_key="disable_feeding_plan",
            set_fn=lambda device: device.set_feeding_plan(False),
            name="Disable Feeding Plan"
        )
    ],
    GranarySmartFeeder: [
        PetLibroButtonEntityDescription[GranarySmartFeeder](
            key="manual_feed",
            translation_key="manual_feed",
            set_fn=lambda device: device.set_manual_feed(),
            name="Manual Feed"
        ),
        PetLibroButtonEntityDescription[GranarySmartFeeder](
            key="enable_feeding_plan",
            translation_key="enable_feeding_plan",
            set_fn=lambda device: device.set_feeding_plan(True),
            name="Enable Feeding Plan"
        ),
        PetLibroButtonEntityDescription[GranarySmartFeeder](
            key="disable_feeding_plan",
            translation_key="disable_feeding_plan",
            set_fn=lambda device: device.set_feeding_plan(False),
            name="Disable Feeding Plan"
        )
    ],
    GranarySmartCameraFeeder: [
        PetLibroButtonEntityDescription[GranarySmartCameraFeeder](
            key="manual_feed",
            translation_key="manual_feed",
            set_fn=lambda device: device.set_manual_feed(),
            name="Manual Feed"
        ),
        PetLibroButtonEntityDescription[GranarySmartCameraFeeder](
            key="enable_feeding_plan",
            translation_key="enable_feeding_plan",
            set_fn=lambda device: device.set_feeding_plan(True),
            name="Enable Feeding Plan"
        ),
        PetLibroButtonEntityDescription[GranarySmartCameraFeeder](
            key="disable_feeding_plan",
            translation_key="disable_feeding_plan",
            set_fn=lambda device: device.set_feeding_plan(False),
            name="Disable Feeding Plan"
        )
    ],
    OneRFIDSmartFeeder: [
        PetLibroButtonEntityDescription[OneRFIDSmartFeeder](
            key="manual_feed",
            translation_key="manual_feed",
            set_fn=lambda device: device.set_manual_feed(),
            name="Manual Feed"
        ),
        PetLibroButtonEntityDescription[OneRFIDSmartFeeder](
            key="enable_feeding_plan",
            translation_key="enable_feeding_plan",
            set_fn=lambda device: device.set_feeding_plan(True),
            name="Enable Feeding Plan"
        ),
        PetLibroButtonEntityDescription[OneRFIDSmartFeeder](
            key="disable_feeding_plan",
            translation_key="disable_feeding_plan",
            set_fn=lambda device: device.set_feeding_plan(False),
            name="Disable Feeding Plan"
        ),
        PetLibroButtonEntityDescription[OneRFIDSmartFeeder](
            key="manual_lid_open",
            translation_key="manual_lid_open",
            set_fn=lambda device: device.set_manual_lid_open(),
            name="Manually Open Lid"
        ),
        PetLibroButtonEntityDescription[OneRFIDSmartFeeder](
            key="display_on",
            translation_key="display_on",
            set_fn=lambda device: device.set_display_on(),
            name="Turn On Display"
        ),
        PetLibroButtonEntityDescription[OneRFIDSmartFeeder](
            key="display_off",
            translation_key="display_off",
            set_fn=lambda device: device.set_display_off(),
            name="Turn Off Display"
        ),
        PetLibroButtonEntityDescription[OneRFIDSmartFeeder](
            key="sound_on",
            translation_key="sound_on",
            set_fn=lambda device: device.set_sound_on(),
            name="Turn On Sound"
        ),
        PetLibroButtonEntityDescription[OneRFIDSmartFeeder](
            key="sound_off",
            translation_key="sound_off",
            set_fn=lambda device: device.set_sound_off(),
            name="Turn Off Sound"
        ),
        PetLibroButtonEntityDescription[OneRFIDSmartFeeder](
            key="desiccant_reset",
            translation_key="desiccant_reset",
            set_fn=lambda device: device.set_desiccant_reset(),
            name="Desiccant Replaced"
        )

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
    entry: ConfigEntry,  # Use ConfigEntry
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up PETLIBRO buttons using config entry."""
    # Retrieve the hub from hass.data that was set up in __init__.py
    hub: PetLibroHub = hass.data[DOMAIN].get(entry.entry_id)

    if not hub:
        _LOGGER.error("Hub not found for entry: %s", entry.entry_id)
        return

    # Ensure that the devices are loaded
    if not hub.devices:
        _LOGGER.warning("No devices found in hub during button setup.")
        return

    # Log the contents of the hub data for debugging
    _LOGGER.debug("Hub data: %s", hub)

    devices = hub.devices  # Devices should already be loaded in the hub
    _LOGGER.debug("Devices in hub: %s", devices)

    # Create button entities for each device based on the button map
    entities = [
        PetLibroDescribedButtonEntity(device, hub.coordinator, description)
        for device in devices  # Iterate through devices from the hub
        for device_type, entity_descriptions in DEVICE_BUTTON_MAP.items()
        if isinstance(device, device_type)
        for description in entity_descriptions
    ]

    if not entities:
        _LOGGER.warning("No buttons added, entities list is empty!")
    else:
        # Log the number of entities and their details
        _LOGGER.debug("Adding %d PetLibro buttons", len(entities))
        for entity in entities:
            _LOGGER.debug("Adding button entity: %s for device %s", entity.entity_description.name, entity.device.name)

        # Add button entities to Home Assistant
        async_add_entities(entities)




