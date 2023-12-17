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
    theme = gr.themes.Soft(
        primary_hue="red",
    # secondary_hue="orange",
        neutral_hue="stone",
    )

    app = gr.Blocks(theme=theme)

    Disclaimer = """This application utilizes artificial intelligence to simulate and infuse Moroccan style elements into interior design images. It is important to note that the generated results are based on patterns learned from a diverse range of Moroccan design aesthetics. While the AI strives to enhance and complement the given images with Moroccan-inspired features, the outcomes may not be an exact representation of authentic Moroccan designs.

    Users are encouraged to use the application as a creative tool and to exercise their own judgment in refining the final design. The AI-generated results should be considered as suggestions rather than definitive representations of Moroccan design principles. Additionally, individual preferences and cultural interpretations may vary, and the application may not account for all nuances of Moroccan design.

    The developers of this application are not responsible for any discrepancies, inaccuracies, or deviations from traditional Moroccan design standards. Users should review and modify the AI-generated designs to ensure they align with their personal vision and preferences.

    By using this application, users acknowledge that the AI-generated designs are for inspiration purposes only, and final decisions regarding interior design choices should be made with consideration of personal taste, cultural sensitivity, and other relevant factors.
    """

    with app:
        gr.HTML("""<div style="display:flex"><img src="https://github.com/wassim249/TIG_MI/blob/v2/imgs/logo.jpg?raw=true" width="50" /> &nbsp; <h1 style="font-weight: 900; margin-bottom: 7px;margin-top:5px ;font-size=16px'">Tigmi: your Heritage,your place,our innovation</div>""")
        gr.HTML("""<img src="https://github.com/wassim249/TIG_MI/blob/v2/imgs/4_video.gif?raw=true" width="500" />""")

        gr.HTML(f"""<p style="margin-bottom: 7px;margin-top:5px ;font-size=16px;text-align: justify">{Disclaimer}</p>""")
        gr.HTML("""<b><i>This application is still in developement</i></b>""")
        with gr.Tabs():
                with gr.TabItem("📷 Image to image"):
                    with gr.Row():
                        img = gr.Image(sources=["upload"], type="filepath", label="Initial image:")
                    with gr.Row():
                        prompt = gr.Text(placeholder='Enter your prompt',label='Prompt:',info='Set your preferred moroccan style e.g Chefchaouan blue style (optional)')
                    with gr.Row():
                        negative_prompt = gr.Text(placeholder='Enter your negative prompt',label='Negative prompt:',value='human,animals,cartoonic,blurry',info='Conditions the model to not include things in an image')
                        strength = gr.Slider(label='Strength:', minimum = 0.1, maximum = 1, step = .05,
                                            value = .5,info='Determines how much the generated image resembles the initial image')
                    with gr.Row():
                        num_inference_steps =  gr.Slider(label = "Number of inference steps:",
                                                        minimum = 10, maximum = 100, step = 1, value=30,info='A larger number of steps increases the quality of the output but it takes longer to generate')

                    output_img = gr.Image(label="")
                    gr.HTML("""<h1 style="font-weight: 900; margin-bottom: 7px;margin-top:5px ;font-size=16px'">👉 Try out those examples !</h1>""")
                    gr.Examples(
                        [["https://images.pexels.com/photos/262047/pexels-photo-262047.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1", "Chefchaouen style","human,animals,cartoonic,blurry,modern",.3,30],
                        ["https://images.pexels.com/photos/1457842/pexels-photo-1457842.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1", "Marrakesh style,traditional orange theme","human,animals,cartoonic,blurry,modern",.3,30],
                        ["https://images.pexels.com/photos/37347/office-sitting-room-executive-sitting.jpg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1", "Zelij,pottery style,traditional yellow theme","human,animals,cartoonic,blurry,modern",.5,30],
                        ],
                        [img, prompt,negative_prompt,strength,num_inference_steps],
                        output_img,
                        inference_img2img,
                        cache_examples=False,
                    )
                    
                    img_button = gr.Button('Generate image')

                with gr.TabItem("📹 Image to video"):
                    gr.HTML("""<p>Coming soon</p>""")


        img_button.click(inference_img2img, inputs=[
                        img,
                        prompt,
                        negative_prompt,
                        strength,
                        num_inference_steps
                    ], outputs=[output_img])

    app.title = '🏠🇲🇦 TIGMI | your Heritage,your place,our innovation'
    app.launch(debug=True,share=True)


if __name__ == '__main__':
    main()