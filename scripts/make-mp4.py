"""
Encodes the captured PNG frames into an iPhone-compatible MP4 (H.264).
- 800x450, 20fps, H.264 high-quality, looped 6× for a ~30-second file
- -movflags faststart so it streams/opens instantly
"""
import os, imageio_ffmpeg

FRAMES_DIR = os.path.join(os.path.dirname(__file__), '..', 'frames')
OUT        = os.path.join(os.path.dirname(__file__), '..', 'illusion-engine.mp4')
FFMPEG     = imageio_ffmpeg.get_ffmpeg_exe()
SKIP       = 30
LOOP_LEN   = 100   # frames in one cycle
REPEATS    = 6     # × 5 seconds = ~30-second file
FPS        = 20

# Build ordered input list: frames 30-129 repeated REPEATS times
frame_paths = []
for _ in range(REPEATS):
    for i in range(SKIP, SKIP + LOOP_LEN):
        p = os.path.join(FRAMES_DIR, f'frame{i:04d}.png')
        frame_paths.append(p)

total = len(frame_paths)
print(f'Encoding {total} frames ({total / FPS:.0f}s) → {OUT}')

writer = imageio_ffmpeg.write_frames(
    OUT,
    size=(800, 450),
    fps=FPS,
    codec='libx264',
    pix_fmt_out='yuv420p',     # iPhone requires this
    quality=8,                 # 0-10 scale, 8 = high quality
    output_params=[
        '-preset', 'slow',
        '-profile:v', 'high',
        '-level', '4.1',
        '-movflags', '+faststart',
    ],
    macro_block_size=16,
)
writer.send(None)  # init

for idx, path in enumerate(frame_paths):
    import imageio.v3 as iio
    frame = iio.imread(path)
    writer.send(frame)
    if idx % 100 == 0:
        print(f'  {idx}/{total}')

writer.close()

size_mb = os.path.getsize(OUT) / 1024 / 1024
print(f'Done → {OUT}  ({size_mb:.1f} MB)')
