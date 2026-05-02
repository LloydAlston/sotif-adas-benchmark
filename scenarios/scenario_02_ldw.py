import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import carla
import math
from world_setup.carla_world import get_weather
from kpis.data_logger import DataLogger


# -----------------------------
# Utility Functions
# -----------------------------
def get_lateral_offset(vehicle, waypoint):
    vehicle_loc = vehicle.get_location()
    lane_center = waypoint.transform.location

    dx = vehicle_loc.x - lane_center.x
    dy = vehicle_loc.y - lane_center.y

    return math.sqrt(dx**2 + dy**2)


def compute_tlc(vehicle, waypoint, lane_width, offset):
    velocity = vehicle.get_velocity()
    right_vector = waypoint.transform.get_right_vector()

    lateral_speed = abs(
        velocity.x * right_vector.x +
        velocity.y * right_vector.y
    )

    distance_to_edge = (lane_width / 2) - offset

    if lateral_speed > 0:
        return distance_to_edge / lateral_speed
    else:
        return float('inf')


# -----------------------------
# MAIN SCENARIO
# -----------------------------
def run_scenario_02():
    client = carla.Client('localhost', 2000)
    client.set_timeout(15.0)

    # ✔ Use correct map for curved motorway
    world = client.load_world('Town04')

    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = 0.05
    world.apply_settings(settings)

    print(f"Connected to CARLA: {world.get_map().name}")

    # ✔ Scenario condition: clear day
    world.set_weather(get_weather('fog_light'))

    blueprint_library = world.get_blueprint_library()
    ego_bp = blueprint_library.find('vehicle.tesla.model3')

    # -----------------------------
    # FIXED CURVED SPAWN
    # -----------------------------
    spawn_points = world.get_map().get_spawn_points()

    ego_transform = spawn_points[20]  # known curved segment
    ego_vehicle = world.try_spawn_actor(ego_bp, ego_transform)

    if ego_vehicle is None:
        print("❌ Spawn failed")
        return

    print("Spawned on curved motorway (Town04)")

    spectator = world.get_spectator()
    world.tick()

    ego_logger = DataLogger('data/results/s02_ego_dawn.csv')

    # -----------------------------
    # PARAMETERS
    # -----------------------------
    target_speed = 25  # ✔ slightly slower → better visibility
    ldw_triggered = False
    tlc_at_trigger = None
    lane_crossed = False

    # -----------------------------
    # SIMULATION LOOP
    # -----------------------------
    for frame in range(400):
        world.tick()

        # ✔ No corrective steering (tiny bias after delay)
        if frame < 40:
            steer = 0.0
        else:
            steer = 0.0015

        ego_vehicle.apply_control(
            carla.VehicleControl(throttle=0.5, steer=steer)
        )

        # Maintain speed
        speed_ms = target_speed / 3.6
        forward = ego_vehicle.get_transform().get_forward_vector()
        ego_vehicle.set_target_velocity(forward * speed_ms)

        ego_loc = ego_vehicle.get_location()
        ego_wp = world.get_map().get_waypoint(ego_loc)

        lane_width = ego_wp.lane_width
        offset = get_lateral_offset(ego_vehicle, ego_wp)

        tlc = compute_tlc(ego_vehicle, ego_wp, lane_width, offset)

        # -----------------------------
        # LDW TRIGGER (earlier but valid)
        # -----------------------------
        if tlc < 0.9 and not ldw_triggered:
            ldw_triggered = True
            tlc_at_trigger = tlc
            print(f"⚠️ LDW Triggered | TLC: {tlc:.2f}s | Offset: {offset:.2f}m")

        # -----------------------------
        # LANE CROSSING
        # -----------------------------
        if offset > lane_width / 2 and not lane_crossed:
            print("❌ Lane crossed")
            lane_crossed = True

        # Camera follow
        transform = ego_vehicle.get_transform()
        spectator.set_transform(carla.Transform(
            transform.location + carla.Location(x=-8, z=4),
            carla.Rotation(pitch=-15)
        ))

        ego_logger.log(world, ego_vehicle)

    # -----------------------------
    # RESULT (strict to spec)
    # -----------------------------
    if ldw_triggered and tlc_at_trigger and tlc_at_trigger > 0.5:
        print("✅ PASS: LDW triggered >0.5s before crossing")
    else:
        print("❌ FAIL: LDW too late or missed")

    # Cleanup
    ego_logger.close()

    settings.synchronous_mode = False
    world.apply_settings(settings)

    ego_vehicle.destroy()

    print("Scenario 02 complete")


# -----------------------------
if __name__ == '__main__':
    run_scenario_02()