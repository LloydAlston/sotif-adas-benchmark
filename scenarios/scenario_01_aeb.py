import sys
import os
import time
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import carla
from world_setup.carla_world import get_weather
from kpis.data_logger import DataLogger


def get_speed(vehicle):
    v = vehicle.get_velocity()
    return math.sqrt(v.x**2 + v.y**2 + v.z**2) * 3.6  # km/h


def get_distance(v1, v2):
    l1 = v1.get_transform().location
    l2 = v2.get_transform().location
    return l1.distance(l2)


def run_scenario_01():
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)

    world = client.get_world()

    # Sync mode
    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = 0.067
    world.apply_settings(settings)

    print(f"Connected to CARLA: {world.get_map().name}")

    world.set_weather(get_weather('dry_day'))

    blueprint_library = world.get_blueprint_library()

    # Spawn vehicles in same lane
    spawn_point = world.get_map().get_spawn_points()[0]

    ego_bp = blueprint_library.find('vehicle.tesla.model3')
    ego_bp.set_attribute('color', '255,0,0')

    lead_bp = blueprint_library.find('vehicle.tesla.model3')
    lead_bp.set_attribute('color', '0,0,255')

    # Lead vehicle (front)
    lead_vehicle = world.spawn_actor(lead_bp, spawn_point)

    # Ego vehicle behind lead
    forward_vec = spawn_point.get_forward_vector()
    ego_location = spawn_point.location - forward_vec * 15
    ego_transform = carla.Transform(ego_location, spawn_point.rotation)

    ego_vehicle = world.spawn_actor(ego_bp, ego_transform)

    print("Vehicles spawned in same lane")

    # Traffic Manager (lead only for lane keeping)
    traffic_manager = client.get_trafficmanager(8000)
    traffic_manager.set_synchronous_mode(True)

    lead_vehicle.set_autopilot(True)
    traffic_manager.auto_lane_change(lead_vehicle, False)

    # Spectator
    spectator = world.get_spectator()

    # Loggers
    ego_logger = DataLogger('data/results/s01_ego_dry.csv')
    lead_logger = DataLogger('data/results/s01_lead_dry.csv')

    throttle = 0.5
    triggered = False
    collision = False

    print("Running scenario...")

    for step in range(300):
        world.tick()
        time.sleep(0.067)

        distance = get_distance(ego_vehicle, lead_vehicle)
        ego_speed = get_speed(ego_vehicle)
        lead_speed = get_speed(lead_vehicle)

        relative_speed = ego_speed - lead_speed
        ttc = distance / max(relative_speed / 3.6, 0.01)

        # Trigger sudden braking
        if not triggered and distance < 20:
            print(f"Lead braking triggered at {distance:.2f} m")
            lead_vehicle.apply_control(
                carla.VehicleControl(throttle=0.0, brake=1.0)
            )
            triggered = True

        # Ego continues forward (no AEB yet)
        ego_vehicle.apply_control(carla.VehicleControl(throttle=throttle))

        # Collision detection
        if distance < 2.0 and not collision:
            print("Collision detected")
            collision = True

        # Debug output
        print(f"Step {step} | Dist: {distance:.2f} m | TTC: {ttc:.2f}s | Ego: {ego_speed:.1f} km/h")

        # Camera follow
        transform = ego_vehicle.get_transform()
        spectator.set_transform(carla.Transform(
            transform.location + carla.Location(x=-8, z=4),
            carla.Rotation(pitch=-15)
        ))

        # Log data
        ego_logger.log(world, ego_vehicle)
        lead_logger.log(world, lead_vehicle)

    # Cleanup
    ego_logger.close()
    lead_logger.close()

    ego_vehicle.destroy()
    lead_vehicle.destroy()

    settings.synchronous_mode = False
    world.apply_settings(settings)

    print("Scenario complete")


if __name__ == '__main__':
    run_scenario_01()