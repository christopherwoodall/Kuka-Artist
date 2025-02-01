from pathlib import Path
import cv2
import numpy as np
import matplotlib.pyplot as plt


def outline_image(image_path, output_path):
  # Read image in grayscale
  img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)

  if img is None:
    raise ValueError(f"Could not load image at {image_path}")

  blurred = cv2.GaussianBlur(img, (5, 5), 0)

  # _, thresh = cv2.threshold(
  #   blurred, 128, 255, cv2.THRESH_BINARY_INV
  # )

  t_lower = 100
  t_upper = 200
  aperture_size = 3
  L2Gradient = True
  edges = cv2.Canny(blurred, t_lower, t_upper, L2gradient = L2Gradient )

  inverted_edges = cv2.bitwise_not(edges)

  # TODO: Remove this line (or add argparse option to control saving)
  cv2.imwrite(output_path, inverted_edges)

  return inverted_edges


def project_image_to_canvas(image_data, canvas_size_inches=(8.5, 11), dpi=300, orientation="landscape"):

  if orientation == "landscape":
    canvas_width, canvas_height = canvas_size_inches
    canvas_width_px = int(canvas_height * dpi)
    canvas_height_px = int(canvas_width * dpi)
  else:
    canvas_width, canvas_height = canvas_size_inches
    canvas_width_px = int(canvas_width * dpi)
    canvas_height_px = int(canvas_height * dpi)

  canvas = np.ones((canvas_height_px, canvas_width_px), dtype=np.uint8) * 255

  # Center image on canvas
  image_height, image_width = image_data.shape
  image_center_x = canvas_width_px // 2
  image_center_y = canvas_height_px // 2

  image_x_start = image_center_x - image_width // 2
  image_y_start = image_center_y - image_height // 2

  canvas[
    image_y_start : image_y_start + image_height,
    image_x_start : image_x_start + image_width,
  ] = image_data

  inverted_canvas = cv2.bitwise_not(canvas)

  # TODO: Remove this line (or add argparse option to control saving)
  cv2.imwrite("canvas.png", canvas)
  return canvas


def generate_contour_points(image_data):
  inverted_canvas = cv2.bitwise_not(image_data)
  contours, _ = cv2.findContours(inverted_canvas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  contour_points = []
  for contour in contours:
    squeezed_contour = contour.squeeze()

    # Invert the y-coordinates because OpenCV uses a different coordinate system
    inverted_y = image_data.shape[0] - squeezed_contour[:, 1]

    # Create a new array with inverted y-coordinates
    inverted_contour = np.column_stack((squeezed_contour[:, 0], inverted_y))
    contour_points.append(inverted_contour)

  return contour_points


def plot_contours(contours):
  fig, ax = plt.subplots()
  for contour in contours:
    x, y = contour.T
    ax.plot(x, y)

  # Save plot to file
  plt.savefig("contour_plot.png")


def write_contours_to_txt(contour_points, output_filepath):
  with open(output_filepath, 'w') as f:
    for contour in contour_points:
      for point in contour:
        x, y = point
        f.write(f"{x}, {y}\n")


def main():
  # TODO: Add argparse to accept image path as input

  image_file = Path("./data/Lenna_(test_image).png")
  output_file = Path("./image_outline.png")

  outline = outline_image(image_file, output_file)

  canvas = project_image_to_canvas(outline)

  contours = generate_contour_points(canvas)
  plot_contours(contours)

  output_txt_filepath = Path("./contours.txt")
  write_contours_to_txt(contours, output_txt_filepath)

if __name__ == "__main__":
    main()
