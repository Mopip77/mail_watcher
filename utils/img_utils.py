def get_image_contents(image_paths):
    result = []
    for image_path in image_paths:
        with open(image_path, 'rb') as f:
            result.append(f.read())

    return result