#!/usr/bin/env python
'''Linear interpolation using Optical Flow.
'''

import numpy as np
import cv2
if __debug__:
    import time
import logging
LOGGING_FORMAT = "(%(levelname)s) %(module)s: %(message)s"
logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO)

def read_image(filename:str) -> np.ndarray:
    image = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    return image

def write_image(filename:str, image: np.ndarray) -> None:
    cv2.imwrite(filename, image)

OF_LEVELS = 3
OF_WINDOW_SIDE = 33
OF_ITERS = 3
OF_POLY_N = 5
OF_POLY_SIGMA = 1.2

def estimate(
        predicted_image:np.ndarray,
        reference_image:np.ndarray,
        initial_flow:np.ndarray=None,
        levels:int = OF_LEVELS,
        wside:int = OF_WINDOW_SIDE,
        iters:int = OF_ITERS,
        poly_n:float = OF_POLY_N,
        poly_sigma:float = OF_POLY_SIGMA) -> np.ndarray:
    
    flow = cv2.calcOpticalFlowFarneback(
        prev=predicted_image,
        next=reference_image,
        flow=initial_flow,
        pyr_scale=0.5,
        levels=levels,
        winsize=wside,
        iterations=iters,
        poly_n=poly_n,
        poly_sigma=poly_sigma,
        flags=cv2.OPTFLOW_USE_INITIAL_FLOW | \
              cv2.OPTFLOW_FARNEBACK_GAUSSIAN)
    return flow

def make_prediction(reference_image:np.ndarray,
                    flow:np.ndarray) -> np.ndarray:
    
    height, width = flow.shape[:2]
    map_x = np.tile(np.arange(width), (height, 1))
    map_y = np.swapaxes(np.tile(np.arange(height), (width, 1)), 0, 1)
    map_xy = (flow + np.dstack((map_x, map_y))).astype('float32')
    return cv2.remap(src = reference_image,
                     map1 = map_xy,
                     map2 = None,
                     interpolation = cv2.INTER_LINEAR,
                     borderMode = cv2.BORDER_CONSTANT)

N_DIGITS = 3
EXTENSION_LENGTH = 3
def compose_filename(images, index):
    prefix = images.split('%')[0]
    enumeration_digits = \
        images.split('%')[1][-(N_DIGITS + EXTENSION_LENGTH + 1):]\
        [0:N_DIGITS]
    extension = images[-N_DIGITS:]
    filename = f"{prefix}{index:{enumeration_digits}}.{extension}"
    return filename

def linear_OF_interpolation(
        #input_prefix:str,
        #output_prefix:str,
        #enumeration_digits:int,
        #extension:str,
        images:str,
        first_image:int,
        N_images:int,
        I_factor:int,
        levels:int,
        wside:int,
        iters:int) -> None:
    
    for i in range(first_image, first_image + N_images // I_factor):
        prev_image_index = i * I_factor
        next_image_index = (i+1) * I_factor
        prev_image_filename = \
            compose_filename(images, prev_image_index)
        logging.info(f"reading image \"{prev_image_filename}\"")
        next_image_filename = \
            compose_filename(images, next_image_index)
        logging.info(f"reading image \"{next_image_filename}\"")
        prev_image = read_image(prev_image_filename)
        next_image = read_image(next_image_filename)
        
        for j in range(1, I_factor):
            interpolated_image_index = i * I_factor + j
            prev_image_contribution = \
                (next_image_index - interpolated_image_index) / I_factor
            next_image_contribution = \
                (interpolated_image_index - prev_image_index) / I_factor
            
            forward_flow = np.zeros(
                (next_image.shape[0], next_image.shape[1], 2),
                dtype=np.float32)
            backward_flow = np.zeros(
                (next_image.shape[0], next_image.shape[1], 2),
                dtype=np.float32)
            if __debug__:
                time_0 = time.process_time()
            forward_flow = estimate(
                predicted_image = next_image,
                reference_image = prev_image,
                initial_flow = forward_flow,
                levels = levels,
                wside = wside,
                iters = iters)
            backward_flow = estimate(
                predicted_image = prev_image,
                reference_image = next_image,
                initial_flow = backward_flow,
                levels = levels,
                wside = wside,
                iters = iters)
            prev_prediction = \
                make_prediction(reference_image = prev,
                                flow = forward_flow*next_image_contribution)
            next_prediction = \
                make_prediction(reference_image = next,
                                flow = backward_flow*prev_image_contribution)
            interpolation_image = \
                (prev_prediction * prev_image_contribution + \
                 next_prediction * next_image_contribution).astype(np.uint8)
            if __debug__:
                time_1 = time.process_time()
                logging.info(f"CPU time =", time_1 - time_0)
            output_file_name = \
                compose_filename(images, interpolated_image_index)
            logging.info("writting image \"{interpolated_image_index}\"")
            write_image(interpolation_image, output_file_name)

def rename_images(images:str, N_images:int, I_factor:int) -> None:
    for i in range(N_images - 1, -1, -1):
        old_image_filename = compose_filename(images, i)
        new_image_filename = compose_filename(images, i * I_factor)
        logging.info(f"renaming {old_image_filename} to {new_image_filename}")
        #os.rename(f"old_image_filename}",
        #          f"/tmp/{new_image_filename}")

import argparse

def int_or_str(text):
    '''Helper function for argument parsing.'''
    try:
        return int(text)
    except ValueError:
        return text

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-i", "--images", type=int_or_str,
                    help="Input images filename template",
                    default="./img_%03d.tif")
parser.add_argument("-f", "--interpolation_factor", type=int_or_str,
                    help="Interpolation factor",
                    default=2)
parser.add_argument("-n", "--number_of_images", type=int_or_str,
                    help="Number of input images",
                    default=2)

if __name__ == "__main__":
    parser.description = __doc__
    args = parser.parse_known_args()[0]
    image = args.images
    N_images = args.number_of_images
    I_factor = args.interpolation_factor
    rename_images(images, N_images, I_factor)
    linear_OF_interpolation(
        images = args.images,
        first_image = 0,
        N_images = N_images,
        I_factor = args.interpolation_factor,
        levels = OF_LEVELS,
        wside = OF_WINDOW_SIDE,
        iters = OF_ITERS)
