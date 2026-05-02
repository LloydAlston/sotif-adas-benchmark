import sys
import os
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import carla
from world_setup.carla_world import get_weather
from kpis.data_logger import DataLogger


# -----------------------------
# Utility Functions
# -----------------------------
def get_distance(vehicle1, vehicle2):
    loc1 = vehicle1.get_location()
    loc2 = vehicle2.get_location()
    return ((loc1.x - loc2.x)**2 +
            (loc1.y - loc2.y)**2 +
            (loc1.z - loc2.z)**2) ** 0.5


def set_speed(vehicle, speed_kmh):
    speed_ms = speed_kmh / 3.6
    forward = vehicle.get_transform().get_forward_vector()
    vehicle.set_target_velocity(forward * speed_ms)


# -----------------------------
# MAIN SCENARIO
# -----------------------------
def run_scenario_01():
    client = carla.Client('localhost', 2000)
    client.set_timeout(15.0)

    world = client.get_world()

    # Sync mode
    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = 0.05
    world.apply_settings(settings)

    print(f"Connected to CARLA: {world.get_map().name}")

    # Weather (as per your scenario.md)
    world.set_weather(get_weather('dry_day'))

    blueprint_library = world.get_blueprint_library()

    ego_bp = blueprint_library.find('vehicle.tesla.model3')
    ego_bp.set_attribute('color', '255,0,0')  # red (ego)

    lead_bp = blueprint_library.find('vehicle.tesla.model3')
    lead_bp.set_attribute('color', '0,0,255')  # blue (lead)

    # -----------------------------
    # SAFE SPAWN
    # -----------------------------
    spawn_points = world.get_map().get_spawn_points()

    ego_vehicle = None
    lead_vehicle = None

    for sp in spawn_points:
        forward = sp.get_forward_vector()

        lead_transform = carla.Transform(
            sp.location + forward * 20,
            sp.rotation
        )

        ego_vehicle = world.try_spawn_actor(ego_bp, sp)
        lead_vehicle = world.try_spawn_actor(lead_bp, lead_transform)

        if ego_vehicle and lead_vehicle:
            print("Spawn successful")
            break
        else:
            if ego_vehicle:
                ego_vehicle.destroy()
            if lead_vehicle:
                lead_vehicle.destroy()

    if ego_vehicle is None or lead_vehicle is None:
        print("Could not spawn vehicles")
        return

    spectator = world.get_spectator()
    world.tick()

    # -----------------------------
    # COLLISION SENSOR (FIX)
    # -----------------------------
    collision_flag = {"ego": False}

    def collision_callback(event):
        collision_flag["ego"] = True
        print("Collision detected (sensor)")

    collision_bp = blueprint_library.find('sensor.other.collision')

    collision_sensor = world.spawn_actor(
        collision_bp,
        carla.Transform(),
        attach_to=ego_vehicle
    )

    collision_sensor.listen(collision_callback)

    # -----------------------------
    # LOGGERS
    # -----------------------------
    ego_logger = DataLogger('data/results/s01_ego_dry.csv')
    lead_logger = DataLogger('data/results/s01_lead_dry.csv')

    # -----------------------------
    # DRIVING PHASE (~50 km/h)
    # -----------------------------
    for _ in range(60):
        world.tick()

        ego_vehicle.apply_control(carla.VehicleControl(throttle=0.5))
        lead_vehicle.apply_control(carla.VehicleControl(throttle=0.5))

        set_speed(ego_vehicle, 50)
        set_speed(lead_vehicle, 50)

        transform = ego_vehicle.get_transform()
        spectator.set_transform(carla.Transform(
            transform.location + carla.Location(x=-8, z=4),
            carla.Rotation(pitch=-15)
        ))

        ego_logger.log(world, ego_vehicle)
        lead_logger.log(world, lead_vehicle)

    print("Vehicles driving straight at ~50 km/h")

    # -----------------------------
    # BRAKING PHASE
    # -----------------------------
    lead_vehicle.apply_control(carla.VehicleControl(throttle=0.0, brake=1.0))
    print("Lead vehicle braking hard")

    ego_braking = False
    min_distance = float('inf')

    for _ in range(75):
        world.tick()

        distance = get_distance(ego_vehicle, lead_vehicle)
        min_distance = min(min_distance, distance)

        if distance < 17.0 and not ego_braking:
            ego_vehicle.apply_control(
                carla.VehicleControl(throttle=0.0, brake=1.0)
            )
            ego_braking = True
            print("Ego vehicle AEB activated")

        if not ego_braking:
            ego_vehicle.apply_control(carla.VehicleControl(throttle=0.5))
            set_speed(ego_vehicle, 50)

        transform = ego_vehicle.get_transform()
        spectator.set_transform(carla.Transform(
            transform.location + carla.Location(x=-8, z=4),
            carla.Rotation(pitch=-15)
        ))

        ego_logger.log(world, ego_vehicle)
        lead_logger.log(world, lead_vehicle)

    # -----------------------------
    # RESULTS (FIXED)
    # -----------------------------
    print(f"Minimum distance during braking: {min_distance:.2f} meters")

    if collision_flag["ego"]:
        print("Collision occurred")
    else:
        print("No collision")

    # -----------------------------
    # CLEANUP
    # -----------------------------
    collision_sensor.stop()
    collision_sensor.destroy()

    ego_logger.close()
    lead_logger.close()

    settings.synchronous_mode = False
    world.apply_settings(settings)

    ego_vehicle.destroy()
    lead_vehicle.destroy()

    print("Scenario 1 complete")


# -----------------------------
if __name__ == '__main__':
    run_scenario_01()