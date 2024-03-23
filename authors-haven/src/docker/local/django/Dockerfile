ARG PYTHON_VERSION=3.11.2-bullseye

FROM python:${PYTHON_VERSION} as python

# multistage build

# 1st stage build python dep wheel
# 라이브러리를 패키징 하고 배포하기 위한 바이너리 형식의 파일
# 기존 소스 배포에 비해 더 효율적이고 빠르게 설치할 수 있도록 설계됨.
FROM python as python-build-stage
ARG BUILD_ENVIRONMENT=local

# RUN Docker의 빌드 프로세스 중 쉘 명령을 실행하는 데 사용
# 패키지를 설치하거나, 시스템을 구성하거나, 환경을 설정하거나 기타 작업을 수행할 수 있음
# -y 플래그는 자동으로 yes 응답 ( 사용자의 개입 없이)
# build essential 은 필수 빌드 도구가 설치되도록 하는 메타 패키지
# libpq-dev 일반적으로 Postgres 데이터베이스 시스템용
# -- psycopg2 등이 포함된
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev


# COPY source dest
# 기본적으로 호스트 컴퓨터에서 컨테이너로 파일을 복사함
COPY ./requirements .

# --wheel-dir 은 휠이 있는 디렉토리를 지정
# ARG BUILD_ENVIRONMENT=local 를 선언했기에 local.txt 를 사용한다
RUN pip wheel --wheel-dir /usr/src/app/wheels \
  -r ${BUILD_ENVIRONMENT}.txt


# 2nd stage run python
FROM python as python-run-stage
ARG BUILD_ENVIRONMENT=local

# working dir
ARG APP_HOME=/app

# 모듈을 가져올 때 바이트 코드 파일 작성을 건너 뛰도록
# 파이썬이 모듈을 임포트할 떄, 보통 소스 코드를 바이트 코드로 컴파일 후 저장하기에
ENV PYTHONDONTWRITEBYTECODE 1

# 파이썬 출력이 버퍼링되지 않고 터미널로 직접 전송됨을 의미
# 이를 통해 응용프로그램의 출력을 실시간을 표시할 수 있음
ENV PYTHONUNBUFFERED 1

ENV BUILD_ENV ${BUILD_ENVIRONMENT}

# cmd 엔트리포인트(진입점) 에 대한 기본적인 작업 경로를 설정한다
WORKDIR ${APP_HOME}

# gettext 국제화 및 지역화를 위한 도구 셋 프로그램 메세지 및 UI요소를 번역할 떄 자주 사용됨
# 후에 사용하지 않는 파일을 정리함
RUN apt-get update && apt-get install --no-install-recommends -y \
  libpq-dev \
  gettext \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# wheel 복사
COPY --from=python-build-stage /usr/src/app/wheels /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/

# 이 실행 명령의 목적은 슬래시 진입점 파일에 고유한 스타일 라인이 있는지 확인하는 것입니다
# Windows 스타일 
# Docker 는 일반적으로 리눅스 배포판과 같은 유닉스 기반 시스템이기에
# winodws 스타일 endline ? 을 사용하면 스크립트를 실행하거나 읽을 떄 문제가 발생할 수 있음.

# 표현식의 부분은 대체할 패턴과 그 패턴을 정의함
COPY ./docker/local/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

# 모든 모델이 마이그레이션 되고 Django 서버가 실행되면 static file이 수집됨
COPY ./docker/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./docker/local/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./docker/local/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower


COPY . ${APP_HOME}

# 컨테이너가 시작될 때 실행할 기본 명령을 정의한다.
ENTRYPOINT [ "/entrypoint" ]