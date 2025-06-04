import os
import argparse
from removerPdf import remove_layer_watermarks, remove_watermark_from_pdf
from removerWord import remove_watermark_from_word


def process_file(file_path: str, output_dir: str, mode: str) -> None:
    """Process a single file based on its extension."""
    filename = os.path.basename(file_path)
    output_path = os.path.join(output_dir, filename)

    if file_path.lower().endswith('.pdf'):
        if mode == 'fast':
            print(f"Fast removal: {filename}")
            msg = remove_layer_watermarks(file_path, output_path)
            print(msg)
        else:
            print(f"Deep removal: {filename}")
            result_path = remove_watermark_from_pdf(file_path)
            if result_path and os.path.exists(result_path):
                os.rename(result_path, output_path)
    elif file_path.lower().endswith(('.docx', '.doc')):
        print(f"Processing Word file: {filename}")
        result_path = remove_watermark_from_word(file_path)
        if result_path and os.path.exists(result_path):
            os.rename(result_path, output_path)
    else:
        print(f"Skipping unsupported file: {file_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Watermark Removal Tool (CLI)")
    parser.add_argument('input', help='File or directory to process')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    parser.add_argument('-m', '--mode', choices=['fast', 'deep'], default='fast',
                        help='Removal mode for PDF files (default: fast)')
    args = parser.parse_args()

    input_path = args.input
    output_dir = args.output
    mode = args.mode

    os.makedirs(output_dir, exist_ok=True)

    if os.path.isfile(input_path):
        process_file(input_path, output_dir, mode)
    else:
        for name in sorted(os.listdir(input_path)):
            path = os.path.join(input_path, name)
            if os.path.isfile(path) and path.lower().endswith(('.pdf', '.docx', '.doc')):
                process_file(path, output_dir, mode)


if __name__ == '__main__':
    main()
