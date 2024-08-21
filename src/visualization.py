# src/visualization.py

import cv2

import plotly.graph_objects as go

def plot_tags(tag_data):
    """
    Plots all the tags as rectangles with their ID numbers inside using Plotly.
    
    Args:
    - tag_data (list of dicts): A list where each element is a dictionary containing:
        - 'id': The ID of the tag.
        - 'corners': The positions of the four corners of the tag in the format:
            [
                [x1, y1, z1],  # Top-left corner
                [x2, y2, z2],  # Top-right corner
                [x3, y3, z3],  # Bottom-right corner
                [x4, y4, z4]   # Bottom-left corner
            ]
    
    Returns:
    - fig (plotly.graph_objects.Figure): A Plotly figure object with the tags plotted.
    """
    fig = go.Figure()
    print(f"Tag data: {tag_data}")

    for tag in tag_data:
        tag = tag[0] #TODO
        tag_id = tag['id']
        corners = tag['corners']

        # Extract x, y, z coordinates of the corners
        x_coords = [corner[0] for corner in corners] + [corners[0][0]]  # Close the rectangle by adding the first point at the end
        y_coords = [corner[1] for corner in corners] + [corners[0][1]]
        z_coords = [corner[2] for corner in corners] + [corners[0][2]]

        # Plot the rectangle
        fig.add_trace(go.Scatter3d(
            x=x_coords,
            y=y_coords,
            z=z_coords,
            mode='lines',
            line=dict(color='blue', width=2),
            name=f'Tag {tag_id}'
        ))

        # Add the tag ID in the center of the rectangle
        center_x = sum(x_coords[:-1]) / 4
        center_y = sum(y_coords[:-1]) / 4
        center_z = sum(z_coords[:-1]) / 4

        fig.add_trace(go.Scatter3d(
            x=[center_x],
            y=[center_y],
            z=[center_z],
            mode='text',
            text=[str(tag_id)],
            textposition='middle center',
            showlegend=False
        ))

    # Update the layout for better visualization
    fig.update_layout(
        scene=dict(
            xaxis_title='X (mm)',
            yaxis_title='Y (mm)',
            zaxis_title='Z (mm)',
            aspectmode='data'
        ),
        title='3D Tag Plot',
        showlegend=False
    )

    return fig

def plot_tags_2d(tag_data):
    """
    Plots all the tags as rectangles with their ID numbers inside on the X-Y plane using Plotly.
    
    Args:
    - tag_data (list of dicts): A list where each element is a dictionary containing:
        - 'id': The ID of the tag.
        - 'corners': The positions of the four corners of the tag in the format:
            [
                [x1, y1, z1],  # Top-left corner
                [x2, y2, z2],  # Top-right corner
                [x3, y3, z3],  # Bottom-right corner
                [x4, y4, z4]   # Bottom-left corner
            ]
    
    Returns:
    - fig (plotly.graph_objects.Figure): A Plotly figure object with the tags plotted on the X-Y plane.
    """
    fig = go.Figure()
    for tag in tag_data:
        tag = tag[0] #TODO
        tag_id = tag['id']
        corners = tag['corners']

        # Extract x and y coordinates of the corners 
        x_coords = [corner[0] for corner in corners] + [corners[0][0]] 
        y_coords = [corner[1] for corner in corners] + [corners[0][1]]

        # Plot the rectangle on the X-Y plane
        fig.add_trace(go.Scatter(
            x=x_coords,
            y=y_coords,
            mode='lines',
            line=dict(color='blue', width=2),
            name=f'Tag {tag_id}'
        ))

        # Add the tag ID in the center of the rectangle
        center_x = sum(x_coords[:-1]) / 4
        center_y = sum(y_coords[:-1]) / 4

        fig.add_trace(go.Scatter(
            x=[center_x],
            y=[center_y],
            mode='text',
            text=[str(tag_id)],
            textposition='middle center',
            showlegend=False
        ))

    # Update the layout for better visualization
    fig.update_layout(
        xaxis_title='X (mm)',
        yaxis_title='Y (mm)',
        title='2D Projection of Tags on X-Y Plane',
        showlegend=False
    )

    return fig