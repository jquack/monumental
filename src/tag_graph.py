from collections import defaultdict
import heapq

class TagGraph:
    def __init__(self):
        # Graph representation: each tag ID points to a list of tuples (connected_tag_id, frame_index)
        self.graph = defaultdict(list)
    
    def add_frame(self, detected_tags, frame_index):
        # Add edges between all tags detected in the same frame
        tag_ids = [tag.tag_id for tag in detected_tags]
        
        for i in range(len(tag_ids)):
            for j in range(i + 1, len(tag_ids)):
                tag1, tag2 = tag_ids[i], tag_ids[j]
                self.graph[tag1].append((tag2, frame_index))
                self.graph[tag2].append((tag1, frame_index))
                
    def get_paths_to_origin(self, origin_tag):
        # Use Dijkstra's algorithm to find the shortest path from every tag to the origin tag
        paths = {}
        
        for tag in self.graph:
            if tag == origin_tag:
                paths[origin_tag] = [origin_tag]
            else:
                shortest_path, path_distance = self.dijkstra_shortest_path(tag, origin_tag)
                paths[tag] = shortest_path
        return paths
    

    def dijkstra_shortest_path(self, start_tag, end_tag):
        """
        Finds the shortest path between two tags (start_tag and end_tag)
        
        The function returns a list of tuples, where each tuple contains:
        - The start node (tag ID) of the edge.
        - The end node (tag ID) of the edge.
        - The frame index where the edge (connection between the two nodes) was detected.
        
        It also returns the total distance (in terms of the number of edges) between the start and end tags.

        Args:
        - start_tag (int): The tag ID of the starting node.
        - end_tag (int): The tag ID of the ending node.

        Returns:
        - path (list of tuples): The shortest path from start_tag to end_tag, including frame indexes.
        - path_distance (int): The total distance of the path.
        """
        pq = []  # Priority queue to store (cost, node)
        weight = 1
        
        heapq.heappush(pq, (0, start_tag))
        distances = {start_tag: 0}
        previous_nodes = {start_tag: None}
        edge_indexes = {}  # Track the frame index for each edge
        
        while pq:
            current_distance, current_tag = heapq.heappop(pq)
            
            if current_tag == end_tag:
                break  # Found the shortest path
            
            for neighbor, frame_index in self.graph[current_tag]:
                distance = current_distance + weight
                if neighbor not in distances or distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))
                    previous_nodes[neighbor] = current_tag
                    edge_indexes[(current_tag, neighbor)] = frame_index
        
        # Reconstruct the path from start_tag to end_tag, including the frame indexes
        # So we can find it back to calculate the transformation matrices
        path = []
        current_node = end_tag
        while current_node is not None:
            prev_node = previous_nodes[current_node]
            if prev_node is not None:
                frame_index = edge_indexes[(prev_node, current_node)]
                path.append((prev_node, current_node, frame_index))
            current_node = prev_node
        
        path.reverse() #TODO: fix also down in the code
        
        return path, distances.get(end_tag, float('inf'))