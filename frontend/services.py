import base64


def get_path_upload_photos_(instance, file):
    return f'images/pereval-{instance.pereval.id}/{file}'


def encode_image_file_to_binary_string(encode_image):
    with open(encode_image, 'rb') as image_file:
        file_content = image_file.read()

    encode_string = base64.b64encode(file_content)

    return encode_string.decode("utf-8")


def decode_binary_string_to_image_file(pereval_id, title, b_string):
    title = title.replace(' ', '-') + '-pereval_id' + str(pereval_id)
    with open(f'media/photos/{title}.jpeg', 'wb') as file:
        file.write(base64.b64decode(b_string))

    return file
