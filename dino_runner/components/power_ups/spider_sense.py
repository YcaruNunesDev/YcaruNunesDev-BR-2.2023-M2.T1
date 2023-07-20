from dino_runner.utils.constants import SPIDER_SENSE, SPIDER_SENSE_TYPE
from dino_runner.components.power_ups.power_up import PowerUp


class Spider_sense(PowerUp):
    def __init__(self):
        self.image = SPIDER_SENSE
        self.type = SPIDER_SENSE_TYPE
        super().__init__(self.image, self.type)