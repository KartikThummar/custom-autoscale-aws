FROM public.ecr.aws/lambda/python:3.8
COPY requirements.txt .
RUN  pip3 install -r requirements.txt
COPY . .
CMD [ "exam_shedule.multi_sevice_shedule_rule" ]
