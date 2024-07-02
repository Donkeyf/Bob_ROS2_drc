def pinehsv_to_cvhsv(pine):

    # Input pine is a length 3 tuple
    # Output hsv is a length 3 tuple
    
    hsv_0 = pine[0] * 180 / 360
    hsv_1 = pine[1] * 255 / 100
    hsv_2 = pine[2] * 255 / 100

    hsv = (hsv_0, hsv_1, hsv_2)

    return hsv