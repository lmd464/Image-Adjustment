'''
############################################################
# Image Padding : Filtering 내부에서 전처리에 사용
# 따로 사용 X
def padding(src, filter):
    (h, w) = src.shape
    (h_pad, w_pad) = filter.shape
    h_pad = h_pad // 2
    w_pad = w_pad // 2
    padding_img = np.zeros((h+h_pad*2, w+w_pad*2))
    padding_img[h_pad:h+h_pad, w_pad:w+w_pad] = src
    return padding_img

# Normalize : bilateral 내에서 사용, 픽셀값 0~1에서 0~255로 변환
# 따로 사용 X
def normalize(src):
    dst = src.copy()
    dst *= 255
    dst = np.clip(dst, 0, 255)
    return dst.astype(np.uint8)
############################################################


# Image Filtering : 필터를 받아 필터링
# 인자 ~ src : 원본 이미지 (numpy 배열) / filter : 적용할 필터
# 반환 : 필터링 결과 이미지 (numpy 배열)
def filtering(src, filter):
    (h, w) = src.shape
    (m_h, m_w) = filter.shape
    pad_img = padding(src, filter)
    dst = np.zeros((h, w))
    for row in range(h):
        for col in range(w):
            dst[row, col] = np.sum(pad_img[row:row + m_h, col:col + m_w] * filter)

    dst = (dst + 0.5).astype(np.uint8)

    print("Filtering Complete")
    return dst

'''

'''
# Bilateral filtering : 매 번 다른 필터를 적용하기 떄문에, filtering 함수를 거치지 않음
# 인자 ~ src : 원본 이미지 (numpy 배열) / fsize : 필터의 크기 (홀수 정수, 기본값 5)
# 반환 : Bilateral filtering 결과 이미지 (numpy 배열)
def bilateral_filtering(src, fsize=5, sigma=10, sigma_r=0.1):
    src = src / 255
    (h, w) = src.shape

    mid = fsize // 2
    pad = fsize // 2
    mask = np.zeros((fsize, fsize))
    src_pad = padding(src, mask)     # pad : index 초과 방지용
    dst = np.zeros((h, w))

    for i in range(h):
        print('\rBilateral filtering %d / %d ...' %(i,h), end="")
        for j in range(w):
            # temp 에 원본 이미지의 대상 영역 복사
            temp = src_pad[i+pad-mid : i+pad+mid+1 , j+pad-mid : j+pad+mid+1]

            # 복사된 영역을 대상으로 mask의 값을 계산 ~ 시간 좀 걸림
            y, x = np.mgrid[0:fsize, 0:fsize]
            mask = np.exp(-(((mid - y) ** 2) / (2 * (sigma ** 2))) - (((mid - x) ** 2) / (2 * (sigma ** 2)))) * \
                         np.exp(-(((temp[mid, mid] - temp[y, x]) ** 2) / (2 * (sigma_r ** 2))))
            mask /= np.sum(mask)

            dst[i, j] = np.sum(temp * mask)

    # 0~1 -> 0~255 범위로 변환
    dst = normalize(dst)

    return dst
'''