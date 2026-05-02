import sys
import os
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import carla
from world_setup.carla_world import get_weather
from kpis.data_logger import DataLogger


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


def compute_ttc(ego, lead):
    v_ego = ego.get_velocity()
    v_lead = lead.get_velocity()

    rel_speed = math.sqrt(
        (v_ego.x - v_lead.x)**2 +
        (v_ego.y - v_lead.y)**2 +
        (v_ego.z - v_lead.z)**2
    )

    distance = get_distance(ego, lead)

    if rel_speed > 0:
        return distance / rel_speed
    return float('inf')


def run_scenario_01(condition='dry_day'):

    client = carla.Client('localhost', 2000)
    client.set_timeout(15.0)

    world = client.get_world()

    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = 0.05
    world.apply_settings(settings)

    print(f"Connected to CARLA: {world.get_map().name}")

    world.set_weather(get_weather(condition))

    # -----------------------------
    # CONDITION PARAMETERS
    # -----------------------------
    if condition == 'dry_day':
        reaction_time = 0.3
        friction = 1.0
    elif condition == 'wet_night':
        reaction_time = 0.6
        friction = 0.7
    elif condition == 'heavy_rain':
        reaction_time = 0.8
        friction = 0.5
    else:
        reaction_time = 0.3
        friction = 1.0

    blueprint_library = world.get_blueprint_library()

    ego_bp = blueprint_library.find('vehicle.tesla.model3')
    lead_bp = blueprint_library.find('vehicle.tesla.model3')

    ego_bp.set_attribute('color', '255,0,0')
    lead_bp.set_attribute('color', '0,0,255')

    # -----------------------------
    # SPAWN (TIGHTER GAP)
    # -----------------------------
    spawn_points = world.get_map().get_spawn_points()

    ego_vehicle = None
    lead_vehicle = None

    for sp in spawn_points:
        forward = sp.get_forward_vector()

        lead_transform = carla.Transform(
            sp.location + forward * 26,   # 🔥 reduced gap
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
        print("Spawn failed")
        return

    # -----------------------------
    # APPLY PHYSICS
    # -----------------------------
    for v in [ego_vehicle, lead_vehicle]:
        physics = v.get_physics_control()
        for wheel in physics.wheels:
            wheel.tire_friction = friction
        v.apply_physics_control(physics)

    print(f"Physics applied (friction={friction})")

    # -----------------------------
    # COLLISION SENSOR
    # -----------------------------
    collision_flag = {"ego": False}

    def collision_callback(event):
        collision_flag["ego"] = True
        print("💥 Collision detected")

    collision_sensor = world.spawn_actor(
        blueprint_library.find('sensor.other.collision'),
        carla.Transform(),
        attach_to=ego_vehicle
    )

    collision_sensor.listen(collision_callback)

    ego_logger = DataLogger(f'data/results/s01_ego_{condition}.csv')
    lead_logger = DataLogger(f'data/results/s01_lead_{condition}.csv')

    spectator = world.get_spectator()
    world.tick()

    # -----------------------------
    # DRIVE PHASE
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

    print("Cruising at 50 km/h")

    # -----------------------------
    # LEAD BRAKES
    # -----------------------------
    lead_vehicle.apply_control(carla.VehicleControl(brake=1.0))
    print("Lead braking")

    # -----------------------------
    # AEB LOGIC (TIGHTENED)
    # -----------------------------
    delay_frames = int(reaction_time / settings.fixed_delta_seconds)

    detected = False
    delay_counter = 0
    ego_braking = False

    for _ in range(120):
        world.tick()

        ttc = compute_ttc(ego_vehicle, lead_vehicle)

        # 🔥 tighter detection
        if ttc < 2.6 and not detected:
            detected = True
            delay_counter = delay_frames
            print(f"Object detected (TTC={ttc:.2f}s)")

        if detected and delay_counter > 0:
            delay_counter -= 1

        elif detected and not ego_braking:
            ego_vehicle.apply_control(
                carla.VehicleControl(throttle=0.0, brake=1.0)
            )
            ego_braking = True
            print("AEB activated")

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
    # RESULT
    # -----------------------------
    if collision_flag["ego"]:
        print("❌ Collision occurred")
    else:
        print("✅ No collision")

    collision_sensor.stop()
    collision_sensor.destroy()

    ego_logger.close()
    lead_logger.close()

    settings.synchronous_mode = False
    world.apply_settings(settings)

    ego_vehicle.destroy()
    lead_vehicle.destroy()

    print("Scenario complete")


if __name__ == '__main__':
    condition = sys.argv[1] if len(sys.argv) > 1 else 'dry_day'
    run_scenario_01(condition)