# O-LANGE Backend (한국어 -> 한국 수어 변환 백엔드)

이 프로젝트는 한국어를 한국 수어로 변환하는 서비스의 백엔드 부분입니다. 이 백엔드 서버는 형태소 분리와 한국 수어 조회를 담당합니다.

## 폴더 구조
```
korean-sign-language-translater_BE_public-main/
├── .gitignore
├── Dockerfile
├── LICENSE
├── deptree
├── main.py
├── requirements.txt
└── parser/
    ├── parser.py
    └── sep.py
```

- `.gitignore`: Git에서 추적하지 않을 파일 및 디렉토리를 지정합니다.
- `Dockerfile`: Docker 이미지를 빌드하는 데 사용되는 설정 파일입니다.
- `LICENSE`: 프로젝트의 라이선스 정보가 포함되어 있습니다.
- `deptree`: 프로젝트의 의존성 트리 정보가 포함되어 있습니다.
- `main.py`: 백엔드 서버의 메인 파일입니다.
- `requirements.txt`: 프로젝트에 필요한 Python 패키지 목록입니다.
- `parser/`: 형태소 분석 및 분리를 담당하는 파서 모듈이 포함되어 있습니다.
  - `parser.py`
  - `sep.py`

## 설치 및 실행 방법

### 1. 저장소 클론
```bash
git clone https://github.com/your-repo/korean-sign-language-translater_BE_public-main.git
cd korean-sign-language-translater_BE_public-main
```

### 2. 가상 환경 설정 (선택 사항)
```bash
python -m venv venv
source venv/bin/activate  # Windows의 경우 `venv\Scripts\activate`
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 서버 실행
```bash
python main.py
```

## Docker를 이용한 실행
```bash
docker build -t korean-sign-language-translater .
docker run -p 8000:8000 korean-sign-language-translater
```

## 기여 방법
기여는 항상 환영합니다! 문제를 발견하거나 개선 사항이 있으면 이슈를 남겨주세요. 기여 절차는 다음과 같습니다:

1. 이 저장소를 포크합니다.
2. 새로운 브랜치를 생성합니다. (`git checkout -b feature/amazing-feature`)
3. 변경 사항을 커밋합니다. (`git commit -m 'Add some amazing feature'`)
4. 브랜치에 푸시합니다. (`git push origin feature/amazing-feature`)
5. 풀 리퀘스트를 생성합니다.
