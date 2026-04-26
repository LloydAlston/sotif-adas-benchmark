import csv
import os


class DataLogger:
    def __init__(self, filename):
        # open the CSV file and write the header row
        self.file = open(filename, mode='w', newline='')
        self.writer = csv.writer(self.file)

        self.writer.writerow([
            'frame',
            'timestamp',
            'vehicle_x', 'vehicle_y', 'vehicle_z',
            'velocity_kmh',
            'acceleration',
            'throttle', 'brake', 'steer'
        ])

    def log(self, world, vehicle):
        # collect data from simulation and write one row
        snapshot = world.get_snapshot()
        frame = snapshot.frame
        timestamp = snapshot.timestamp.elapsed_seconds

        transform = vehicle.get_transform()
        velocity = vehicle.get_velocity()
        accel = vehicle.get_acceleration()
        control = vehicle.get_control()

        speed_kmh = 3.6 * (velocity.x**2 + velocity.y**2 + velocity.z**2) ** 0.5
        accel_mag = (accel.x**2 + accel.y**2 + accel.z**2) ** 0.5

        self.writer.writerow([
            frame,
            timestamp,
            transform.location.x,
            transform.location.y,
            transform.location.z,
            speed_kmh,
            accel_mag,
            control.throttle,
            control.brake,
            control.steer
        ])

    def close(self):
        # close the file
        self.file.close()