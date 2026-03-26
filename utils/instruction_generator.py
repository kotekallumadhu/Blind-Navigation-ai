def generate_instruction(detections, image_width=640, image_height=480):
    """
    Generate navigation instruction from object detections.
    :param detections: List of detected objects
    :param image_width: Width of the image
    :param image_height: Height of the image
    :return: Instruction string
    """
    if not detections:
        return "Path clear."

    # Simple logic: check for obstacles in center
    center_x = image_width / 2
    center_threshold = image_width * 0.3  # 30% of width

    obstacles_ahead = []
    for det in detections:
        x1, y1, x2, y2 = det['bbox']
        center_obj = (x1 + x2) / 2
        if abs(center_obj - center_x) < center_threshold and y2 > image_height * 0.5:  # In lower half
            obstacles_ahead.append(det['class'])

    if obstacles_ahead:
        return f"Obstacle ahead: {', '.join(set(obstacles_ahead))}. Move left or right."

    # Check sides
    left_obstacles = [d['class'] for d in detections if d['bbox'][0] < center_x - center_threshold]
    right_obstacles = [d['class'] for d in detections if d['bbox'][2] > center_x + center_threshold]

    instructions = []
    if left_obstacles:
        instructions.append(f"Objects on left: {', '.join(set(left_obstacles))}")
    if right_obstacles:
        instructions.append(f"Objects on right: {', '.join(set(right_obstacles))}")

    if instructions:
        return ". ".join(instructions) + "."

    return "Path clear."