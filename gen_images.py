# Program to generate images  

import cv2
from PIL import Image
import numpy as np
import os
import random

def generate_images(input_path, M = 1024, M1 = 1024, num = 1000):
  # N is no of shapes we need to identify
  # M x M1 is dimensions of output image (default 1024x1024), 
  # num is total number of images to be generated (default 100, can take 1000 too)
  # given output image will contain k images of each type
  N,k = 4,10 # reasonable assumptions

  # Define class labels
  class_labels = [0,1,2,3] # EACH FOR ['disc', 'gear', 'hexagon', 'square']
  # or we can use dictionary based approach too class_labels = {'disc':0, 'gear':1, 'hexagon':2, 'square':3}

  # to store data for each image
  samples = []
  labels = []

  for j in range(1, N + 1): # For N shapes
      image_path = f'{input_path}/{j}.jpg' # Reading N images from the input folder assuming images are named as per their type ie disc is named 1.jpg and so on. If not , need to do that before processing here
      sample = cv2.imread(image_path)
      samples.append(sample)
      labels.append(j-1) # Label for the type, ranging from 0 to 3
    
  #creating ground truth labels named gt
  gt = list(zip(samples, labels))

  # setting output dimensions as required
  dim,dim1 = M,M1
  # If wish to take dimensions input , we can use second method as shown - dim = int(input("Enter image dimensions")) # OR 256*(2**(nout+1))

  # Calculating the number of images here 
  n = int(dim/64) # or since M=M1 here we are using either of them, else use samples[0].size[0]
  num_images = k*N # if N = 5 ie 5 shapes and k = 20 ie 20 instances of each type per image , then num_images = 5*20 = 100
  #num_images = int(input("Enter number of images needed: \n"))

  # divide the background into grids for better selection of coordinates
  all_dims = [(i * 64,j * 64) for i in range(n) for j in range(n)]

  # start of image generation
  for nout in range(num):
      # making a black background
      bg_image = np.zeros((dim, dim,3), np.uint8)
      # Alternative method => bg_image = Image.new('RGB', out_dims, (5, 5, 5)) or Image.new("RGB", out_dims, "black")

      # Create a list to store the images, positions, and ground truth labels
      image_data = []
      dims = []
      # finding non-overlapping positions
      dims = random.sample(all_dims,num_images)

      for i in range(0, num_images, N):
          for j in range(N):
              # getting x,y coordinate of image  
              x, y = dims[i+j]

              # creating a copy of original data before transformation
              img,label = gt[j] # or samples[j].copy

              # random scaling bw 0.75 to 0.95 , here we not scaling from .75 to 1.0 
              # as latter will lead to shapes overlapping with each other in some cases
              scale_factor = random.uniform(0.75,0.95)
              img = cv2.resize(img,(0,0), fx = scale_factor, fy = scale_factor)

              # random rotation bw 0 to 90 degree
              angle = random.uniform(0,90)
              M = cv2.getRotationMatrix2D((img.shape[1] / 2, img.shape[0] / 2), angle, 1)
              img = cv2.warpAffine(img, M, (img.shape[1],img.shape[0]))

              # Paste the four images at the selected positions
              bg_image[y:y+img.shape[1], x:x+img.shape[0]] = img

              # Getting centroid and width & hieght of image

              x1 = (x+(img.shape[1]//2))/1024 # normalised x coordinate of centroid
              y1 = (y+(img.shape[0]//2))/1024 # normalised y coordinate of centroid

              h = img.shape[0]/1024  # Normalized dimensions Hieght and Width 
              w = img.shape[1]/1024  

              # append the ground truth label
              image_data.append((label,x1,y1,w,h))

      # Saving the file in output directory 
      output_filename = f'generated_images/gen_image_{nout}.png'
      cv2.imwrite(output_filename, bg_image)

      # Save the corresponding annotation file
      with open(f'generated_annotations/gen_annotations_{nout}.txt', 'w') as file:
        for obj in image_data: # reading the annotated data stored as tuples 
          label,x1,y1,w,h = obj # getting (label,centroid x, centroid y,width,height) as tuple
          file.write(f"{label} {x1} {y1} {w} {h}\n")

  print("success")
  return None

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Generate k images of N type')
    parser.add_argument('--input', type=str, required=True, help='Input directory containing sample images')
    parser.add_argument('--out-dims', type=int, nargs=2, required=True, help='Dimensions of output images')
    parser.add_argument('--nout', type=int, required=True, help='Number of output images to generate')

    args = parser.parse_args()
    M, M1 = args.out_dims  # Unpack out_dims into M and M1

    generate_images(args.input, M, M1 , args.nout)