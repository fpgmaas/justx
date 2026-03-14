# Demo gif

Record with Kap, export to webm, then convert;

```sh
ffmpeg -i justx-demo2.webm -vf "fps=6,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse=dither=bayer:bayer_scale=3" demo2.gif
```