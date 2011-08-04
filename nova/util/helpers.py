import Image
import re
from uuid import uuid4
from os.path import splitext

def gen_image_cache(file_data):
    data = file_data.value
    basename, ext = splitext(file_data.filename)

    new_basename = str(uuid4())
    fil = open("nova/public/images/assets/%s_o%s" % (new_basename, ext), 'wb')
    fil.write(data)
    fil.close()

    image_data = Image.open("nova/public/images/assets/%s_o%s" % (new_basename, ext))
    img_t_s = image_data.copy()
    img_t_s.thumbnail((32,32), Image.ANTIALIAS)
    img_t_s.save("nova/public/images/assets/%s_s%s" % (new_basename, ext))

    img_t_m = image_data.copy()
    img_t_m.thumbnail((200,200), Image.ANTIALIAS)
    img_t_m.save("nova/public/images/assets/%s_m%s" % (new_basename, ext))

    img_t_l = image_data.copy()
    img_t_l.thumbnail((600,600), Image.ANTIALIAS)
    img_t_l.save("nova/public/images/assets/%s_l%s" % (new_basename, ext))

    return new_basename, ext

def distill(data_in, sep=','):
    data = filter((lambda x: len(x) > 0), data_in.split(sep))
    for i, d in enumerate(data):
        data[i] = d.strip()

    data = [x for x in data if len(x) is not 0]

    return data
