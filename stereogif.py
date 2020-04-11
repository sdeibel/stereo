# Simple experiment to combined two images into an oscillating gif, as a way to
# see how they perform in stereo without needing a viewer

# Mostly abandoned this idea, as the image separation needs to be smaller for
# these than for a combined stereo pair that is used with a viewer.

import os
import imageio

dirname = '/Users/sdeibel/Desktop/garden-stereo-experiment'
filenames = [
  'DSCN4663.jpg',
  'DSCN4664.jpg',
]

images = []
for filename in filenames:
  filename = os.path.join(dirname, filename)
  images.append(imageio.imread(filename))

imageio.mimsave('/Users/sdeibel/Desktop/movie5.gif', images, duration=0.10)
