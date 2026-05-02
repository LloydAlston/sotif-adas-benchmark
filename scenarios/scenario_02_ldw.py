import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import carla
import math
from world_setup.carla_world import get_weather
from kpis.data_logger import DataLogger


# -----------------------------
# Utility
# -----------------------------
def get_speed(vehicle):
    v = vehicle.get_velocity()
    return math.sqrt(v.x**2 + v.y**2 + v.z**2)


def get_lateral_offset(vehicle, waypoint):
    vehicle_loc = vehicle.get_location()
    lane_center = waypoint.transform.location

    dx = vehicle_loc.x - lane_center.x
    dy = vehicle_loc.y - lane_center.y

    return math.sqrt(dx**2 + dy**2)


# -----------------------------
# MAIN SCENARIO
# -----------------------------
def run_scenario_02():
    client = carla.Client('localhost', 2000)
    client.set_timeout(15.0)

    world = client.get_world()

    # Sync mode
    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = 0.05
    world.apply_settings(settings)

    print(f"Connected to CARLA: {world.get_map().name}")

    # Weather (change as per test matrix)
    world.set_weather(get_weather('dry_day'))

    blueprint_library = world.get_blueprint_library()

    ego_bp = blueprint_library.find('vehicle.tesla.model3')
    ego_bp.set_attribute('color', '255,255,0')

    # -----------------------------
    # FIND CURVED ROAD SPAWN
    # -----------------------------
    spawn_points = world.get_map().get_spawn_points()

    ego_vehicle = None
    ego_wp = None

    for sp in spawn_points:
        wp = world.get_map().get_waypoint(sp.location)

        # pick curved road (has next waypoint with angle change)
        next_wp = wp.next(10.0)
        if len(next_wp) > 0:
            yaw_diff = abs(wp.transform.rotation.yaw - next_wp[0].transform.rotation.yaw)

            if yaw_diff > 5:  # curved segment
                ego_vehicle = world.try_spawn_actor(ego_bp, sp)
                ego_wp = wp
                if ego_vehicle:
                    print("Spawned on curved road")
                    break

    if ego_vehicle is None:
        print("❌ Could not find curved spawn")
        return

    spectator = world.get_spectator()
    world.tick()

    # Logger
    ego_logger = DataLogger('data/results/s02_ego.csv')

    # -----------------------------
    # PARAMETERS
    # -----------------------------
    target_speed = 50  # km/h
    drift_steer = 0.02  # slight drift (no driver correction)
    ldw_triggered = False

    # -----------------------------
    # SIMULATION LOOP
    # -----------------------------
    for frame in range(150):
        world.tick()

        # apply constant throttle + slight drift
        ego_vehicle.apply_control(
            carla.VehicleControl(throttle=0.5, steer=drift_steer)
        )

        # stabilize speed
        speed_ms = target_speed / 3.6
        forward = ego_vehicle.get_transform().get_forward_vector()
        ego_vehicle.set_target_velocity(forward * speed_ms)

        # get current waypoint
        ego_loc = ego_vehicle.get_location()
        ego_wp = world.get_map().get_waypoint(ego_loc)

        # lane width
        lane_width = ego_wp.lane_width

        # lateral offset
        offset = get_lateral_offset(ego_vehicle, ego_wp)

        # approximate TLC (time to lane crossing)
        speed = get_speed(ego_vehicle)
        if speed > 0:
            tlc = (lane_width/2 - offset) / speed
        else:
            tlc = float('inf')

        # LDW trigger condition
        if tlc < 0.5 and not ldw_triggered:
            print(f"⚠️ LDW Triggered | TLC: {tlc:.2f}s | Offset: {offset:.2f}m")
            ldw_triggered = True

        # lane crossing check
        if offset > lane_width / 2:
            print("❌ Lane crossed")
            break

        # camera follow
        transform = ego_vehicle.get_transform()
        spectator.set_transform(carla.Transform(
            transform.location + carla.Location(x=-8, z=4),
            carla.Rotation(pitch=-15)
        ))

        # log data
        ego_logger.log(world, ego_vehicle)

    # -----------------------------
    # RESULT
    # -----------------------------
    if ldw_triggered:
        print("✅ LDW triggered before lane crossing")
    else:
        print("❌ LDW failed (missed warning)")

    # Cleanup
    ego_logger.close()

    settings.synchronous_mode = False
    world.apply_settings(settings)

    ego_vehicle.destroy()

    print("Scenario 02 complete")


# -----------------------------
if __name__ == '__main__':
    run_scenario_02()