import os
import gradio as gr
from PIL import Image
import torch

  
os.system('wget https://github.com/JingyunLiang/SwinIR/releases/download/v0.0/003_realSR_BSRGAN_DFO_s64w8_SwinIR-M_x4_GAN.pth -P experiments/pretrained_models')

def inference(img):
    os.system('mkdir test')
    basewidth = 256
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    img.save("test/1.jpg", "JPEG")
    os.system('python main_test_swinir.py --task real_sr --model_path experiments/pretrained_models/003_realSR_BSRGAN_DFO_s64w8_SwinIR-M_x4_GAN.pth --folder_lq test --scale 4')
    return 'results/swinir_real_sr_x4/1_SwinIR.png'
        
title = "SwinIR"
description = "Gradio demo for SwinIR. SwinIR achieves state-of-the-art performance on six tasks: image super-resolution (including classical, lightweight and real-world image super-resolution), image denoising (including grayscale and color image denoising) and JPEG compression artifact reduction. See the paper and project page for detailed results below. Here, we provide a demo for real-world image SR.To use it, simply upload your image, or click one of the examples to load them."
article = "<p style='text-align: center'><a href='https://arxiv.org/abs/2108.10257' target='_blank'>SwinIR: Image Restoration Using Swin Transformer</a> | <a href='https://github.com/JingyunLiang/SwinIR' target='_blank'>Github Repo</a></p>"

examples=[['ETH_LR.png']]
demo = gr.Interface(
    inference, 
    [gr.inputs.Image(type="pil", label="Input")], 
    gr.outputs.Image(type="file", label="Output"),
    title=title,
    description=description,
    article=article,
    enable_queue=True,
    examples=examples
    )


demo.queue(concurrency_count=1, max_size=4)
demo.launch(server_port=8266)
