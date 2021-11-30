import logging

from background_task import background

logger = logging.getLogger('DRONE-BATTERY')
logger.setLevel(logging.INFO)

ch = logging.FileHandler('drones.log')
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)

logger.addHandler(ch)


@background(schedule=10)
def log_drone_state(drone_id):
    from misc.models import Drone
    try:
        drone = Drone.objects.get(pk=drone_id)
        logger.info(f"SERIAL_NUMBER: {drone.serial_number}, BATERRY_LEVEL: {drone.battery_capacity}")
    except:
        pass
