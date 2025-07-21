# ericapython
2025년 여름방학 한양대학교 파이썬게임 개발
- 주제: 키우기 게임(거지게임)
- 팀명: 5KEY
- 팀원: 1710_류정훈, 1722_최지호, 1721_최연우, 2806_권민서, 2808_김도윤
- http://hue-youthsw.com/26 , osgc2025
- sellbuymusic 
- https://giventofly.github.io/pixelit/#tryit
- 레알팜

## 2025.07.21(월)
[질의응답 게시판 바로가기](http://www.hue-youthsw.com/22) , 패스워드: osgc2025 <br>
[BGM(배경음악) 사이ㅡ 셀바이뮤직](https://www.sellbuymusic.com) <br>
[도트이미지로 변환](https://giventofly.github.io/pixelit/#tryit)

[프로젝트 환경 구성]
1. Python 환경 및 의존성 설정 
  - 설치 프로그램 : 최신버전 파이썬 Python3.13, Git Bash, Visual Studio Code
  - 설치 경로 : D:\python3.13, ( 그외 프로그램은 D:\ 에 설치함 )

2. 구글 계정으로 github에 가입 후 github에 'ericapython' repo(저장소) 생성 > 깃 허브 주소 "복사"

3. Git 초기화 및 기본 폴더 구조 설정
  - 탐색기 실행 : D:\ > 우클릭 > Open Git Bash Here > git clone "붙여넣기" > 인증받기
  - D:\저장소이름과 같은 폴더가 자동 생성됨

4. VSCode 에서 가상환경 구성 및 pygame 모듈 설치 후 테스트코드로 실행해보기
  - 탐색기 실행 > 주소줄 클릭 > "cmd" 입력 후 엔터 > "code . " 입력 > Visual Studio Code 실행됨.
  - 'python' 확장 팩 설치 하기
  - git bash 터미널 열기 : <Ctrl> + `(빽틱)
  - python -m venv venv
  - source venv/Scripts/activate
  - 활성화 되면 (venv) 표시가 나타납니다.
  - 가상환경이 활성화 된 상태에서 아래 명령어로 pygame 모듈 설치
  - pip install pygame
  - 설치가 완료되면 아래 명령어로 pygame이 정상 설치되었는지 확인할 수 있어요.
  - python -m pygame.examples.aliens

5. 나중에 팀원이 같은 환경을 만들 때 필요한 requirements.txt 파일을 만들 수 있습니다.
  - pip reeeze > requirements.txt

6. 팀원이 아래 명령어로 동일한 패키지 패키지를 설치할 수 있습니다.
  - pip install -r requirements.txt

## 2025.07.22(화)

1. 목표
  - 작물별 성장 로직 구조화(클래스 사용)
  - assets, src, tests, docs 폴더 정리
  - VSCode에서 GitHub 연동
  - README.md, .gitignore, requirements.txt 포함

2. 효율적인 프로젝트 폴더 구조
```
ericapython/
├── assets/                # 이미지, 사운드 등 리소스
│   ├── images/
│   │   ├── potato.png
│   │   ├── sunflower.png
│   │   ├── pea.png
│   │   ├── lettuce.png
│   │   └── apple_tree.png
│   └── fonts/
├── src/                   # 메인 게임 코드
│   ├── __init__.py
│   ├── main.py
│   ├── game.py            # 전체 게임 흐름 제어
│   ├── plant.py           # 작물 클래스 정의
│   └── settings.py        # 전역 설정
├── tests/                 # 테스트 코드 (옵션)
│   └── test_growth.py
├── docs/                  # 설명 자료나 PPT (수업용)
├── requirements.txt       # 설치 패키지
├── .gitignore             # Git에 올리지 않을 파일
├── README.md              # 프로젝트 설명
└── venv/                  # 가상환경 (Git에는 제외)
```

3. 각 파일 역할 요약
  파일/폴더              설명
  plant.py              감자, 해바라기, 상추, 완두콩, 사과나무 등 작물 클래스 정의(OOP)
  game.py               게임 흐름 관리: 시작, 클릭 처리, 성장, 판매
  main.py               진입점, game.run() 호출
  assets/               작물 이미지 등 리소스 저장
  settings.py           화면 크기, 색상, 폰트 설정 등 전역 변수 관리

4. 작물 클래스 예시(src/plant.py)
```
lass Plant:
    def __init__(self, name, image_path, growth_rate):
        self.name = name
        self.image_path = image_path
        self.growth_rate = growth_rate
        self.growth = 0

    def grow(self):
        self.growth += self.growth_rate

    def get_status(self):
        if self.growth < 10:
            return "새싹"
        elif self.growth < 20:
            return "성장 중"
        else:
            return "완전히 자람"
```
5. .gitignore 예시
```
venv/
__pycache__/
*.pyc
.DS_Store
```

6. requirements.txt 예시
```
mkdir assets src tests
cd assets
mkdir fonts images sounds
cd ..
secho "__pycache__/"
python -m venv venv
source venv/Scripts/activate
pip install pygame
python -m pygame.examples.aliens
pip freeze > requirements.txt
```

7. VSCode에서 GitHub 연동
- VSCode에서 폴더 열기(eriapython)
- git bash 터미널에서 Git 초기화:
```
git init
git remote add origin https://github.com/lilyjeongwon/ericapython.git
```
  - 첫 커밋 및 푸시
```
git add .
git commit -m " 프로젝트 초기 설저어 및 작물 클래스 생성"
git brtanch -M main
git push -u origin main
```

8. README.md
```
# 🌱 Erica's 작물 키우기 게임

5가지 작물을 키우는 파이썬 pygame 게임입니다.

## 작물 종류
- 감자
- 해바라기
- 완두콩
- 상추
- 사과나무

## 실행 방법
```bash
pip install -r requirements.txt
python src/main.py
```
9. 질의응답 게시판 바로가기
```
---

## ✨ 다음 작업 추천

- 작물별 이미지 구분
- 클릭마다 성장 → 이미지 상태 변경
- 성장단계에 따라 텍스트 변화

---

```

