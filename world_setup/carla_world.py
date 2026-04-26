import carla
import time


def get_weather(condition):
    if condition == 'dry_day':
        return carla.WeatherParameters(
            cloudiness=10.0,
            precipitation=0.0,
            precipitation_deposits=0.0,
            wind_intensity=5.0,
            sun_altitude_angle=70.0,
            fog_density=0.0,
            fog_distance=100.0,
            wetness=0.0
        )

    elif condition == 'wet_night':
        return carla.WeatherParameters(
            cloudiness=80.0,
            precipitation=60.0,
            precipitation_deposits=70.0,
            wind_intensity=30.0,
            sun_altitude_angle=-30.0,
            fog_density=20.0,
            fog_distance=50.0,
            wetness=80.0
        )

    elif condition == 'heavy_rain':
        return carla.WeatherParameters(
            cloudiness=100.0,
            precipitation=100.0,
            precipitation_deposits=100.0,
            wind_intensity=60.0,
            sun_altitude_angle=60.0,
            fog_density=40.0,
            fog_distance=30.0,
            wetness=100.0
        )

    elif condition == 'fog_light':
        return carla.WeatherParameters(
            cloudiness=50.0,
            precipitation=0.0,
            precipitation_deposits=20.0,
            wind_intensity=5.0,
            sun_altitude_angle=40.0,
            fog_density=30.0,
            fog_distance=10.0,
            wetness=40.0
        )

    elif condition == 'fog_heavy':
        return carla.WeatherParameters(
            cloudiness=70.0,
            precipitation=0.0,
            precipitation_deposits=40.0,
            wind_intensity=10.0,
            sun_altitude_angle=30.0,
            fog_density=80.0,
            fog_distance=5.0,
            wetness=60.0
        )

    else:
        print("Unknown condition, defaulting to clear")
        return carla.WeatherParameters()


def setup_world():
    client = carla.Client('localhost', 2000)
    client.set_timeout(15.0)

    world = client.get_world()
    print(f"Connected to CARLA. MAP: {world.get_map().name}")

    world.set_weather(get_weather('dry_day'))
    print("Weather set: dry day")

    blueprint_library = world.get_blueprint_library()
    vehicle_bp = blueprint_library.find('vehicle.tesla.model3')

    spawn_points = world.get_map().get_spawn_points()
    ego_vehicle = world.spawn_actor(vehicle_bp, spawn_points[3])
    print(f"Ego vehicle spawned: {ego_vehicle.type_id}")

    time.sleep(2)

    spectator = world.get_spectator()
    transform = ego_vehicle.get_transform()
    spectator.set_transform(carla.Transform(
        transform.location + carla.Location(x=-8, z=4),
        carla.Rotation(pitch=-15)
    ))

    time.sleep(5)

    camera_bp = blueprint_library.find('sensor.camera.rgb')
    camera_bp.set_attribute('image_size_x', '1280')
    camera_bp.set_attribute('image_size_y', '720')

    camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
    camera = world.spawn_actor(camera_bp, camera_transform, attach_to=ego_vehicle)

    print("Camera attached to ego vehicle")

    def on_image(image):
        print(f"Frame {image.frame} | Timestamp: {image.timestamp:.2f}s | Resolution: {image.width}x{image.height}")

    camera.listen(on_image)

    time.sleep(5)

    print("5 seconds of camera data captured")

    camera.stop()
    camera.destroy()
    ego_vehicle.destroy()

    print("Simulation ended, actors destroyed")


if __name__ == "__main__":
    setup_world()