import io, os
import pillow_avif  # noqa: registers AVIF opener for Pillow
from PIL import Image

UP = r"C:\Users\Echev\AppData\Roaming\Claude\local-agent-mode-sessions\c8571ed9-bb0a-40e6-9eb5-238d0bb31cac\be324864-0652-486e-b204-42e3ae02271f\local_6cbcf33b-2a4d-4be1-bced-76d7dd2738b2\uploads"
OUT = r"C:\Users\Echev\AppData\Roaming\Claude\local-agent-mode-sessions\c8571ed9-bb0a-40e6-9eb5-238d0bb31cac\be324864-0652-486e-b204-42e3ae02271f\local_6cbcf33b-2a4d-4be1-bced-76d7dd2738b2\outputs\images"
os.makedirs(OUT, exist_ok=True)

def resize_max(img, max_w):
    w, h = img.size
    if w > max_w:
        nh = int(h * (max_w / w))
        img = img.resize((max_w, nh), Image.LANCZOS)
    return img

print("STEP 1: plane background removal")
from rembg import remove
plane_path = os.path.join(UP, "B1185837336.jpg")
with open(plane_path, "rb") as f:
    plane_bytes = f.read()
out_bytes = remove(plane_bytes)
plane_cut = Image.open(io.BytesIO(out_bytes)).convert("RGBA")
bbox = plane_cut.getbbox()
if bbox:
    pad = 8
    l, t, r, b = bbox
    l = max(0, l - pad); t = max(0, t - pad)
    r = min(plane_cut.width, r + pad); b = min(plane_cut.height, b + pad)
    plane_cut = plane_cut.crop((l, t, r, b))
plane_cut = resize_max(plane_cut, 900)
plane_cut.save(os.path.join(OUT, "avion-cutout.png"))
print("plane done", plane_cut.size)

print("STEP 2: ship photo (full, just optimized)")
ship_path = os.path.join(UP, "vista-superior-transporte-carga-buque-portacontenedores-buque-portacontenedores-alta-mar-ia-generativa_74760-5313.avif")
ship = Image.open(ship_path).convert("RGB")
ship = resize_max(ship, 1400)
ship.save(os.path.join(OUT, "barco-contenedores.jpg"), quality=85)
print("ship done", ship.size)

print("STEP 3: containers (resize only, stacked via CSS later)")
c1 = Image.open(os.path.join(UP, "descargar.webp")).convert("RGB")
c1 = resize_max(c1, 700)
c1.save(os.path.join(OUT, "contenedor-1.jpg"), quality=85)
print("contenedor-1 done", c1.size)

c2 = Image.open(os.path.join(UP, "descargar (1).webp")).convert("RGB")
c2 = resize_max(c2, 700)
c2.save(os.path.join(OUT, "contenedor-2.jpg"), quality=85)
print("contenedor-2 done", c2.size)

print("ALL DONE")
