from moms_apriltag import TagGenerator3
from matplotlib import pyplot as plt

# Initialize the TagGenerator
tg = TagGenerator3(name="tagStandard52h13")

# Generate 4 tags with different IDs
tag_ids = [2, 3, 39, 140]
tags = [tg.generate(tag_id=tag_id) for tag_id in tag_ids]

# Set the dimensions: each tag is 42mm wide, and we add a 27mm margin between them
tag_width_mm = 42
margin_mm = 27

# Convert mm to inches for matplotlib (1 inch = 25.4 mm)
tag_width_in = tag_width_mm / 25.4
margin_in = margin_mm / 25.4

# Calculate the total figure size
fig_width_in = (2 * tag_width_in) + (margin_in)
fig_height_in = (2 * tag_width_in) + (margin_in)

# Create a figure with the calculated dimensions
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(fig_width_in, fig_height_in))

# Plot each tag in the grid with margins
for i, ax in enumerate(axs.flatten()):
    ax.imshow(tags[i], cmap="gray")
    ax.set_title(f"Tag ID: {tag_ids[i]}")
    ax.axis("off")

# Adjust layout with the required spacing (margins)
plt.subplots_adjust(wspace=margin_in/tag_width_in, hspace=margin_in/tag_width_in)

# Save the plot as a PNG file
plt.savefig("tags_2x2_test_grid.png")
plt.show()
