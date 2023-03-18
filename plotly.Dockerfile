FROM jupyter/minimal-notebook:latest

ENV PATH "$PATH:/home/jovyan/.local/bin"

WORKDIR /work
RUN pip install plotly pandas numpy scipy --user

EXPOSE 8888
