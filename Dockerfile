# Alpine 기반 이미지 사용
FROM alpine:latest

# 타임존 설정
RUN apk add --no-cache tzdata
ENV TZ=Asia/Seoul

# nginx, python3, pip 및 필요 패키지 설치
RUN apk add --no-cache nginx python3 py3-pip py3-mysqlclient \
    gcc musl-dev mariadb-connector-c-dev pkgconfig python3-dev

# 가상 환경 생성 및 활성화
RUN python3 -m venv /var/www/sisu2/venv
ENV PATH="/var/www/sisu2/venv/bin:$PATH"

# nginx.conf 설정 변경
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# default.conf 파일 복사
ADD default.conf /etc/nginx/http.d/default.conf

# 애플리케이션 소스 코드 복사
ADD ./ /var/www/sisu2
WORKDIR /var/www/sisu2

# 가상 환경에서 Python 모듈 설치
RUN . /var/www/sisu2/venv/bin/activate && pip install -r requirements.txt

# 엔트리포인트 스크립트에 실행 권한 추가
RUN chmod +x entrypoint.sh

# 포트 노출
EXPOSE 80
EXPOSE 443

# 엔트리포인트 설정
ENTRYPOINT ["./entrypoint.sh"]
