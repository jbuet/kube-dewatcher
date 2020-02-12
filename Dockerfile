FROM python:3.7.6-stretch

RUN pip install --upgrade pip && adduser  worker

USER worker

WORKDIR /app

ENV PATH="/home/worker/.local/bin:${PATH}"

COPY --chown=worker:worker requirements.txt requirements.txt

RUN pip install --upgrade pip --user && pip install --user -r requirements.txt

COPY --chown=worker:worker . /app

CMD [ "python", "./app.py" ]