from PIL import Image, ImageEnhance, ImageFilter


def enhance_for_document(image_path, output_image_path, output_pdf_path):
    # Load the image
    image = Image.open(image_path)

    # Step 1: Brightness enhancement
    bright_enhancer = ImageEnhance.Brightness(image)
    bright_image = bright_enhancer.enhance(1.2)  # Slightly increase brightness

    # Step 2: Contrast enhancement
    contrast_enhancer = ImageEnhance.Contrast(bright_image)
    contrast_image = contrast_enhancer.enhance(1.3)  # Slightly increase contrast

    # Step 3: Sharpen the image
    sharpened_image = contrast_image.filter(ImageFilter.SHARPEN)

    # Step 4: Optional - Resize (increase resolution)
    resized_image = sharpened_image.resize((sharpened_image.width * 2, sharpened_image.height * 2), Image.LANCZOS)

    # Save enhanced image as PNG
    resized_image.save(output_image_path)

    # Save as PDF
    resized_image.save(output_pdf_path, "PDF")

    print(f"Enhanced image saved to {output_image_path}")
    print(f"Enhanced PDF saved to {output_pdf_path}")


input_image_path = "chc_organ.png"
output_image_path = "enhanced.png"
output_pdf_path = "enhanced_chart.pdf"

# Enhance and save
enhance_for_document(input_image_path, output_image_path, output_pdf_path)
