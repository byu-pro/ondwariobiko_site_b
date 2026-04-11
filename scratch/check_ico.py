import struct
with open(r'c:\Users\Admin\Documents\github\ondwariobiko_site_b\img\favicon\favicon.ico', 'rb') as f:
    f.seek(4)
    n = struct.unpack('<H', f.read(2))[0]
    print(f"Number of images in ico: {n}")
    for i in range(n):
        f.seek(6 + 16*i)
        w, h = struct.unpack("BB", f.read(2))
        print(f"Size: {w or 256}x{h or 256}")
