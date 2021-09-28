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

    cv2.imshow('original', src)
    cv2.imshow('avg_processed', dst_avg)
    cv2.imshow('shp_processed', dst_shp)
    cv2.imshow('bi_processed', dst_bi)
    cv2.imshow('med_processed', dst_med)
    cv2.imshow('he_processed', dst_he)
    
    cv2.waitKey()
    cv2.destroyAllWindows()



    '''
    # Segmentation 테스트중
    # bilateral -> canny -> closing
    #bi = cv2.bilateralFilter(src, -1, 30, 30)
    #can = cv2.Canny(bi, 190, 200)
    gaus = np.dot(cv2.getGaussianKernel(5, 10), cv2.getGaussianKernel(5, 5).T)

    dog = cv2.Sobel(gaus, cv2.CV_64F, 1, 1, 5)
    dog = dog / (np.sum(dog) + 0.001)
    dst = cv2.filter2D(cv2.imread('./img/ex3.jpg', cv2.IMREAD_GRAYSCALE), -1, dog)

    
    kernel = np.ones((3, 3), np.uint8)
    dst = cv2.morphologyEx(can, cv2.MORPH_CLOSE, kernel)
    dst[:5, :5] = 0
    cv2.floodFill(dst, None, (0, 0), (255, 255, 255))
    dst = 255 - dst
    dst = cv2.morphologyEx(dst, cv2.MORPH_OPEN, kernel)
    

    #cnts, _ = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    #for cnt in cnts:
        #cv2.drawContours(dst, [cnt], -1, (255, 255, 255), cv2.FILLED)
    cv2.imshow("test", dst)
    cv2.waitKey()
    cv2.destroyAllWindows()
    '''

if __name__ == '__main__':
    main()
