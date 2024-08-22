import replicate
import time

# def replicate_sdxl(prompt):
#     output = replicate.run(
#         "stability-ai/sdxl:7762fd07cf82c948538e41f63f77d685e02b063e37e496e96eefd46c929f9bdc",
#         input={
#             "width": 1024,
#             "height": 1024,
#             "prompt": prompt,
#             "refine": "expert_ensemble_refiner",
#             "scheduler": "K_EULER",
#             "lora_scale": 0.6,
#             "num_outputs": 1,
#             "guidance_scale": 7.5,
#             "apply_watermark": False,
#             "high_noise_frac": 0.8,
#             "negative_prompt": "",
#             "prompt_strength": 0.8,
#             "num_inference_steps": 20
#         }
#     )
#     print(output)
#     return output
prompt="The background of the image depicts a whimsical, vibrant landscape painted with a bold, impressionist style. Dominating the backdrop is a glowing, large yellow moon hanging low in the sky, radiating a warm light. The sky surrounding the moon features a mix of deep blues and purples, transitioning to soft pink and lavender hues closer to the horizon, suggesting either dawn or dusk. In the midground, towering coniferous trees frame either side of the scene, their dark green branches contrasting against the lighter sky. Behind these trees, a series of mountain ranges stretch across the image, painted in layers of blues and greens, with the highest peak capped in white, indicating snow. The foreground is a vibrant, blooming meadow filled with an assortment of colorful wildflowers. The grass in the meadow is painted in rich green tones, interspersed with patches of yellow, and dotted with flowers in hues of pink, orange, red, blue, and white. The entire scene is rich in texture, with bold, sweeping brushstrokes that give the painting a dynamic, lively feel, evoking a sense of beauty and tranquility as if capturing a serene, dreamlike moment in nature."
# replicate_sdxl(prompt)
#
# for i in range(5):
#     start_time = time.time()
#     replicate_sdxl(prompt)
#     end_time = time.time()
#     execution_time = end_time - start_time
#     print(f"Execution time : {execution_time:.6f} seconds")



from app.modules.aliyun_conn import aliyun_sdxl

for i in range(5):
    start_time = time.time()
    aliyun_sdxl(prompt,steps=60)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time : {execution_time:.6f} seconds")
