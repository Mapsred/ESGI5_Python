FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /project
WORKDIR /project

ADD requirements.txt /project/
#RUN pip install -r requirements.txt
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
