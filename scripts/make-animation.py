"""
Assembles captured PNG frames into a seamlessly-looping animated WebP (+ APNG fallback).

Strategy:
  - Skip first 30 frames (extra warmup buffer)
  - Use frames 30-129  → 100 frames = 5-second loop at 20fps
  - Crossfade last 25 frames with first 25 frames to hide the loop seam
"""
import sys
import os
import numpy as np
from PIL import Image

FRAMES_DIR = os.path.join(os.path.dirname(__file__), '..', 'frames')
OUT_DIR    = os.path.join(os.path.dirname(__file__), '..')
SKIP       = 30    # skip warmup frames
TOTAL      = 100   # frames in final loop
BLEND      = 25    # crossfade length at seam
FPS        = 20
DURATION   = int(1000 / FPS)   # ms per frame


def load_frames(skip, total):
    frames = []
    for i in range(skip, skip + total):
        p = os.path.join(FRAMES_DIR, f'frame{i:04d}.png')
        if not os.path.exists(p):
            sys.exit(f'Missing frame: {p}')
        frames.append(np.array(Image.open(p).convert('RGB'), dtype=np.float32))
        if i % 20 == skip:
            print(f'  loaded {i - skip + 1}/{total}')
    return frames


def crossfade(frames):
    n = len(frames)
    core = frames[:n - BLEND]
    result = list(core)
    for i in range(BLEND):
        alpha = i / BLEND          # 0 = all-tail, 1 = all-head
        tail  = frames[n - BLEND + i]
        head  = frames[i]
        blended = (tail * (1 - alpha) + head * alpha).clip(0, 255).astype(np.uint8)
        result.append(Image.fromarray(blended))
    return result


def to_pil(arr):
    if isinstance(arr, np.ndarray):
        return Image.fromarray(arr.clip(0, 255).astype(np.uint8))
    return arr


def save_webp(pil_frames, path):
    pil_frames[0].save(
        path,
        format='WEBP',
        save_all=True,
        append_images=pil_frames[1:],
        loop=0,
        duration=DURATION,
        quality=87,
        method=4,
    )
    size_kb = os.path.getsize(path) / 1024
    print(f'WebP  → {path}  ({size_kb:.0f} KB)')


def save_apng(pil_frames, path):
    pil_frames[0].save(
        path,
        format='PNG',
        save_all=True,
        append_images=pil_frames[1:],
        loop=0,
        duration=DURATION,
    )
    size_kb = os.path.getsize(path) / 1024
    print(f'APNG  → {path}  ({size_kb:.0f} KB)')


if __name__ == '__main__':
    print(f'Loading {TOTAL} frames (skip={SKIP})…')
    raw = load_frames(SKIP, TOTAL)

    print('Crossfading loop seam…')
    output = crossfade(raw)
    pil_frames = [to_pil(f) for f in output]

    print(f'Encoding {len(pil_frames)} frames…')
    save_webp(pil_frames, os.path.join(OUT_DIR, 'illusion-engine.webp'))
    save_apng(pil_frames, os.path.join(OUT_DIR, 'illusion-engine.apng'))

    print('Done.')
