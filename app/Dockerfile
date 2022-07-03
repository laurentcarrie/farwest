FROM python:3.8

RUN pip install streamlit
COPY src src
RUN pip install -e src

ENTRYPOINT ["streamlit", "run","src/farwest/app.py","--server.enableCORS=false","server.enableXsrfProtection=false"]
