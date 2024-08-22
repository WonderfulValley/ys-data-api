from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
import dashscope

model = "stable-diffusion-xl"
dashscope.api_key = "sk-13f158d94a4d43038055a89acd8024f2"


def aliyun_sdxl(prompt, steps=60, scale=12, size="1024*1024", n=1, negative_prompt="garfield"):
    rsp = dashscope.ImageSynthesis.call(model=model,
                                        prompt=prompt,
                                        negative_prompt=negative_prompt,
                                        n=n,
                                        steps=steps,
                                        scale=scale,
                                        size=size)
    # if rsp.status_code == HTTPStatus.OK:
    #     print(rsp.output)
    #     # save file to current directory
    #     for result in rsp.output.results:
    #         file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
    #         with open('./%s' % file_name, 'wb+') as f:
    #             f.write(requests.get(result.url).content)
    # else:
    #     print('Failed, status_code: %s, code: %s, message: %s' %
    #           (rsp.status_code, rsp.code, rsp.message))
    # return rsp.output.results[0].url
    return rsp.output.results

# aliyun_sdxl("The background of the image showcases a mesmerizing cosmic scene with a vast expanse of the night sky filled with countless stars, shimmering and twinkling in various shades of blue and white. The sky is also adorned with swirling, dreamy nebulae, adding depth and texture to the dark backdrop. A prominent feature of the background is the large, glowing ring of light that encircles the scene, emitting a golden hue and dotted with tiny sparkles, giving a sense of a magical or celestial phenomenon. Towards the horizon, the landscape exhibits a barren, extraterrestrial terrain with jagged, rocky formations and a palette of purples and blues, blending into the luminous path that stretches across the ground, sparkling with lights. Additionally, a distant planet or moon is visible, small in comparison to the surrounding elements yet distinctly purple and ethereal. The entire scene conveys a sense of wonder and the vastness of the universe, creating an otherworldly atmosphere that feels both serene and awe-inspiring.This detailed description should help in recreating the celestial and mystical ambiance of the background, incorporating elements like the star-filled sky, glowing ring, nebulae, rocky terrain, and distant planetary body.")
