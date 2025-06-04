import numpy as np
import os

import removerPdf
import removerWord

# Test the color detection helpers

def test_is_text_color_rgb_and_hsv():
    # Create a small image with one black pixel and one white pixel
    img = np.array([
        [[0, 0, 0], [255, 255, 255]],
        [[10, 10, 10], [130, 130, 130]],
    ], dtype=np.uint8)
    rgb_mask = removerPdf.is_text_color_rgb(img)
    hsv_mask = removerPdf.is_text_color_hsv(img)
    # The darker pixels should be detected
    assert rgb_mask[0,0] and hsv_mask[0,0]
    assert rgb_mask[1,0] and hsv_mask[1,0]
    # The lighter pixel should not be detected
    assert not rgb_mask[0,1]


def test_handle_sets_non_text_to_white():
    img = np.array([
        [[0, 0, 0], [255, 0, 0]],
        [[0, 0, 0], [200, 200, 200]],
    ], dtype=np.uint8)
    result = removerPdf.handle(img.copy())
    # Non-text pixels become white
    assert np.array_equal(result[0,1], [255, 255, 255])
    assert np.array_equal(result[1,1], [255, 255, 255])
    # Text pixels remain unchanged (black)
    assert np.array_equal(result[0,0], [0, 0, 0])
    assert np.array_equal(result[1,0], [0, 0, 0])


def test_remove_watermark_from_word_invalid(tmp_path):
    # Nonexistent file should result in None
    fake_path = os.path.join(tmp_path, "missing.docx")
    assert removerWord.remove_watermark_from_word(fake_path) is None


def test_remove_layer_watermarks_invalid(tmp_path):
    # Should return an error string when the pdf cannot be opened
    fake_input = os.path.join(tmp_path, "missing.pdf")
    fake_output = os.path.join(tmp_path, "out.pdf")
    result = removerPdf.remove_layer_watermarks(fake_input, fake_output)
    assert isinstance(result, str) and result.startswith("Error processing PDF")


def test_remove_watermark_from_pdf_invalid(tmp_path):
    fake_input = os.path.join(tmp_path, "missing.pdf")
    assert removerPdf.remove_watermark_from_pdf(fake_input) is None
