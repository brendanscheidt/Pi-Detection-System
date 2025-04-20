from detection_system import DetectionSystem

if __name__ == "__main__":
    detection_system = DetectionSystem(name="Front Door")
    detection_system.set_max_distance(600)
    detection_system.set_trigger_threshold(30)
    detection_system.run()