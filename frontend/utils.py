from frontend.services import encode_image_file_to_binary_string

image = 'images/pereval_1.jpg'

binary_string = encode_image_file_to_binary_string(image)

print(binary_string)

pereval_dict = {
    "id": 1,
    "beauty_title": "пер.",
    "title": "Пхия",
    "other_titles": "Триев",
    "connect": "коннектор-соедин",
    "user": {
        "email": "qwerty@mail.ru",
        "fam": "Пупкин",
        "name": "Василий",
        "otc": "Иванович",
        "phone": "8 999 999 99 99"
    },
    "coords": {
        "latitude": "45.38",
        "longitude": "7.15",
        "height": 1200
    },
    "level": {
        "winter": "1А",
        "summer": "1А",
        "autumn": "1А",
        "spring": "1А"
    },
    "images": [
        {
            "data": "binary_string",
            "title": "название"
        }
    ]
}
