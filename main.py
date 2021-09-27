from basic_filtering import *

# 사용 예시
def main():

    # 이미지 읽어오기
    #src = cv2.imread('./img/ex3.jpg', cv2.IMREAD_GRAYSCALE)
    #src_salt = cv2.imread('./img/salt_img.png', cv2.IMREAD_GRAYSCALE)
    src = cv2.imread('./img/ex3.jpg', cv2.IMREAD_COLOR)
    src_salt = cv2.imread('./img/salt_img3.jpg', cv2.IMREAD_COLOR)

    '''
    # 참조용 : 수치조정 없이 개별 필터링만 테스트, 실제로는 사용하지 않음
    sharpening_filter = sharpening_filtering(src) 
    
    #dst_average = cv2.blur(src, (3, 3))
    #dst_sharpening = cv2.filter2D(src, -1, sharpening_filter)
    #dst_bilateral = cv2.bilateralFilter(src, -1, 10, 5)
    #dst_median = cv2.medianBlur(src, 5)

    # 출력
    #cv2.imshow('original', src)
    #cv2.imshow('average filter', dst_average)
    #cv2.imshow('sharpening filter', dst_sharpening)
    #cv2.imshow('bilateral filter', dst_bilateral)
    #cv2.imshow('median filter', dst_median)
    
    #cv2.waitKey()
    #cv2.destroyAllWindows()
    '''

    # TEST
    dst_avg = average_filtering(src)
    dst_shp = sharpening_filtering(src)
    dst_bi = bilateral_filtering(src)
    dst_med = median_filtering(src_salt)

    cv2.imshow('avg_processed', dst_avg)
    cv2.imshow('shp_processed', dst_shp)
    cv2.imshow('bi_processed', dst_bi)
    cv2.imshow('med_processed', dst_med)

    cv2.waitKey()
    cv2.destroyAllWindows()



if __name__ == '__main__':
    main()