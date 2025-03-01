import struct


def read_bmp(filename):
    with open(filename, 'rb') as f:
        header = f.read(54)
        info = struct.unpack('<IIII', header[18:34])
        width, height = info[0], info[1]
        pixels = []
        for y in range(height):
            row = []
            for x in range(width):
                b, g, r = struct.unpack('BBB', f.read(3))
                row.append((r, g, b))
            pixels.append(row)
        pixels.reverse()
        return pixels


def write_bmp(filename, pixels):
    height = len(pixels)
    width = len(pixels[0])
    with open(filename, 'wb') as f:
        f.write(struct.pack('B', 0x42))
        f.write(struct.pack('B', 0x4D))
        f.write(struct.pack('<I', 54 + width * height * 3))
        f.write(struct.pack('<I', 0))
        f.write(struct.pack('<I', 54))

        f.write(struct.pack('<I', 40))
        f.write(struct.pack('<I', width))
        f.write(struct.pack('<I', height))
        f.write(struct.pack('<H', 1))
        f.write(struct.pack('<H', 24))
        f.write(struct.pack('<I', 0))
        f.write(struct.pack('<I', width * height * 3))
        f.write(struct.pack('<I', 0))
        f.write(struct.pack('<I', 0))
        f.write(struct.pack('<I', 0))
        f.write(struct.pack('<I', 0))

        for row in reversed(pixels):  # BMP files are bottom to top
            for (r, g, b) in row:
                f.write(struct.pack('BBB', b, g, r))


def invert(pixels):
    return [[(255 - r, 255 - g, 255 - b) for r, g, b in row] for row in pixels]


def adjust_brightness(pixels, factor):
    def adjust(color):
        return max(0, min(255, int(color * factor)))

    return [[(adjust(r), adjust(g), adjust(b)) for r, g, b in row] for row in pixels]


def mirror_horizontal(pixels):
    return [list(reversed(row)) for row in pixels]


def mirror_vertical(pixels):
    return list(reversed(pixels))


def to_grayscale(pixels):
    return [
        [(int(0.3 * r + 0.59 * g + 0.11 * b), int(0.3 * r + 0.59 * g + 0.11 * b), int(0.3 * r + 0.59 * g + 0.11 * b))
         for r, g, b in row] for row in pixels]


def rotate_90(pixels):
    height = len(pixels)
    width = len(pixels[0])
    return [[pixels[height - 1 - j][i] for j in range(height)] for i in range(width)]


pixels = read_bmp("in.bmp")
neg_pixels = invert(pixels)
bright_pixels = adjust_brightness(pixels, 1.2)
dark_pixels = adjust_brightness(pixels, 0.8)
mirror_h_pixels = mirror_horizontal(pixels)
mirror_v_pixels = mirror_vertical(pixels)
gray_pixels = to_grayscale(pixels)
rotated_pixels = rotate_90(pixels)

write_bmp("output_negative.bmp", neg_pixels)
write_bmp("output_bright.bmp", bright_pixels)
write_bmp("output_dark.bmp", dark_pixels)
write_bmp("output_mirror_h.bmp", mirror_h_pixels)
write_bmp("output_mirror_v.bmp", mirror_v_pixels)
write_bmp("output_gray.bmp", gray_pixels)
write_bmp("output_rotated.bmp", rotated_pixels)
