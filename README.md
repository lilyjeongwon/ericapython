# ericapython
2025년 여름방학 한양대학교 파이썬게임 개발

## 2025.07.21(월)
[질의응답 게시판 바로가기](http://www.hue-youthsw.com/22)  <br> 패스워드: osgc2025 <br>
[BGM(배경음악) 사이ㅡ 셀바이뮤직](https://www.sellbymusic.com) <br>
[도트이미지로 변환]()

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

##
4. 프로젝트 문서 작성
  - 프로젝트 개요 및 가이드 문서 작성
