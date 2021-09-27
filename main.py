from basic_filtering import *

# 사용 예시
def main():

    # 이미지 읽어오기
    #src = cv2.imread('./img/ex3.jpg', cv2.IMREAD_GRAYSCALE)
    #src_salt = cv2.imread('./img/salt_img.png', cv2.IMREAD_GRAYSCALE)
    src = cv2.imread('./img/ex3.jpg', cv2.IMREAD_COLOR)
    src_salt = cv2.imread('./img/salt_img3.jpg', cv2.IMREAD_COLOR)


    # TEST

    dst_avg = average_filtering(src)
    dst_shp = sharpening_filtering(src)
    dst_bi = bilateral_filtering(src)
    dst_med = median_filtering(src_salt)
    dst_he = equalize_hist(src)

    cv2.imshow('avg_processed', dst_avg)
    cv2.imshow('shp_processed', dst_shp)
    cv2.imshow('bi_processed', dst_bi)
    cv2.imshow('med_processed', dst_med)
    cv2.imshow('he_processed', dst_he)
    
    cv2.waitKey()
    cv2.destroyAllWindows()


    '''
    # Segmentation 테스트중
    bi = cv2.bilateralFilter(src, -1, 30, 30)
    can = cv2.Canny(bi, 190, 200)

    kernel = np.ones((3, 3), np.uint8)
    dst = cv2.morphologyEx(can, cv2.MORPH_CLOSE, kernel)
    dst = cv2.dilate(dst, kernel, iterations=2)

    #cnts, _ = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    #for cnt in cnts:
        #cv2.drawContours(dst, [cnt], -1, (255, 255, 255), cv2.FILLED)
    '''


if __name__ == '__main__':
    main()