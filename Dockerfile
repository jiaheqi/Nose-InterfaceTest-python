FROM mirror.youle.game/python:3.7 as builder

ENV TZ=Asia/Shanghai
ADD ./ /app/
WORKDIR /app
RUN pip install -r /app/requirements.txt --trusted-host nexus.youle.game -i http://nexus.youle.game/repository/pypi-public/simple

ENV HOST=https://zeus.topjoy.com
ENV APP_ID=7AVS2D5QH2TV
ENV SECRET_KEY=DF864TCE1XWZE1NH
ENV USER_ID=10001

RUN python main.py || echo "Finished."

FROM nginx:alpine
COPY --from=builder /app/report/heat-report.html /usr/share/nginx/html/index.html