from diffusers import AutoPipelineForImage2Image , UniPCMultistepScheduler
import torch
import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
import gradio as gr
from utils import remove_colors

STABLE_DIFFUSION_MODEL_NAME = 'stabilityai/sdxl-turbo'
IMG_DESCRIPTION_MODEL_NAME = 'Salesforce/blip-image-captioning-large'


# load stable diffusion xl turbo model
pipe = AutoPipelineForImage2Image.from_pretrained(STABLE_DIFFUSION_MODEL_NAME,
                                                    torch_dtype=torch.float16,
                                                    use_safetensors=True,
                                                    ).to('cuda')
pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
# For memory efficiency, we can enable sequential CPU offload
pipe.enable_sequential_cpu_offload()
    
# load image description model
processor = BlipProcessor.from_pretrained(IMG_DESCRIPTION_MODEL_NAME)
model = BlipForConditionalGeneration.from_pretrained(IMG_DESCRIPTION_MODEL_NAME,
                                                     torch_dtype=torch.float16).to("cuda")


def inference_img2img(
    img: str,
    prompt: str,
    negative_prompt = 'human,animals,cartoonic,blurry',
    strength = .3,
    num_inference_steps=30,

):
    """Inference image to image
    Args:
        img (str): Path to image
        prompt (str): Prompt to use for inference
        negative_prompt (str): Negative prompt to use for inference
        strength (float): Strength of diffusion
        num_inference_steps (int): Number of inference steps
    Returns:
        PIL.Image: Inferred image
    
    """
    inputs = processor(Image.open(img),
                        return_tensors="pt").to("cuda", torch.float16)
    photo_description = processor.decode(model.generate(**inputs)[0], skip_special_tokens=True)
    photo_description = remove_colors(photo_description)

    prompt = f"""{photo_description} Moroccan Moroccan Moroccan style {prompt} HD,hpyer detail,real life,cinematic lighting,8K"""

    inferenced_img = pipe(prompt ,
                        negative_prompt = negative_prompt,
                        image=Image.open(img),
                        strength= strength,
                        num_inference_steps=num_inference_steps
                        ).images[0]

    inferenced_img.save('i.png')

    return inferenced_img


def main():
    """Main function
    """
    app = gr.Blocks()

    with app:
        gr.HTML("""<h1 style="font-weight: 900; margin-bottom: 7px;margin-top:5px">🏠 Tigmi:</h1>""")
        gr.HTML("""<p>Adding custom moroccan touch to your space,This application is still in developement:</p>""")
        with gr.Tabs():
                with gr.TabItem("Image to image"):
                    with gr.Row():
                        img = gr.Image(sources=["upload"], type="filepath", label="Initial image:")
                    with gr.Row():
                        prompt = gr.Text(placeholder='Enter your prompt',label='Prompt:')
                    with gr.Row():
                        negative_prompt = gr.Text(placeholder='Enter your negative prompt',label='Negative prompt:',value='human,animals,cartoonic,blurry')
                        strength = gr.Slider(label='Strength:', minimum = 0.1, maximum = 1, step = .05,
                                            value = .5)
                    with gr.Row():
                        num_inference_steps =  gr.Slider(label = "Number of inference steps:",
                                                        minimum = 10, maximum = 100, step = 1, value=30)

                    output_img = gr.Image(label="")
                    img_button = gr.Button('Generate image')
                with gr.TabItem("Image to video"):
                    gr.HTML("""<p>Coming soon</p>""")


        img_button.click(inference_img2img, inputs=[
                        img,
                        prompt,
                        negative_prompt,
                        strength,
                        num_inference_steps
                    ], outputs=[output_img])

    app.launch(debug=True,share=True)


if __name__ == '__main__':
    main()