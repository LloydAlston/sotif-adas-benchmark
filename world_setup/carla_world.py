import carla
import time
client= carla.Client('localhost',2000)
client.set_timeout(15.0)
world=client.get_world()
print(f"connected to CARLA. MAP : {world.get_map().name}")
weather=carla.WeatherParameters(cloudiness=0.0, precipitation=0.0, sun_altitude_angle=70.0)
world.set_weather(weather)
print("Weather set to clear sky, sun high in the sky")
blueprint_library=world.get_blueprint_library()
vehicle_bp=blueprint_library.find('vehicle.tesla.model3')
spawn_points=world.get_map().get_spawn_points()
ego_vehicle=world.spawn_actor(vehicle_bp, spawn_points[0])
print(f"Ego vehicle spawned: {ego_vehicle.type_id}")
spectator = world.get_spectator()
transform = ego_vehicle.get_transform()
spectator.set_transform(carla.Transform(
    transform.location + carla.Location(z=50),
    carla.Rotation(pitch=-90)
))
camera_bp= blueprint_library.find('sensor.camera.rgb')
camera_bp.set_attribute('image_size_x', '1280')
camera_bp.set_attribute('image_size_y', '720')
camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
camera=world.spawn_actor(camera_bp,camera_transform,attach_to=ego_vehicle)
print("Camera attached to ego vehicle")
def on_image(image):
    print(f"Frame {image.frame} | Timestamp: {image.timestamp:.2f}s | Resolution: {image.width}x{image.height}")
camera.listen(on_image)
time.sleep(5)
print("5 seconds of camera data captured")

