import os
import cv2 # type: ignore
import gc
import pymupdf  # PyMuPDF # type: ignore
from pdf2image import * # type: ignore
import numpy as np # type: ignore
from skimage import io # type: ignore
from PIL import Image # type: ignore
from PyPDF2 import PdfMerger
import pikepdf

Image.MAX_IMAGE_PIXELS = None

# Helper function to check if a pixel is within a wider black color range in RGB
def is_text_color_rgb(img_array):
    # Widen the range to accommodate thinner or lighter black text
    mask = (
      # Descent WaterMark Preset
        # (img_array[:, :, 0] < 130) &  # Red channel threshold increased
        # (img_array[:, :, 1] < 200) &  # Green channel threshold increased
        # (img_array[:, :, 2] < 200)    # Blue channel threshold increased
        # 25, 190
      # # BrownishGreen WaterMark
      #   (img_array[:, :, 0] < 60) &  # Red channel threshold increased
      #   (img_array[:, :, 1] < 115) &  # Green channel threshold increased
      #   (img_array[:, :, 2] < 200)    # Blue channel threshold increased
        # 30,210
      # # Blue JB WaterMark
      # (img_array[:, :, 0] < 200) &  # Red channel threshold increased
      # (img_array[:, :, 1] < 200) &  # Green channel threshold increased
      # (img_array[:, :, 2] < 175)    # Blue channel threshold increased
      # # 0,250
      # # BADIMAGE WaterMark WITH RED WATERMARK
      # (img_array[:, :, 0] < 175) &  # Red channel threshold increased
      # (img_array[:, :, 1] < 200) &  # Green channel threshold increased
      # (img_array[:, :, 2] < 200)    # Blue channel threshold increased
      
      # GreenishGreen WaterMark
      # (img_array[:, :, 0] < 120) &  # Red channel threshold increased
      # (img_array[:, :, 1] < 120) &  # Green channel threshold increased
      # (img_array[:, :, 2] < 120)    # Blue channel threshold increased
      
      # QR CODE
      # (img_array[:, :, 0] < 150) &  # Red channel threshold increased
      # (img_array[:, :, 1] < 150) &  # Green channel threshold increased
      # (img_array[:, :, 2] < 150)    # Blue channel threshold increased
      # # 0,180
      
      # # Prod
      (img_array[:, :, 0] < 130) &  # Red channel threshold increased
      (img_array[:, :, 1] < 200) &  # Green channel threshold increased
      (img_array[:, :, 2] < 200)    # Blue channel threshold increased
      
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
    mask = (hsv_img[:, :, 1] < 25) & (hsv_img[:, :, 2] < 190)
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
  
def remove_all_ocgs(pdf_path, output_path):
    """
    Removes all Optional Content Groups (OCGs) and their references from the PDF.

    Args:
        pdf_path (str): Path to the input PDF.
        output_path (str): Path to save the cleaned PDF.
    Returns:
        str: A success or error message.
    """
    try:
        with pikepdf.Pdf.open(pdf_path, allow_overwriting_input=True) as pdf:
            # Remove /OCProperties from the document catalog
            if "/OCProperties" in pdf.Root:
                del pdf.Root["/OCProperties"]
                print("Removed /OCProperties from the PDF catalog.")

            # Iterate over all pages to clean OCG references
            for page_number, page in enumerate(pdf.pages, start=1):
                print(f"Processing page {page_number}...")
                if "/Contents" in page:
                    content_obj = page["/Contents"]
                    if isinstance(content_obj, pikepdf.Array):
                        new_contents = pikepdf.Array()
                        for obj in content_obj:
                            stream = obj.read_bytes()
                            # Remove all OCG-related commands
                            stream = stream.replace(b"/OC", b"").replace(b"/BDC", b"").replace(b"/EMC", b"")
                            new_obj = pdf.make_stream(stream)
                            new_contents.append(new_obj)
                        page["/Contents"] = new_contents
                    elif isinstance(content_obj, pikepdf.Stream):
                        stream = content_obj.read_bytes()
                        stream = stream.replace(b"/OC", b"").replace(b"/BDC", b"").replace(b"/EMC", b"")
                        page["/Contents"] = pdf.make_stream(stream)

                # Remove XObjects tied to OCGs
                if "/Resources" in page:
                    resources = page["/Resources"]
                    if "/XObject" in resources:
                        xobjects = resources["/XObject"]
                        keys_to_remove = []
                        for key, obj in xobjects.items():
                            # Identify OCG-related XObjects by analyzing their properties
                            if obj.get("/OC"):
                                keys_to_remove.append(key)
                        for key in keys_to_remove:
                            print(f"Removing XObject '{key}' tied to OCGs.")
                            del xobjects[key]

                # Remove annotations tied to OCGs
                if "/Annots" in page:
                    annotations = page["/Annots"]
                    page["/Annots"] = pikepdf.Array([annot for annot in annotations if "/OC" not in annot])

            # Save the cleaned PDF
            pdf.save(output_path)
            print(f"Saved cleaned PDF without any OCGs to {output_path}")
            return f"Successfully removed all OCGs and saved to {output_path}"
    except Exception as e:
        return f"Error processing PDF: {str(e)}"

def remove_layer_watermarks(pdf_path, output_path):
    """
    Wrapper function to remove layer watermarks by calling remove_all_ocgs.

    Args:
        pdf_path (str): Path to the input PDF.
        output_path (str): Path to save the cleaned PDF.
    Returns:
        str: A success or error message.
    """
    return remove_all_ocgs(pdf_path, output_path)
      

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
        for img in convert_from_path(file_path, dpi=400, grayscale=True, fmt="jpeg", thread_count=os.cpu_count() * 2):
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
        final_pdf_path = file_path
        with Image.open(modified_images[0]).convert("RGB") as first_image:
            first_image.save(
                final_pdf_path,
                save_all=True,
                append_images=(
                    Image.open(img_path).convert("RGB") for img_path in modified_images[1:]
                )
            )
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
      
      