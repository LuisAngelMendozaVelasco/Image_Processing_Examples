def get_image_info(image):
    image_info = dict()
    image_attributes = ["filename", "format", "mode", "size", "width", "height", "palette", "is_animated", "n_frames"]
    for image_attribute in image_attributes:
        image_info[image_attribute] = image.__getattribute__(image_attribute)

    image_info_attribute = image.__getattribute__("info")
    for key in image_info_attribute.keys():
        if key == "Comment":
            for data in image_info_attribute[key].split("|"):
                if len(data) > 0:
                    data_split = data.split(":", maxsplit=1)
                    image_info[data_split[0]] = data_split[1].strip()
        else:
            image_info[key] = image_info_attribute[key]

    return image_info