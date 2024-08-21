import numpy as np

def calculate_distance_between_tags(detected_tags, tag_id_1, tag_id_2):
    tag1 = None
    tag2 = None
    
    for tag in detected_tags:
        if tag.tag_id == tag_id_1:
            tag1 = tag
        elif tag.tag_id == tag_id_2:
            tag2 = tag
    
    if tag1 is None or tag2 is None:
        raise ValueError(f"One or both of the tags with ID {tag_id_1} and {tag_id_2} were not found.")
    
    # Extract the center positions in 3D space (pose_t gives x, y, z in meters)
    center1 = np.array(tag1.pose_t).flatten()
    center2 = np.array(tag2.pose_t).flatten()
    
    # # Calculate the distances in each direction
    distance_x = (center2[0] - center1[0]) * 1000  # Distance in x direction (in mm)
    distance_y = (center2[1] - center1[1]) * 1000  # Distance in y direction (in mm)
    distance_z = (center2[2] - center1[2]) * 1000  # Distance in z direction (in mm)
    distance_vector = np.array([distance_x, distance_y, distance_z])
    # print(f"Distance in x, y, z: {distance_x}, {distance_y}, {distance_z}")
    
    # Calculate the Euclidean distance between the two centers
    distance = np.linalg.norm(center2 - center1)
    
    # Convert the distance to millimeters (pose_t is typically in meters)
    distance_mm = distance * 1000
    
    return distance_mm, distance_vector

def calculate_R_and_t_to_origin(tag_collection, path):
    """
    Calculates the relative position and orientation of the end tag in the path relative to the start tag (origin).
    
    Args:
    - tag_collection (list of lists): A list where each element is a list of Detection objects from a frame.
    - path (list of tuples): The path from the origin to the target tag, including frame indexes.
    
    Returns:
    - relative_position (numpy array): The position of the end node relative to the origin in millimeters.
    - relative_rotation (numpy array): The rotation matrix of the end node relative to the origin.
    """
    current_position = np.array([0.0, 0.0, 0.0])  # Start at the origin
    current_rotation = np.eye(3)  # Start with no rotation (identity matrix)
    
    for start_node, end_node, frame_index in path:
        # Get the relevant frame from the tag_collection
        frame = tag_collection[frame_index]
        
        # Find the Detection objects for the start and end nodes in the frame
        start_tag = next(tag for tag in frame if tag.tag_id == start_node)
        end_tag = next(tag for tag in frame if tag.tag_id == end_node)
        
        # Calculate the relative rotation and translation between the start and end tags
        rotation_matrix = np.array(end_tag.pose_R)
        translation_vector = np.array(end_tag.pose_t).flatten() - np.array(start_tag.pose_t).flatten()
        # TODO: this is wrong the camera position changes so eg the z distance changes so this needs to be accounted for
        
        # Transform the translation vector by the current rotation
        transformed_translation = np.dot(current_rotation, translation_vector)
        
        # Update the current position by adding the transformed translation vector
        current_position += transformed_translation * 1000  # Convert to millimeters
        
        # Update the current rotation by applying the relative rotation
        current_rotation = np.dot(current_rotation, rotation_matrix)
    
    return current_position, current_rotation

def calculate_tag_corners(tag_collection, path, tag_size_mm=42.0):
    """
    Calculates the positions of the corners of the tag based on the relative translation and rotation from the origin.
    
    Args:
    - tag_collection (list of lists): A list where each element is a list of Detection objects from a frame.
    - path (list of tuples): The path from the origin to the target tag, including frame indexes.
    - tag_size_mm (float): The size of the tag (length of a side) in millimeters. Default is 42.0 mm.
    
    Returns:
    - tag_data (list of dicts): A list where each element is a dictionary containing the tag ID and the 
        3D positions of its four corners in millimeters.
    """
    tag_data = []
    
    # Define the corners of the tag
    half_size = tag_size_mm / 2.0
    local_corners = np.array([
        [-half_size, half_size, 0],   # Top-left corner
        [half_size, half_size, 0],    # Top-right corner
        [half_size, -half_size, 0],   # Bottom-right corner
        [-half_size, -half_size, 0]   # Bottom-left corner
    ])
    
    # Do coordinate transformation unless it's the origin tag
    if isinstance(path[0], int):
        # Origin Tag doesn't have a path
        global_corners = local_corners
        end_tag_id = path[0]
    else:
        # Calculate the relative rotation and translation for the tag at the end of the path
        relative_position, relative_rotation = calculate_R_and_t_to_origin(tag_collection, path)

        # Calculate the global positions of the corners by applying the rotation and translation
        global_corners = [np.dot(relative_rotation, corner) + relative_position for corner in local_corners]
        
        # Correct the X-axis (flip X coordinates)
        # TODO: don't, fix translation
        global_corners = [[-corner[0], corner[1], corner[2]] for corner in global_corners]
        
        # Get the tag ID for the end tag
        end_tag_id = path[0][0]
    
    # Round
    global_corners = np.round(global_corners, decimals=1)
    
    # Create the tag data dictionary
    tag_data.append({
        "id": end_tag_id,
        "corners": global_corners.tolist()
    })
    
    return tag_data


def get_center_from_corners(corners):
    x_coords = [corner[0] for corner in corners] + [corners[0][0]] 
    y_coords = [corner[1] for corner in corners] + [corners[0][1]]
    z_coords = [corner[2] for corner in corners] + [corners[0][2]] 
    center_x = sum(x_coords[:-1]) / 4
    center_y = sum(y_coords[:-1]) / 4
    center_z = sum(z_coords[:-1]) / 4
    return [center_x, center_y, center_z]


