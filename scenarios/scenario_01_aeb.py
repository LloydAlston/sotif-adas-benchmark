import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import carla
from world_setup.carla_world import get_weather
from kpis.data_logger import DataLogger


def run_scenario_01():
    client = carla.Client('localhost', 2000)
    client.set_timeout(15.0)

    world = client.get_world()

    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = 0.067  # ~15 FPS
    world.apply_settings(settings)

    print(f"Connected to CARLA. Map: {world.get_map().name}")

    world.set_weather(get_weather('dry_day'))

    blueprint_library = world.get_blueprint_library()
    ego_vehicle_bp = blueprint_library.find('vehicle.tesla.model3')
    ego_vehicle_bp.set_attribute('color', '255,0,0')

    spawn_points = world.get_map().get_spawn_points()

    ego_vehicle = world.spawn_actor(ego_vehicle_bp, spawn_points[5])
    lead_vehicle = world.spawn_actor(ego_vehicle_bp, spawn_points[6])

    print("Both vehicles spawned")

    spectator = world.get_spectator()

    # Initial camera placement
    transform = ego_vehicle.get_transform()
    spectator.set_transform(carla.Transform(
        transform.location + carla.Location(x=-8, z=4),
        carla.Rotation(pitch=-15)
    ))

    world.tick()

    ego_logger = DataLogger('data/results/s01_ego_dry.csv')
    lead_logger = DataLogger('data/results/s01_lead_dry.csv')

    control = carla.VehicleControl(throttle=0.5)
    ego_vehicle.apply_control(control)
    lead_vehicle.apply_control(control)

    print("Vehicles driving at ~50 km/h")

    # Driving phase
    for _ in range(60):
        world.tick()
        time.sleep(0.067)

        transform = ego_vehicle.get_transform()
        spectator.set_transform(carla.Transform(
            transform.location + carla.Location(x=-8, z=4),
            carla.Rotation(pitch=-15)
        ))

        ego_logger.log(world, ego_vehicle)
        lead_logger.log(world, lead_vehicle)

    # Braking phase
    brake_control = carla.VehicleControl(throttle=0.0, brake=1.0)
    lead_vehicle.apply_control(brake_control)

    print("Lead vehicle braking hard")

    for _ in range(75):
        world.tick()
        time.sleep(0.067)

        transform = ego_vehicle.get_transform()
        spectator.set_transform(carla.Transform(
            transform.location + carla.Location(x=-8, z=4),
            carla.Rotation(pitch=-15)
        ))

        ego_logger.log(world, ego_vehicle)
        lead_logger.log(world, lead_vehicle)

    ego_logger.close()
    lead_logger.close()

    settings.synchronous_mode = False
    world.apply_settings(settings)

    lead_vehicle.destroy()
    ego_vehicle.destroy()

    print("Scenario 1 complete")


if __name__ == '__main__':
    run_scenario_01()