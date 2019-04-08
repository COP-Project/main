from openalpr import Alpr

alpr = Alpr('us', "openalpr.conf", "runtime_data")


def read_a_plate(img, region):
    platevalue = None
    if not alpr.is_loaded():
        print("Error loading OpenALPR")
    else:
        alpr.set_top_n(7)
        alpr.set_default_region(region)
        alpr.set_detect_region(False)
        jpeg_bytes = open(img, "rb").read()
        results = alpr.recognize_array(jpeg_bytes)
        i = 0
        num_plates = len(results['results'])
        list = [0]*num_plates            # how many plates were found
        while i < num_plates:
            list[i] = results['results'][i]['plate']
            i += 1
    return list


def read_plate_from_stream(img, region):
    platevalue = None
    if not alpr.is_loaded():
        print("Error loading OpenALPR")
    else:
        alpr.set_top_n(7)
        alpr.set_default_region(region)
        alpr.set_detect_region(False)
        results = alpr.recognize_array(img)
        i = 0
        num_plates = len(results['results'])
        list = [0]*num_plates            # how many plates were found
        while i < num_plates:
            list[i] = results['results'][i]['plate']
            i += 1
    return list
