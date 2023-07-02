# stable-diffusion-disable-inpainting-overlay

import cv2
import PIL
import numpy
import gradio as gr
from modules import scripts
import modules.masking as masking
import modules.processing as processing

class DisableInpaintingOverlay(scripts.Script):
    def title(self):
        return 'Disable Inpainting Overlay'
    def show(self, is_img2img):
        return scripts.AlwaysVisible
    def ui(self, is_img2img):
        if not is_img2img:
            return None
        with gr.Accordion('Disable Inpainting Overlay', open=False):
            with gr.Row():
                gr_disable = gr.Checkbox(False,label='Disable inpainting overlay (leave picture from U-Net as-is)')
                gr_align = gr.Checkbox(False,label='Align mask on VAE squares (for exact latents positions, 8*8)')
                gr_masked = gr.Checkbox(False,label='When "Only masked", ignore padding but crop to 1:1 resolution')
        return [gr_disable,gr_align,gr_masked]
    def before_process(self,p,gr_disable,gr_align,gr_masked):
        if (not gr_disable) and (not gr_align):
            return
        if gr_align and hasattr(p,'image_mask'):
            np_mask = numpy.array(p.image_mask)
            if p.mask_blur_x > 0:
                kernel_size = 2 * int(4 * p.mask_blur_x + 0.5) + 1
                np_mask = cv2.GaussianBlur(np_mask, (kernel_size, 1), p.mask_blur_x)
                p.mask_blur_x = 0
            if p.mask_blur_y > 0:
                kernel_size = 2 * int(4 * p.mask_blur_y + 0.5) + 1
                np_mask = cv2.GaussianBlur(np_mask, (1, kernel_size), p.mask_blur_y)
                p.mask_blur_y = 0
            p.mask_blur = 0
            mult = 8
            width = np_mask.shape[1]//mult
            height = np_mask.shape[0]//mult
            for y in range(height):
                y1 = y*mult
                y2 = (y+1)*mult
                for x in range(width):
                    x1 = x*mult
                    x2 = (x+1)*mult
                    np_mask[y1:y2,x1:x2] = 255 if np_mask[y1:y2,x1:x2].max()>127 else 0
            p.image_mask = PIL.Image.fromarray(np_mask)
        if gr_disable and (not hasattr(processing.apply_overlay,'_DisableInpaintingOverlay')):
                if hasattr(processing.apply_overlay,'_DisableInpaintingOverlay'):
                    processing.apply_overlay = getattr(processing.apply_overlay,'_DisableInpaintingOverlay')
                mock = lambda image,*ar,**kw: image
                setattr(mock,'_DisableInpaintingOverlay',processing.apply_overlay)
                processing.apply_overlay = mock
        if gr_masked and hasattr(p,'inpaint_full_res') and (p.inpaint_full_res):
                if hasattr(masking.get_crop_region,'_DisableInpaintingOverlay'):
                    masking.get_crop_region = getattr(masking.get_crop_region,'_DisableInpaintingOverlay')
                old = masking.get_crop_region
                mock = lambda mask,pad=0: DisableInpaintingOverlay_masked(old(mask,0),mask.shape,p.width,p.height)
                setattr(mock,'_DisableInpaintingOverlay',masking.get_crop_region)
                masking.get_crop_region = mock
    def postprocess(self,*ar,**kw):
        if hasattr(processing.apply_overlay,'_DisableInpaintingOverlay'):
            processing.apply_overlay = getattr(processing.apply_overlay,'_DisableInpaintingOverlay')
        if hasattr(masking.get_crop_region,'_DisableInpaintingOverlay'):
            masking.get_crop_region = getattr(masking.get_crop_region,'_DisableInpaintingOverlay')

def DisableInpaintingOverlay_masked(crop,shape,width,height):
    x,y,w,h = crop
    H,W = shape
    w -= x
    h -= y
    x -= (width-w)//2
    y -= (height-h)//2
    w = (x+width)-W
    h = (y+height)-H
    if w>0:
        x -= w;
    if h>0:
        y -= h;
    if x<0:
        x = 0
    if y<0:
        y = 0
    return (x,y,x+width,y+height)

#EOF
