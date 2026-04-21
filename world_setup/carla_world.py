import carla
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

