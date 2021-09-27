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

##########################
#       Interfaces       #
#  슬라이드바로 값 조정 후,  #
#  아무 키나 누르면 적용됨   #
#  ESC 누르면 루틴 종료     #
##########################

# Average Filtering
def average_filtering(src):
    # Test : 비교용
    cv2.imshow('Original', src)

    cv2.namedWindow('Average Filter', cv2.WINDOW_AUTOSIZE)
    cv2.createTrackbar('Blurrity', 'Average Filter', 0, 20, trackbar_change)

    while True:
        blurrity = cv2.getTrackbarPos('Blurrity', 'Average Filter')
        filter_size = blurrity * 2 + 1
        print("Blurrity : " + str(blurrity))
        print("Filter Size : " + str(filter_size))

        dst = cv2.blur(src, (filter_size, filter_size))
        cv2.imshow('Average Filter', dst)


        # ESC : 종료, 다른 키가 눌렸다면 blur 처리
        input = cv2.waitKey() & 0xFF
        if input == 27:
            print("ESC")
            break
        else:
            continue

    cv2.destroyAllWindows()
    return dst


# Sharpening Filtering
def sharpening_filtering(src):
    # Test : 비교용
    cv2.imshow('Original', src)

    cv2.namedWindow('Sharpening Filter', cv2.WINDOW_AUTOSIZE)
    cv2.createTrackbar('Sharpness', 'Sharpening Filter', 0, 100, trackbar_change)

    while True:
        sharpness = cv2.getTrackbarPos('Sharpness', 'Sharpening Filter')
        filter_size = sharpness * 2 + 1
        print("Sharpness : " + str(sharpness))
        print("Filter Size : " + str(filter_size))

        sharpening_filter = generate_sharpening_filter((filter_size, filter_size))
        dst = cv2.filter2D(src, -1, sharpening_filter)
        cv2.imshow('Sharpening Filter', dst)

        # ESC : 종료, 다른 키가 눌렸다면 Sharpening 처리
        input = cv2.waitKey() & 0xFF
        if input == 27:
            print("ESC")
            break
        else:
            continue

    cv2.destroyAllWindows()
    return dst


# Bilateral filtering
# 적용 키 누르고 시간 좀 걸릴 수 있음
def bilateral_filtering(src):
    # Test : 비교용
    cv2.imshow('Original', src)

    cv2.namedWindow('Bilateral Filter', cv2.WINDOW_AUTOSIZE)
    cv2.createTrackbar('Sigma Color', 'Bilateral Filter', 0, 50, trackbar_change)
    cv2.createTrackbar('Sigma Space', 'Bilateral Filter', 0, 50, trackbar_change)

    while True:
        sigma_color = cv2.getTrackbarPos('Sigma Color', 'Bilateral Filter')
        sigma_space = cv2.getTrackbarPos('Sigma Space', 'Bilateral Filter')
        print("Sigma Color : " + str(sigma_color))
        print("Sigma Space : " + str(sigma_space))

        dst = cv2.bilateralFilter(src, -1, sigma_color, sigma_space)
        cv2.imshow('Bilateral Filter', dst)

        # ESC : 종료, 다른 키가 눌렸다면 blur 처리
        input = cv2.waitKey() & 0xFF
        if input == 27:
            print("ESC")
            break
        else:
            continue

    cv2.destroyAllWindows()
    return dst


# Median Filtering
def median_filtering(src):
    # Test : 비교용
    cv2.imshow('Original', src)

    cv2.namedWindow('Median Filter', cv2.WINDOW_AUTOSIZE)
    cv2.createTrackbar('Smoothness', 'Median Filter', 0, 10, trackbar_change)

    while True:
        smoothness = cv2.getTrackbarPos('Smoothness', 'Median Filter')
        filter_size = smoothness * 2 + 1
        print("Smoothness : " + str(smoothness))
        print("Filter Size : " + str(filter_size))

        dst = cv2.medianBlur(src, filter_size)
        cv2.imshow('Median Filter', dst)


        # ESC : 종료, 다른 키가 눌렸다면 blur 처리
        input = cv2.waitKey() & 0xFF
        if input == 27:
            print("ESC")
            break
        else:
            continue

    cv2.destroyAllWindows()
    return dst







