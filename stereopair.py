# Utility to convert a directory of individual image pairs into a single image
# for each pair that contains two images, left and right, for use with a stereo viewer
# such as this one:  https://shop.londonstereo.com/OWL-B-ENV.html

import os
from PIL import Image

# Configuration
dirname = '/Users/sdeibel/Desktop/garden-stereo-experiment'
suffix = '.JPG'
result_dir = os.path.join(dirname, 'stereo')
kSpacing = 20
kTargetSize = 600

if not os.path.exists(result_dir):
  os.mkdir(result_dir)  

# Create list of image pairs; assumes they are in order by name
files = [fn for fn in os.listdir(dirname) if fn.endswith(suffix)]
files.sort()
pairs = []
curr_pair = []
for fn in files:
  curr_pair.append(fn)
  if len(curr_pair) == 2:
    pairs.append(tuple(curr_pair))
    curr_pair = []
assert not curr_pair

# Process each pair
for pair_num, pair in enumerate(pairs):

  # Read the two images
  images = []
  for fn in pair:
    fn = os.path.join(dirname, fn)
    images.append(Image.open(fn))
  widths, heights = zip(*(i.size for i in images))

  # Crop images to square, using the center of the image
  if widths[0] > heights[0]:
    diff = int((widths[0] - heights[0]) / 2)
    crop_area = (diff, 0, widths[0] - diff - 1, heights[0] - 1)
  elif heights[0] > widths[0]:
    diff = int((heights[0] - widths[0]) / 2)
    crop_area = (0, diff, widths[0] - 1, heights[0] - diff - 1)
  else:
    crop_area = None

  if crop_area is not None:
    for i in range(0, len(images)):
      images[i] = images[i].crop(crop_area)
    widths, heights = zip(*(i.size for i in images))

  # Resize images to the target size so they are the right size on screen
  # (for print, this would be left at higher resolution)
  for i in range(0, len(images)):
    images[i] = images[i].resize((kTargetSize, kTargetSize), Image.ANTIALIAS)
  widths, heights = zip(*(i.size for i in images))

  # Build the combined image and write it to disk
  total_width = sum(widths)
  max_height = max(heights)
  new_im = Image.new('RGB', (total_width+kSpacing, max_height))
  
  x_offset = 0
  for im in images:
    new_im.paste(im, (x_offset,0))
    x_offset += im.size[0] + kSpacing
    
  result_fn = os.path.join(result_dir, 'stereo%i.png' % (pair_num+1))
  new_im.save(result_fn, dpi=(1200, 1200))
  
