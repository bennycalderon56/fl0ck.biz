FROM python:3.9

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

# install python dependencies
RUN pip cache purge
RUN pip uninstall pandas
RUN python3 -m pip install --upgrade pip
##RUN pip3 list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip3 install -U 
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
#RUN pip install --upgrade matplotlib
#RUN pip freeze > to_update.txt THIS IS TO INCLUDE LIBRARIES FOR PYTORCH AND BACKTESTING
#RUN pip install -r requirements.txt --upgrade

# COPY . app
# COPY run_server.sh ./
# RUN chmod +x run_server.sh
# EXPOSE 8000
# ENTRYPOINT ["./run_server.sh"]


COPY env.sample .env

COPY . .

#running migrations
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py generate-api

#make it do runserver manually if gunicorn dont work
# gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]

