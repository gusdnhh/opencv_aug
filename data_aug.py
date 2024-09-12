# 1. 배경 : 흰색 책상, 우드 테이블
# 2. 데이터 증식 조건
#   2-0. 스마트폰으로 사진 촬영 후 이미지 크기를 줄여주자 (이미지 크기 : 224x224)
#        대상 촬영을 어떻게 해야할지 고민(이미지를 축소하면 물체가 잘 안 보일 수도 있음)
#   2-1. 회전(10~30도) 범위 안에서 어느정도 각도를 넣어야 인식이 잘 되는가?
#   2-2. hflip, vflip : 도움이 되는가? 넣을 것인가?
#   2-3. resize, crop : 가능하면 적용해 보자.
#   2-4. 파일명을 다르게 저장 cf) jelly_wood.jpg, jelly_white.jpg,
#                               jelly_wood_rot_15.jpg, jelly_wood_hflip.jpg, jelly_wood_resize.jpg
#   2-5. 클래스 별로 폴더를 생성
#   2-6. 데이터를 어떻게 넣느냐에 따라 어떻게 동작되는지 1~2줄로 요약

# 구성 순서
# 1. 촬영하기
# 2. 이미지를 컴퓨터로 복사, resize 한다.
# 3. 육안으로 확인, 이렇게 사용해도 되는가?
# 4. 함수들을 만든다. resive ,rotate, hflip, vflip, crop
#    원본 파일명을 읽어서 파일명을 생성하는 기능은 모든 함수에 있어야 한다.
# 5. 단일 함수를 검증
# 6. 함수를 활용해서 기능 구현
# 7. 테스트(경우의 수)
# 8. 데이터 셋을 teachable machine 사이트에 올려서 테스트
# 9. 인식이 잘 안되는 켕시를 분석하고 케이스를 추가, 구현된 기능을이용


# 파일이 들어있는 폴더를 넣음
# 첫번째 함수로 폴더에 있는 파일 목록을 리스트로 불러옴
# 1. 폴더 경로를 넣었을 때 파일 경로를 반환하는 함수
# 2. 파일 경로를 넣으면
#    리사이즈, 로테이트( -50 ~ 50) 해서 aug 폴더에 저장 ,

import cv2, sys
import numpy as np
import os
import glob


# 폴더 내 파일 경로 리스트를 반환하는 함수
def get_file_path_list(folder_path):
    file_path_list = glob.glob(os.path.join(folder_path, '*'))
    return file_path_list

# 이미지 리사이즈 후 저장하는 함수
def Aug_resized_img(img, width, height, filePath):
    resized_img = cv2.resize(img, (width, height), cv2.INTER_AREA)

    directory, filename = os.path.split(filePath)
    file_base, file_ext = os.path.splitext(filename)
    
    # 저장 폴더를 원본 폴더명에 '_aug'를 추가한 폴더로 변경
    new_directory = directory + '_aug'
    os.makedirs(new_directory, exist_ok=True)  # 폴더가 없으면 생성

    new_filename = f"{file_base}_resized{file_ext}"
    new_filepath = os.path.join(new_directory, new_filename)
    
    cv2.imwrite(new_filepath, resized_img)
    
    return resized_img
    
# 이미지 회전 후 저장하는 함수
def Aug_rotated_img(img, filePath):
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)

    # 저장 폴더를 원본 폴더명에 '_aug'를 추가한 폴더로 변경
    directory, filename = os.path.split(filePath)
    new_directory = directory + '_aug'
    os.makedirs(new_directory, exist_ok=True)  # 폴더가 없으면 생성

    for angle in range(-50, 0, 10):
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated_img = cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REPLICATE)

        file_base, file_ext = os.path.splitext(filename)
        new_filename = f"{file_base}_rot_{angle}{file_ext}"
        new_filepath = os.path.join(new_directory, new_filename)
        
        cv2.imwrite(new_filepath, rotated_img)
        
    for angle in range(10, 51, 10):
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated_img = cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REPLICATE)

        file_base, file_ext = os.path.splitext(filename)
        new_filename = f"{file_base}_rot_{angle}{file_ext}"
        new_filepath = os.path.join(new_directory, new_filename)
        
        cv2.imwrite(new_filepath, rotated_img)

# 이미지 플립 후 저장하는 함수
def Aug_flipped_img(img, filePath):
    img = cv2.resize(img, (224, 224), cv2.INTER_AREA)

    Vflipped_img = cv2.flip(img, 0)  # 수직 플립
    Hflipped_img = cv2.flip(img, 1)  # 수평 플립
    VHflipped_img = cv2.flip(img, -1)  # 수직 + 수평 플립

    # 저장 폴더를 원본 폴더명에 '_aug'를 추가한 폴더로 변경
    directory, filename = os.path.split(filePath)
    new_directory = directory + '_aug'
    os.makedirs(new_directory, exist_ok=True)  # 폴더가 없으면 생성

    file_base, file_ext = os.path.splitext(filename)

    Vflipped_filename = f"{file_base}_VF{file_ext}"
    Hflipped_filename = f"{file_base}_HF{file_ext}"
    VHflipped_filename = f"{file_base}_VHF{file_ext}"

    Vflipped_filepath = os.path.join(new_directory, Vflipped_filename)
    Hflipped_filepath = os.path.join(new_directory, Hflipped_filename)
    VHflipped_filepath = os.path.join(new_directory, VHflipped_filename)

    cv2.imwrite(Vflipped_filepath, Vflipped_img)
    cv2.imwrite(Hflipped_filepath, Hflipped_img)
    cv2.imwrite(VHflipped_filepath, VHflipped_img)


# 폴더 경로 안에 있는 파일의 목록을 리스트로 불러옵니다
fileList = get_file_path_list('dataAug/sofa')

for filePath in fileList:
    
    # 원본 이미지를 불러옵니다.    
    img = cv2.imread(filePath)
    
    # 이미지의 크기를 (224,224)로 바꾸고 파일로 저장합니다.
    resized_img = Aug_resized_img(img, 244, 244, filePath)
    
    # 회전된 이미지를 파일을 생성합니다.
    Aug_rotated_img(resized_img, filePath)
    
    # 플립된 이미지파일을 생성합니다.
    Aug_flipped_img(resized_img, filePath)
