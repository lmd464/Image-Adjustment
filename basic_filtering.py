import cv2
import numpy as np

#########################################################

# Average Filter 생성
# 인자 ~ fshape : 필터의 크기 (튜플)
# 반환 : Average Filter (numpy 배열)
def generate_average_filter(fshape):
    return np.ones(fshape) / (fshape[0] * fshape[1])


# Sharpening Filter 생성
# 인자 ~ fshape : 필터의 크기 (튜플)
# 반환 : Sharpening Filter (numpy 배열)
def generate_sharpening_filter(fshape):

    # 차이가 적은 방법
    mask = np.zeros(fshape)
    mask[fshape[0] // 2, fshape[1] // 2] = 2
    mask = mask - generate_average_filter(fshape)

    '''
    결과 변동이 심한 방법
    mask = -np.ones(fshape)
    mask[fshape[0] // 2, fshape[1] // 2] = fshape[0] * fshape[1]
    '''
    return mask


# 트랙바를 위한 콜백함수
def trackbar_change(x):
    pass

#########################################################

##############################
#       Interfaces           #
#  슬라이드바로 값 조정 시 적용됨 #
#     ESC 누르면 루틴 종료      #
##############################

# Average Filtering
def average_filtering(src):
    h, w = src.shape[0], src.shape[1]
    cv2.namedWindow('Average Filter', cv2.WINDOW_AUTOSIZE)
    cv2.resizeWindow('Average Filter', width=w, height=h+50)
    cv2.createTrackbar('Blurrity', 'Average Filter', 0, 20, trackbar_change)
    blurrity = 0

    while True:
        prev_blurrity = blurrity
        blurrity = cv2.getTrackbarPos('Blurrity', 'Average Filter')
        filter_size = blurrity * 2 + 1

        if prev_blurrity != blurrity:
            print("Blurrity : " + str(blurrity))
            print("Filter Size : " + str(filter_size))

        dst = cv2.blur(src, (filter_size, filter_size))
        cv2.imshow('Average Filter', dst)


        # ESC : 종료 / 필터 적용 지연시간 0.1초
        input = cv2.waitKey(100) & 0xFF
        if input == 27:
            print("Average Filtering Complete")
            print("----------------------------")
            break
        else:
            continue

    cv2.destroyAllWindows()
    return dst


# Sharpening Filtering
def sharpening_filtering(src):
    h, w = src.shape[0], src.shape[1]
    cv2.namedWindow('Sharpening Filter', cv2.WINDOW_AUTOSIZE)
    cv2.resizeWindow('Sharpening Filter', width=w, height=h+50)
    cv2.createTrackbar('Sharpness', 'Sharpening Filter', 0, 100, trackbar_change)
    sharpness = 0

    while True:
        prev_sharpness = sharpness
        sharpness = cv2.getTrackbarPos('Sharpness', 'Sharpening Filter')
        filter_size = sharpness * 2 + 1

        if prev_sharpness != sharpness:
            print("Sharpness : " + str(sharpness))
            print("Filter Size : " + str(filter_size))

        sharpening_filter = generate_sharpening_filter((filter_size, filter_size))
        dst = cv2.filter2D(src, -1, sharpening_filter)
        cv2.imshow('Sharpening Filter', dst)

        # ESC : 종료 / 필터 적용 지연시간 0.1초
        input = cv2.waitKey(100) & 0xFF
        if input == 27:
            print("Sharpening Filtering Complete")
            print("----------------------------")
            break
        else:
            continue

    cv2.destroyAllWindows()
    return dst


# Bilateral filtering
# 시간 좀 걸릴 수 있음
def bilateral_filtering(src):
    h, w = src.shape[0], src.shape[1]
    cv2.namedWindow('Bilateral Filter', cv2.WINDOW_AUTOSIZE)
    cv2.resizeWindow('Bilateral Filter', width=w, height=h+100)
    cv2.createTrackbar('Sigma Color', 'Bilateral Filter', 0, 30, trackbar_change)
    cv2.createTrackbar('Sigma Space', 'Bilateral Filter', 0, 30, trackbar_change)
    sigma_color = 0
    sigma_space = 0

    while True:
        prev_sigma_color = sigma_color
        prev_sigma_space = sigma_space
        sigma_color = cv2.getTrackbarPos('Sigma Color', 'Bilateral Filter')
        sigma_space = cv2.getTrackbarPos('Sigma Space', 'Bilateral Filter')

        if prev_sigma_color != sigma_color:
            print("Sigma Color : " + str(sigma_color))
        if prev_sigma_space != sigma_space:
            print("Sigma Space : " + str(sigma_space))

        dst = cv2.bilateralFilter(src, -1, sigma_color, sigma_space)
        cv2.imshow('Bilateral Filter', dst)

        # ESC : 종료 / 필터 적용 지연시간 3초
        input = cv2.waitKey(3000) & 0xFF
        if input == 27:
            print("Bilateral Filtering Complete")
            print("----------------------------")
            break
        else:
            continue

    cv2.destroyAllWindows()
    return dst


# Median Filtering
def median_filtering(src):
    h, w = src.shape[0], src.shape[1]
    cv2.namedWindow('Median Filter', cv2.WINDOW_AUTOSIZE)
    cv2.resizeWindow('Median Filter', width=w, height=h+50)
    cv2.createTrackbar('Smoothness', 'Median Filter', 0, 10, trackbar_change)
    smoothness = 0

    while True:
        prev_smoothness = smoothness
        smoothness = cv2.getTrackbarPos('Smoothness', 'Median Filter')
        filter_size = smoothness * 2 + 1

        if prev_smoothness != smoothness:
            print("Smoothness : " + str(smoothness))
            print("Filter Size : " + str(filter_size))

        dst = cv2.medianBlur(src, filter_size)
        cv2.imshow('Median Filter', dst)

        # ESC : 종료 / 필터 적용 지연시간 0.1초
        input = cv2.waitKey(100) & 0xFF
        if input == 27:
            print("Median Filtering Complete")
            print("----------------------------")
            break
        else:
            continue

    cv2.destroyAllWindows()
    return dst


# Histogram Equalization
def equalize_hist(src):

    # RGB -> HSV 후 , V Channel에 HE 적용
    img_hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    img_hsv[:, :, 2] = cv2.equalizeHist(img_hsv[:, :, 2])

    dst = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)

    cv2.imshow('Histogram Equalization', dst)
    cv2.waitKey()
    print("Histogram Equalization Complete")
    print("----------------------------")
    cv2.destroyAllWindows()

    return dst


# HSV Adjustment
def HSV_Adjustment(src):
    h, w = src.shape[0], src.shape[1]
    cv2.namedWindow('HSV Adjustment', cv2.WINDOW_AUTOSIZE)
    cv2.resizeWindow('HSV Adjustment', width=w, height=h+150)

    # Hue : 180step / Saturation : 255step / Value : 255step
    cv2.createTrackbar('Hue', 'HSV Adjustment', 1, 180, trackbar_change)
    cv2.createTrackbar('Saturation', 'HSV Adjustment', 1, 255, trackbar_change)
    cv2.createTrackbar('Value', 'HSV Adjustment', 1, 255, trackbar_change)

    # HSV화 -> float화 -> 채널분리
    hsv_src = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    hsv_src = np.float64(hsv_src)
    Original_Hue_Channel, Original_Saturation_Channel, Original_Value_Channel = cv2.split(hsv_src)
    hue_scale, saturation_scale, value_scale = 0, 0, 0

    while True:
        prev_hue_scale = hue_scale
        prev_saturation_scale = saturation_scale
        prev_value_scale = value_scale


        # Scale : HSV 변경 정도 조정
        hue_scale = cv2.getTrackbarPos('Hue', 'HSV Adjustment')
        saturation_scale = cv2.getTrackbarPos('Saturation', 'HSV Adjustment')
        value_scale = cv2.getTrackbarPos('Value', 'HSV Adjustment')


        # Scale 값 반영하여 H, S, V Channel 값 조정
        Hue_Channel = np.clip(Original_Hue_Channel / np.median(Original_Hue_Channel) * hue_scale, 0, 180)
        Saturation_Channel = np.clip(Original_Saturation_Channel / np.median(Original_Saturation_Channel) * saturation_scale, 0, 255)
        Value_Channel = np.clip(Original_Value_Channel / np.median(Original_Value_Channel) * value_scale, 0, 255)


        if prev_hue_scale != hue_scale:
            print("Hue Scale : " + str(hue_scale))
        if prev_saturation_scale != saturation_scale:
            print("Saturation Scale : " + str(saturation_scale))
        if prev_value_scale != value_scale:
            print("Value Scale : " + str(value_scale))

        hsv_dst = cv2.merge( [Hue_Channel, Saturation_Channel, Value_Channel] )
        hsv_dst = np.uint8(hsv_dst)
        dst = cv2.cvtColor(hsv_dst, cv2.COLOR_HSV2BGR)
        cv2.imshow('HSV Adjustment', dst)

        # ESC : 종료 / 필터 적용 지연시간 0.1초
        input = cv2.waitKey(100) & 0xFF
        if input == 27:
            print("HSV Adjustment Complete")
            print("----------------------------")
            break
        else:
            continue

    cv2.destroyAllWindows()
    return dst


