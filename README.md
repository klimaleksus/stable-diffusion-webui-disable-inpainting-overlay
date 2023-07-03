### Discussion: `https://github.com/AUTOMATIC1111/stable-diffusion-webui/discussions/TODO`

# disable-inpainting-overlay

This is WIP Extension for [AUTOMATIC1111/stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) for having more control over inpainting.

## Installation:
Copy the link to this repository into `Extension index URL` in WebUI Extensions tab:
```
https://github.com/klimaleksus/stable-diffusion-webui-disable-inpainting-overlay
```
Also you may clone/download this repository and put it to `stable-diffusion-webui/extensions` directory.

## Usage:
You will see a section titled `Disable Inpainting Overlay` on img2img tab. It has 3 checkboxes:

### Disable inpainting overlay (leave picture from U-Net as-is)
It will save to final result the same image that you may see in preview during generation. Which means:
- Unmasked area **will** be changed, because of VAE conversion
- Quality of your image will quickly **degrade**, if you will use your output as input again
- When "Inpaint area"="Only masked" you will have **cropped** result, not pasted back to original image
- However, there should be **no seam** on mask boundaries

Why you may need this? In case if you want to manually put your inpainting result to a top layer in photoshop to erase its outer area by yourself. This way you will get much more freedom, compared to just a tiny blurred border of the mask otherwise.  
Use this ONLY when you plan to composite your inpainting manually!

<details><summary>Example!</summary>
  
TODO

</details>

### Ignore padding but crop to 1:1 resolution (when "Only masked")
It will sharpen the mask, getting rid of semi-transparent areas. You will see actual latent squares, which means:
- The mask border will be rough, with much more visible seam
- Mask blurring will be ignored (but applied before rounding the mask)
- However, no transparency will be involved when compositing your final image, so that re-inpainting the same region (after using your output as a new input) will not contain "semi-redrawn" pixels: each pixel will be either original, or fully inpainted.

Why you may need this? Probably in case when you want to refine your inpainted contents sequentially, by sending your best result back to inpaint with the same mask again and again, but without blurring/destroying the area around mask edges (that often becomes visible otherwise).  
There is no reason to use this mode together with previous (because the previous one is generally better since you will then work manually anyway).

<details><summary>Example!</summary>
  
TODO

</details>

### When "Only masked", ignore padding but crop to 1:1 resolution
It will drop your "Only masked padding, pixels" value, but calculate inpainting region so that inpaint window will be exactly width\*height pixels, centered around the masked area. Which means:
- You won't get high-quality image downscaled and pasted into your region
- Some parts of a very large mask might be left out-of-bounds
- However, no scaling would be done whatsoever (it's like auto-calculated pixel-perfect padding, independently for width and height)

Why you may need this? In cases when you already upscaled your image large enough that inpainting at native resolution is feasible, but you don't want to crop the area manually, nor you want to calculate or pick-up the value of padding yourself.  
To see the target area exactly, set the first checkbox here ("Disable inpainting overlay") too.

<details><summary>Example!</summary>
  
TODO

</details>

This extension does not add anything to generation info.
## EOF
