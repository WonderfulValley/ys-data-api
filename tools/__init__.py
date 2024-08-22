from PIL import Image

# 加载背景图片和主体图片
background_image = Image.open('background.png')
subject_image = Image.open('subject.png')

# 获取图片尺寸
background_width, background_height = background_image.size
subject_width, subject_height = subject_image.size

# 计算主体图片在背景图片上的位置
# 居中放置，并且稍微偏下（比如距离底部为高度的1/4）  
top_position = (background_height - subject_height) // 4
left_position = (background_width - subject_width) // 2

# 使用alpha合成模式将主体图片粘贴到背景图片上
background_image.alpha_composite(subject_image, (left_position, top_position))

# 保存结果图片
background_image.save('result.png')