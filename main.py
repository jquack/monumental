import os
import json

from src.utils import load_video, load_calibration_data, get_D_and_K_from_calibration, get_last_frame, get_X_frames
from src.april_tag import detect_april_tag_in_frame
from src.tag_graph import TagGraph
from src.geometry import calculate_tag_corners, get_center_from_corners
from src.visualization import plot_tags, plot_tags_2d

#1 TODO: load video and camera calibration file
#3 TODO: detect april tags in video
#2 TODO: correct video against calibration
#  TODO: make a tree on how tags are connected
#4 TODO: calculate relative positons of april tags to each other for each frame
#5 TODO: fuse the data to make a coherent map
#6 TODO: add some random fun stuff when still motivated

def main():
    
    origin_tag          = 3 # let's use this as an origin
    tag_size            = 0.042 # meter
    video_path          = "data/plantage_shed.mp4"
    calibration_path    = "data/cam.json"
    output_file         = "tag_positions.json"
    test_tags           = [2,39]
    
    detected_tags       = []
    
    ## Load data
    video               = load_video(video_path)
    print(f".. loaded video from {video_path}")
    calibration_data    = load_calibration_data(calibration_path)
    K, D, fx, fy, cx, cy = get_D_and_K_from_calibration(calibration_data) 
    print(f".. loaded calibration data from {calibration_path}")
    # print(f"Calibration Data: \n{calibration_data}")
    # print(f"K: {K}\nD: {D}")
    
    ## Open video and detect tags
    print(f".. reading tags from video")
    # Select only a subset of frames from the video for effiency
    # TODO: make faster and use all frames
    frames = []
    ret, first_frame = video.read()
    frames.append(first_frame)
    last_frame = get_last_frame(video_path)
    frames.append(last_frame)
    for frame in get_X_frames(video_path=video_path, number_of_frames=3):
        frames.append(frame) #TODO: don't; also why doesn't it work with even numbers?
    for frame in frames:
        detected_tags.append(detect_april_tag_in_frame(frame=frame, 
                                                tag_standard="tagStandard52h13",
                                                K=K, D=D, fx=fx, fy=fy, cx=cx, cy=cy,
                                                tag_size=tag_size))

    ## Create a graph and find shortest path to origin tag
    print(f".. calculate tag positions")
    
    # Initialize the graph
    tag_graph = TagGraph()
    # Add new nodes for every frame
    for index, tag_collection in enumerate(detected_tags):
        tag_graph.add_frame(detected_tags=tag_collection, 
                            frame_index=index)

    ## Get shotest paths from all tags to the origin tag
    paths = tag_graph.get_paths_to_origin(origin_tag)
    # print(paths)
    
    ## Calculate position in reference to the origin tag based on shortest path
    tag_positions = []
    for tag_id, path in paths.items():
        tag_positions.append(calculate_tag_corners(tag_collection=detected_tags, 
                                                                path=path,
                                                                tag_size_mm=tag_size*1000))
        # if tag_id in test_tags:
        #     center = get_center_from_corners(corners=corners)
        #     distance = np.linalg.norm(center)
        #     print(f"Test tag {tag_id} distance from origin tag {origin_tag}: {distance}mm")
            
        
    # Save to JSON
    with open(output_file, 'w') as f:
        json.dump(tag_positions, f, indent=2)
    print(f".. results saved in {output_file}")

    # # Vizualize in 3D for debugging purposes
    # fig = plot_tags(tag_data=tag_positions)
    # fig.show()
    
    fig = plot_tags_2d(tag_data=tag_positions)
    fig.show()
        

if __name__ == "__main__":
    main()