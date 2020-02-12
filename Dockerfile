FROM python:3.7.2-alpine

RUN pip install --upgrade pip && adduser -D worker

USER worker

WORKDIR /app

ENV PATH="/home/worker/.local/bin:${PATH}"

COPY --chown=worker:worker requirements.txt requirements.txt

RUN pip install --user -r requirements.txt

COPY --chown=worker:worker . /app

CMD [ "python", "./app.py" ]