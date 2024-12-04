import cairo
import os

def create_text_image(text, font_size=100, image_size=(1080, 120)):
    # Create a new image surface
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, image_size[0], image_size[1])
    context = cairo.Context(surface)

    # Set background to transparent
    context.set_source_rgba(1, 1, 1, 0)  # RGBA (white, transparent)
    context.paint()

    # Set font and size
    context.select_font_face("Bauhaus 93", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    context.set_font_size(font_size)

    # Measure text size
    text_extents = context.text_extents(text)
    text_width = text_extents.width
    text_height = text_extents.height+5

    # Calculate position to center the text
    x = (image_size[0] - text_width) / 2
    y = (image_size[1] + text_height) / 2 - 22  # Adjust y to be vertically centered

    # Draw the dense black border by drawing the text multiple times
    context.set_source_rgb(0, 0, 0)  # Black color
    border_width = 5  # Width of the border

    for dx in range(-border_width, border_width + 1):
        for dy in range(-border_width, border_width + 1):
            context.move_to(x + dx, y + dy)
            context.show_text(text)

    # Draw the white text on top
    context.set_source_rgb(1, 1, 1)  # White color
    context.move_to(x, y)
    context.show_text(text)

    # Finish and save the image
    surface.write_to_png(os.path.join(os.path.join(os.getcwd(), 'texts'),f"{text.replace(" ","_").replace(":","")}.png"))
    print(f"Imagem salva como '{f"{text.replace(" ","_").replace(":","")}.png"}'.")

# Create and save the image
inpu = str(input("Frase: "))
create_text_image(inpu)
