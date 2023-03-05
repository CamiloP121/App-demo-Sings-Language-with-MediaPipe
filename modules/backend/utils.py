import base64

def base64toimage(img_data: str, save:bool = True):
    '''
    Converts base64 to image
    ----------------------------------------------------------------
    Arg:
    img_data (str): base64 string
    save (bool, optional): whether to save the image or not. Defaults to True.
    '''
    image_as_bytes = str.encode(img_data)  # convert string to bytes
    print('SEP 1')
    image = base64.b64decode(image_as_bytes)
    if save:
        with open('../temp/image.jpg', 'wb') as file:
            file.write(image)

    return image
