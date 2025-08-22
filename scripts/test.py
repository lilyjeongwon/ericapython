from pathlib import Path
import json
import pygame
import sys
import os
import random
import math
import time
import atexit

# 튜토리얼 스킵 관련 변수
skip_tutorial = False
skip_e_pressed = False
skip_e_start_time = 0
skip_e_duration = 1.0  # 1초

# 튜토리얼 스킵 UI 원 그리기 함수
def draw_skip_circle(screen, progress):
    x, y = screen.get_width() - 32, screen.get_height() - 32
    radius = 22
    thickness = 7
    # 폰트 설정 (기존 button_font가 있으면 사용, 없으면 기본)
    try:
        font = button_font
    except:
        font = pygame.font.SysFont('malgungothic', 20)
    # 문구 렌더링
    text = font.render('E를 눌러 스킵', True, (255, 255, 180))
    text_rect = text.get_rect(midright=(x - radius - 10, y))
    screen.blit(text, text_rect)
    # 위치와 크기 조정 (설정 아이콘과 겹치지 않게)
    x, y = screen.get_width() - 32, screen.get_height() - 32
    radius = 22
    thickness = 7
    color_yellow = (255, 220, 0)
    # 투명 Surface에 arc를 그림
    arc_surface = pygame.Surface((radius*2+thickness, radius*2+thickness), pygame.SRCALPHA)
    arc_rect = pygame.Rect(thickness//2, thickness//2, radius*2, radius*2)
    start_angle = -0.5 * math.pi
    if progress > 0:
        end_angle = start_angle + (2 * math.pi * progress)
        pygame.draw.arc(arc_surface, color_yellow, arc_rect, start_angle, end_angle, thickness)
    # arc_surface를 화면에 합성
    screen.blit(arc_surface, (x - radius - thickness//2, y - radius - thickness//2))

# --- 상대 경로를 위한 기본 경로 설정 ---
# 이 스크립트 파일이 위치한 디렉터리를 기준으로 경로를 설정합니다.
BASE_DIR = Path(__file__).resolve().parent.parent
# 예: "C:\Users\user\Project"
# 이렇게 하면 다른 컴퓨터로 프로젝트 폴더를 옮겨도 항상 올바른 경로를 찾습니다.
# ----------------------------------------

# 설정 파일 경로
SETTINGS_FILE = BASE_DIR / "settings.json"

# 기본 설정
DEFAULT_SETTINGS = {
    "volume": 1  # 기본 볼륨 (50%)
}

# 설정 저장 함수
def save_settings(settings):
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)
        print("설정이 저장되었습니다.")
    except Exception as e:
        print(f"설정 저장 중 오류 발생: {e}")

# 설정 로드 함수
def load_settings():
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"설정 로드 중 오류 발생: {e}")
    return DEFAULT_SETTINGS.copy()

# 설정 로드
settings = load_settings()

# Pygame 초기화
pygame.init()
pygame.mixer.init()
# 볼륨 설정
pygame.mixer.music.set_volume(settings["volume"])

# 게임 종료 시 설정 저장
def on_exit():
    save_settings(settings)

# 볼륨 변경 예시
def set_volume(new_volume):
    settings["volume"] = max(0.0, min(1.0, new_volume))  # 0.0 ~ 1.0 범위로 제한
    pygame.mixer.music.set_volume(settings["volume"])
    print(f"볼륨이 {settings['volume'] * 100:.0f}%로 설정되었습니다.")

# 게임 종료 시 호출

atexit.register(on_exit)
# Pygame 초기화
pygame.init()
pygame.mixer.init()

# 화면 설정
WIDTH, HEIGHT = 1100, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("농장 시뮬레이터") # 캡션 변경

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0) # 다 자란 작물 테두리 색상
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
TOOL_DISABLED_COLOR = (100, 100, 100)
BROWN = (139, 69, 19)
TAB_INACTIVE_COLOR = (100, 100, 100) # 탭 비활성화 색상
TAB_ACTIVE_COLOR = (70, 70, 70) # 탭 활성화 색상

# 메인 화면 영역
middle_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)

image_names = ["a.png"]
images = []
for name in image_names:
    path = BASE_DIR / "assets" / "images" / name
    try:
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, (WIDTH, HEIGHT))
        images.append(img)
    except pygame.error as e:
        print(f"이미지 로드 오류 {path}: {e}")
        print("이미지 파일이 'assets/images' 폴더에 있는지 확인하세요.")
        sys.exit()

title_background_image = None
title_bg_path = BASE_DIR / "assets" / "images" / "title_bg.png"
try:
    title_background_image = pygame.image.load(title_bg_path)
    title_background_image = pygame.transform.scale(title_background_image, (WIDTH, HEIGHT))
except pygame.error as e:
    print(f"타이틀 배경 이미지 로드 오류 {title_bg_path}: {e}")
    print("타이틀 배경 이미지 파일이 'assets/images' 폴더에 있는지 확인하세요. (예: title_bg.png)")

settings_icon = None
settings_icon_path = BASE_DIR / "assets" / "images" / "settings_icon.png"
SETTINGS_ICON_SIZE = 50
try:
    settings_icon = pygame.image.load(settings_icon_path)
    settings_icon = pygame.transform.scale(settings_icon, (SETTINGS_ICON_SIZE, SETTINGS_ICON_SIZE))
except pygame.error as e:
    print(f"설정 아이콘 로드 오류 {settings_icon_path}: {e}")
    print("설정 아이콘 파일이 'assets/images' 폴더에 있는지 확인하세요. (예: settings_icon.png)")

TOOL_ICON_SIZE = 100
TOOL_BORDER_THICKNESS = 4
PLOT_BORDER_THICKNESS = 4 # 밭/화분 테두리 두께

watering_can_image = None # 기존 물뿌리개 이미지 (기본 도구 아이콘)
watering_can_path = BASE_DIR / "assets" / "images" / "watering_can.png"
try:
    watering_can_image = pygame.image.load(watering_can_path)
    watering_can_image = pygame.transform.scale(watering_can_image, (TOOL_ICON_SIZE, TOOL_ICON_SIZE))
except pygame.error as e:
    print(f"물뿌리개 이미지 로드 오류 {watering_can_path}: {e}")
    print("물뿌리개 이미지 파일이 'assets/images' 폴더에 있는지 확인하세요.")

scythe_image = None # 기존 낫 이미지 (기본 도구 아이콘)
scythe_path = BASE_DIR / "assets" / "images" / "scythe.png"
try:
    scythe_image = pygame.image.load(scythe_path)
    scythe_image = pygame.transform.scale(scythe_image, (TOOL_ICON_SIZE, TOOL_ICON_SIZE))
except pygame.error as e:
    print(f"낫 이미지 로드 오류 {scythe_path}: {e}")
    print("낫 이미지 파일이 'assets/images' 폴더에 있는지 확인하세요.")

seed_select_button_image = None
seed_select_button_path = BASE_DIR / "assets" / "images" / "seed_button.png"
try:
    seed_select_button_image = pygame.image.load(seed_select_button_path)
    seed_select_button_image = pygame.transform.scale(seed_select_button_image, (TOOL_ICON_SIZE, TOOL_ICON_SIZE))
except pygame.error as e:
    print(f"씨앗 선택 버튼 이미지 로드 오류 {seed_select_button_path}: {e}")
    print("씨앗 선택 버튼 이미지 파일이 'assets/images' 폴더에 있는지 확인하세요.")

# 개별 씨앗 이미지 로드 및 크기 설정 (파일 이름 변경 반영)
seed_sunflower_image = None
seed_lettuce_image = None
seed_potato_image = None
seed_pea_image = None
seed_dragonfruit_image = None

try:
    seed_sunflower_image = pygame.image.load(BASE_DIR / "assets" / "images" / "seed_sunflower.png")
    seed_sunflower_image = pygame.transform.scale(seed_sunflower_image, (TOOL_ICON_SIZE, TOOL_ICON_SIZE))
    seed_lettuce_image = pygame.image.load(BASE_DIR / "assets" / "images" / "seed_lettuce.png")
    seed_lettuce_image = pygame.transform.scale(seed_lettuce_image, (TOOL_ICON_SIZE, TOOL_ICON_SIZE))
    seed_potato_image = pygame.image.load(BASE_DIR / "assets" / "images" / "seed_potato.png")
    seed_potato_image = pygame.transform.scale(seed_potato_image, (TOOL_ICON_SIZE, TOOL_ICON_SIZE))
    seed_pea_image = pygame.image.load(BASE_DIR / "assets" / "images" / "seed_pea.png")
    seed_pea_image = pygame.transform.scale(seed_pea_image, (TOOL_ICON_SIZE, TOOL_ICON_SIZE))
    seed_dragonfruit_image = pygame.image.load(BASE_DIR / "assets" / "images" / "seed_dragonfruit.png")
    seed_dragonfruit_image = pygame.transform.scale(seed_dragonfruit_image, (TOOL_ICON_SIZE, TOOL_ICON_SIZE))
except pygame.error as e:
    print(f"씨앗 이미지 로드 오류: {e}")
    print("모든 씨앗 이미지 파일이 'assets/images' 폴더에 있는지 확인하세요. (예: seed_sunflower.png)")

# 씨앗 이름 (변수명 그대로 유지, 파일 이름과 구분)
seed_sunflower_name = "해바라기 씨앗"
seed_lettuce_name = "상추 씨앗"
seed_potato_name = "감자 씨앗"
seed_pea_name = "완두콩 씨앗"
seed_dragonfruit_name = "용과 씨앗"

# 식물 성장 프레임 정의 (각 씨앗별 도달해야 하는 총 성장 프레임 수)
plant_sunflower_growth_frames = 30
plant_lettuce_growth_frames = 35
plant_potato_growth_frames = 45
plant_pea_growth_frames = 60
plant_dragonfruit_growth_frames = 100

# 식물 이미지 로드 (파일 이름 변경 반영)
# 이제 여기에 로드되는 이미지는 "원본" 즉, 완전히 자란 상태의 풀 사이즈 이미지입니다.
plant_sunflower_image_original = None
plant_lettuce_image_original = None
plant_potato_image_original = None
plant_pea_image_original = None
plant_dragonfruit_image_original = None

try:
    plant_sunflower_image_original = pygame.image.load(BASE_DIR / "assets" / "images" / "plant_sunflower.png").convert_alpha()
    plant_lettuce_image_original = pygame.image.load(BASE_DIR / "assets" / "images" / "plant_lettuce.png").convert_alpha()
    plant_potato_image_original = pygame.image.load(BASE_DIR / "assets" / "images" / "plant_potato.png").convert_alpha()
    plant_pea_image_original = pygame.image.load(BASE_DIR / "assets" / "images" / "plant_pea.png").convert_alpha()
    plant_dragonfruit_image_original = pygame.image.load(BASE_DIR / "assets" / "images" / "plant_dragonfruit.png").convert_alpha()
except pygame.error as e:
    print(f"식물 이미지 로드 오류: {e}")
    print(f"경고: 식물 이미지 파일이 'assets/images' 폴더에 있는지 확인하세요. (예: plant_sunflower.png)")

# 식물 정보를 딕셔너리로 관리하여 인덱스 대신 이름으로 접근할 수 있도록 함 (변수명 그대로 유지)
PLANT_INFO = {
    "sunflower": {
        "seed_image": seed_sunflower_image,
        "seed_name": seed_sunflower_name,
        "growth_frames": plant_sunflower_growth_frames,
        "plant_image_original": plant_sunflower_image_original # 원본 이미지 저장
    },
    "lettuce": {
        "seed_image": seed_lettuce_image,
        "seed_name": seed_lettuce_name,
        "growth_frames": plant_lettuce_growth_frames,
        "plant_image_original": plant_lettuce_image_original
    },
    "potato": {
        "seed_image": seed_potato_image,
        "seed_name": seed_potato_name,
        "growth_frames": plant_potato_growth_frames,
        "plant_image_original": plant_potato_image_original
    },
    "pea": {
        "seed_image": seed_pea_image,
        "seed_name": seed_pea_name,
        "growth_frames": plant_pea_growth_frames,
        "plant_image_original": plant_pea_image_original
    },
    "dragonfruit": {
        "seed_image": seed_dragonfruit_image,
        "seed_name": seed_dragonfruit_name,
        "growth_frames": plant_dragonfruit_growth_frames,
        "plant_image_original": plant_dragonfruit_image_original
    },
}

# + 모양 이미지 로드 및 크기 설정
plus_sign_image = None
PLUS_SIGN_SIZE = 40 # Adjust this value to change the size of the plus sign
try:
    # Assuming the user provided image is named 'plus_sign.png' and is in assets/images
    plus_sign_path = BASE_DIR / "assets" / "images" / "plus_sign.png"
    plus_sign_image = pygame.image.load(plus_sign_path).convert_alpha()
    plus_sign_image = pygame.transform.scale(plus_sign_image, (PLUS_SIGN_SIZE, PLUS_SIGN_SIZE))
except pygame.error as e:
    print(f"플러스 사인 이미지 로드 오류 {plus_sign_path}: {e}")
    print("플러스 사인 이미지 파일이 'assets/images' 폴더에 있는지 확인하세요. (예: plus_sign.png)")


# 배경 음악 파일 경로
music_files = [
    BASE_DIR / "assets" / "sounds" / "bgm1.mp3", # 'music'을 'sounds'로 변경
    BASE_DIR / "assets" / "sounds" / "bgm2.mp3", # 'music'을 'sounds'로 변경
    BASE_DIR / "assets" / "sounds" / "bgm3.mp3", # 'music'을 'sounds'로 변경
]

# 효과음 파일 경로 (MP3로 변경)
scythe_harvest_sound = None
scythe_harvest_sound_path = BASE_DIR / "assets" / "sounds" / "harvest.mp3" # harvest.mp3로 변경
try:
    scythe_harvest_sound = pygame.mixer.Sound(scythe_harvest_sound_path)
except pygame.error as e:
    print(f"수확 효과음 로드 오류 {scythe_harvest_sound_path}: {e}")
    print("수확 효과음 파일이 'assets/sounds' 폴더에 있는지 확인하세요. (예: harvest.mp3)")

purchase_success_sound = None
purchase_success_sound_path = BASE_DIR / "assets" / "sounds" / "purchase_success.mp3" # 구매 성공 효과음
try:
    purchase_success_sound = pygame.mixer.Sound(purchase_success_sound_path)
except pygame.error as e:
    print(f"구매 성공 효과음 로드 오류 {purchase_success_sound_path}: {e}")
    print("구매 성공 효과음 파일이 'assets/sounds' 폴더에 있는지 확인하세요. (예: purchase_success.mp3)")

purchase_fail_sound = None
purchase_fail_sound_path = BASE_DIR / "assets" / "sounds" / "purchase_fail.mp3" # 구매 실패 효과음
try:
    purchase_fail_sound = pygame.mixer.Sound(purchase_fail_sound_path)
except pygame.error as e:
    print(f"구매 실패 효과음 로드 오류 {purchase_fail_sound_path}: {e}")
    print("구매 실패 효과음 파일이 'assets/sounds' 폴더에 있는지 확인하세요. (예: purchase_fail.mp3)")

# 현재 일차
total_days_passed = 0

def save_game(filename="save_data.json"):
    # 저장할 데이터 구조 확장: 소유/장착 장비, 날짜, 돈, 볼륨, 밭/화분 상태
    data = {
        "player_inventory": player_inventory,
        "player_tools": player_tools,
        "equipped_tools": {
            "watering_can": player_tools.get("watering_can", {}).get("id", ""),
            "scythe": player_tools.get("scythe", {}).get("id", "")
        },
        "date": {
            "year": current_year,
            "month": current_month,
            "day": current_day
        },
        "player_money": player_money,
        "volume": {
            "master": master_volume,
            "music": music_volume,
            "sfx": sfx_volume
        },
        "fields": [
            {
                "planted_plant_type": f.get("planted_plant_type"),
                "current_growth_frame": f.get("current_growth_frame"),
                "final_scale_factor": f.get("final_scale_factor")
            } for f in field_states
        ],
        "pots": [
            {
                "planted_plant_type": p.get("planted_plant_type"),
                "current_growth_frame": p.get("current_growth_frame"),
                "final_scale_factor": p.get("final_scale_factor")
            } for p in pot_states
        ]
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    # 볼륨 설정도 별도 settings.json에 저장
    save_settings(settings)

def load_game(filename="save_data.json"):
    global player_inventory, player_tools, current_year, current_month, current_day, player_money, master_volume, music_volume, sfx_volume, field_states, pot_states
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            player_inventory = data.get("player_inventory", player_inventory)
            player_tools = data.get("player_tools", player_tools)
            eq = data.get("equipped_tools", {})
            if "watering_can" in eq:
                player_tools["watering_can"]["id"] = eq["watering_can"]
                # 이어하기 시 물뿌리개 이미지 업데이트
                for t in tool_shop_items["watering_can"]:
                    if t["id"] == eq["watering_can"]:
                        global watering_can_image
                        if t["image"]:
                            watering_can_image = pygame.transform.scale(t["image"], (TOOL_ICON_SIZE, TOOL_ICON_SIZE))
                        break
            if "scythe" in eq:
                player_tools["scythe"]["id"] = eq["scythe"]
                # 이어하기 시 낫 이미지 업데이트
                for t in tool_shop_items["scythe"]:
                    if t["id"] == eq["scythe"]:
                        global scythe_image
                        if t["image"]:
                            scythe_image = pygame.transform.scale(t["image"], (TOOL_ICON_SIZE, TOOL_ICON_SIZE))
                        break
            date = data.get("date", {})
            current_year = date.get("year", current_year)
            current_month = date.get("month", current_month)
            current_day = date.get("day", current_day)
            player_money = data.get("player_money", player_money)
            vol = data.get("volume", {})
            master_volume = vol.get("master", master_volume)
            music_volume = vol.get("music", music_volume)
            sfx_volume = vol.get("sfx", sfx_volume)
            # 볼륨 값이 1보다 크면(0~100 정수로 저장된 경우) 100으로 나눔
            if master_volume > 1:
                master_volume /= 100
            if music_volume > 1:
                music_volume /= 100
            if sfx_volume > 1:
                sfx_volume /= 100
            fields = data.get("fields", [])
            for i, f in enumerate(fields):
                if i < len(field_states):
                    field_states[i]["planted_plant_type"] = f.get("planted_plant_type")
                    field_states[i]["current_growth_frame"] = f.get("current_growth_frame", 0)
                    field_states[i]["final_scale_factor"] = f.get("final_scale_factor", 1.0)
            pots = data.get("pots", [])
            for i, p in enumerate(pots):
                if i < len(pot_states):
                    pot_states[i]["planted_plant_type"] = p.get("planted_plant_type")
                    pot_states[i]["current_growth_frame"] = p.get("current_growth_frame", 0)
                    pot_states[i]["final_scale_factor"] = p.get("final_scale_factor", 1.0)
    except FileNotFoundError:
        print("저장 파일이 없습니다. 새 게임을 시작합니다.")

    # 볼륨 슬라이더 위치도 볼륨 값에 맞게 항상 갱신
    global master_vol_knob_x, master_vol_knob_rect, music_vol_knob_x, music_vol_knob_rect, sfx_vol_knob_x, sfx_vol_knob_rect
    master_vol_knob_x = master_vol_slider_x + int(master_volume * SLIDER_WIDTH)
    master_vol_knob_rect = pygame.Rect(master_vol_knob_x - KNOB_RADIUS, master_vol_slider_y + SLIDER_HEIGHT // 2 - KNOB_RADIUS, KNOB_RADIUS * 2, KNOB_RADIUS * 2)
    music_vol_knob_x = music_vol_slider_x + int(music_volume * SLIDER_WIDTH)
    music_vol_knob_rect = pygame.Rect(music_vol_knob_x - KNOB_RADIUS, music_vol_slider_y + SLIDER_HEIGHT // 2 - KNOB_RADIUS, KNOB_RADIUS * 2, KNOB_RADIUS * 2)
    sfx_vol_knob_x = sfx_vol_slider_x + int(sfx_volume * SLIDER_WIDTH)
    sfx_vol_knob_rect = pygame.Rect(sfx_vol_knob_x - KNOB_RADIUS, sfx_vol_slider_y + SLIDER_HEIGHT // 2 - KNOB_RADIUS, KNOB_RADIUS * 2, KNOB_RADIUS * 2)

    # 이어하기 시 볼륨 값이 실제 소리에 즉시 반영되도록
    apply_volume()



# 게임 속도 및 시간 관리
clock = pygame.time.Clock()

# 게임 데이터 (돈, 날짜)
player_money = 10000

start_year = 2025
start_month = 3
start_day = 1

current_year = start_year
current_month = start_month
current_day = start_day

# 월별 일수 정보
days_in_month_base = {
    1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
    7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
}

def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def get_days_in_month(year, month):
    if month == 2 and is_leap_year(year):
        return 29
    return days_in_month_base[month]

DAY_CHANGE_INTERVAL = 10
last_day_change_time = time.time()
fast_growth_mode = False # F1 키로 토글될 빠른 성장 모드

# 폰트 설정
font_name = "Galmuri14.ttf" # 사용하려는 폰트 파일 이름으로 변경하세요 (예: NanumGothicCoding.ttf)
font_path = BASE_DIR / "assets" / "fonts" / font_name # 'assets/fonts/' 폴더에 폰트를 넣었을 경우

try:
    font = pygame.font.Font(font_path, 30)
    price_text_font = pygame.font.Font(font_path, 25) # 가격 텍스트 폰트
    multiplier_text_font = pygame.font.Font(font_path, 20) # 배율 텍스트 폰트
    title_font = pygame.font.Font(font_path, 70)
    ingame_button_font = pygame.font.Font(font_path, 25) #버튼 폰트
    button_font = pygame.font.Font(font_path, 35)
    settings_title_font = pygame.font.Font(font_path, 50)
    volume_label_font = pygame.font.Font(font_path, 30)
    shop_title_font = pygame.font.Font(font_path, 50)
    seed_name_font = pygame.font.Font(font_path, 20)
    cooldown_font = pygame.font.Font(font_path, 40)
    tool_shop_title_font = pygame.font.Font(font_path, 25) # 제작대 -> 도구상점 폰트 변경
    tool_shop_pirce_font = pygame.font.Font(font_path, 25) # 도구 상점 가격 폰트
    description_font = pygame.font.Font(font_path, 18) # 새로 추가된 설명 폰트
except FileNotFoundError:
    print(f"오류: 폰트 파일을 찾을 수 없습니다. 경로를 확인하세요: {font_path}")
    print("시스템에 맑은 고딕이 없거나, 다른 OS를 사용한다면 적절한 한글 폰트 경로로 변경하거나,")
    print("프로젝트 폴더에 .ttf 폰트 파일을 넣고 그 경로를 사용해 주세요.")
    # 폰트 파일을 찾을 수 없을 때 대체 폰트 사용 (한글 폰트가 지원되는 시스템 폰트)
    font = pygame.font.SysFont('malgungothic', 30)
    price_text_font = pygame.font.SysFont('malgungothic', 25) # 가격 텍스트 폰트
    multiplier_text_font = pygame.font.SysFont('malgungothic', 20) # 배율 텍스트 폰트
    title_font = pygame.font.SysFont('malgungothic', 70)
    button_font = pygame.font.SysFont('malgungothic', 40)
    settings_title_font = pygame.font.SysFont('malgungothic', 50)
    volume_label_font = pygame.font.SysFont('malgungothic', 30)
    shop_title_font = pygame.font.SysFont('malgungothic', 50)
    seed_name_font = pygame.font.SysFont('malgungothic', 20)
    cooldown_font = pygame.font.SysFont('malgungothic', 40)
    tool_shop_title_font = pygame.font.SysFont('malgungothic', 50) # 대체 폰트도 함께 설정
    tool_shop_pirce_font = pygame.font.SysFont('malgungothic', 20) # 도구 상점 가격 폰트
    description_font = pygame.font.SysFont('malgungothic', 18) # 대체 폰트도 함께 설정
except Exception as e:
    print(f"폰트 로드 중 알 수 없는 오류 발생: {e}")
    # 다른 오류 발생 시 시스템 폰트 사용
    font = pygame.font.SysFont('malgungothic', 30)
    title_font = pygame.font.SysFont('malgungothic', 70)
    button_font = pygame.font.SysFont('malgungothic', 40)
    settings_title_font = pygame.font.SysFont('malgungothic', 50)
    volume_label_font = pygame.font.SysFont('malgungothic', 30)
    shop_title_font = pygame.font.SysFont('malgungothic', 50)
    seed_name_font = pygame.font.SysFont('malgungothic', 20)
    cooldown_font = pygame.font.SysFont('malgungothic', 40)
    tool_shop_title_font = pygame.font.SysFont('malgungothic', 50) # 대체 폰트도 함께 설정
    tool_shop_pirce_font = pygame.font.SysFont('malgungothic', 20) # 도구 상점 가격 폰트
    description_font = pygame.font.SysFont('malgungothic', 18) # 대체 폰트도 함께 설정

# --- 사운드 볼륨 변수 및 초기 설정 ---
master_volume = 1
music_volume = 1
sfx_volume = 1 # 새로운 효과음 볼륨 변수

is_music_paused_by_code = False
EPSILON = 0.001
current_playing_music_path = None

def apply_volume():
    global is_music_paused_by_code
    global current_playing_music_path

    current_final_music_volume = master_volume * music_volume
    if abs(current_final_music_volume) < EPSILON:
        current_final_music_volume = 0.0

    music_loaded_and_playable = (pygame.mixer.music.get_pos() != -1)

    if music_loaded_and_playable and current_final_music_volume == 0 and not is_music_paused_by_code:
        pygame.mixer.music.pause()
        is_music_paused_by_code = True

    elif music_loaded_and_playable and current_final_music_volume > 0 and is_music_paused_by_code:
        if current_playing_music_path and not pygame.mixer.music.get_busy():
            try:
                pygame.mixer.music.load(current_playing_music_path)
                pygame.mixer.music.play()
                pygame.mixer.music.set_endevent(MUSIC_END_EVENT)
                is_music_paused_by_code = False
            except pygame.error as e:
                print(f"DEBUG ERROR: 음악 재시작 실패: {e}")
        else:
            pygame.mixer.music.unpause()
            is_music_paused_by_code = False

    pygame.mixer.music.set_volume(current_final_music_volume)

    # 효과음 볼륨 적용 (사운드가 로드된 경우에만)
    if scythe_harvest_sound:
        scythe_harvest_sound.set_volume(master_volume * sfx_volume)
    if purchase_success_sound:
        purchase_success_sound.set_volume(master_volume * sfx_volume)
    if purchase_fail_sound:
        purchase_fail_sound.set_volume(master_volume * sfx_volume)


apply_volume()
# --- 여기까지 사운드 볼륨 변수 및 초기 설정 ---

# 게임 상태 관리
game_state = 'TITLE'
previous_game_state = 'TITLE' # 설정, 상점 등 닫았을 때 돌아갈 상태
show_tutorial = False  # 튜토리얼 오버레이 상태

# 튜토리얼 단계 관리 변수 추가
tutorial_step = 1  # 1: 씨앗 목록 버튼 클릭 안내, 2: 씨앗1(해바라기) 클릭 안내

# 시작 버튼 설정
start_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 70)  # 처음부터 버튼
continue_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 140, 200, 70)  # 이어하기 버튼

def play_random_music():
    global is_music_paused_by_code
    global current_playing_music_path
    if not music_files:
        print("재생할 음악 파일이 없습니다.")
        return

    selected_music = random.choice(music_files)
    current_playing_music_path = selected_music

    try:
        pygame.mixer.music.load(selected_music)
        pygame.mixer.music.play()
        is_music_paused_by_code = False
        apply_volume()
        print(f"음악 재생 시작: {Path(selected_music).name}")
    except pygame.error as e:
        print(f"음악 재생 오류: {e}")
        print(f"파일 경로 확인: {selected_music}")

MUSIC_END_EVENT = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSIC_END_EVENT)

# --- 설정 화면 관련 변수 ---
settings_panel_rect = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 250, 400, 500)
close_button_rect = pygame.Rect(settings_panel_rect.right - 40, settings_panel_rect.top + 10, 30, 30) # 설정 닫기 버튼 기준

SLIDER_WIDTH = 250
SLIDER_HEIGHT = 10
KNOB_RADIUS = 15

master_vol_slider_x = settings_panel_rect.centerx - SLIDER_WIDTH // 2
master_vol_slider_y = settings_panel_rect.top + 150
master_vol_slider_rect = pygame.Rect(master_vol_slider_x, master_vol_slider_y, SLIDER_WIDTH, SLIDER_HEIGHT)
master_vol_knob_x = master_vol_slider_x + int(master_volume * SLIDER_WIDTH)
master_vol_knob_rect = pygame.Rect(master_vol_knob_x - KNOB_RADIUS, master_vol_slider_y + SLIDER_HEIGHT // 2 - KNOB_RADIUS, KNOB_RADIUS * 2, KNOB_RADIUS * 2)

music_vol_slider_x = settings_panel_rect.centerx - SLIDER_WIDTH // 2
music_vol_slider_y = settings_panel_rect.top + 250
music_vol_slider_rect = pygame.Rect(music_vol_slider_x, music_vol_slider_y, SLIDER_WIDTH, SLIDER_HEIGHT)
music_vol_knob_x = music_vol_slider_x + int(music_volume * SLIDER_WIDTH)
music_vol_knob_rect = pygame.Rect(music_vol_knob_x - KNOB_RADIUS, music_vol_slider_y + SLIDER_HEIGHT // 2 - KNOB_RADIUS, KNOB_RADIUS * 2, KNOB_RADIUS * 2)

# 효과음 볼륨 슬라이더 변수
sfx_vol_slider_x = settings_panel_rect.centerx - SLIDER_WIDTH // 2
sfx_vol_slider_y = settings_panel_rect.top + 350 # 기존 슬라이더보다 아래에 위치
sfx_vol_slider_rect = pygame.Rect(sfx_vol_slider_x, sfx_vol_slider_y, SLIDER_WIDTH, SLIDER_HEIGHT)
sfx_vol_knob_x = sfx_vol_slider_x + int(sfx_volume * SLIDER_WIDTH)
sfx_vol_knob_rect = pygame.Rect(sfx_vol_knob_x - KNOB_RADIUS, sfx_vol_slider_y + SLIDER_HEIGHT // 2 - KNOB_RADIUS, KNOB_RADIUS * 2, KNOB_RADIUS * 2)


is_dragging_master_vol = False
is_dragging_music_vol = False
is_dragging_sfx_vol = False # 효과음 볼륨 드래그 상태 변수
# --- 여기까지 설정 화면 관련 변수 ---

# --- 상점 및 도구 상점 버튼 관련 변수 ---
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 60
BUTTON_MARGIN = 10

shop_button_rect = pygame.Rect(WIDTH - BUTTON_WIDTH - BUTTON_MARGIN,
                               HEIGHT // 2 - BUTTON_HEIGHT - BUTTON_MARGIN // 2,
                               BUTTON_WIDTH, BUTTON_HEIGHT)

tool_shop_button_rect = pygame.Rect(WIDTH - BUTTON_WIDTH - BUTTON_MARGIN,
                               shop_button_rect.bottom + BUTTON_MARGIN,
                               BUTTON_WIDTH, BUTTON_HEIGHT)

# 상점 스크롤 관련 변수 (다른 전역 변수들 아래에 추가)
shop_scroll_offset = 0 # 현재 스크롤 위치. 음수 값은 아래로 스크롤되었음을 의미
SHOP_SCROLL_SPEED = 30 # 마우스 휠 스크롤 속도
is_dragging_scrollbar = False # 스크롤바 핸들 드래그 중인지 여부
scrollbar_drag_offset_y = 0 # 스크롤바 핸들 드래그 시작 시 마우스와 핸들의 상대 위치
scrollbar_rect = None # 스크롤바 전체 영역 (매 프레임 업데이트될 수 있음)
scrollbar_handle_rect = None # 스크롤바 핸들 영역 (매 프레임 업데이트될 수 있음)

# 상점 패널 크기 및 위치 조정
SHOP_PANEL_WIDTH = 1000 # 가로 길이 더 늘림
SHOP_PANEL_HEIGHT = 600
shop_panel_rect = pygame.Rect(WIDTH // 2 - SHOP_PANEL_WIDTH // 2, HEIGHT // 2 - SHOP_PANEL_HEIGHT // 2, SHOP_PANEL_WIDTH, SHOP_PANEL_HEIGHT)

# 도구 상점 패널 (상점과 동일한 크기 및 위치)
TOOL_SHOP_PANEL_WIDTH = 1000
TOOL_SHOP_PANEL_HEIGHT = 600
tool_shop_panel_rect = pygame.Rect(WIDTH // 2 - TOOL_SHOP_PANEL_WIDTH // 2, HEIGHT // 2 - TOOL_SHOP_PANEL_HEIGHT // 2, TOOL_SHOP_PANEL_WIDTH, TOOL_SHOP_PANEL_HEIGHT)


# --- 여기까지 상점 및 판매 버튼 관련 변수 ---

# --- 도구 버튼 관련 변수 ---
TOOL_ICON_MARGIN = 20
TOOL_SPACING = 15

watering_can_rect = pygame.Rect(TOOL_ICON_MARGIN,
                                 HEIGHT - TOOL_ICON_SIZE - TOOL_ICON_MARGIN,
                                 TOOL_ICON_SIZE, TOOL_ICON_SIZE)

scythe_rect = pygame.Rect(watering_can_rect.right + TOOL_SPACING,
                          HEIGHT - TOOL_ICON_SIZE - TOOL_ICON_MARGIN,
                          TOOL_ICON_SIZE, TOOL_ICON_SIZE)

seed_select_button_rect = pygame.Rect(scythe_rect.right + TOOL_SPACING,
                                      HEIGHT - TOOL_ICON_SIZE - TOOL_ICON_MARGIN,
                                      TOOL_ICON_SIZE, TOOL_ICON_SIZE)

active_tool_on_click = None

WATERING_CAN_COOLDOWN = 2
last_watering_can_use_time = 0

show_seed_options = False
is_seed_animating = False
seed_animation_target_offset = 0.0
seed_animation_current_offset = 0.0
seed_animation_speed = 4.0 # 애니메이션 속도 증가

selected_seed_name = None # 선택된 씨앗의 이름을 저장 (예: "sunflower")

# --- 인벤토리 ---
# 씨앗 이름 (예: "sunflower") -> 수량
player_inventory = {
    "sunflower": 5,
    "lettuce": 5,
    "potato": 5,
    "pea": 5,
    "dragonfruit": 5
} # 초기 소지 씨앗

# 플레이어가 현재 소지한 도구 정보 (ID, 배율)
player_tools = {
    'watering_can': {'id': 'watering_can_rusted', 'multiplier': 1, 'owned_tool_ids': []},
    'scythe': {'id': 'sickle_cracked', 'multiplier': 1, 'owned_tool_ids': []} # 낫은 기본 배율 1로 시작
}


# --- 상점 아이템 데이터 (판매할 씨앗 정보) ---
# 가격은 임의로 설정합니다. 실제 게임에 맞춰 조정하세요.
shop_items = [
    {"plant_type": "sunflower", "name": PLANT_INFO["sunflower"]["seed_name"], "price": 2000, "image": PLANT_INFO["sunflower"]["seed_image"], "description": "해바라기가 만개를 하면 팔 수 있지않을까?"},
    {"plant_type": "lettuce", "name": PLANT_INFO["lettuce"]["seed_name"], "price": 16000, "image": PLANT_INFO["lettuce"]["seed_image"], "description": "꽤 쓸만한 작물일거 같다 1000개를 채집하면 30,000,000?"},
    {"plant_type": "potato", "name": PLANT_INFO["potato"]["seed_name"], "price": 25000, "image": PLANT_INFO["potato"]["seed_image"], "description": "감자는 '만'ㅎ을수록 좋다."},
    {"plant_type": "pea", "name": PLANT_INFO["pea"]["seed_name"], "price": 200000, "image": PLANT_INFO["pea"]["seed_image"], "description": "신비한 힘이 깃든거 같다."},
    {"plant_type": "dragonfruit", "name": PLANT_INFO["dragonfruit"]["seed_name"], "price": 5000000, "image": PLANT_INFO["dragonfruit"]["seed_image"], "description": "비싸지만 값어치는 하는 것 같다."},
]

# 파일 상단이나, load_tool_image 함수 호출 전에
SHOP_ITEM_IMAGE_SIZE = 128  # 원하는 이미지 크기로 설정 (예: 128x128 픽셀)

def load_tool_image(image_name):
    # 수정된 부분: BASE_DIR을 사용하여 경로 생성
    image_path = BASE_DIR / "assets" / "images" / image_name
    if not image_path.exists():
        # 기본 이미지 로드 또는 오류 처리
        return None # 또는 적절한 기본 이미지
    img = pygame.image.load(image_path).convert_alpha()
    return pygame.transform.scale(img, (SHOP_ITEM_IMAGE_SIZE, SHOP_ITEM_IMAGE_SIZE))

# --- 도구 상점 아이템 데이터 (물뿌리개와 낫) ---
# 이미지 로드를 위한 헬퍼 함수
def load_tool_image(filename):
    # 수정된 부분: BASE_DIR을 사용하여 경로 생성
    path = BASE_DIR / "assets" / "images" / filename
    try:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, (SHOP_ITEM_IMAGE_SIZE, SHOP_ITEM_IMAGE_SIZE))
    except pygame.error as e:
        print(f"도구 이미지 로드 오류 {path}: {e}")
        # 이미지 로드 실패 시 기본 이미지 반환 또는 None 반환
        return pygame.transform.scale(pygame.Surface((SHOP_ITEM_IMAGE_SIZE, SHOP_ITEM_IMAGE_SIZE)), (SHOP_ITEM_IMAGE_SIZE, SHOP_ITEM_IMAGE_SIZE)) # 빈 Surface 반환

tool_shop_items = {
    "watering_can": [
        {"id": "watering_can_rusted", "name": "녹슨 물뿌리개", "price": 0, "multiplier": 1, "description": "오래되어 녹이 슨 물뿌리개입니다. 물을 줍니다.", "image": load_tool_image("watering_can_rusted.png") if (BASE_DIR / "assets" / "images" / "watering_can_rusted.png").exists() else watering_can_image},
        {"id": "watering_can_basic", "name": "기본 물뿌리개", "price": 50000, "multiplier": 2, "description": "기본적으로 제공되는 물뿌리개입니다. 물을 줍니다.", "image": load_tool_image("watering_can_tier1.png")},
        {"id": "watering_can_good", "name": "조금 쓸만한 물뿌리개", "price": 200000, "multiplier": 4, "description": "조금 더 강력해진 물뿌리개입니다. 물을 더 많이 줍니다.", "image": load_tool_image("watering_can_tier2.png")},
        {"id": "watering_can_better", "name": "좋아진 물뿌리개", "price": 1000000, "multiplier": 8, "description": "성능이 향상된 물뿌리개입니다. 작물 성장을 촉진합니다.", "image": load_tool_image("watering_can_tier3.png")},
        {"id": "watering_can_powerful", "name": "강력해진 물뿌리개", "price": 5000000, "multiplier": 16, "description": "매우 강력한 물뿌리개입니다. 기적적인 성장을 가능케 합니다.", "image": load_tool_image("watering_can_tier4.png")},
        {"id": "watering_can_masterpiece", "name": "장인이 만든 물뿌리개", "price": 20000000, "multiplier": 32, "description": "장인의 손길이 닿은 명품 물뿌리개입니다. 성장의 극치를 보여줍니다.", "image": load_tool_image("watering_can_tier5.png")},
        {"id": "watering_can_legendary", "name": "전설의 물뿌리개", "price": 100000000, "multiplier": 64, "description": "전설 속에서만 전해지던 물뿌리개입니다. 전체 밭에 영향을 줍니다.", "image": load_tool_image("watering_can_tier6.png")},
    ],
    "scythe": [
        {"id": "sickle_cracked", "name": "금이 간 낫", "price": 0, "multiplier": 1, "description": "금이가서 위태로워 보이는 낫입니다. 수확에 사용합니다.", "image": load_tool_image("sickle_cracked.png") if (BASE_DIR / "assets" / "images" / "sickle_cracked.png").exists() else scythe_image}, # 기본 낫은 가격 0
        {"id": "scythe_basic", "name": "기본 낫", "price": 0, "multiplier": 1, "description": "기본적으로 제공되는 낡은 낫입니다. 수확에 사용됩니다.", "image": load_tool_image("scythe_tier1.png")},
        {"id": "scythe_decent", "name": "조금 쓸만한 낫", "price": 150000, "multiplier": 1.5, "description": "날이 잘 선 낫입니다. 조금 더 많은 수확물을 얻을 수 있습니다.", "image": load_tool_image("scythe_tier2.png")},
        {"id": "scythe_normal", "name": "평범한 낫", "price": 1000000, "multiplier": 2, "description": "무난하게 사용할 수 있는 낫입니다. 안정적인 수확량에 기여합니다.", "image": load_tool_image("scythe_tier3.png")},
        {"id": "scythe_improved", "name": "좋아진 낫", "price": 5000000, "multiplier": 2.5, "description": "수확 효율이 눈에 띄게 좋아진 낫입니다. 농가의 희망이죠.", "image": load_tool_image("scythe_tier4.png")},
        {"id": "scythe_abandoned_master", "name": "장인이 쓰다 버린 낫", "price": 20000000, "multiplier": 4, "description": "장인이 더 이상 사용하지 않아 버려진 낫입니다. 엄청난 힘이 숨겨져 있습니다.", "image": load_tool_image("scythe_tier5.png")},
        {"id": "scythe_omniblade", "name": "모든걸 베어버릴것 같은 낫", "price": 100000000, "multiplier": 6, "description": "강력한 힘이 느껴지는 낫입니다. 베지 못할 것이 없습니다.", "image": load_tool_image("scythe_tier6.png")},
        {"id": "scythe_legendary", "name": "전설의 낫", "price": 500000000, "multiplier": 10, "description": "전설 속에 등장하는 낫입니다. 모든 작물을 풍요롭게 만듭니다.", "image": load_tool_image("scythe_tier7.png")},
    ]
}

# 상점 스크롤 관련 변수
shop_scroll_offset = 0
SHOP_SCROLL_SPEED = 20 # 한 번 스크롤할 때 이동할 픽셀 수

# 상점 패널 내 아이템 목록 영역을 전역 변수로 선언 (이벤트 처리에서 사용하기 위함)
shop_item_list_rect = pygame.Rect(0, 0, 0, 0) # 초기화

# 도구 상점 스크롤 관련 변수
tool_shop_scroll_offset = 0
tool_shop_item_list_rect = pygame.Rect(0, 0, 0, 0) # 초기화
selected_tool_category = "watering_can" # 기본적으로 물뿌리개 탭이 선택

# 상점 UI 레이아웃을 위한 변수
SHOP_ITEM_HEIGHT = 100
SHOP_ITEM_PADDING = 10
SHOP_ITEM_IMAGE_SIZE = 60
SHOP_RIGHT_PANEL_WIDTH_RATIO = 0.35 # 오른쪽 패널이 전체 패널 너비에서 차지하는 비율
# SHOP_RIGHT_PANEL_WIDTH는 SHOP_PANEL_WIDTH에 따라 동적으로 계산됩니다.

# 선택된 아이템 (상세 정보를 표시하기 위함)
selected_shop_item_index = -1
selected_tool_shop_item_index = -1

# 구매 버튼
buy_button_rect = pygame.Rect(0, 0, 120, 50) # 위치는 draw_shop_screen에서 계산

class TemporaryMessageDisplay:
    def __init__(self, text_or_parts, center_pos_tuple, duration=2.0, color=BLACK, font=None, is_multi_colored=False):
        # 텍스트가 화면 위쪽에서 나오도록 center_pos_tuple을 사용
        self.center_pos = center_pos_tuple
        self.duration = duration
        self.fade_in_duration = duration * 0.4
        self.hold_duration = duration * 0.2
        self.fade_out_duration = duration * 0.4
        self.font = font
        self.start_time = time.time()
        self.alpha = 0
        self.done = False
        self.is_multi_colored = is_multi_colored
        if self.is_multi_colored:
            # text_or_parts is a list of (text_string, color_tuple)
            self.text_parts = text_or_parts
        else:
            # text_or_parts is a single string, convert to consistent format
            self.text_parts = [(text_or_parts, color)]

    def update(self):
        if self.done:
            return
        elapsed_time = time.time() - self.start_time
        if elapsed_time < self.fade_in_duration:
            self.alpha = int(255 * (elapsed_time / self.fade_in_duration))
        elif elapsed_time < self.fade_in_duration + self.hold_duration:
            self.alpha = 255
        elif elapsed_time < self.duration:
            fade_out_elapsed = elapsed_time - (self.fade_in_duration + self.hold_duration)
            self.alpha = int(255 * (1 - (fade_out_elapsed / self.fade_out_duration)))
        else:
            self.alpha = 0
            self.done = True

    def draw(self, surface):
        if self.done:
            return

        # Calculate total width to center the multi-part text
        total_width = 0
        rendered_parts = []
        for text_part, part_color in self.text_parts:
            part_surface = self.font.render(text_part, True, part_color)
            total_width += part_surface.get_width()
            rendered_parts.append(part_surface)

        start_x = self.center_pos[0] - total_width // 2
        current_x = start_x
        for part_surface in rendered_parts:
            part_surface.set_alpha(self.alpha)
            surface.blit(part_surface, (current_x, self.center_pos[1] - part_surface.get_height() // 2))
            current_x += part_surface.get_width()

active_temporary_messages = []

# 씨앗 선택 메뉴 옵션 (PLANT_INFO 딕셔너리를 사용하여 동적으로 생성)
seed_options = []
seed_index_map = [] # 옵션의 순서와 PLANT_INFO의 키를 매핑
x_offset_multiplier = 0 # 씨앗 버튼 옆으로 나열될 때의 x 위치 계산에 사용
for plant_type, info in PLANT_INFO.items():
    seed_initial_x = seed_select_button_rect.x
    seed_target_x = seed_select_button_rect.right + TOOL_SPACING + (x_offset_multiplier * (TOOL_ICON_SIZE + TOOL_SPACING))
    seed_y = seed_select_button_rect.y
    seed_rect = pygame.Rect(seed_initial_x, seed_y, TOOL_ICON_SIZE, TOOL_ICON_SIZE)
    seed_image = info["seed_image"]
    seed_options.append({'rect': seed_rect, 'image': seed_image, 'plant_type': plant_type, 'target_x': seed_target_x, 'initial_x': seed_initial_x})
    seed_index_map.append(plant_type) # 순서대로 식물 타입 저장
    x_offset_multiplier += 1

MAX_SEED_ANIMATION_DISTANCE = seed_options[0]['target_x'] - seed_options[0]['initial_x']

# --- 밭(경작지) 및 화분 관련 변수 (사진과 동일하게 조정) ---
ITEM_SIZE = 80 # 밭과 화분의 가로세로 크기
ITEM_GAP_X = 15
ITEM_GAP_Y = 15
NUM_ITEMS_PER_ROW = 6
GLOBAL_X_OFFSET = 30
FIELD_START_X = 140 + GLOBAL_X_OFFSET
FIELD_START_Y = 400

field_states = []
for col in range(NUM_ITEMS_PER_ROW):
    x = FIELD_START_X + col * (ITEM_SIZE + ITEM_GAP_X)
    y = FIELD_START_Y
    field_rect = pygame.Rect(x, y, ITEM_SIZE, ITEM_SIZE)
    field_states.append({
        'rect': field_rect,
        'planted_plant_type': None, # 심겨진 식물 타입 (예: "sunflower", "potato")
        'current_growth_frame': 0,
        'final_scale_factor': 1.0 # 작물의 최종 크기 배율 (0.7 ~ 1.3 범위)
    })

POT_START_X = 140 + GLOBAL_X_OFFSET + (1.5 * (ITEM_SIZE + ITEM_GAP_X))
POT_START_Y = FIELD_START_Y + ITEM_SIZE + ITEM_GAP_Y
pot_states = []
for col in range(NUM_ITEMS_PER_ROW):
    x = POT_START_X + col * (ITEM_SIZE + ITEM_GAP_X)
    y = POT_START_Y
    pot_rect = pygame.Rect(x, y, ITEM_SIZE, ITEM_SIZE)
    pot_states.append({
        'rect': pot_rect,
        'planted_plant_type': None, # 심겨진 식물 타입 (예: "sunflower", "potato")
        'current_growth_frame': 0,
        'final_scale_factor': 1.0 # 작물의 최종 크기 배율 (0.7 ~ 1.3 범위)
    })

hovered_plot_type = None
hovered_plot_index = -1

# 작물별 가격 정보 (키는 식물 타입 문자열과 매칭)

CROP_PRICES = {
    "sunflower": {
        "type": "fixed",
        "quantity": 1,
        "price_per_item": 100,
        "name": "해바라기"
    },
    "lettuce": {
        "type": "fixed",
        "quantity": 1,
        "price_per_item": 1500,
        "name": "상추"
    },
    "potato": {
        "type": "fixed",
        "quantity": 1,
        "price_per_item": 5000,
        "name": "감자"
    },
    "pea": {
        "type": "fixed",
        "quantity": 1,
        "price_per_item": 30000,
        "name": "완두콩"
    },
    "dragonfruit": {
        "type": "fixed",
        "quantity": 1,
        "price_per_item": 100000,
        "name": "용과"
    }
}

# --- 인벤토리 ---
# 씨앗 이름 (예: "sunflower") -> 수량
player_inventory = {
    "sunflower": 5,
    "lettuce": 5,
    "potato": 5,
    "pea": 5,
    "dragonfruit": 5
} # 초기 소지 씨앗

# 플레이어가 현재 소지한 도구 정보 (ID, 배율)
player_tools = {
    'watering_can': {'id': 'watering_can_rusted', 'multiplier': 1},
    'scythe': {'id': 'sickle_cracked', 'multiplier': 1} # 낫은 기본 배율 1로 시작
}

# --- 상점 아이템 데이터 (판매할 씨앗 정보) ---
# 가격은 임의로 설정합니다. 실제 게임에 맞춰 조정하세요.
shop_items = [
    {"plant_type": "sunflower", "name": PLANT_INFO["sunflower"]["seed_name"], "price": 2000, "image": PLANT_INFO["sunflower"]["seed_image"], "description": "해바라기가 만개를 하면 팔 수 있지않을까?"},
    {"plant_type": "lettuce", "name": PLANT_INFO["lettuce"]["seed_name"], "price": 16000, "image": PLANT_INFO["lettuce"]["seed_image"], "description": "꽤 쓸만한 작물일거 같다 1000개를 채집하면 30,000,000?"},
    {"plant_type": "potato", "name": PLANT_INFO["potato"]["seed_name"], "price": 25000, "image": PLANT_INFO["potato"]["seed_image"], "description": "감자는 '만'ㅎ을수록 좋다."},
    {"plant_type": "pea", "name": PLANT_INFO["pea"]["seed_name"], "price": 200000, "image": PLANT_INFO["pea"]["seed_image"], "description": "신비한 힘이 깃든거 같다."},
    {"plant_type": "dragonfruit", "name": PLANT_INFO["dragonfruit"]["seed_name"], "price": 5000000, "image": PLANT_INFO["dragonfruit"]["seed_image"], "description": "비싸지만 값어치는 하는 것 같다."},
]

# 파일 상단이나, load_tool_image 함수 호출 전에
SHOP_ITEM_IMAGE_SIZE = 128  # 원하는 이미지 크기로 설정 (예: 128x128 픽셀)

def load_tool_image(image_name):
    # 수정된 부분: BASE_DIR을 사용하여 경로 생성
    image_path = BASE_DIR / "assets" / "images" / image_name
    if not image_path.exists():
        # 기본 이미지 로드 또는 오류 처리
        return None # 또는 적절한 기본 이미지
    img = pygame.image.load(image_path).convert_alpha()
    return pygame.transform.scale(img, (SHOP_ITEM_IMAGE_SIZE, SHOP_ITEM_IMAGE_SIZE))

# --- 도구 상점 아이템 데이터 (물뿌리개와 낫) ---
# 이미지 로드를 위한 헬퍼 함수
def load_tool_image(filename):
    # 수정된 부분: BASE_DIR을 사용하여 경로 생성
    path = BASE_DIR / "assets" / "images" / filename
    try:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, (SHOP_ITEM_IMAGE_SIZE, SHOP_ITEM_IMAGE_SIZE))
    except pygame.error as e:
        print(f"도구 이미지 로드 오류 {path}: {e}")
        # 이미지 로드 실패 시 기본 이미지 반환 또는 None 반환
        return pygame.transform.scale(pygame.Surface((SHOP_ITEM_IMAGE_SIZE, SHOP_ITEM_IMAGE_SIZE)), (SHOP_ITEM_IMAGE_SIZE, SHOP_ITEM_IMAGE_SIZE)) # 빈 Surface 반환

tool_shop_items = {
    "watering_can": [
        {"id": "watering_can_rusted", "name": "녹슨 물뿌리개", "price": 0, "multiplier": 1, "description": "오래되어 녹이 슨 물뿌리개입니다. 물을 줍니다.", "image": load_tool_image("watering_can_rusted.png") if (BASE_DIR / "assets" / "images" / "watering_can_rusted.png").exists() else watering_can_image},
        {"id": "watering_can_basic", "name": "기본 물뿌리개", "price": 50000, "multiplier": 2, "description": "기본적으로 제공되는 물뿌리개입니다. 물을 줍니다.", "image": load_tool_image("watering_can_tier1.png")},
        {"id": "watering_can_good", "name": "조금 쓸만한 물뿌리개", "price": 200000, "multiplier": 4, "description": "조금 더 강력해진 물뿌리개입니다. 물을 더 많이 줍니다.", "image": load_tool_image("watering_can_tier2.png")},
        {"id": "watering_can_better", "name": "좋아진 물뿌리개", "price": 1000000, "multiplier": 8, "description": "성능이 향상된 물뿌리개입니다. 작물 성장을 촉진합니다.", "image": load_tool_image("watering_can_tier3.png")},
        {"id": "watering_can_powerful", "name": "강력해진 물뿌리개", "price": 5000000, "multiplier": 16, "description": "매우 강력한 물뿌리개입니다. 기적적인 성장을 가능케 합니다.", "image": load_tool_image("watering_can_tier4.png")},
        {"id": "watering_can_masterpiece", "name": "장인이 만든 물뿌리개", "price": 20000000, "multiplier": 32, "description": "장인의 손길이 닿은 명품 물뿌리개입니다. 성장의 극치를 보여줍니다.", "image": load_tool_image("watering_can_tier5.png")},
        {"id": "watering_can_legendary", "name": "전설의 물뿌리개", "price": 100000000, "multiplier": 64, "description": "전설 속에서만 전해지던 물뿌리개입니다. 전체 밭에 영향을 줍니다.", "image": load_tool_image("watering_can_tier6.png")},
    ],
    "scythe": [
        {"id": "sickle_cracked", "name": "금이 간 낫", "price": 0, "multiplier": 1, "description": "금이가서 위태로워 보이는 낫입니다. 수확에 사용합니다.", "image": load_tool_image("sickle_cracked.png") if (BASE_DIR / "assets" / "images" / "sickle_cracked.png").exists() else scythe_image}, # 기본 낫은 가격 0
        {"id": "scythe_basic", "name": "기본 낫", "price": 0, "multiplier": 1, "description": "기본적으로 제공되는 낡은 낫입니다. 수확에 사용됩니다.", "image": load_tool_image("scythe_tier1.png")},
        {"id": "scythe_decent", "name": "조금 쓸만한 낫", "price": 150000, "multiplier": 1.5, "description": "날이 잘 선 낫입니다. 조금 더 많은 수확물을 얻을 수 있습니다.", "image": load_tool_image("scythe_tier2.png")},
        {"id": "scythe_normal", "name": "평범한 낫", "price": 1000000, "multiplier": 2, "description": "무난하게 사용할 수 있는 낫입니다. 안정적인 수확량에 기여합니다.", "image": load_tool_image("scythe_tier3.png")},
        {"id": "scythe_improved", "name": "좋아진 낫", "price": 5000000, "multiplier": 2.5, "description": "수확 효율이 눈에 띄게 좋아진 낫입니다. 농가의 희망이죠.", "image": load_tool_image("scythe_tier4.png")},
        {"id": "scythe_abandoned_master", "name": "장인이 쓰다 버린 낫", "price": 20000000, "multiplier": 4, "description": "장인이 더 이상 사용하지 않아 버려진 낫입니다. 엄청난 힘이 숨겨져 있습니다.", "image": load_tool_image("scythe_tier5.png")},
        {"id": "scythe_omniblade", "name": "모든걸 베어버릴것 같은 낫", "price": 100000000, "multiplier": 6, "description": "강력한 힘이 느껴지는 낫입니다. 베지 못할 것이 없습니다.", "image": load_tool_image("scythe_tier6.png")},
        {"id": "scythe_legendary", "name": "전설의 낫", "price": 500000000, "multiplier": 10, "description": "전설 속에 등장하는 낫입니다. 모든 작물을 풍요롭게 만듭니다.", "image": load_tool_image("scythe_tier7.png")},
    ]
}

# 상점 스크롤 관련 변수
shop_scroll_offset = 0
SHOP_SCROLL_SPEED = 20 # 한 번 스크롤할 때 이동할 픽셀 수

# 상점 패널 내 아이템 목록 영역을 전역 변수로 선언 (이벤트 처리에서 사용하기 위함)
shop_item_list_rect = pygame.Rect(0, 0, 0, 0) # 초기화

# 도구 상점 스크롤 관련 변수
tool_shop_scroll_offset = 0
tool_shop_item_list_rect = pygame.Rect(0, 0, 0, 0) # 초기화
selected_tool_category = "watering_can" # 기본적으로 물뿌리개 탭이 선택

# 상점 UI 레이아웃을 위한 변수
SHOP_ITEM_HEIGHT = 100
SHOP_ITEM_PADDING = 10
SHOP_ITEM_IMAGE_SIZE = 60
SHOP_RIGHT_PANEL_WIDTH_RATIO = 0.35 # 오른쪽 패널이 전체 패널 너비에서 차지하는 비율
# SHOP_RIGHT_PANEL_WIDTH는 SHOP_PANEL_WIDTH에 따라 동적으로 계산됩니다.

# 선택된 아이템 (상세 정보를 표시하기 위함)
selected_shop_item_index = -1
selected_tool_shop_item_index = -1

# 구매 버튼
buy_button_rect = pygame.Rect(0, 0, 120, 50) # 위치는 draw_shop_screen에서 계산

class TemporaryMessageDisplay:
    def __init__(self, text_or_parts, center_pos_tuple, duration=2.0, color=BLACK, font=None, is_multi_colored=False):
        # 텍스트가 화면 위쪽에서 나오도록 center_pos_tuple을 사용
        self.center_pos = center_pos_tuple
        self.duration = duration
        self.fade_in_duration = duration * 0.4
        self.hold_duration = duration * 0.2
        self.fade_out_duration = duration * 0.4
        self.font = font
        self.start_time = time.time()
        self.alpha = 0
        self.done = False
        self.is_multi_colored = is_multi_colored
        if self.is_multi_colored:
            # text_or_parts is a list of (text_string, color_tuple)
            self.text_parts = text_or_parts
        else:
            # text_or_parts is a single string, convert to consistent format
            self.text_parts = [(text_or_parts, color)]

    def update(self):
        if self.done:
            return
        elapsed_time = time.time() - self.start_time
        if elapsed_time < self.fade_in_duration:
            self.alpha = int(255 * (elapsed_time / self.fade_in_duration))
        elif elapsed_time < self.fade_in_duration + self.hold_duration:
            self.alpha = 255
        elif elapsed_time < self.duration:
            fade_out_elapsed = elapsed_time - (self.fade_in_duration + self.hold_duration)
            self.alpha = int(255 * (1 - (fade_out_elapsed / self.fade_out_duration)))
        else:
            self.alpha = 0
            self.done = True

    def draw(self, surface):
        if self.done:
            return

        # Calculate total width to center the multi-part text
        total_width = 0
        rendered_parts = []
        for text_part, part_color in self.text_parts:
            part_surface = self.font.render(text_part, True, part_color)
            total_width += part_surface.get_width()
            rendered_parts.append(part_surface)

        start_x = self.center_pos[0] - total_width // 2
        current_x = start_x
        for part_surface in rendered_parts:
            part_surface.set_alpha(self.alpha)
            surface.blit(part_surface, (current_x, self.center_pos[1] - part_surface.get_height() // 2))
            current_x += part_surface.get_width()

active_temporary_messages = []

# 씨앗 선택 메뉴 옵션 (PLANT_INFO 딕셔너리를 사용하여 동적으로 생성)
seed_options = []
seed_index_map = [] # 옵션의 순서와 PLANT_INFO의 키를 매핑
x_offset_multiplier = 0 # 씨앗 버튼 옆으로 나열될 때의 x 위치 계산에 사용
for plant_type, info in PLANT_INFO.items():
    seed_initial_x = seed_select_button_rect.x
    seed_target_x = seed_select_button_rect.right + TOOL_SPACING + (x_offset_multiplier * (TOOL_ICON_SIZE + TOOL_SPACING))
    seed_y = seed_select_button_rect.y
    seed_rect = pygame.Rect(seed_initial_x, seed_y, TOOL_ICON_SIZE, TOOL_ICON_SIZE)
    seed_image = info["seed_image"]
    seed_options.append({'rect': seed_rect, 'image': seed_image, 'plant_type': plant_type, 'target_x': seed_target_x, 'initial_x': seed_initial_x})
    seed_index_map.append(plant_type) # 순서대로 식물 타입 저장
    x_offset_multiplier += 1

MAX_SEED_ANIMATION_DISTANCE = seed_options[0]['target_x'] - seed_options[0]['initial_x']

# --- 밭(경작지) 및 화분 관련 변수 (사진과 동일하게 조정) ---
ITEM_SIZE = 80 # 밭과 화분의 가로세로 크기
ITEM_GAP_X = 15
ITEM_GAP_Y = 15
NUM_ITEMS_PER_ROW = 6
GLOBAL_X_OFFSET = 30
FIELD_START_X = 140 + GLOBAL_X_OFFSET
FIELD_START_Y = 400

field_states = []
for col in range(NUM_ITEMS_PER_ROW):
    x = FIELD_START_X + col * (ITEM_SIZE + ITEM_GAP_X)
    y = FIELD_START_Y
    field_rect = pygame.Rect(x, y, ITEM_SIZE, ITEM_SIZE)
    field_states.append({
        'rect': field_rect,
        'planted_plant_type': None, # 심겨진 식물 타입 (예: "sunflower", "potato")
        'current_growth_frame': 0,
        'final_scale_factor': 1.0 # 작물의 최종 크기 배율 (0.7 ~ 1.3 범위)
    })

POT_START_X = 140 + GLOBAL_X_OFFSET + (1.5 * (ITEM_SIZE + ITEM_GAP_X))
POT_START_Y = FIELD_START_Y + ITEM_SIZE + ITEM_GAP_Y
pot_states = []
for col in range(NUM_ITEMS_PER_ROW):
    x = POT_START_X + col * (ITEM_SIZE + ITEM_GAP_X)
    y = POT_START_Y
    pot_rect = pygame.Rect(x, y, ITEM_SIZE, ITEM_SIZE)
    pot_states.append({
        'rect': pot_rect,
        'planted_plant_type': None, # 심겨진 식물 타입 (예: "sunflower", "potato")
        'current_growth_frame': 0,
        'final_scale_factor': 1.0 # 작물의 최종 크기 배율 (0.7 ~ 1.3 범위)
    })

hovered_plot_type = None
hovered_plot_index = -1


# 작물별 가격 정보 (키는 식물 타입 문자열과 매칭)
# (중복 선언 제거, 위에서 이미 선언됨)

# --- 인벤토리 ---
# 씨앗 이름 (예: "sunflower") -> 수량
player_inventory = {
    "sunflower": 5,
    "lettuce": 5,
    "potato": 5,
    "pea": 5,
    "dragonfruit": 5
} # 초기 소지 씨앗

# 플레이어가 현재 소지한 도구 정보 (ID, 배율)
player_tools = {
    'watering_can': {'id': 'watering_can_rusted', 'multiplier': 1},
    'scythe': {'id': 'sickle_cracked', 'multiplier': 1} # 낫은 기본 배율 1로 시작
}

# --- 상점 아이템 데이터 (판매할 씨앗 정보) ---
# 가격은 임의로 설정합니다. 실제 게임에 맞춰 조정하세요.
shop_items = [
    {"plant_type": "sunflower", "name": PLANT_INFO["sunflower"]["seed_name"], "price": 2000, "image": PLANT_INFO["sunflower"]["seed_image"], "description": "해바라기가 만개를 하면 팔 수 있지않을까?"},
    {"plant_type": "lettuce", "name": PLANT_INFO["lettuce"]["seed_name"], "price": 16000, "image": PLANT_INFO["lettuce"]["seed_image"], "description": "꽤 쓸만한 작물일거 같다 1000개를 채집하면 30,000,000?"},
    {"plant_type": "potato", "name": PLANT_INFO["potato"]["seed_name"], "price": 25000, "image": PLANT_INFO["potato"]["seed_image"], "description": "감자는 '만'ㅎ을수록 좋다."},
    {"plant_type": "pea", "name": PLANT_INFO["pea"]["seed_name"], "price": 200000, "image": PLANT_INFO["pea"]["seed_image"], "description": "신비한 힘이 깃든거 같다."},
    {"plant_type": "dragonfruit", "name": PLANT_INFO["dragonfruit"]["seed_name"], "price": 5000000, "image": PLANT_INFO["dragonfruit"]["seed_image"], "description": "비싸지만 값어치는 하는 것 같다."},
]

# 파일 상단이나, load_tool_image 함수 호출 전에
SHOP_ITEM_IMAGE_SIZE = 128  # 원하는 이미지 크기로 설정 (예: 128x128 픽셀)

def load_tool_image(image_name):
    # 수정된 부분: BASE_DIR을 사용하여 경로 생성
    image_path = BASE_DIR / "assets" / "images" / image_name
    if not image_path.exists():
        # 기본 이미지 로드 또는 오류 처리
        return None # 또는 적절한 기본 이미지
    img = pygame.image.load(image_path).convert_alpha()
    return pygame.transform.scale(img, (SHOP_ITEM_IMAGE_SIZE, SHOP_ITEM_IMAGE_SIZE))

# --- 도구 상점 아이템 데이터 (물뿌리개와 낫) ---
# 이미지 로드를 위한 헬퍼 함수
def load_tool_image(filename):
    # 수정된 부분: BASE_DIR을 사용하여 경로 생성
    path = BASE_DIR / "assets" / "images" / filename
    try:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, (SHOP_ITEM_IMAGE_SIZE, SHOP_ITEM_IMAGE_SIZE))
    except pygame.error as e:
        print(f"도구 이미지 로드 오류 {path}: {e}")
        # 이미지 로드 실패 시 기본 이미지 반환 또는 None 반환
        return pygame.transform.scale(pygame.Surface((SHOP_ITEM_IMAGE_SIZE, SHOP_ITEM_IMAGE_SIZE)), (SHOP_ITEM_IMAGE_SIZE, SHOP_ITEM_IMAGE_SIZE)) # 빈 Surface 반환

tool_shop_items = {
    "watering_can": [
        {"id": "watering_can_rusted", "name": "녹슨 물뿌리개", "price": 0, "multiplier": 1, "description": "오래되어 녹이 슨 물뿌리개입니다. 물을 줍니다.", "image": load_tool_image("watering_can_rusted.png") if (BASE_DIR / "assets" / "images" / "watering_can_rusted.png").exists() else watering_can_image},
        {"id": "watering_can_basic", "name": "기본 물뿌리개", "price": 50000, "multiplier": 2, "description": "기본적으로 제공되는 물뿌리개입니다. 물을 줍니다.", "image": load_tool_image("watering_can_tier1.png")},
        {"id": "watering_can_good", "name": "조금 쓸만한 물뿌리개", "price": 200000, "multiplier": 4, "description": "조금 더 강력해진 물뿌리개입니다. 물을 더 많이 줍니다.", "image": load_tool_image("watering_can_tier2.png")},
        {"id": "watering_can_better", "name": "좋아진 물뿌리개", "price": 1000000, "multiplier": 8, "description": "성능이 향상된 물뿌리개입니다. 작물 성장을 촉진합니다.", "image": load_tool_image("watering_can_tier3.png")},
        {"id": "watering_can_powerful", "name": "강력해진 물뿌리개", "price": 5000000, "multiplier": 16, "description": "매우 강력한 물뿌리개입니다. 기적적인 성장을 가능케 합니다.", "image": load_tool_image("watering_can_tier4.png")},
        {"id": "watering_can_masterpiece", "name": "장인이 만든 물뿌리개", "price": 20000000, "multiplier": 32, "description": "장인의 손길이 닿은 명품 물뿌리개입니다. 성장의 극치를 보여줍니다.", "image": load_tool_image("watering_can_tier5.png")},
        {"id": "watering_can_legendary", "name": "전설의 물뿌리개", "price": 100000000, "multiplier": 64, "description": "전설 속에서만 전해지던 물뿌리개입니다. 전체 밭에 영향을 줍니다.", "image": load_tool_image("watering_can_tier6.png")},
    ],
    "scythe": [
        {"id": "sickle_cracked", "name": "금이 간 낫", "price": 0, "multiplier": 1, "description": "금이가서 위태로워 보이는 낫입니다. 수확에 사용합니다.", "image": load_tool_image("sickle_cracked.png") if (BASE_DIR / "assets" / "images" / "sickle_cracked.png").exists() else scythe_image}, # 기본 낫은 가격 0
        {"id": "scythe_basic", "name": "기본 낫", "price": 0, "multiplier": 1, "description": "기본적으로 제공되는 낡은 낫입니다. 수확에 사용됩니다.", "image": load_tool_image("scythe_tier1.png")},
        {"id": "scythe_decent", "name": "조금 쓸만한 낫", "price": 150000, "multiplier": 1.5, "description": "날이 잘 선 낫입니다. 조금 더 많은 수확물을 얻을 수 있습니다.", "image": load_tool_image("scythe_tier2.png")},
        {"id": "scythe_normal", "name": "평범한 낫", "price": 1000000, "multiplier": 2, "description": "무난하게 사용할 수 있는 낫입니다. 안정적인 수확량에 기여합니다.", "image": load_tool_image("scythe_tier3.png")},
        {"id": "scythe_improved", "name": "좋아진 낫", "price": 5000000, "multiplier": 2.5, "description": "수확 효율이 눈에 띄게 좋아진 낫입니다. 농가의 희망이죠.", "image": load_tool_image("scythe_tier4.png")},
        {"id": "scythe_abandoned_master", "name": "장인이 쓰다 버린 낫", "price": 20000000, "multiplier": 4, "description": "장인이 더 이상 사용하지 않아 버려진 낫입니다. 엄청난 힘이 숨겨져 있습니다.", "image": load_tool_image("scythe_tier5.png")},
        {"id": "scythe_omniblade", "name": "모든걸 베어버릴것 같은 낫", "price": 100000000, "multiplier": 6, "description": "강력한 힘이 느껴지는 낫입니다. 베지 못할 것이 없습니다.", "image": load_tool_image("scythe_tier6.png")},
        {"id": "scythe_legendary", "name": "전설의 낫", "price": 500000000, "multiplier": 10, "description": "전설 속에 등장하는 낫입니다. 모든 작물을 풍요롭게 만듭니다.", "image": load_tool_image("scythe_tier7.png")},
    ]
}

# 상점 스크롤 관련 변수
shop_scroll_offset = 0
SHOP_SCROLL_SPEED = 20 # 한 번 스크롤할 때 이동할 픽셀 수

# 상점 패널 내 아이템 목록 영역을 전역 변수로 선언 (이벤트 처리에서 사용하기 위함)
shop_item_list_rect = pygame.Rect(0, 0, 0, 0) # 초기화

# 도구 상점 스크롤 관련 변수
tool_shop_scroll_offset = 0
tool_shop_item_list_rect = pygame.Rect(0, 0, 0, 0) # 초기화
selected_tool_category = "watering_can" # 기본적으로 물뿌리개 탭이 선택

# 상점 UI 레이아웃을 위한 변수
SHOP_ITEM_HEIGHT = 100
SHOP_ITEM_PADDING = 10
SHOP_ITEM_IMAGE_SIZE = 60
SHOP_RIGHT_PANEL_WIDTH_RATIO = 0.35 # 오른쪽 패널이 전체 패널 너비에서 차지하는 비율
# SHOP_RIGHT_PANEL_WIDTH는 SHOP_PANEL_WIDTH에 따라 동적으로 계산됩니다.

# 선택된 아이템 (상세 정보를 표시하기 위함)
selected_shop_item_index = -1
selected_tool_shop_item_index = -1

# 구매 버튼
buy_button_rect = pygame.Rect(0, 0, 120, 50) # 위치는 draw_shop_screen에서 계산

class TemporaryMessageDisplay:
    def __init__(self, text_or_parts, center_pos_tuple, duration=2.0, color=BLACK, font=None, is_multi_colored=False):
        # 텍스트가 화면 위쪽에서 나오도록 center_pos_tuple을 사용
        self.center_pos = center_pos_tuple
        self.duration = duration
        self.fade_in_duration = duration * 0.4
        self.hold_duration = duration * 0.2
        self.fade_out_duration = duration * 0.4
        self.font = font
        self.start_time = time.time()
        self.alpha = 0
        self.done = False
        self.is_multi_colored = is_multi_colored
        if self.is_multi_colored:
            # text_or_parts is a list of (text_string, color_tuple)
            self.text_parts = text_or_parts
        else:
            # text_or_parts is a single string, convert to consistent format
            self.text_parts = [(text_or_parts, color)]

    def update(self):
        if self.done:
            return
        elapsed_time = time.time() - self.start_time
        if elapsed_time < self.fade_in_duration:
            self.alpha = int(255 * (elapsed_time / self.fade_in_duration))
        elif elapsed_time < self.fade_in_duration + self.hold_duration:
            self.alpha = 255
        elif elapsed_time < self.duration:
            fade_out_elapsed = elapsed_time - (self.fade_in_duration + self.hold_duration)
            self.alpha = int(255 * (1 - (fade_out_elapsed / self.fade_out_duration)))
        else:
            self.alpha = 0
            self.done = True

    def draw(self, surface):
        if self.done:
            return

        # Calculate total width to center the multi-part text
        total_width = 0
        rendered_parts = []
        for text_part, part_color in self.text_parts:
            part_surface = self.font.render(text_part, True, part_color)
            total_width += part_surface.get_width()
            rendered_parts.append(part_surface)

        start_x = self.center_pos[0] - total_width // 2
        current_x = start_x
        for part_surface in rendered_parts:
            part_surface.set_alpha(self.alpha)
            surface.blit(part_surface, (current_x, self.center_pos[1] - part_surface.get_height() // 2))
            current_x += part_surface.get_width()

active_temporary_messages = []

# 씨앗 선택 메뉴 옵션 (PLANT_INFO 딕셔너리를 사용하여 동적으로 생성)
seed_options = []
seed_index_map = [] # 옵션의 순서와 PLANT_INFO의 키를 매핑
x_offset_multiplier = 0 # 씨앗 버튼 옆으로 나열될 때의 x 위치 계산에 사용
for plant_type, info in PLANT_INFO.items():
    seed_initial_x = seed_select_button_rect.x
    seed_target_x = seed_select_button_rect.right + TOOL_SPACING + (x_offset_multiplier * (TOOL_ICON_SIZE + TOOL_SPACING))
    seed_y = seed_select_button_rect.y
    seed_rect = pygame.Rect(seed_initial_x, seed_y, TOOL_ICON_SIZE, TOOL_ICON_SIZE)
    seed_image = info["seed_image"]
    seed_options.append({'rect': seed_rect, 'image': seed_image, 'plant_type': plant_type, 'target_x': seed_target_x, 'initial_x': seed_initial_x})
    seed_index_map.append(plant_type) # 순서대로 식물 타입 저장
    x_offset_multiplier += 1

MAX_SEED_ANIMATION_DISTANCE = seed_options[0]['target_x'] - seed_options[0]['initial_x']

# --- 밭(경작지) 및 화분 관련 변수 (사진과 동일하게 조정) ---
ITEM_SIZE = 80 # 밭과 화분의 가로세로 크기
ITEM_GAP_X = 15
ITEM_GAP_Y = 15
NUM_ITEMS_PER_ROW = 6
GLOBAL_X_OFFSET = 30
FIELD_START_X = 140 + GLOBAL_X_OFFSET
FIELD_START_Y = 400

field_states = []
for col in range(NUM_ITEMS_PER_ROW):
    x = FIELD_START_X + col * (ITEM_SIZE + ITEM_GAP_X)
    y = FIELD_START_Y
    field_rect = pygame.Rect(x, y, ITEM_SIZE, ITEM_SIZE)
    field_states.append({
        'rect': field_rect,
        'planted_plant_type': None, # 심겨진 식물 타입 (예: "sunflower", "potato")
        'current_growth_frame': 0,
        'final_scale_factor': 1.0 # 작물의 최종 크기 배율 (0.7 ~ 1.3 범위)
    })

POT_START_X = 140 + GLOBAL_X_OFFSET + (1.5 * (ITEM_SIZE + ITEM_GAP_X))
POT_START_Y = FIELD_START_Y + ITEM_SIZE + ITEM_GAP_Y
pot_states = []
for col in range(NUM_ITEMS_PER_ROW):
    x = POT_START_X + col * (ITEM_SIZE + ITEM_GAP_X)
    y = POT_START_Y
    pot_rect = pygame.Rect(x, y, ITEM_SIZE, ITEM_SIZE)
    pot_states.append({
        'rect': pot_rect,
        'planted_plant_type': None, # 심겨진 식물 타입 (예: "sunflower", "potato")
        'current_growth_frame': 0,
        'final_scale_factor': 1.0 # 작물의 최종 크기 배율 (0.7 ~ 1.3 범위)
    })

hovered_plot_type = None
hovered_plot_index = -1

# 작물별 가격 정보 (키는 식물 타입 문자열과 매칭)
CROP_PRICES = {
    "sunflower": {
        "type": "fixed",
        "quantity": 1,
        "price_per_item": 100,
        "name": "해바라기"
    },
    "lettuce": {
        "type": "fixed",
        "quantity": 1,
        "price_per_item": 1500,
        "name": "상추"
    },
    "potato": {
        "type": "fixed",
        "quantity": 1,
        "price_per_item": 5000,
        "name": "감자"
    },
    "pea": {
        "type": "fixed",
        "quantity": 1,
        "price_per_item": 30000,
        "name": "완두콩"
    },
    "dragonfruit": {
        "type": "fixed",
        "quantity": 1,
        "price_per_item": 100000,
        "name": "용과"
    }
}

def draw_settings_screen():
    """설정 화면을 그립니다."""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))

    pygame.draw.rect(screen, DARK_GRAY, settings_panel_rect, border_radius=15)
    pygame.draw.rect(screen, WHITE, settings_panel_rect, 5, border_radius=15)

    title_text = settings_title_font.render("설정", True, WHITE)
    title_text_rect = title_text.get_rect(center=(settings_panel_rect.centerx, settings_panel_rect.top + 50))
    screen.blit(title_text, title_text_rect)

    # 설정 닫기 버튼은 shop_panel_rect가 아닌 settings_panel_rect를 기준으로 배치
    current_close_button_rect = pygame.Rect(settings_panel_rect.right - 40, settings_panel_rect.top + 10, 30, 30)
    pygame.draw.rect(screen, RED, current_close_button_rect, border_radius=5)
    close_text = font.render("X", True, WHITE)
    close_text_rect = close_text.get_rect(center=(current_close_button_rect.centerx, current_close_button_rect.centery + 1.5))
    screen.blit(close_text, close_text_rect)


    master_label = volume_label_font.render(f"마스터 볼륨: {int(master_volume * 100)}%", True, WHITE)
    master_label_rect = master_label.get_rect(midleft=(master_vol_slider_x, master_vol_slider_y - 30))
    screen.blit(master_label, master_label_rect)
    pygame.draw.rect(screen, GRAY, master_vol_slider_rect)
    pygame.draw.circle(screen, LIGHT_GRAY, master_vol_knob_rect.center, KNOB_RADIUS)

    music_label = volume_label_font.render(f"배경 음악 볼륨: {int(music_volume * 100)}%", True, WHITE)
    music_label_rect = music_label.get_rect(midleft=(music_vol_slider_x, music_vol_slider_y - 30))
    screen.blit(music_label, music_label_rect)
    pygame.draw.rect(screen, GRAY, music_vol_slider_rect)
    pygame.draw.circle(screen, LIGHT_GRAY, music_vol_knob_rect.center, KNOB_RADIUS)

    # 효과음 볼륨 슬라이더 그리기
    sfx_label = volume_label_font.render(f"효과음 볼륨: {int(sfx_volume * 100)}%", True, WHITE)
    sfx_label_rect = sfx_label.get_rect(midleft=(sfx_vol_slider_x, sfx_vol_slider_y - 30))
    screen.blit(sfx_label, sfx_label_rect)
    pygame.draw.rect(screen, GRAY, sfx_vol_slider_rect)
    pygame.draw.circle(screen, LIGHT_GRAY, sfx_vol_knob_rect.center, KNOB_RADIUS)


def draw_shop_screen():
    """상점 화면을 그립니다."""
    global shop_item_list_rect # 전역 변수 업데이트를 위해 선언
    global scrollbar_rect, scrollbar_handle_rect, shop_scroll_offset

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))

    pygame.draw.rect(screen, DARK_GRAY, shop_panel_rect, border_radius=15)
    pygame.draw.rect(screen, WHITE, shop_panel_rect, 5, border_radius=15)

    # 상점 제목을 더 아래로 내림
    shop_title_text = shop_title_font.render("상점", True, WHITE)
    shop_title_text_rect = shop_title_text.get_rect(center=(shop_panel_rect.centerx, shop_panel_rect.top + 70)) # 제목 Y 좌표 조정
    screen.blit(shop_title_text, shop_title_text_rect)

    # 닫기 버튼 (상점 패널 기준으로 배치)
    current_close_button_rect = pygame.Rect(shop_panel_rect.right - 40, shop_panel_rect.top + 10, 30, 30)
    pygame.draw.rect(screen, RED, current_close_button_rect, border_radius=5)
    close_text = font.render("X", True, WHITE)
    close_text_rect = close_text.get_rect(center=(current_close_button_rect.centerx, current_close_button_rect.centery + 1.5))
    screen.blit(close_text, close_text_rect)

    # 왼쪽 아이템 목록 영역 (늘어난 패널 크기에 맞게 조정)
    actual_shop_right_panel_width = int(SHOP_PANEL_WIDTH * SHOP_RIGHT_PANEL_WIDTH_RATIO)
    shop_item_list_rect = pygame.Rect( # 전역 변수에 할당
        shop_panel_rect.left + 20, # 좌측 여백 증가
        shop_panel_rect.top + shop_title_text_rect.height + 60, # 제목이 내려감에 따라 Y 시작점 조정
        shop_panel_rect.width - actual_shop_right_panel_width - 40, # 오른쪽 패널 너비만큼 제외, 좌우 여백 추가
        shop_panel_rect.height - (shop_title_text_rect.height + 60) - 20 # 상단 제목 및 하단 여백 제외
    )
    pygame.draw.rect(screen, GRAY, shop_item_list_rect, border_radius=5)
    pygame.draw.rect(screen, LIGHT_GRAY, shop_item_list_rect, 2, border_radius=5)

    # 오른쪽 상세 정보 영역 (늘어난 패널 크기에 맞게 조정)
    detail_panel_rect = pygame.Rect(
        shop_item_list_rect.right + 10, # 목록 패널과의 간격
        shop_item_list_rect.y,
        actual_shop_right_panel_width - 20, # 동적으로 계산된 너비 사용 (우측 여백 고려)
        shop_item_list_rect.height
    )
    pygame.draw.rect(screen, GRAY, detail_panel_rect, border_radius=5)
    pygame.draw.rect(screen, LIGHT_GRAY, detail_panel_rect, 2, border_radius=5)

    # 아이템 목록 렌더링
    total_items_height = len(shop_items) * (SHOP_ITEM_HEIGHT + SHOP_ITEM_PADDING)
    # 실제 아이템들이 그려질 수 있는 영역의 높이
    visible_list_height = shop_item_list_rect.height - (SHOP_ITEM_PADDING * 2) # 상단/하단 패딩 고려

    # 최대 스크롤 오프셋 계산 (전체 아이템 높이 - 보이는 영역 높이)
    # 마이너스 값은 스크롤이 필요 없다는 의미이므로 0으로 제한
    max_scroll_offset = max(0, total_items_height - visible_list_height)

    # shop_scroll_offset이 최대값을 초과하지 않도록 보정 (이벤트 루프에서도 처리되지만, 만약을 대비)
    shop_scroll_offset = max(0, min(shop_scroll_offset, max_scroll_offset))

    # 클리핑 영역 설정
    screen.set_clip(shop_item_list_rect)

    for i, item in enumerate(shop_items):
        # 스크롤 오프셋 적용된 실제 아이템 위치 계산
        item_relative_y = i * (SHOP_ITEM_HEIGHT + SHOP_ITEM_PADDING) + SHOP_ITEM_PADDING
        item_y = shop_item_list_rect.top + item_relative_y - shop_scroll_offset

        # 아이템이 현재 보이는 목록 영역 내에 있는지 확인 (위쪽/아래쪽 모두)
        # 클리핑이 적용되었으므로 이 조건은 사실상 필요 없지만, 명시적으로 남겨둠
        if item_y + SHOP_ITEM_HEIGHT > shop_item_list_rect.top and item_y < shop_item_list_rect.bottom:
            item_rect_in_list = pygame.Rect(shop_item_list_rect.left + SHOP_ITEM_PADDING, item_y,
                                            shop_item_list_rect.width - SHOP_ITEM_PADDING * 2, SHOP_ITEM_HEIGHT)

            # 선택된 아이템만 노란색 하이라이트, 나머지는 기본색
            if i == selected_tool_shop_item_index:
                pygame.draw.rect(screen, YELLOW, item_rect_in_list, border_radius=5)
            else:
                pygame.draw.rect(screen, LIGHT_GRAY, item_rect_in_list, border_radius=5)
            if item["image"]:
                # 이미지 원본 크기를 SHOP_ITEM_IMAGE_SIZE에 맞춰 스케일
                scaled_item_image = pygame.transform.scale(item["image"], (SHOP_ITEM_IMAGE_SIZE, SHOP_ITEM_IMAGE_SIZE))
                # 이미지를 item_rect_in_list의 왼쪽에서 SHOP_ITEM_PADDING 만큼 띄우고 중앙 정렬
                img_rect = scaled_item_image.get_rect(midleft=(item_rect_in_list.left + SHOP_ITEM_PADDING, item_rect_in_list.centery))
                screen.blit(scaled_item_image, img_rect)

            # 아이템 이름 (오른쪽으로 이동)
            name_text = seed_name_font.render(item["name"], True, BLACK)
            # 이미지 너비(SHOP_ITEM_IMAGE_SIZE)와 패딩을 고려하여 텍스트 시작 위치 조정
            name_text_rect = name_text.get_rect(midleft=(item_rect_in_list.left + SHOP_ITEM_PADDING + SHOP_ITEM_IMAGE_SIZE + 20, item_rect_in_list.centery - 15))
            screen.blit(name_text, name_text_rect)

            # 아이템 가격 (오른쪽으로 이동)
            price_text = font.render(f"가격: {item['price']:,}골드", True, BLUE)
            price_text_rect = price_text.get_rect(midleft=(item_rect_in_list.left + SHOP_ITEM_PADDING + SHOP_ITEM_IMAGE_SIZE + 20, item_rect_in_list.centery + 15))
            screen.blit(price_text, price_text_rect)
    
    # 클리핑 영역 해제
    screen.set_clip(None)

    # 스크롤바 렌더링
    if max_scroll_offset > 0:
        scrollbar_width = 15
        scrollbar_x = shop_item_list_rect.right - scrollbar_width - 10 # 스크롤바와 아이템 목록 간격 조정
        scrollbar_y = shop_item_list_rect.top + 5
        scrollbar_height = shop_item_list_rect.height - 10
        scrollbar_rect = pygame.Rect(scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height)
        pygame.draw.rect(screen, LIGHT_GRAY, scrollbar_rect, border_radius=5)

        # 스크롤바 핸들 계산
        handle_height_ratio = visible_list_height / total_items_height
        handle_height = scrollbar_height * handle_height_ratio
        handle_y_offset = (shop_scroll_offset / max_scroll_offset) * (scrollbar_height - handle_height)
        scrollbar_handle_rect = pygame.Rect(scrollbar_x, scrollbar_y + handle_y_offset, scrollbar_width, handle_height)
        pygame.draw.rect(screen, DARK_GRAY, scrollbar_handle_rect, border_radius=5)

    # 오른쪽 상세 정보 패널 내용
    if selected_shop_item_index != -1:
        selected_item = shop_items[selected_shop_item_index]

        # 아이템 이미지
        if selected_item["image"]:
            detail_img_size = 150
            detail_img = pygame.transform.scale(selected_item["image"], (detail_img_size, detail_img_size))
            detail_img_rect = detail_img.get_rect(center=(detail_panel_rect.centerx, detail_panel_rect.top + 80))
            screen.blit(detail_img, detail_img_rect)

        # 아이템 이름
        detail_name_text = shop_title_font.render(selected_item["name"], True, WHITE)
        detail_name_text_rect = detail_name_text.get_rect(center=(detail_panel_rect.centerx, detail_panel_rect.top + 200))
        screen.blit(detail_name_text, detail_name_text_rect)

        # 아이템 가격
        detail_price_text = font.render(f"가격: {selected_item['price']:,}골드", True, YELLOW)
        detail_price_text_rect = detail_price_text.get_rect(center=(detail_panel_rect.centerx, detail_panel_rect.top + 250))
        screen.blit(detail_price_text, detail_price_text_rect)

        # 아이템 설명 (크기 줄이기 위해 max_width 조정)
        description_lines = wrap_text(selected_item["description"], description_font, detail_panel_rect.width - 60) # description_font 사용
        desc_y = detail_panel_rect.top + 300
        for line in description_lines:
            desc_text = description_font.render(line, True, LIGHT_GRAY) # description_font 사용
            desc_text_rect = desc_text.get_rect(centerx=detail_panel_rect.centerx, top=desc_y)
            screen.blit(desc_text, desc_text_rect)
            desc_y += desc_text_rect.height + 5

        # 구매 버튼 (씨앗/상점 아이템은 장착/소지 개념 없음)
        buy_button_rect.center = (detail_panel_rect.centerx, detail_panel_rect.bottom - 50)
        button_label = "구매"
        button_color = GREEN if player_money >= selected_item["price"] else TOOL_DISABLED_COLOR
        pygame.draw.rect(screen, button_color, buy_button_rect, border_radius=5)
        buy_text = button_font.render(button_label, True, WHITE)
        buy_text_rect = buy_text.get_rect(center=buy_button_rect.center)
        screen.blit(buy_text, buy_text_rect)


def draw_tool_shop_screen(): # 기존 draw_crafting_screen에서 이름 변경
    """도구 상점 화면을 그립니다."""
    global tool_shop_item_list_rect # 전역 변수 업데이트를 위해 선언
    global scrollbar_rect, scrollbar_handle_rect, tool_shop_scroll_offset

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))

    pygame.draw.rect(screen, DARK_GRAY, tool_shop_panel_rect, border_radius=15)
    pygame.draw.rect(screen, WHITE, tool_shop_panel_rect, 5, border_radius=15)

    tool_shop_title_text = shop_title_font.render("도구 상점", True, WHITE)
    tool_shop_title_text_rect = tool_shop_title_text.get_rect(center=(tool_shop_panel_rect.centerx, tool_shop_panel_rect.top + 70))
    screen.blit(tool_shop_title_text, tool_shop_title_text_rect)

    # 닫기 버튼
    current_close_button_rect = pygame.Rect(tool_shop_panel_rect.right - 40, tool_shop_panel_rect.top + 10, 30, 30)
    pygame.draw.rect(screen, RED, current_close_button_rect, border_radius=5)
    close_text = font.render("X", True, WHITE)
    close_text_rect = close_text.get_rect(center=(current_close_button_rect.centerx, current_close_button_rect.centery + 1.5))
    screen.blit(close_text, close_text_rect)

    # --- 도구 카테고리 탭 버튼 ---
    tab_height = 50
    tab_width = 150
    tab_margin = 10
    
    watering_can_tab_rect = pygame.Rect(tool_shop_panel_rect.left + 20, tool_shop_panel_rect.top + 20, tab_width, tab_height)
    scythe_tab_rect = pygame.Rect(watering_can_tab_rect.right + tab_margin, tool_shop_panel_rect.top + 20, tab_width, tab_height)

    # 물뿌리개 탭
    wc_tab_color = TAB_ACTIVE_COLOR if selected_tool_category == "watering_can" else TAB_INACTIVE_COLOR
    pygame.draw.rect(screen, wc_tab_color, watering_can_tab_rect, border_radius=5)
    wc_tab_text = button_font.render("물뿌리개", True, WHITE)
    wc_tab_text_rect = wc_tab_text.get_rect(center=watering_can_tab_rect.center)
    screen.blit(wc_tab_text, wc_tab_text_rect)

    # 낫 탭
    sc_tab_color = TAB_ACTIVE_COLOR if selected_tool_category == "scythe" else TAB_INACTIVE_COLOR
    pygame.draw.rect(screen, sc_tab_color, scythe_tab_rect, border_radius=5)
    sc_tab_text = button_font.render("낫", True, WHITE)
    sc_tab_text_rect = sc_tab_text.get_rect(center=scythe_tab_rect.center)
    screen.blit(sc_tab_text, sc_tab_text_rect)
    # --- 여기까지 도구 카테고리 탭 버튼 ---


    # 현재 선택된 카테고리에 맞는 아이템 목록 가져오기
    current_tool_items = tool_shop_items[selected_tool_category]

    # 왼쪽 아이템 목록 영역
    actual_tool_shop_right_panel_width = int(TOOL_SHOP_PANEL_WIDTH * SHOP_RIGHT_PANEL_WIDTH_RATIO)
    tool_shop_item_list_rect = pygame.Rect( # 전역 변수에 할당
        tool_shop_panel_rect.left + 20, # 좌측 여백 증가
        tool_shop_panel_rect.top + tool_shop_title_text_rect.height + 60, # 제목이 내려감에 따라 Y 시작점 조정
        tool_shop_panel_rect.width - actual_tool_shop_right_panel_width - 40, # 오른쪽 패널 너비만큼 제외, 좌우 여백 추가
        tool_shop_panel_rect.height - (tool_shop_title_text_rect.height + 60) - 20 # 상단 제목 및 하단 여백 제외
    )
    pygame.draw.rect(screen, GRAY, tool_shop_item_list_rect, border_radius=5)
    pygame.draw.rect(screen, LIGHT_GRAY, tool_shop_item_list_rect, 2, border_radius=5)

    # 오른쪽 상세 정보 영역
    detail_panel_rect = pygame.Rect(
        tool_shop_item_list_rect.right + 10, # 목록 패널과의 간격
        tool_shop_item_list_rect.y,
        actual_tool_shop_right_panel_width - 20, # 동적으로 계산된 너비 사용 (우측 여백 고려)
        tool_shop_item_list_rect.height
    )
    pygame.draw.rect(screen, GRAY, detail_panel_rect, border_radius=5)
    pygame.draw.rect(screen, LIGHT_GRAY, detail_panel_rect, 2, border_radius=5)

    # 아이템 목록 렌더링
    total_items_height = len(current_tool_items) * (SHOP_ITEM_HEIGHT + SHOP_ITEM_PADDING)
    visible_list_height = tool_shop_item_list_rect.height - (SHOP_ITEM_PADDING * 2)

    max_scroll_offset = max(0, total_items_height - visible_list_height)
    tool_shop_scroll_offset = max(0, min(tool_shop_scroll_offset, max_scroll_offset))

    screen.set_clip(tool_shop_item_list_rect)

    for i, item in enumerate(current_tool_items):
        item_relative_y = i * (SHOP_ITEM_HEIGHT + SHOP_ITEM_PADDING) + SHOP_ITEM_PADDING
        item_y = tool_shop_item_list_rect.top + item_relative_y - tool_shop_scroll_offset

        if item_y + SHOP_ITEM_HEIGHT > tool_shop_item_list_rect.top and item_y < tool_shop_item_list_rect.bottom:
            item_rect_in_list = pygame.Rect(tool_shop_item_list_rect.left + SHOP_ITEM_PADDING, item_y,
                                            tool_shop_item_list_rect.width - SHOP_ITEM_PADDING * 2, SHOP_ITEM_HEIGHT)

            equipped_id = player_tools[selected_tool_category]['id']
            # 실제 구매한 도구 id 목록을 관리
            if 'owned_tool_ids' not in player_tools[selected_tool_category]:
                player_tools[selected_tool_category]['owned_tool_ids'] = []
            owned_tool_ids = player_tools[selected_tool_category]['owned_tool_ids']
            is_equipped = (equipped_id == item['id'])
            is_owned = item['id'] in owned_tool_ids

            # 선택된 아이템만 노란색 하이라이트, 나머지는 기본색
            if i == selected_tool_shop_item_index:
                pygame.draw.rect(screen, YELLOW, item_rect_in_list, border_radius=5)
            else:
                pygame.draw.rect(screen, LIGHT_GRAY, item_rect_in_list, border_radius=5)

            # 상태 텍스트(장착중/소지함) 표시: 배경색 없이 텍스트만 (아이템 이름 렌더링 이후에 위치)

            pygame.draw.rect(screen, DARK_GRAY, item_rect_in_list, 2, border_radius=5)

            # 아이템 이미지
            if item["image"]:
                img_rect = item["image"].get_rect(midleft=(item_rect_in_list.left + SHOP_ITEM_PADDING, item_rect_in_list.centery))
                screen.blit(item["image"], img_rect)

            # 아이템 이름
            name_text = seed_name_font.render(item["name"], True, BLACK)
            name_text_rect = name_text.get_rect(midleft=(item_rect_in_list.left + (SHOP_ITEM_PADDING + 30) + SHOP_ITEM_IMAGE_SIZE + 20, item_rect_in_list.centery - 15))
            screen.blit(name_text, name_text_rect)

            # 아이템 가격 및 배율
            price_text = price_text_font.render(f"가격: {item['price']:,}골드", True, BLUE)
            price_text_rect = price_text.get_rect(midleft=(item_rect_in_list.left + (SHOP_ITEM_PADDING + 30) + SHOP_ITEM_IMAGE_SIZE + 20, item_rect_in_list.centery + 15))
            screen.blit(price_text, price_text_rect)

            multiplier_text = multiplier_text_font.render(f"배율: {item['multiplier']}{' 전체' if item['id'] == 'watering_can_legendary' else ''}", True, ORANGE)
            multiplier_text_rect = multiplier_text.get_rect(midright=(item_rect_in_list.right - (SHOP_ITEM_PADDING + 30), item_rect_in_list.centery))
            screen.blit(multiplier_text, multiplier_text_rect)

            # 상태 텍스트(장착중/소지함) 가격 아래에는 표시하지 않음 (이름 옆에만 표시)

            # 아이템 가격 및 배율
            price_text = price_text_font.render(f"가격: {item['price']:,}골드", True, BLUE)
            price_text_rect = price_text.get_rect(midleft=(item_rect_in_list.left + (SHOP_ITEM_PADDING + 30) + SHOP_ITEM_IMAGE_SIZE + 20, item_rect_in_list.centery + 15))
            screen.blit(price_text, price_text_rect)

            multiplier_text = multiplier_text_font.render(f"배율: {item['multiplier']}{' 전체' if item['id'] == 'watering_can_legendary' else ''}", True, ORANGE)
            multiplier_text_rect = multiplier_text.get_rect(midright=(item_rect_in_list.right - (SHOP_ITEM_PADDING + 30), item_rect_in_list.centery))
            screen.blit(multiplier_text, multiplier_text_rect)

            # 상태 텍스트 표시
            status_text = None
            status_color = None
            if is_equipped:
                status_text = "장착중"
                status_color = (50, 180, 255)
            elif is_owned:
                status_text = "소지함"
                status_color = (100, 200, 100)
            if status_text:
                status_render = font.render(status_text, True, status_color)
                status_rect = status_render.get_rect(midleft=(name_text_rect.right + 10, name_text_rect.centery))
                screen.blit(status_render, status_rect)
            price_text = price_text_font.render(f"가격: {item['price']:,}골드", True, BLUE)
            price_text_rect = price_text.get_rect(midleft=(item_rect_in_list.left + (SHOP_ITEM_PADDING + 30) + SHOP_ITEM_IMAGE_SIZE + 20, item_rect_in_list.centery + 15))
            screen.blit(price_text, price_text_rect)

            multiplier_text = multiplier_text_font.render(f"배율: {item['multiplier']}{' 전체' if item['id'] == 'watering_can_legendary' else ''}", True, ORANGE)
            multiplier_text_rect = multiplier_text.get_rect(midright=(item_rect_in_list.right - (SHOP_ITEM_PADDING + 30), item_rect_in_list.centery))
            screen.blit(multiplier_text, multiplier_text_rect)

            # 상태 텍스트 표시
            status_text = None
            status_color = None
            if is_equipped:
                status_text = "장착중"
                status_color = (50, 180, 255)
            elif is_owned:
                status_text = "소지함"
                status_color = (100, 200, 100)
            if status_text:
                status_render = font.render(status_text, True, status_color)
                status_rect = status_render.get_rect(midleft=(name_text_rect.right + 10, name_text_rect.centery))
                screen.blit(status_render, status_rect)

    screen.set_clip(None)

    # 스크롤바 렌더링
    if max_scroll_offset > 0:
        scrollbar_width = 15
        scrollbar_x = tool_shop_item_list_rect.right - scrollbar_width - 10
        scrollbar_y = tool_shop_item_list_rect.top + 5
        scrollbar_height = tool_shop_item_list_rect.height - 10
        scrollbar_rect = pygame.Rect(scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height)
        pygame.draw.rect(screen, LIGHT_GRAY, scrollbar_rect, border_radius=5)

        handle_height_ratio = visible_list_height / total_items_height
        handle_height = scrollbar_height * handle_height_ratio
        handle_y_offset = (tool_shop_scroll_offset / max_scroll_offset) * (scrollbar_height - handle_height)
        scrollbar_handle_rect = pygame.Rect(scrollbar_x, scrollbar_y + handle_y_offset, scrollbar_width, handle_height)
        pygame.draw.rect(screen, DARK_GRAY, scrollbar_handle_rect, border_radius=5)

    # 오른쪽 상세 정보 패널 내용
    if selected_tool_shop_item_index != -1:
        selected_item = current_tool_items[selected_tool_shop_item_index]

        # 아이템 이미지
        if selected_item["image"]:
            detail_img_size = 150
            detail_img = pygame.transform.scale(selected_item["image"], (detail_img_size, detail_img_size))
            detail_img_rect = detail_img.get_rect(center=(detail_panel_rect.centerx, detail_panel_rect.top + 80))
            screen.blit(detail_img, detail_img_rect)

        # 아이템 이름
        detail_name_text = tool_shop_title_font.render(selected_item["name"], True, WHITE)
        detail_name_text_rect = detail_name_text.get_rect(center=(detail_panel_rect.centerx, detail_panel_rect.top + 200))
        screen.blit(detail_name_text, detail_name_text_rect)

        # 아이템 가격
        detail_price_text = tool_shop_pirce_font.render(f"가격: {selected_item['price']:,}골드", True, YELLOW)
        detail_price_text_rect = detail_price_text.get_rect(center=(detail_panel_rect.centerx, detail_panel_rect.top + 250))
        screen.blit(detail_price_text, detail_price_text_rect)

        # 아이템 배율
        detail_multiplier_text = font.render(f"배율: {selected_item['multiplier']}{' 전체' if selected_item['id'] == 'watering_can_legendary' else ''}", True, ORANGE)
        detail_multiplier_text_rect = detail_multiplier_text.get_rect(center=(detail_panel_rect.centerx, detail_panel_rect.top + 290))
        screen.blit(detail_multiplier_text, detail_multiplier_text_rect)

        # 아이템 설명
        description_lines = wrap_text(selected_item["description"], description_font, detail_panel_rect.width - 60)
        desc_y = detail_panel_rect.top + 330
        for line in description_lines:
            desc_text = description_font.render(line, True, LIGHT_GRAY)
            desc_text_rect = desc_text.get_rect(centerx=detail_panel_rect.centerx, top=desc_y)
            screen.blit(desc_text, desc_text_rect)
            desc_y += desc_text_rect.height + 5

        # 구매/장착 버튼 (test.py 스타일)
        buy_button_rect.center = (detail_panel_rect.centerx, detail_panel_rect.bottom - 50)
        equipped_id = player_tools[selected_tool_category]['id']
        owned_tool_ids = player_tools[selected_tool_category].get('owned_tool_ids', [])
        if equipped_id not in owned_tool_ids:
            owned_tool_ids.append(equipped_id)
        is_equipped = (equipped_id == selected_item['id'])
        is_owned = selected_item['id'] in owned_tool_ids
        can_afford = player_money >= selected_item["price"]
        if is_owned:
            button_label = "장착"
            button_color = BLUE if not is_equipped else TOOL_DISABLED_COLOR
        else:
            button_label = "구매"
            button_color = GREEN if can_afford else TOOL_DISABLED_COLOR
        pygame.draw.rect(screen, button_color, buy_button_rect, border_radius=5)
        buy_text = button_font.render(button_label, True, WHITE)
        buy_text_rect = buy_text.get_rect(center=buy_button_rect.center)
        screen.blit(buy_text, buy_text_rect)
        is_owned = (player_tools[selected_tool_category]['id'] == selected_item['id'])
        
        buy_button_color = GREEN if can_afford and not is_owned else TOOL_DISABLED_COLOR
        
        pygame.draw.rect(screen, buy_button_color, buy_button_rect, border_radius=5)
        buy_text = button_font.render("구매" if not is_owned else "소지함", True, WHITE)
        buy_text_rect = buy_text.get_rect(center=buy_button_rect.center)
        screen.blit(buy_text, buy_text_rect)


def draw_title_screen():
    """타이틀 화면을 그립니다."""
    if images and title_background_image:
        screen.blit(title_background_image, (0, 0))
    else:
        screen.fill(BLACK) # 배경 이미지가 없으면 검은색으로 채움

    title_text = title_font.render("농장 시뮬레이터", True, WHITE)
    title_text_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(title_text, title_text_rect)

    # 처음부터 버튼
    pygame.draw.rect(screen, GREEN, start_button_rect, border_radius=10)
    start_text = button_font.render("처음부터", True, WHITE)
    start_text_rect = start_text.get_rect(center=start_button_rect.center)
    screen.blit(start_text, start_text_rect)

    # 이어하기 버튼
    pygame.draw.rect(screen, BLUE, continue_button_rect, border_radius=10)
    continue_text = button_font.render("이어하기", True, WHITE)
    continue_text_rect = continue_text.get_rect(center=continue_button_rect.center)
    screen.blit(continue_text, continue_text_rect)

def draw_tool_button(rect, image, tool_name_for_comparison):
    """도구 버튼을 그립니다. 활성화 상태에 따라 테두리 색상과 두께가 변합니다."""
    border_color = BLACK
    border_thickness = TOOL_BORDER_THICKNESS

    if active_tool_on_click == tool_name_for_comparison:
        border_color = YELLOW
        border_thickness = TOOL_BORDER_THICKNESS + 2 # 활성화된 도구는 테두리 더 두껍게

    # 버튼 배경
    pygame.draw.rect(screen, LIGHT_GRAY, rect, border_radius=10)

    # 버튼 이미지 또는 텍스트
    if image:
        screen.blit(image, rect)
    else:
        temp_text = font.render(tool_name_for_comparison.replace('_', ' ').title(), True, BLACK)
        temp_text_rect = temp_text.get_rect(center=rect.center)
        screen.blit(temp_text, temp_text_rect)

    # 테두리
    pygame.draw.rect(screen, border_color, rect, border_thickness, border_radius=10)


def draw_game_screen():
    # 튜토리얼 오버레이 통합
    if show_tutorial:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        # 단계별 오버레이 투명도 및 강조 처리
        if tutorial_step == 7:
            overlay.fill((0, 0, 0, 120))  # 마지막 단계: 오버레이
            tutorial_done_text = button_font.render("튜토리얼이 완료되었습니다!", True, YELLOW)
            tutorial_done_text_rect = tutorial_done_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(tutorial_done_text, tutorial_done_text_rect)
        elif tutorial_step == 6:
            overlay.fill((0, 0, 0, 180))
            pot = pot_states[0]
            pygame.draw.rect(overlay, (0, 0, 0, 0), pot['rect'], border_radius=pot['rect'].width // 8)
            screen.blit(overlay, (0, 0))
            # 안내 텍스트 추가
            combined_text = "화분에 물을 뿌려보세요"
            main_text = button_font.render(combined_text, True, WHITE)
            main_text_rect = main_text.get_rect(center=(WIDTH // 2, 120))
            screen.blit(main_text, main_text_rect)
        else:
            overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        # 단계별 텍스트/강조 처리 (예시: 1~6단계)
        if tutorial_step == 1:
            highlight_rect = seed_select_button_rect.inflate(20, 20)
            pygame.draw.rect(screen, YELLOW, highlight_rect, border_radius=15)
            draw_tool_button(seed_select_button_rect, seed_select_button_image, 'seed_select')
            tutorial_text = button_font.render("씨앗 목록 버튼을 클릭하세요", True, WHITE)
            tutorial_text_rect = tutorial_text.get_rect(center=(seed_select_button_rect.centerx, seed_select_button_rect.top - 40))
            screen.blit(tutorial_text, tutorial_text_rect)
        elif tutorial_step == 2:
            # ...기존 2단계 강조 및 텍스트 코드...
            pass
        # ...3~6단계도 기존대로 분기...
    """게임 화면을 그립니다."""
    if images:
        screen.blit(images[0], (0, 0))
    else:
        screen.fill(BLUE)

    # 상단 정보 바
    pygame.draw.rect(screen, DARK_GRAY, (0, 0, WIDTH, 60))
    
    money_text = font.render(f"돈: {player_money:,}골드", True, YELLOW)
    screen.blit(money_text, (20, 15))

    # 몇 일차인지 계산
    global total_days_passed
    total_days_passed = 0
    temp_year, temp_month, temp_day = start_year, start_month, start_day

    while (temp_year < current_year) or \
          (temp_year == current_year and temp_month < current_month) or \
          (temp_year == current_year and temp_month == current_month and temp_day < current_day):
        total_days_passed += 1
        temp_day += 1
        if temp_day > get_days_in_month(temp_year, temp_month):
            temp_day = 1
            temp_month += 1
            if temp_month > 12:
                temp_month = 1
                temp_year += 1
    total_days_passed += 1 # 현재 날짜 포함

    day_count_text = font.render(f"현재 {total_days_passed}일차", True, WHITE)
    day_count_text_rect = day_count_text.get_rect(x=WIDTH - day_count_text.get_width() - 20, y=15) # 새롭게 rect 생성 및 위치 지정
    screen.blit(day_count_text, day_count_text_rect)

    date_text = font.render(f"날짜: {current_year}년 {current_month}월 {current_day}일", True, WHITE)

    # 날짜와 일차 텍스트 위치 변경: 일차 먼저, 그 다음 날짜
    # day_count_text_rect의 x 값을 기준으로 날짜 텍스트 배치
    date_text_x = day_count_text_rect.x - date_text.get_width() - 20 
    screen.blit(date_text, (date_text_x, 15))


    # 설정 아이콘 (오른쪽 아래로 이동)
    if settings_icon:
        settings_icon_rect = settings_icon.get_rect(bottomright=(WIDTH - 10, HEIGHT - 10)) # 오른쪽 아래에 배치
        screen.blit(settings_icon, settings_icon_rect)
    else:
        # 아이콘이 없을 경우 임시 사각형으로 표시 (디버깅용)
        pygame.draw.rect(screen, BLUE, (WIDTH - 60, HEIGHT - 60, 50, 50), border_radius=5)

    # 상점 및 도구 상점 버튼
    pygame.draw.rect(screen, BLUE, shop_button_rect, border_radius=5)
    shop_text = ingame_button_font.render("상점", True, WHITE)
    shop_text_rect = shop_text.get_rect(center=shop_button_rect.center)
    screen.blit(shop_text, shop_text_rect)

    pygame.draw.rect(screen, BLUE, tool_shop_button_rect, border_radius=5) # 제작대 -> 도구 상점
    tool_shop_text = ingame_button_font.render("도구 상점", True, WHITE) # 텍스트 변경
    tool_shop_text_rect = tool_shop_text.get_rect(center=tool_shop_button_rect.center)
    screen.blit(tool_shop_text, tool_shop_text_rect)

    # 밭 그리기
    for i, field in enumerate(field_states):
        color = BROWN
        
        # 작물 상태에 따라 테두리 색상 변경
        border_color = BLACK # 기본은 검은색 테두리
        if field['planted_plant_type'] is not None and field['current_growth_frame'] >= PLANT_INFO[field['planted_plant_type']]["growth_frames"]:
            border_color = GREEN # 다 자랐으면 초록색 테두리
        
        pygame.draw.rect(screen, color, field['rect'], border_radius=5) # 밭 배경 (모서리 둥글게)
        pygame.draw.rect(screen, border_color, field['rect'], PLOT_BORDER_THICKNESS, border_radius=5) # 테두리 (모서리 둥글게)

        if field['planted_plant_type'] is not None:
            plant_type = field['planted_plant_type']
            growth_info = PLANT_INFO[plant_type]
            growth_ratio = field['current_growth_frame'] / growth_info["growth_frames"]
            
            # 원본 식물 이미지 (fully grown)
            plant_image_original = growth_info["plant_image_original"]

            if plant_image_original:
                # 최대로 자랐을 때 식물의 목표 높이 (ITEM_SIZE에 final_scale_factor 적용)
                max_plant_display_height = int(ITEM_SIZE * field['final_scale_factor'])
                
                # 원본 이미지를 최대 높이에 맞춰 비율 유지하며 스케일
                original_width, original_height = plant_image_original.get_size()
                # 원본 이미지의 가로세로 비율 유지
                scale_ratio = max_plant_display_height / original_height
                scaled_width = int(original_width * scale_ratio)
                
                # 최소 너비와 높이를 보장 (이미지가 너무 작아지는 것 방지)
                scaled_width = max(1, scaled_width)
                max_plant_display_height = max(1, max_plant_display_height)

                scaled_full_plant_image = pygame.transform.scale(plant_image_original, (scaled_width, max_plant_display_height))

                # 현재 성장률에 따른 식물의 현재 높이 (최소 높이 설정)
                current_plant_height_pixels = int(max_plant_display_height * growth_ratio)
                if current_plant_height_pixels < 5: # 최소 5픽셀은 보이도록
                    current_plant_height_pixels = 5
                
                # 이미지를 아래에서부터 현재 높이만큼 잘라냄
                if scaled_full_plant_image.get_height() > 0 and current_plant_height_pixels <= scaled_full_plant_image.get_height():
                    crop_rect = (0, scaled_full_plant_image.get_height() - current_plant_height_pixels,
                                 scaled_full_plant_image.get_width(), current_plant_height_pixels)
                    
                    # Ensure crop_rect does not exceed image bounds (should be handled by logic, but as safeguard)
                    crop_rect_x = max(0, crop_rect[0])
                    crop_rect_y = max(0, crop_rect[1])
                    crop_rect_width = min(scaled_full_plant_image.get_width() - crop_rect_x, crop_rect[2])
                    crop_rect_height = min(scaled_full_plant_image.get_height() - crop_rect_y, crop_rect[3])
                    
                    # Ensure cropped height is positive
                    if crop_rect_height <= 0:
                        continue # 유효한 높이가 아니면 그리지 않음

                    try:
                        display_image = scaled_full_plant_image.subsurface((crop_rect_x, crop_rect_y, crop_rect_width, crop_rect_height))
                    except ValueError:
                        print(f"Subsurface error: crop_rect=({crop_rect_x}, {crop_rect_y}, {crop_rect_width}, {crop_rect_height}), image_size={scaled_full_plant_image.get_size()}")
                        continue # 오류 발생 시 현재 프레임은 그리지 않고 넘어감
                    
                    # 잘라낸 이미지를 밭의 하단 중앙에 위치시킴
                    img_rect = display_image.get_rect(midbottom=field['rect'].midbottom)
                    screen.blit(display_image, img_rect)
        else:
            # 씨앗 심을 수 있는 칸에 '+' 표시
            if plus_sign_image:
                plus_rect = plus_sign_image.get_rect(center=field['rect'].center)
                screen.blit(plus_sign_image, plus_rect)

        if hovered_plot_type == 'field' and hovered_plot_index == i:
            pygame.draw.rect(screen, YELLOW, field['rect'], 3, border_radius=5) # 호버 효과도 둥글게

    # 화분 그리기 (밭과 동일한 색상)
    BRIGHT_BROWN = (180, 120, 60)
    for i, pot in enumerate(pot_states):
        # 튜토리얼 6단계에서 첫 번째 화분만 밝게 처리
        is_tutorial6_highlight = show_tutorial and tutorial_step == 6 and i == 0
        color = BRIGHT_BROWN if is_tutorial6_highlight else BROWN
        border_color = BLACK
        if pot['planted_plant_type'] is not None and pot['current_growth_frame'] >= PLANT_INFO[pot['planted_plant_type']]['growth_frames']:
            border_color = GREEN
        pygame.draw.rect(screen, color, pot['rect'], border_radius=5)
        pygame.draw.rect(screen, border_color, pot['rect'], PLOT_BORDER_THICKNESS, border_radius=5)

        if pot['planted_plant_type'] is not None:
            plant_type = pot['planted_plant_type']
            growth_info = PLANT_INFO[plant_type]
            growth_ratio = pot['current_growth_frame'] / growth_info['growth_frames']
            plant_image_original = growth_info['plant_image_original']
            if plant_image_original:
                max_plant_display_height = int(ITEM_SIZE * pot['final_scale_factor'])
                original_width, original_height = plant_image_original.get_size()
                scale_ratio = max_plant_display_height / original_height
                scaled_width = int(original_width * scale_ratio)
                scaled_width = max(1, scaled_width)
                max_plant_display_height = max(1, max_plant_display_height)
                scaled_full_plant_image = pygame.transform.scale(plant_image_original, (scaled_width, max_plant_display_height))
                current_plant_height_pixels = int(max_plant_display_height * growth_ratio)
                if current_plant_height_pixels < 5:
                    current_plant_height_pixels = 5
                if scaled_full_plant_image.get_height() > 0 and current_plant_height_pixels <= scaled_full_plant_image.get_height():
                    crop_rect = (0, scaled_full_plant_image.get_height() - current_plant_height_pixels,
                                 scaled_full_plant_image.get_width(), current_plant_height_pixels)
                    crop_rect_x = max(0, crop_rect[0])
                    crop_rect_y = max(0, crop_rect[1])
                    crop_rect_width = min(scaled_full_plant_image.get_width() - crop_rect_x, crop_rect[2])
                    crop_rect_height = min(scaled_full_plant_image.get_height() - crop_rect_y, crop_rect[3])
                    if crop_rect_height <= 0:
                        continue
                    try:
                        display_image = scaled_full_plant_image.subsurface((crop_rect_x, crop_rect_y, crop_rect_width, crop_rect_height))
                    except ValueError:
                        print(f"Subsurface error: crop_rect=({crop_rect_x}, {crop_rect_y}, {crop_rect_width}, {crop_rect_height}), image_size={scaled_full_plant_image.get_size()}")
                        continue
                    img_rect = display_image.get_rect(midbottom=pot['rect'].midbottom)
                    # 튜토리얼 6단계 첫 화분은 작물도 밝게
                    # 튜토리얼 6단계도 일반 작물 이미지 그대로 사용 (색 보정 X)
                    screen.blit(display_image, img_rect)
        else:
            if plus_sign_image:
                plus_rect = plus_sign_image.get_rect(center=pot['rect'].center)
                screen.blit(plus_sign_image, plus_rect)
        if hovered_plot_type == 'pot' and hovered_plot_index == i:
            pygame.draw.rect(screen, YELLOW, pot['rect'], 3, border_radius=5)

    # 도구 버튼 그리기 (draw_tool_button 함수 사용)
    draw_tool_button(watering_can_rect, watering_can_image, 'watering_can')
    current_time = time.time()
    if current_time - last_watering_can_use_time < WATERING_CAN_COOLDOWN:
        remaining_time = max(0, WATERING_CAN_COOLDOWN - (current_time - last_watering_can_use_time))
        cooldown_text = cooldown_font.render(f"{remaining_time:.1f}s", True, RED)
        cooldown_text_rect = cooldown_text.get_rect(center=watering_can_rect.center)
        overlay_cooldown = pygame.Surface(watering_can_rect.size, pygame.SRCALPHA)
        overlay_cooldown.fill((0, 0, 0, 150)) # 투명한 검은색 오버레이
        screen.blit(overlay_cooldown, watering_can_rect.topleft)
        screen.blit(cooldown_text, cooldown_text_rect)

    draw_tool_button(scythe_rect, scythe_image, 'scythe')
    draw_tool_button(seed_select_button_rect, seed_select_button_image, 'seed_select')

    # 튜토리얼 오버레이: 단계별 안내 및 강조
    overlay = None
    if show_tutorial:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        if tutorial_step == 6:
            pot = pot_states[0]
            # pot 영역만 투명하게 뚫기
            pygame.draw.rect(overlay, (0, 0, 0, 0), pot['rect'], border_radius=pot['rect'].width // 8)
        screen.blit(overlay, (0, 0))
        if tutorial_step == 1:
            # 씨앗 목록 버튼 강조
            highlight_rect = seed_select_button_rect.inflate(20, 20)
            pygame.draw.rect(screen, YELLOW, highlight_rect, border_radius=15)
            draw_tool_button(seed_select_button_rect, seed_select_button_image, 'seed_select')
            tutorial_text = button_font.render("씨앗 목록 버튼을 클릭하세요", True, WHITE)
            tutorial_text_rect = tutorial_text.get_rect(center=(seed_select_button_rect.centerx, seed_select_button_rect.top - 40))
            screen.blit(tutorial_text, tutorial_text_rect)
        elif tutorial_step == 2:
            # 씨앗1(해바라기) 강조
            # 씨앗 메뉴가 열려있을 때만 강조
            for seed_option in seed_options:
                current_x = seed_select_button_rect.x + (seed_option['target_x'] - seed_select_button_rect.x) * seed_animation_current_offset
                seed_rect = pygame.Rect(current_x, seed_option['rect'].y, seed_option['rect'].width, seed_option['rect'].height)
                if seed_option['plant_type'] == 'sunflower':
                    highlight_rect = seed_rect.inflate(20, 20)
                    pygame.draw.rect(screen, YELLOW, highlight_rect, border_radius=15)
                    tutorial_text = button_font.render("해바라기 씨앗을 클릭하세요", True, WHITE)
                    tutorial_text_rect = tutorial_text.get_rect(center=(seed_rect.centerx, seed_rect.top - 40))
                    screen.blit(tutorial_text, tutorial_text_rect)
                    break
        elif tutorial_step == 3:
            # 튜토리얼3: 왼쪽 첫 번째 화분 강조(노란 테두리 + 밝은 내부)
            left_pot_rect = pot_states[0]['rect']
            pot = pot_states[0]
            color = BROWN
            border_color = BLACK
            if pot['planted_plant_type'] is not None and pot['current_growth_frame'] >= PLANT_INFO[pot['planted_plant_type']]['growth_frames']:
                border_color = GREEN
            pygame.draw.rect(screen, color, left_pot_rect, border_radius=5)
            pygame.draw.rect(screen, border_color, left_pot_rect, PLOT_BORDER_THICKNESS, border_radius=5)
            highlight_yellow = (255, 255, 80)
            pygame.draw.rect(screen, highlight_yellow, left_pot_rect, 6, border_radius=left_pot_rect.width // 8)
            if pot['planted_plant_type'] is None and plus_sign_image:
                plus_rect = plus_sign_image.get_rect(center=left_pot_rect.center)
                screen.blit(plus_sign_image, plus_rect)
            tutorial_text1 = button_font.render("씨앗을 화분에 심어보세요!", True, WHITE)
            tutorial_text2 = button_font.render("씨앗을 선택한 후 화분을 클릭하세요.", True, WHITE)
            tutorial_text1_rect = tutorial_text1.get_rect(center=(left_pot_rect.centerx, left_pot_rect.top - 65))
            tutorial_text2_rect = tutorial_text2.get_rect(center=(left_pot_rect.centerx, left_pot_rect.top - 25))
            screen.blit(tutorial_text1, tutorial_text1_rect)
            screen.blit(tutorial_text2, tutorial_text2_rect)
        elif tutorial_step == 4:
            # 튜토리얼4: 물뿌리개 버튼 강조 (테두리 더 두껍게)
            highlight_rect = watering_can_rect.inflate(10, 10)
            pygame.draw.rect(screen, YELLOW, highlight_rect, 10, border_radius=15)
            draw_tool_button(watering_can_rect, watering_can_image, 'watering_can')
            # 텍스트를 물뿌리개 오른쪽으로 이동, 화면에 잘리지 않게
            tutorial_text = button_font.render("물뿌리개를 클릭하세요!", True, WHITE)
            text_x = watering_can_rect.right + 40
            text_y = watering_can_rect.top + watering_can_rect.height // 2
            tutorial_text_rect = tutorial_text.get_rect(midleft=(text_x, text_y))
            screen.blit(tutorial_text, tutorial_text_rect)
        elif tutorial_step == 5:
            # 튜토리얼5: 씨앗이 심어진 화분 강조(노란 테두리) 및 안내 텍스트, 내부는 원래 색상(BROWN)
            highlighted = False
            for pot in pot_states:
                if pot['planted_plant_type'] is not None:
                    pot_rect = pot['rect']
                    # 내부를 원래 색상으로 그림
                    pygame.draw.rect(screen, BROWN, pot_rect, border_radius=pot_rect.width // 8)
                    # 노란 테두리 강조
                    pygame.draw.rect(screen, YELLOW, pot_rect, 8, border_radius=pot_rect.width // 8)
                    tutorial_text = button_font.render("화분에 물을 뿌려보세요!", True, WHITE)
                    tutorial_text_rect = tutorial_text.get_rect(center=(pot_rect.centerx, pot_rect.top - 40))
                    # 작물 성장 안내 텍스트 추가
                    growth_text = button_font.render("작물은 하루가 지날 때마다 조금씩 자랍니다", True, WHITE)
                    growth_text_rect = growth_text.get_rect(center=(pot_rect.centerx, pot_rect.top - 80))
                    screen.blit(growth_text, growth_text_rect)
                    screen.blit(tutorial_text, tutorial_text_rect)
                    highlighted = True
                    break
            # 심어진 화분이 없으면 왼쪽 첫 번째 화분 강조
            if not highlighted:
                pot_rect = pot_states[0]['rect']
                pygame.draw.rect(screen, BROWN, pot_rect, border_radius=pot_rect.width // 8)
                pygame.draw.rect(screen, YELLOW, pot_rect, 8, border_radius=pot_rect.width // 8)
                tutorial_text = button_font.render("화분에 물을 뿌려보세요!", True, WHITE)
                tutorial_text_rect = tutorial_text.get_rect(center=(pot_rect.centerx, pot_rect.top - 40))
                # 작물 성장 안내 텍스트 추가
                growth_text = button_font.render("작물은 하루가 지날 때마다 조금씩 자랍니다", True, WHITE)
                growth_text_rect = growth_text.get_rect(center=(pot_rect.centerx, pot_rect.top - 80))
                screen.blit(growth_text, growth_text_rect)
                screen.blit(tutorial_text, tutorial_text_rect)
        elif tutorial_step == 6:
            # 튜토리얼6: 낫 버튼 강조 및 안내 + 화분 강조(테두리만, 작물 그린 후)
            highlighted = False
            border_pad = 6  # 강조 테두리용 여유 공간
            for pot in pot_states:
                if pot['planted_plant_type'] is not None:
                    pot_rect = pot['rect']
                    highlight_rect = pot_rect.inflate(border_pad*2, border_pad*2)
                    # 내부(BROWN)는 칠하지 않고 테두리만 그림
                    pygame.draw.rect(screen, YELLOW, highlight_rect, 8, border_radius=highlight_rect.width // 8)
                    highlighted = True
                    break
            if not highlighted:
                pot_rect = pot_states[0]['rect']
                highlight_rect = pot_rect.inflate(border_pad*2, border_pad*2)
                pygame.draw.rect(screen, YELLOW, highlight_rect, 8, border_radius=highlight_rect.width // 8)
            highlight_rect = scythe_rect.inflate(10, 10)
            pygame.draw.rect(screen, YELLOW, highlight_rect, 10, border_radius=15)
            draw_tool_button(scythe_rect, scythe_image, 'scythe')
            tutorial_text = button_font.render("낫을 클릭해 수확하세요!", True, WHITE)
            text_x = scythe_rect.right + 40
            text_y = scythe_rect.top + scythe_rect.height // 2
            tutorial_text_rect = tutorial_text.get_rect(midleft=(text_x, text_y))
            screen.blit(tutorial_text, tutorial_text_rect)

    # 씨앗 선택 메뉴 그리기 (애니메이션 적용)
    if show_seed_options or is_seed_animating:
        for seed_option in seed_options:
            current_x = seed_select_button_rect.x + (seed_option['target_x'] - seed_select_button_rect.x) * seed_animation_current_offset
            seed_rect = pygame.Rect(current_x, seed_option['rect'].y, seed_option['rect'].width, seed_option['rect'].height)

            # 튜토리얼 2, 3단계에서만 씨앗 배경을 밝게(LIGHT_GRAY) 처리, 4단계는 흰색
            if show_tutorial and tutorial_step in (2, 3):
                pygame.draw.rect(screen, LIGHT_GRAY, seed_rect, border_radius=10)
            else:
                pygame.draw.rect(screen, WHITE, seed_rect, border_radius=10)

            if seed_option['image']:
                screen.blit(seed_option['image'], seed_rect)
                # 튜토리얼 2, 3단계에서 해바라기씨앗 이외는 이미지 어둡게 오버레이, 4단계는 모든 씨앗 이미지 어둡게
                if show_tutorial and ((tutorial_step in (2, 3) and seed_option['plant_type'] != 'sunflower') or tutorial_step == 4):
                    dark_img_overlay = pygame.Surface((seed_rect.width, seed_rect.height), pygame.SRCALPHA)
                    dark_img_overlay.fill((0, 0, 0, 160))
                    screen.blit(dark_img_overlay, seed_rect.topleft)
            else:
                temp_text = font.render(seed_option['plant_type'], True, BLACK) # 디버깅용 텍스트
                temp_text_rect = temp_text.get_rect(center=seed_rect.center)
                screen.blit(temp_text, temp_text_rect)
                # 튜토리얼 2, 3단계에서 텍스트 어둡게 오버레이
                if show_tutorial and tutorial_step in (2, 3) and seed_option['plant_type'] != 'sunflower':
                    dark_txt_overlay = pygame.Surface((seed_rect.width, seed_rect.height), pygame.SRCALPHA)
                    dark_txt_overlay.fill((0, 0, 0, 50))
                    screen.blit(dark_txt_overlay, seed_rect.topleft)

            # 수량 표시
            seed_count = player_inventory.get(seed_option['plant_type'], 0)
            count_text = seed_name_font.render(f"{seed_count}개", True, BLACK)
            count_text_rect = count_text.get_rect(center=(seed_rect.centerx, seed_rect.bottom + 10))
            screen.blit(count_text, count_text_rect)

            # 선택된 씨앗 하이라이트 (검은색 테두리보다 나중에 그려서 보이게 함)
            # 선택된 씨앗은 검은색 테두리 대신 노란색 테두리
            if selected_seed_name == seed_option['plant_type']:
                pygame.draw.rect(screen, YELLOW, seed_rect, TOOL_BORDER_THICKNESS + 2, border_radius=10)
            else: # 선택되지 않은 씨앗은 검은색 테두리
                pygame.draw.rect(screen, BLACK, seed_rect, TOOL_BORDER_THICKNESS, border_radius=10)


def wrap_text(text, font, max_width):
    """텍스트를 주어진 너비에 맞춰 여러 줄로 나눕니다."""
    words = text.split(' ')
    lines = []
    current_line = []
    for word in words:
        # 현재 줄에 단어를 추가했을 때의 너비를 확인
        test_line = ' '.join(current_line + [word])
        if font.size(test_line)[0] <= max_width:
            current_line.append(word)
        else:
            # 너비를 초과하면 새 줄 시작
            lines.append(' '.join(current_line))
            current_line = [word]
    lines.append(' '.join(current_line)) # 마지막 줄 추가
    return lines

def handle_game_screen_click(pos):
    global show_tutorial, tutorial_step
    global game_state, previous_game_state, active_tool_on_click, last_watering_can_use_time, show_seed_options, is_seed_animating, seed_animation_target_offset, seed_animation_current_offset, selected_seed_name, player_money
    # 튜토리얼 7단계: 아무 곳이나 클릭하면 튜토리얼 종료
    if show_tutorial and tutorial_step == 7:
        show_tutorial = False
        return
    if show_tutorial:
        if tutorial_step == 4:
            # 4단계에서는 물뿌리개 버튼만 클릭 가능
            if watering_can_rect.collidepoint(pos):
                active_tool_on_click = 'watering_can'
                tutorial_step = 5  # 물뿌리개 클릭 시 5단계로 이동(화분 강조 및 안내)
            return
        elif tutorial_step == 5:
            # 5단계: 강조된 화분에 물을 뿌리면 작물이 즉시 다 자라게 하고 6단계로 이동
            pot = pot_states[0]
            if pot['rect'].collidepoint(pos) and active_tool_on_click == 'watering_can':
                if pot['planted_plant_type'] is not None:
                    pot['current_growth_frame'] = PLANT_INFO[pot['planted_plant_type']]['growth_frames']
                    tutorial_step = 6
            return
        elif tutorial_step == 6:
            # 6단계: 낫 버튼 클릭 시 낫 선택, 강조된(첫 번째) 화분 클릭 시 수확
            if scythe_rect.collidepoint(pos):
                active_tool_on_click = 'scythe'
                return
            pot = pot_states[0]
            if pot['rect'].collidepoint(pos):
                if active_tool_on_click != 'scythe':
                    # 낫이 선택되지 않았을 때 안내
                    message_display_pos = (WIDTH // 2, 100)
                    active_temporary_messages.append(TemporaryMessageDisplay("낫을 먼저 선택하세요!", message_display_pos, duration=1.5, color=ORANGE, font=font))
                    return
                if pot['planted_plant_type'] is not None and pot['current_growth_frame'] >= PLANT_INFO[pot['planted_plant_type']]['growth_frames']:
                    plant_type = pot['planted_plant_type']
                    crop_info = CROP_PRICES[plant_type]
                    harvested_quantity = 0
                    if isinstance(crop_info, dict):
                        if crop_info.get('type') == 'fixed':
                            harvested_quantity = crop_info['quantity']
                        elif crop_info.get('type') == 'random':
                            min_q, max_q = crop_info['quantity_range']
                            harvested_quantity = random.randint(min_q, max_q)
                        income = int(harvested_quantity * crop_info['price_per_item'] * player_tools['scythe']['multiplier'])
                        player_money += income
                        message_display_pos = (WIDTH // 2, 100)
                        active_temporary_messages.append(TemporaryMessageDisplay([
                            ("수확! ", GREEN), (f"{crop_info['name']} {harvested_quantity}개", BLACK), (f" +{income:,}골드", YELLOW)
                        ], message_display_pos, duration=2.0, font=font, is_multi_colored=True))
                        pot['planted_plant_type'] = None
                        pot['current_growth_frame'] = 0
                        pot['final_scale_factor'] = 1.0
                        if scythe_harvest_sound:
                            scythe_harvest_sound.play()
                        # 튜토리얼 7단계로 이동
                        tutorial_step = 7
                    else:
                        # crop_info가 dict가 아니면 수확 로직을 건너뜀 (에러 방지)
                        message_display_pos = (WIDTH // 2, 100)
                        active_temporary_messages.append(TemporaryMessageDisplay("수확 정보 오류", message_display_pos, duration=1.5, color=RED, font=font))
                else:
                    # 수확 조건이 안 맞을 때 안내
                    message_display_pos = (WIDTH // 2, 100)
                    if pot['planted_plant_type'] is None:
                        active_temporary_messages.append(TemporaryMessageDisplay("수확할 작물이 없습니다.", message_display_pos, duration=1.5, color=GRAY, font=font))
                    else:
                        active_temporary_messages.append(TemporaryMessageDisplay("아직 다 자라지 않았습니다!", message_display_pos, duration=1.5, color=RED, font=font))
                return
            # 그 외 클릭은 무시
            return
    # 중복된 global 선언 제거
    if show_tutorial:
        if tutorial_step == 4:
            # 4단계에서는 물뿌리개 버튼만 클릭 가능
            if watering_can_rect.collidepoint(pos):
                active_tool_on_click = 'watering_can'
                tutorial_step = 5  # 물뿌리개 클릭 시 5단계로 이동(화분 강조 및 안내)
            return
        if tutorial_step == 1:
            if seed_select_button_rect.collidepoint(pos):
                active_tool_on_click = 'seed_select'
                show_seed_options = not show_seed_options
                is_seed_animating = True
                if show_seed_options:
                    seed_animation_target_offset = 1.0
                    seed_animation_current_offset = 0.0
                else:
                    seed_animation_target_offset = 0.0
                    seed_animation_current_offset = 1.0
                tutorial_step = 2  # 씨앗 목록 클릭 후 다음 단계로
            return
        elif tutorial_step == 2:
            # 씨앗 메뉴가 열려있을 때만 처리
            for seed_option in seed_options:
                current_x = seed_select_button_rect.x + (seed_option['target_x'] - seed_select_button_rect.x) * seed_animation_current_offset
                seed_rect_current_animated_pos = pygame.Rect(current_x, seed_option['rect'].y, seed_option['rect'].width, seed_option['rect'].height)
                if seed_option['plant_type'] == 'sunflower' and seed_rect_current_animated_pos.collidepoint(pos):
                    selected_seed_name = seed_option['plant_type']
                    active_tool_on_click = 'seed_select'
                    tutorial_step = 3  # 3단계로 이동: 씨앗을 화분에 심기 안내
                    return
            return
        elif tutorial_step == 3:
            # 3단계에서는 강조된(첫 번째) 화분만 클릭 가능, 나머지 클릭은 무시
            pot = pot_states[0]
            if pot['rect'].collidepoint(pos):
                message_display_pos = (WIDTH // 2, 100)
                if active_tool_on_click == 'watering_can':
                    current_time = time.time()
                    if current_time - last_watering_can_use_time >= WATERING_CAN_COOLDOWN:
                        if pot['planted_plant_type'] is not None and pot['current_growth_frame'] < PLANT_INFO[pot['planted_plant_type']]["growth_frames"]:
                            growth_amount = player_tools['watering_can']['multiplier']
                            pot['current_growth_frame'] = min(PLANT_INFO[pot['planted_plant_type']]["growth_frames"], pot['current_growth_frame'] + growth_amount)
                            active_temporary_messages.append(TemporaryMessageDisplay(f"물 주기! +{growth_amount} 성장", message_display_pos, duration=1.5, color=BLUE, font=font))
                            last_watering_can_use_time = current_time
                        elif pot['planted_plant_type'] is not None and pot['current_growth_frame'] >= PLANT_INFO[pot['planted_plant_type']]["growth_frames"]:
                            active_temporary_messages.append(TemporaryMessageDisplay("이미 다 자란 작물입니다!", message_display_pos, duration=1.5, color=ORANGE, font=font))
                        else:
                            active_temporary_messages.append(TemporaryMessageDisplay("아무것도 심어져 있지 않습니다.", message_display_pos, duration=1.5, color=GRAY, font=font))
                    else:
                        active_temporary_messages.append(TemporaryMessageDisplay("물뿌리개 쿨타임 중!", message_display_pos, duration=1.5, color=RED, font=font))
                elif active_tool_on_click == 'scythe':
                    if pot['planted_plant_type'] is not None and pot['current_growth_frame'] >= PLANT_INFO[pot['planted_plant_type']]["growth_frames"]:
                        plant_type = pot['planted_plant_type']
                        crop_info = CROP_PRICES[plant_type]
                        harvested_quantity = 0
                        if isinstance(crop_info, dict):
                            if crop_info.get('type') == 'fixed':
                                harvested_quantity = crop_info['quantity']
                            elif crop_info.get('type') == 'random':
                                min_q, max_q = crop_info['quantity_range']
                                harvested_quantity = random.randint(min_q, max_q)
                            income = int(harvested_quantity * crop_info['price_per_item'] * player_tools['scythe']['multiplier'])
                            player_money += income
                            active_temporary_messages.append(TemporaryMessageDisplay([
                                ("수확! ", GREEN), (f"{crop_info['name']} {harvested_quantity}개", BLACK), (f" +{income:,}골드", YELLOW)
                            ], message_display_pos, duration=2.0, font=font, is_multi_colored=True))
                            pot['planted_plant_type'] = None
                            pot['current_growth_frame'] = 0
                            pot['final_scale_factor'] = 1.0
                            if scythe_harvest_sound:
                                scythe_harvest_sound.play()
                        else:
                            active_temporary_messages.append(TemporaryMessageDisplay("수확 정보 오류", message_display_pos, duration=1.5, color=RED, font=font))
                    elif pot['planted_plant_type'] is not None and pot['current_growth_frame'] < PLANT_INFO[pot['planted_plant_type']]["growth_frames"]:
                        active_temporary_messages.append(TemporaryMessageDisplay("아직 다 자라지 않았습니다!", message_display_pos, duration=1.5, color=RED, font=font))
                    else:
                        active_temporary_messages.append(TemporaryMessageDisplay("수확할 작물이 없습니다.", message_display_pos, duration=1.5, color=GRAY, font=font))
                elif active_tool_on_click == 'seed_select':
                    if selected_seed_name is not None:
                        if pot['planted_plant_type'] is None:
                            if player_inventory.get(selected_seed_name, 0) > 0:
                                pot['planted_plant_type'] = selected_seed_name
                                pot['current_growth_frame'] = 0
                                pot['final_scale_factor'] = random.uniform(0.7, 1.3)
                                player_inventory[selected_seed_name] -= 1
                                active_temporary_messages.append(TemporaryMessageDisplay(f"{PLANT_INFO[selected_seed_name]['seed_name']} 심기!", message_display_pos, duration=1.5, color=GREEN, font=font))
                                # 튜토리얼 3단계에서 씨앗 심으면 씨앗 메뉴 닫기 애니메이션 실행
                                if show_tutorial and tutorial_step == 3 and show_seed_options:
                                    show_seed_options = False
                                    is_seed_animating = True
                                    seed_animation_target_offset = 0.0
                                    seed_animation_current_offset = 1.0
                                tutorial_step = 4  # 씨앗 심으면 4단계로 이동
                            else:
                                active_temporary_messages.append(TemporaryMessageDisplay("씨앗이 부족합니다!", message_display_pos, duration=1.5, color=RED, font=font))
                        else:
                            active_temporary_messages.append(TemporaryMessageDisplay("이미 작물이 심어져 있습니다.", message_display_pos, duration=1.5, color=RED, font=font))
                    else:
                        active_temporary_messages.append(TemporaryMessageDisplay("씨앗을 선택해주세요!", message_display_pos, duration=1.5, color=ORANGE, font=font))
                else:
                    active_temporary_messages.append(TemporaryMessageDisplay("도구를 선택해주세요!", message_display_pos, duration=1.5, color=ORANGE, font=font))
                return
            return
    # 설정 아이콘 클릭
    settings_icon_rect = settings_icon.get_rect(bottomright=(WIDTH - 10, HEIGHT - 10)) # 오른쪽 아래로 이동
    if settings_icon_rect.collidepoint(pos):
        previous_game_state = game_state
        game_state = 'SETTINGS'
        return

    # 상점 버튼 클릭
    if shop_button_rect.collidepoint(pos):
        previous_game_state = game_state
        game_state = 'SHOP'
        return

    # 도구 상점 버튼 클릭 (이름 변경 반영)
    if tool_shop_button_rect.collidepoint(pos):
        previous_game_state = game_state
        game_state = 'TOOL_SHOP' # 상태 변경
        return

    # 도구 버튼 클릭
    if watering_can_rect.collidepoint(pos):
        active_tool_on_click = 'watering_can'
        # (튜토리얼 4단계에서 씨앗 메뉴 닫기 애니메이션 제거)
        return
    elif scythe_rect.collidepoint(pos):
        active_tool_on_click = 'scythe'
        if show_seed_options: # 씨앗 메뉴 열려있으면 닫기 애니메이션
            show_seed_options = False
            is_seed_animating = True
            seed_animation_target_offset = 0.0
            seed_animation_current_offset = 1.0
        return
    elif seed_select_button_rect.collidepoint(pos):
        active_tool_on_click = 'seed_select'
        show_seed_options = not show_seed_options # 씨앗 메뉴 토글
        is_seed_animating = True
        if show_seed_options: # 열리는 애니메이션
            seed_animation_target_offset = 1.0
            seed_animation_current_offset = 0.0
        else: # 닫히는 애니메이션
            seed_animation_target_offset = 0.0
            seed_animation_current_offset = 1.0
        return

    # 씨앗 선택 메뉴 클릭 (show_seed_options가 True일 때만)
    if show_seed_options or is_seed_animating: # 애니메이션 중에도 클릭 가능하게
        for seed_option in seed_options:
            # 애니메이션 중인 씨앗 버튼의 현재 위치 계산
            current_x = seed_select_button_rect.x + (seed_option['target_x'] - seed_select_button_rect.x) * seed_animation_current_offset
            seed_rect_current_animated_pos = pygame.Rect(current_x, seed_option['rect'].y, seed_option['rect'].width, seed_option['rect'].height)
            if seed_rect_current_animated_pos.collidepoint(pos):
                selected_seed_name = seed_option['plant_type']
                # show_seed_options는 유지 (요청에 따라)
                active_tool_on_click = 'seed_select' # 씨앗 선택 후 도구를 씨앗으로 유지
                return

    # 밭 클릭
    for i, field in enumerate(field_states):
        if field['rect'].collidepoint(pos):
            # 텍스트 메시지 위치를 화면 상단으로 변경
            message_display_pos = (WIDTH // 2, 100)
            if active_tool_on_click == 'watering_can':
                current_time = time.time()
                if current_time - last_watering_can_use_time >= WATERING_CAN_COOLDOWN:
                    if field['planted_plant_type'] is not None and field['current_growth_frame'] < PLANT_INFO[field['planted_plant_type']]["growth_frames"]:
                        # 물 주기 시 성장 프레임 추가, 최대 성장 프레임 넘지 않도록
                        # 물뿌리개 배율 적용
                        growth_amount = player_tools['watering_can']['multiplier']
                        field['current_growth_frame'] = min(PLANT_INFO[field['planted_plant_type']]["growth_frames"], field['current_growth_frame'] + growth_amount)
                        active_temporary_messages.append(TemporaryMessageDisplay(f"물 주기! +{growth_amount} 성장", message_display_pos, duration=1.5, color=BLUE, font=font))
                        last_watering_can_use_time = current_time
                    elif field['planted_plant_type'] is not None and field['current_growth_frame'] >= PLANT_INFO[field['planted_plant_type']]["growth_frames"]:
                        active_temporary_messages.append(TemporaryMessageDisplay("이미 다 자란 작물입니다!", message_display_pos, duration=1.5, color=ORANGE, font=font))
                    else:
                        active_temporary_messages.append(TemporaryMessageDisplay("아무것도 심어져 있지 않습니다.", message_display_pos, duration=1.5, color=GRAY, font=font))
                else:
                    active_temporary_messages.append(TemporaryMessageDisplay("물뿌리개 쿨타임 중!", message_display_pos, duration=1.5, color=RED, font=font))
            elif active_tool_on_click == 'scythe':
                if field['planted_plant_type'] is not None and field['current_growth_frame'] >= PLANT_INFO[field['planted_plant_type']]["growth_frames"]:
                    plant_type = field['planted_plant_type']
                    crop_info = CROP_PRICES[plant_type]
                    harvested_quantity = 0
                    if isinstance(crop_info, dict):
                        if crop_info.get('type') == 'fixed':
                            harvested_quantity = crop_info['quantity']
                        elif crop_info.get('type') == 'random':
                            min_q, max_q = crop_info['quantity_range']
                            harvested_quantity = random.randint(min_q, max_q)
                        # 낫 배율 적용
                        income = int(harvested_quantity * crop_info['price_per_item'] * player_tools['scythe']['multiplier'])
                        player_money += income
                        active_temporary_messages.append(TemporaryMessageDisplay(
                            [("수확! ", GREEN), (f"{crop_info['name']} {harvested_quantity}개", BLACK), (f" +{income:,}골드", YELLOW)],
                            message_display_pos, duration=2.0, font=font, is_multi_colored=True
                        ))
                        field['planted_plant_type'] = None
                        field['current_growth_frame'] = 0
                        field['final_scale_factor'] = 1.0 # 초기화
                        if scythe_harvest_sound: # 효과음 재생
                            scythe_harvest_sound.play()
                    else:
                        active_temporary_messages.append(TemporaryMessageDisplay("수확 정보 오류", message_display_pos, duration=1.5, color=RED, font=font))
                elif field['planted_plant_type'] is not None and field['current_growth_frame'] < PLANT_INFO[field['planted_plant_type']]["growth_frames"]:
                    active_temporary_messages.append(TemporaryMessageDisplay("아직 다 자라지 않았습니다!", message_display_pos, duration=1.5, color=RED, font=font))
                else:
                    active_temporary_messages.append(TemporaryMessageDisplay("수확할 작물이 없습니다.", message_display_pos, duration=1.5, color=GRAY, font=font))
            elif active_tool_on_click == 'seed_select':
                if selected_seed_name is not None:
                    if field['planted_plant_type'] is None:
                        if player_inventory.get(selected_seed_name, 0) > 0:
                            field['planted_plant_type'] = selected_seed_name
                            field['current_growth_frame'] = 0
                            field['final_scale_factor'] = random.uniform(0.7, 1.3) # 씨앗 심을 때 크기 결정
                            player_inventory[selected_seed_name] -= 1
                            active_temporary_messages.append(TemporaryMessageDisplay(f"{PLANT_INFO[selected_seed_name]['seed_name']} 심기!", message_display_pos, duration=1.5, color=GREEN, font=font))
                        else:
                            active_temporary_messages.append(TemporaryMessageDisplay("씨앗이 부족합니다!", message_display_pos, duration=1.5, color=RED, font=font))
                    else:
                        active_temporary_messages.append(TemporaryMessageDisplay("이미 작물이 심어져 있습니다.", message_display_pos, duration=1.5, color=RED, font=font))
                else:
                    active_temporary_messages.append(TemporaryMessageDisplay("씨앗을 선택해주세요!", message_display_pos, duration=1.5, color=ORANGE, font=font))
            else:
                active_temporary_messages.append(TemporaryMessageDisplay("도구를 선택해주세요!", message_display_pos, duration=1.5, color=ORANGE, font=font))
            return

    # 화분 클릭 (밭과 동일한 로직)
    for i, pot in enumerate(pot_states):
        if pot['rect'].collidepoint(pos):
            # 텍스트 메시지 위치를 화면 상단으로 변경
            message_display_pos = (WIDTH // 2, 100)
            if active_tool_on_click == 'watering_can':
                current_time = time.time()
                if current_time - last_watering_can_use_time >= WATERING_CAN_COOLDOWN:
                    if pot['planted_plant_type'] is not None and pot['current_growth_frame'] < PLANT_INFO[pot['planted_plant_type']]["growth_frames"]:
                        # 물 주기 시 성장 프레임 추가, 최대 성장 프레임 넘지 않도록
                        # 물뿌리개 배율 적용
                        growth_amount = player_tools['watering_can']['multiplier']
                        pot['current_growth_frame'] = min(PLANT_INFO[pot['planted_plant_type']]["growth_frames"], pot['current_growth_frame'] + growth_amount)
                        active_temporary_messages.append(TemporaryMessageDisplay(f"물 주기! +{growth_amount} 성장", message_display_pos, duration=1.5, color=BLUE, font=font))
                        last_watering_can_use_time = current_time
                    elif pot['planted_plant_type'] is not None and pot['current_growth_frame'] >= PLANT_INFO[pot['planted_plant_type']]["growth_frames"]:
                        active_temporary_messages.append(TemporaryMessageDisplay("이미 다 자란 작물입니다!", message_display_pos, duration=1.5, color=ORANGE, font=font))
                    else:
                        active_temporary_messages.append(TemporaryMessageDisplay("아무것도 심어져 있지 않습니다.", message_display_pos, duration=1.5, color=GRAY, font=font))
                else:
                    active_temporary_messages.append(TemporaryMessageDisplay("물뿌리개 쿨타임 중!", message_display_pos, duration=1.5, color=RED, font=font))
            elif active_tool_on_click == 'scythe':
                if pot['planted_plant_type'] is not None and pot['current_growth_frame'] >= PLANT_INFO[pot['planted_plant_type']]["growth_frames"]:
                    plant_type = pot['planted_plant_type']
                    crop_info = CROP_PRICES[plant_type]
                    harvested_quantity = 0
                    if crop_info['type'] == 'fixed':
                        harvested_quantity = crop_info['quantity']
                    elif crop_info['type'] == 'random':
                        min_q, max_q = crop_info['quantity_range']
                        harvested_quantity = random.randint(min_q, max_q)

                    # 낫 배율 적용
                    income = int(harvested_quantity * crop_info['price_per_item'] * player_tools['scythe']['multiplier'])
                    player_money += income
                    active_temporary_messages.append(TemporaryMessageDisplay(
                        [("수확! ", GREEN), (f"{crop_info['name']} {harvested_quantity}개", BLACK), (f" +{income:,}골드", YELLOW)],
                        message_display_pos, duration=2.0, font=font, is_multi_colored=True
                    ))
                    pot['planted_plant_type'] = None
                    pot['current_growth_frame'] = 0
                    pot['final_scale_factor'] = 1.0 # 초기화
                    if scythe_harvest_sound: # 효과음 재생
                        scythe_harvest_sound.play()
                elif pot['planted_plant_type'] is not None and pot['current_growth_frame'] < PLANT_INFO[pot['planted_plant_type']]["growth_frames"]:
                     active_temporary_messages.append(TemporaryMessageDisplay("아직 다 자라지 않았습니다!", message_display_pos, duration=1.5, color=RED, font=font))
                else:
                    active_temporary_messages.append(TemporaryMessageDisplay("수확할 작물이 없습니다.", message_display_pos, duration=1.5, color=GRAY, font=font))
            elif active_tool_on_click == 'seed_select':
                if selected_seed_name is not None:
                    if pot['planted_plant_type'] is None:
                        if player_inventory.get(selected_seed_name, 0) > 0:
                            pot['planted_plant_type'] = selected_seed_name
                            pot['current_growth_frame'] = 0
                            pot['final_scale_factor'] = random.uniform(0.7, 1.3) # 씨앗 심을 때 크기 결정
                            player_inventory[selected_seed_name] -= 1
                            active_temporary_messages.append(TemporaryMessageDisplay(f"{PLANT_INFO[selected_seed_name]['seed_name']} 심기!", message_display_pos, duration=1.5, color=GREEN, font=font))
                        else:
                            active_temporary_messages.append(TemporaryMessageDisplay("씨앗이 부족합니다!", message_display_pos, duration=1.5, color=RED, font=font))
                    else:
                        active_temporary_messages.append(TemporaryMessageDisplay("이미 작물이 심어져 있습니다.", message_display_pos, duration=1.5, color=RED, font=font))
                else:
                    active_temporary_messages.append(TemporaryMessageDisplay("씨앗을 선택해주세요!", message_display_pos, duration=1.5, color=ORANGE, font=font))
            else:
                active_temporary_messages.append(TemporaryMessageDisplay("도구를 선택해주세요!", message_display_pos, duration=1.5, color=ORANGE, font=font))
            return
    
    # 위에서 처리된 클릭이 없었다면, 도구 선택을 해제할지 판단
    # 클릭된 위치가 어떤 상호작용 가능한 UI 요소나 밭/화분에도 해당하지 않는 경우
    # (이미 다른 함수에서 처리된 경우는 이 지점까지 오지 않으므로, 이 곳은 '빈 공간' 클릭으로 간주)
    if active_tool_on_click is not None:
        active_tool_on_click = None
        if show_seed_options: # 씨앗 메뉴가 열려 있었다면 닫기
            show_seed_options = False
            is_seed_animating = True
            seed_animation_target_offset = 0.0
            seed_animation_current_offset = 1.0 # 닫는 애니메이션을 위해 1.0에서 시작
            selected_seed_name = None # 선택된 씨앗도 해제


def handle_settings_screen_click(pos):
    """설정 화면 클릭 이벤트를 처리합니다."""
    global game_state, previous_game_state, is_dragging_master_vol, is_dragging_music_vol, is_dragging_sfx_vol

    # 닫기 버튼
    current_close_button_rect = pygame.Rect(settings_panel_rect.right - 40, settings_panel_rect.top + 10, 30, 30)
    if current_close_button_rect.collidepoint(pos):
        game_state = previous_game_state
        return

    # 마스터 볼륨 슬라이더 핸들
    if master_vol_knob_rect.collidepoint(pos):
        is_dragging_master_vol = True
        return
    # 음악 볼륨 슬라이더 핸들
    if music_vol_knob_rect.collidepoint(pos):
        is_dragging_music_vol = True
        return
    # 효과음 볼륨 슬라이더 핸들
    if sfx_vol_knob_rect.collidepoint(pos):
        is_dragging_sfx_vol = True
        return

def handle_shop_screen_click(pos):
    """상점 화면 클릭 이벤트를 처리합니다."""
    global game_state, previous_game_state, selected_shop_item_index, player_money, player_inventory

    # 닫기 버튼
    current_close_button_rect = pygame.Rect(shop_panel_rect.right - 40, shop_panel_rect.top + 10, 30, 30)
    if current_close_button_rect.collidepoint(pos):
        game_state = previous_game_state
        selected_shop_item_index = -1 # 상점 닫을 때 선택 초기화
        return

    # 아이템 목록 클릭
    if shop_item_list_rect.collidepoint(pos):
        for i, item in enumerate(shop_items):
            item_relative_y = i * (SHOP_ITEM_HEIGHT + SHOP_ITEM_PADDING) + SHOP_ITEM_PADDING
            item_y = shop_item_list_rect.top + item_relative_y - shop_scroll_offset

            # 아이템이 현재 보이는 목록 영역 내에 있는지 확인
            if item_y + SHOP_ITEM_HEIGHT > shop_item_list_rect.top and item_y < shop_item_list_rect.bottom:
                item_rect_in_list = pygame.Rect(shop_item_list_rect.left + SHOP_ITEM_PADDING, item_y,
                                                shop_item_list_rect.width - SHOP_ITEM_PADDING * 2, SHOP_ITEM_HEIGHT)
                if item_rect_in_list.collidepoint(pos):
                    selected_shop_item_index = i
                    break
    # 구매 버튼 클릭
    if selected_shop_item_index != -1 and buy_button_rect.collidepoint(pos):
        item_to_buy = shop_items[selected_shop_item_index]
        if player_money >= item_to_buy["price"]:
            player_money -= item_to_buy["price"]
            # 씨앗 구매 로직 (plant_type으로 인벤토리에 추가)
            plant_type_to_buy = item_to_buy["plant_type"]
            player_inventory[plant_type_to_buy] = player_inventory.get(plant_type_to_buy, 0) + 1
            active_temporary_messages.append(TemporaryMessageDisplay(
                [("구매 완료! ", GREEN), (f"{item_to_buy['name']}", BLACK)],
                (buy_button_rect.centerx, buy_button_rect.top - 30), duration=1.5, font=font, is_multi_colored=True # 메시지 위치
            ))
            if purchase_success_sound: # 구매 성공 효과음 재생
                purchase_success_sound.play()
        else:
            active_temporary_messages.append(TemporaryMessageDisplay("돈이 부족합니다!", (buy_button_rect.centerx, buy_button_rect.top - 30), duration=1.5, color=RED, font=font)) # 메시지 위치
            if purchase_fail_sound: # 구매 실패 효과음 재생
                purchase_fail_sound.play()

def handle_tool_shop_screen_click(pos): # 기존 handle_crafting_screen_click에서 이름 변경
    """도구 상점 화면 클릭 이벤트를 처리합니다."""
    global game_state, previous_game_state, selected_tool_category, selected_tool_shop_item_index, player_money, player_tools, tool_shop_scroll_offset

    # 닫기 버튼
    current_close_button_rect = pygame.Rect(tool_shop_panel_rect.right - 40, tool_shop_panel_rect.top + 10, 30, 30)
    if current_close_button_rect.collidepoint(pos):
        game_state = previous_game_state
        selected_tool_shop_item_index = -1 # 상점 닫을 때 선택 초기화
        tool_shop_scroll_offset = 0 # 스크롤 오프셋 초기화
        return

    # 탭 버튼 클릭
    tab_height = 50
    tab_width = 150
    tab_margin = 10
    
    watering_can_tab_rect = pygame.Rect(tool_shop_panel_rect.left + 20, tool_shop_panel_rect.top + 20, tab_width, tab_height)
    scythe_tab_rect = pygame.Rect(watering_can_tab_rect.right + tab_margin, tool_shop_panel_rect.top + 20, tab_width, tab_height)

    if watering_can_tab_rect.collidepoint(pos):
        if selected_tool_category != "watering_can":
            selected_tool_category = "watering_can"
            selected_tool_shop_item_index = -1 # 탭 변경 시 선택 초기화
            tool_shop_scroll_offset = 0 # 스크롤 초기화
        return
    elif scythe_tab_rect.collidepoint(pos):
        if selected_tool_category != "scythe":
            selected_tool_category = "scythe"
            selected_tool_shop_item_index = -1 # 탭 변경 시 선택 초기화
            tool_shop_scroll_offset = 0 # 스크롤 초기화
        return

    # 아이템 목록 클릭 (현재 선택된 카테고리의 아이템으로)
    current_tool_items = tool_shop_items[selected_tool_category]
    if tool_shop_item_list_rect.collidepoint(pos):
        for i, item in enumerate(current_tool_items):
            item_relative_y = i * (SHOP_ITEM_HEIGHT + SHOP_ITEM_PADDING) + SHOP_ITEM_PADDING
            item_y = tool_shop_item_list_rect.top + item_relative_y - tool_shop_scroll_offset

            if item_y + SHOP_ITEM_HEIGHT > tool_shop_item_list_rect.top and item_y < tool_shop_item_list_rect.bottom:
                item_rect_in_list = pygame.Rect(tool_shop_item_list_rect.left + SHOP_ITEM_PADDING, item_y,
                                                tool_shop_item_list_rect.width - SHOP_ITEM_PADDING * 2, SHOP_ITEM_HEIGHT)
                if item_rect_in_list.collidepoint(pos):
                    selected_tool_shop_item_index = i
                    break
    
    # 구매 버튼 클릭 (도구 상점)
    if selected_tool_shop_item_index != -1 and buy_button_rect.collidepoint(pos):
        item_to_buy = current_tool_items[selected_tool_shop_item_index]
        # 실제 구매한 도구 id 목록을 관리
        equipped_id = player_tools[selected_tool_category]['id']
        if 'owned_tool_ids' not in player_tools[selected_tool_category]:
            player_tools[selected_tool_category]['owned_tool_ids'] = []
        owned_tool_ids = player_tools[selected_tool_category]['owned_tool_ids']
        is_equipped = (equipped_id == item_to_buy['id'])
        is_owned = item_to_buy['id'] in owned_tool_ids

        # 이미 소지한 도구는 0원에 구매
        price_to_pay = 0 if is_owned else item_to_buy["price"]
        if player_money >= price_to_pay:
            player_money -= price_to_pay
            # 도구 업데이트 (장착)
            player_tools[selected_tool_category]['id'] = item_to_buy['id']
            player_tools[selected_tool_category]['multiplier'] = item_to_buy['multiplier']
            # 장착한 도구 id를 항상 owned_tool_ids에 추가
            if player_tools[selected_tool_category]['id'] not in owned_tool_ids:
                owned_tool_ids.append(player_tools[selected_tool_category]['id'])
            # 물뿌리개 이미지 업데이트
            if selected_tool_category == "watering_can":
                global watering_can_image
                if item_to_buy['image']:
                    watering_can_image = pygame.transform.scale(item_to_buy['image'], (TOOL_ICON_SIZE, TOOL_ICON_SIZE))
                else:
                    watering_can_image = pygame.image.load(os.path.join("assets", "images", "watering_can.png"))
                    watering_can_image = pygame.transform.scale(watering_can_image, (TOOL_ICON_SIZE, TOOL_ICON_SIZE))
            elif selected_tool_category == "scythe":
                global scythe_image
                if item_to_buy['image']:
                    scythe_image = pygame.transform.scale(item_to_buy['image'], (TOOL_ICON_SIZE, TOOL_ICON_SIZE))
                else:
                    scythe_image = pygame.image.load(os.path.join("assets", "images", "scythe.png"))
                    scythe_image = pygame.transform.scale(scythe_image, (TOOL_ICON_SIZE, TOOL_ICON_SIZE))
            active_temporary_messages.append(TemporaryMessageDisplay(
                [("구매 완료! ", GREEN), (f"{item_to_buy['name']}", BLACK), (f" (장착됨)", BLUE) if is_equipped else ("", BLACK)],
                (buy_button_rect.centerx, buy_button_rect.top - 30), duration=1.5, font=font, is_multi_colored=True
            ))
            if purchase_success_sound:
                purchase_success_sound.play()
        else:
            active_temporary_messages.append(TemporaryMessageDisplay("돈이 부족합니다!", (buy_button_rect.centerx, buy_button_rect.top - 30), duration=1.5, color=RED, font=font))
            if purchase_fail_sound:
                purchase_fail_sound.play()


def update_date():
    """날짜를 업데이트합니다."""
    global current_day, current_month, current_year, last_day_change_time
    global field_states, pot_states
    
    current_time = time.time()
    if current_time - last_day_change_time >= DAY_CHANGE_INTERVAL:
        last_day_change_time = current_time
        
        current_day += 1
        days_in_current_month = get_days_in_month(current_year, current_month)

        if current_day > days_in_current_month:
            current_day = 1
            current_month += 1
            if current_month > 12:
                current_month = 1
                current_year += 1
        
        # 작물 성장 업데이트
        for field in field_states:
            if field['planted_plant_type'] is not None and field['current_growth_frame'] < PLANT_INFO[field['planted_plant_type']]["growth_frames"]:
                growth_rate = 1 # 하루에 1 성장 프레임
                if fast_growth_mode:
                    growth_rate = 5 # 빠른 성장 모드일 때는 5배 빠르게 성장
                
                field['current_growth_frame'] = min(PLANT_INFO[field['planted_plant_type']]["growth_frames"], field['current_growth_frame'] + growth_rate)

        for pot in pot_states:
            if pot['planted_plant_type'] is not None and pot['current_growth_frame'] < PLANT_INFO[pot['planted_plant_type']]["growth_frames"]:
                growth_rate = 1 # 하루에 1 성장 프레임
                if fast_growth_mode:
                    growth_rate = 5 # 빠른 성장 모드일 때는 5배 빠르게 성장
                
                pot['current_growth_frame'] = min(PLANT_INFO[pot['planted_plant_type']]["growth_frames"], pot['current_growth_frame'] + growth_rate)


def get_days_in_month(month, year):
    if month == 2: # 2월
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0): # 윤년
            return 29
        else:
            return 28
    elif month in [4, 6, 9, 11]: # 4, 6, 9, 11월 (30일)
        return 30
    else: # 나머지 월 (31일)
        return 31

# 메인 게임 루프
running = True
play_random_music() # 게임 시작 시 음악 재생

while running:
    dt = clock.tick(60) / 1000.0 # 초 단위
        # 튜토리얼 스킵 진행도 및 UI는 튜토리얼 상태에서만 동작
    skip_progress = 0.0
    if show_tutorial:
        if skip_e_pressed:
            elapsed = time.time() - skip_e_start_time
            skip_progress = min(elapsed / skip_e_duration, 1.0)
            if skip_progress >= 1.0 and not skip_tutorial:
                skip_tutorial = True
                show_tutorial = False  # 튜토리얼 오버레이 종료
                last_day_change_time = time.time()  # 튜토리얼 종료 시 날짜 즉시 증가 방지
                print("튜토리얼 스킵!")

    # 메인 게임 루프 내의 이벤트 처리 부분
    for event in pygame.event.get():
        # 튜토리얼 상태에서만 E 키 꾹 누름 감지
        if show_tutorial:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if not skip_e_pressed:
                    skip_e_pressed = True
                    skip_e_start_time = time.time()
            if event.type == pygame.KEYUP and event.key == pygame.K_e:
                skip_e_pressed = False
                skip_e_start_time = 0
        if event.type == pygame.QUIT:
            save_game()  # 게임 종료 시 자동 저장
            save_settings(settings)  # 볼륨 설정 저장
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                save_game()  # ESC로 종료 시 자동 저장
                save_settings(settings)  # 볼륨 설정 저장
                running = False
            # F3 키를 눌렀을 때 소지금 증가
            elif event.key == pygame.K_F3:
                player_money += 100000000  # 예시: 10만 원 증가. 원하는 금액으로 조절하세요.
                print(f"소지금이 증가했습니다! 현재 소지금: {player_money}원") # 확인용 출력

        if event.type == pygame.QUIT:
            save_game()  # 게임 종료 시 자동 저장
            running = False
        elif event.type == MUSIC_END_EVENT:
            play_random_music() # 음악 끝나면 다음 곡 재생
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # 좌클릭
                if game_state == 'TITLE':
                    if start_button_rect.collidepoint(event.pos):
                        # 처음부터: 게임 상태 초기화(불러오기 X)
                        game_state = 'GAME'
                        show_tutorial = True  # 튜토리얼 오버레이 시작
                    elif continue_button_rect.collidepoint(event.pos):
                        # 이어하기: 저장된 데이터 불러오기
                        load_game()
                        game_state = 'GAME'
                elif game_state == 'GAME':
                    handle_game_screen_click(event.pos)
                elif game_state == 'SETTINGS':
                    handle_settings_screen_click(event.pos)
                elif game_state == 'SHOP':
                    handle_shop_screen_click(event.pos)
                    # 상점 스크롤바 드래그 시작 로직
                    if scrollbar_handle_rect and scrollbar_handle_rect.collidepoint(event.pos):
                        is_dragging_scrollbar = True
                        scrollbar_drag_offset_y = event.pos[1] - scrollbar_handle_rect.y
                elif game_state == 'TOOL_SHOP': # 도구 상점 클릭 처리
                    handle_tool_shop_screen_click(event.pos)
                    # 도구 상점 스크롤바 드래그 시작 로직
                    if scrollbar_handle_rect and scrollbar_handle_rect.collidepoint(event.pos): # tool_shop_screen에도 스크롤바가 있으므로 이를 참조
                        is_dragging_scrollbar = True
                        scrollbar_drag_offset_y = event.pos[1] - scrollbar_handle_rect.y

            elif event.button == 4: # 마우스 휠 위로
                if game_state == 'SHOP':
                    shop_scroll_offset = max(0, shop_scroll_offset - SHOP_SCROLL_SPEED)
                elif game_state == 'TOOL_SHOP': # 도구 상점 스크롤
                    tool_shop_scroll_offset = max(0, tool_shop_scroll_offset - SHOP_SCROLL_SPEED)
            elif event.button == 5: # 마우스 휠 아래로
                if game_state == 'SHOP':
                    total_items_height = len(shop_items) * (SHOP_ITEM_HEIGHT + SHOP_ITEM_PADDING)
                    visible_list_height = shop_item_list_rect.height - (SHOP_ITEM_PADDING * 2)
                    max_scroll_offset = max(0, total_items_height - visible_list_height)
                    shop_scroll_offset = min(max_scroll_offset, shop_scroll_offset + SHOP_SCROLL_SPEED)
                elif game_state == 'TOOL_SHOP': # 도구 상점 스크롤
                    current_tool_items = tool_shop_items[selected_tool_category]
                    total_items_height = len(current_tool_items) * (SHOP_ITEM_HEIGHT + SHOP_ITEM_PADDING)
                    visible_list_height = tool_shop_item_list_rect.height - (SHOP_ITEM_PADDING * 2)
                    max_scroll_offset = max(0, total_items_height - visible_list_height)
                    tool_shop_scroll_offset = min(max_scroll_offset, tool_shop_scroll_offset + SHOP_SCROLL_SPEED)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: # 좌클릭 떼기
                is_dragging_master_vol = False
                is_dragging_music_vol = False
                is_dragging_sfx_vol = False # 효과음 볼륨 드래그 해제
                is_dragging_scrollbar = False

        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            # 설정 화면 볼륨 슬라이더 드래그
            if game_state == 'SETTINGS':
                if is_dragging_master_vol:
                    new_knob_x = max(master_vol_slider_x, min(master_vol_slider_x + SLIDER_WIDTH, mouse_x))
                    master_volume = (new_knob_x - master_vol_slider_x) / SLIDER_WIDTH
                    master_vol_knob_rect.centerx = new_knob_x
                    apply_volume()
                if is_dragging_music_vol:
                    new_knob_x = max(music_vol_slider_x, min(music_vol_slider_x + SLIDER_WIDTH, mouse_x))
                    music_volume = (new_knob_x - music_vol_slider_x) / SLIDER_WIDTH
                    music_vol_knob_rect.centerx = new_knob_x
                    apply_volume()
                if is_dragging_sfx_vol: # 효과음 볼륨 슬라이더 드래그
                    new_knob_x = max(sfx_vol_slider_x, min(sfx_vol_slider_x + SLIDER_WIDTH, mouse_x))
                    sfx_volume = (new_knob_x - sfx_vol_slider_x) / SLIDER_WIDTH
                    sfx_vol_knob_rect.centerx = new_knob_x
                    apply_volume()
            # 호버 효과 업데이트 (게임 화면에서만)
            if game_state == 'GAME':
                found_hover = False
                for i, field in enumerate(field_states):
                    if field['rect'].collidepoint(mouse_x, mouse_y):
                        hovered_plot_type = 'field'
                        hovered_plot_index = i
                        found_hover = True
                        break
                # 화분 호버 (밭 호버가 아니면서)
                if not found_hover:
                    for i, pot in enumerate(pot_states):
                        if pot['rect'].collidepoint(mouse_x, mouse_y):
                            hovered_plot_type = 'pot'
                            hovered_plot_index = i
                            found_hover = True
                            break
                if not found_hover:
                    hovered_plot_type = None
                    hovered_plot_index = -1
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                fast_growth_mode = not fast_growth_mode
                print(f"빠른 성장 모드: {fast_growth_mode}")

    # 애니메이션 업데이트 (씨앗 선택 메뉴)
    if is_seed_animating:
        if seed_animation_target_offset > seed_animation_current_offset: # 열리는 애니메이션
            seed_animation_current_offset += seed_animation_speed * dt
            if seed_animation_current_offset >= seed_animation_target_offset:
                seed_animation_current_offset = seed_animation_target_offset
                is_seed_animating = False
        elif seed_animation_target_offset < seed_animation_current_offset: # 닫히는 애니메이션
            seed_animation_current_offset -= seed_animation_speed * dt
            if seed_animation_current_offset <= seed_animation_target_offset:
                seed_animation_current_offset = seed_animation_target_offset
                is_seed_animating = False

    # 임시 메시지 업데이트
    for msg in list(active_temporary_messages): # 순회 중 리스트 변경 방지를 위해 list()로 복사
        msg.update()
        if msg.done:
            active_temporary_messages.remove(msg)

    # 날짜/시간 업데이트 (튜토리얼 중에는 모두 멈춤)
    if game_state == 'GAME' and not show_tutorial:
        update_date()
    elif show_tutorial:
        last_day_change_time = time.time()  # 튜토리얼 중에는 시간 기준값도 고정

    # 화면 그리기
    screen.fill(BLACK) # 기본 배경

    if game_state == 'TITLE':
        draw_title_screen()
    elif game_state == 'GAME':
        draw_game_screen()
    elif game_state == 'SETTINGS':
        draw_game_screen() # 게임 화면 위에 설정 화면이 오버레이되도록
        draw_settings_screen()
    elif game_state == 'SHOP':
        draw_game_screen() # 게임 화면 위에 상점 화면이 오버레이되도록
        draw_shop_screen()
    elif game_state == 'TOOL_SHOP': # 도구 상점 그리기
        draw_game_screen() # 게임 화면 위에 도구 상점 화면이 오버레이되도록
        draw_tool_shop_screen()

    # 모든 임시 메시지 그리기
    for msg in active_temporary_messages:
        msg.draw(screen)

    # 튜토리얼 상태일 때만 원 표시
    if show_tutorial:
        draw_skip_circle(screen, skip_progress)
    pygame.display.flip()

pygame.quit()
sys.exit()