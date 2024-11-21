import os
import cv2
import gc
import pymupdf  # PyMuPDF # type: ignore
from pdf2image import * # type: ignore
import numpy as np # type: ignore
from skimage import io # type: ignore
from PIL import Image # type: ignore
Image.MAX_IMAGE_PIXELS = None


# # Helper function to check if a pixel is within the purplish-gray RGB range
# def select_pixel(img_array):
#     # Create masks for the purplish-gray color range
#     mask = (
#         (img_array[:, :, 0] > 120) & (img_array[:, :, 0] < 180) &  # Red channel
#         (img_array[:, :, 1] > 100) & (img_array[:, :, 1] < 160) &  # Green channel
#         (img_array[:, :, 2] > 120) & (img_array[:, :, 2] < 180)    # Blue channel
#     )
#     return mask

# # Helper function to check if a pixel is within the light grayish RGB range
# def select_pixel1(img_array):
#     # Create masks for the light grayish color range
#     mask = (
#         (img_array[:, :, 0] > 175) & (img_array[:, :, 0] < 250) &  # Red channel
#         (img_array[:, :, 1] > 175) & (img_array[:, :, 2] > 175) &  # Green and Blue channels
#         (img_array[:, :, 2] < 250)
#     )
#     return mask

# # Function to handle and modify image pixels using vectorized operations
# def handle(img_array):
#     # First pass: Remove the purplish-gray watermark
#     mask1 = select_pixel(img_array)
#     img_array[mask1] = [255, 255, 255]  # Set to white
#     print("Purplish-gray layer removed")

#     # Second pass: Remove the light grayish watermark
#     mask2 = select_pixel1(img_array)
#     img_array[mask2] = [255, 255, 255]  # Set to white
#     print("Light grayish layer removed")

#     return img_array


# Helper function to check if a pixel is within a wider black color range
# # Function to handle and modify image pixels
# def handle(img_array):
#     # Create a mask for pixels that match the wider black text color range
#     text_mask = is_text_color(img_array)
    
#     # Set all pixels that are not part of the black text color to white
#     img_array[~text_mask] = [255, 255, 255]  # Set to white
#     print("All non-black colors removed, wider range applied to retain thinner text")

#     return img_array
  
# # Function to remove image watermarks from the PDF using PyMuPDF
# def remove_image_watermarks(file_path):
#     try:
#         doc = pymupdf.open(file_path)

#         # Iterate through each page and remove images that are likely watermarks
#         for page_num in range(doc.page_count):
#             page = doc.load_page(page_num)
#             image_list = page.get_images(full=True)
#             for image in image_list:
#                 xref = image[0]  # Image reference number
#                 page.delete_image(xref)

#         # Save the PDF with image watermarks removed
#         output_pdf_path = file_path.replace(".pdf", "_no_image_watermark.pdf")
#         doc.save(output_pdf_path)
#         print("Image watermarks removed. Modified PDF saved.")
        
#         return output_pdf_path
#     except Exception as e:
#         print(f"Error: {e}")
#         return None

# Helper function to check if a pixel is within a wider black color range in RGB
def is_text_color_rgb(img_array):
    # Widen the range to accommodate thinner or lighter black text
    mask = (
        (img_array[:, :, 0] < 140) &  # Red channel threshold increased
        (img_array[:, :, 1] < 140) &  # Green channel threshold increased
        (img_array[:, :, 2] < 140)    # Blue channel threshold increased
    )
    return mask

# Helper function to check if a pixel is black-like in HSV
def is_text_color_hsv(img_array):
    # Convert the RGB image to HSV
    hsv_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)

    # Create a mask for low saturation (black or near-black colors)
    # Hue doesn't matter for black, so we focus on saturation and value
    # Dark Red
    # mask = (hsv_img[:, :, 1] < 40) & (hsv_img[:, :, 2] < 180)
    # QR Code
    # mask = (hsv_img[:, :, 1] < 35) & (hsv_img[:, :, 2] < 155)
    # QR Code & Red Text
    mask = (hsv_img[:, :, 1] < 40) & (hsv_img[:, :, 2] < 160)
    return mask

# Function to handle and modify image pixels using both RGB and HSV checks
def handle(img_array):
    # Create masks using both RGB and HSV checks
    text_mask_rgb = is_text_color_rgb(img_array)
    text_mask_hsv = is_text_color_hsv(img_array)

    # Combine both masks to get the final text mask
    text_mask = text_mask_rgb | text_mask_hsv

    # Set all pixels that are not part of the black text color to white
    img_array[~text_mask] = [255, 255, 255]  # Set to white
    print("All non-black and dark red colors removed, combined RGB and HSV filtering applied")

    return img_array

# Function to remove layer-based watermarks (OCGs)
def remove_layer_watermarks(file_path):
    try:
        doc = pymupdf.open(file_path)
        ocgs = doc.get_ocgs()  # Get the list of all Optional Content Groups (layers)
        print(ocgs)

        if ocgs:
          print("Found layers in the PDF.")
          for ocg in ocgs:
              names = ocgs[ocg]  # Get the details dictionary
              details = doc.xref_object(ocg, compressed=True)
              name = names.get('name', 'Unnamed Layer')  # Extract the 'name' field
              print(f"Layer xref: {ocg}, Name: {name}")
              
              if "watermark" or "background" in str(name).lower():
                print(f"Disabling watermark layer: {name}")
                doc.set_layer(-1, on=None, off=[ocg])
                
              elif "background" in str(name).lower():
                print(f"Disabling watermark layer: {name}")
                doc.set_layer(-1, on=None, off=[ocg])
                

        # Save the PDF with layer watermarks removed
        output_pdf_path = file_path.replace(".pdf", "_no_layer_watermark.pdf")
        doc.save(output_pdf_path)
        print("Layer watermarks removed. Modified PDF saved.")
  
        return output_pdf_path
    except Exception as e:
        print(f"Error: {e}")
        return None


# Main function to remove both text-based, image-based, and layer-based watermarks
def remove_watermark_from_pdf(file_path):
    try:
        print("Starting watermark removal (Optimized).")

        # Create a temporary folder to store modified images
        temp_dir = "./temp_images"
        os.makedirs(temp_dir, exist_ok=True)

        # Step 1: Incremental processing of PDF pages
        page_num = 0
        modified_images = []
        for img in convert_from_path(file_path, dpi=450, grayscale=False, fmt="jpeg", thread_count=os.cpu_count() * 2):
            page_num += 1

            # Convert PIL image to NumPy array
            img_array = np.array(img)

            # Apply watermark removal logic
            img_array = handle(img_array)

            # Save processed image immediately
            output_image_path = os.path.join(temp_dir, f"modified_page_{page_num}.jpg")
            io.imsave(output_image_path, img_array, quality=80)  # Save with compression
            modified_images.append(output_image_path)

            print(f"Processed page {page_num}, shape: {img_array.shape}")

            # Free memory
            del img_array
            gc.collect()

        # Step 2: Merge processed images into a single PDF incrementally
        final_pdf_path = file_path.replace(".pdf", "_no_watermark.pdf")
        with Image.open(modified_images[0]).convert("RGB") as first_image:
            first_image.save(final_pdf_path, save_all=True, append_images=[
                Image.open(img_path).convert("RGB") for img_path in modified_images[1:]
            ])
        print("Text-based watermarks removed. Final modified PDF saved.")

        # Step 3: Delete temporary images
        for image_path in modified_images:
            try:
                os.remove(image_path)
                print(f"Deleted {image_path}")
            except Exception as e:
                print(f"Error deleting {image_path}: {e}")

        os.rmdir(temp_dir)  # Remove temporary directory

        return final_pdf_path

    except Exception as e:
        print(f"Error: {e}")
        return None
    