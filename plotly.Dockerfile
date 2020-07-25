FROM jupyter/minimal-notebook:latest

ENV PATH "$PATH:/home/jovyan/.local/bin"

WORKDIR /work
RUN pip install plotly numpy scipy --user

EXPOSE 8888


