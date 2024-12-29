from typing import Dict, Type

from ..core import Device
from .feeders.feeder import Feeder
from .feeders.air_smart_feeder import AirSmartFeeder
from .feeders.granary_smart_feeder import GranarySmartFeeder
from .feeders.granary_smart_camera_feeder import GranarySmartCameraFeeder
from .feeders.one_rfid_smart_feeder import OneRFIDSmartFeeder
from .feeders.polar_wet_food_feeder import PolarWetFoodFeeder
from .fountains.dockstream_smart_fountain import DockstreamSmartFountain
from .fountains.dockstream_smart_rfid_fountain import DockstreamSmartRFIDFountain

product_name_map : Dict[str, Type[Device]] = {
    "Air Smart Feeder": AirSmartFeeder,
    "Granary Smart Feeder": GranarySmartFeeder,
    "Granary Smart Camera Feeder": GranarySmartCameraFeeder,
    "One RFID Smart Feeder": OneRFIDSmartFeeder,
    "Polar Wet Food Feeder": PolarWetFoodFeeder,
    "Dockstream Smart Fountain": DockstreamSmartFountain,
    "Dockstream Smart RFID Fountain": DockstreamSmartRFIDFountain
}
