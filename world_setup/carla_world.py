import carla
client= carla.Client('localhost',2000)
client.set_timeout(15.0)
world=client.get_world()
print(f"connected to CARLA. MAP : {world.get_map().name}")