# General Approach: 
# Create WorkDir app
# Put ./src, ./.streamlit, ./requirements.txt, ./.env, ./main.py in 
# expose port 80 
# define entry point 
# run command

FROM python:3.10-slim 
WORKDIR /app 
COPY ./src/ /app/src
COPY ./.streamlit/ /app/.streamlit  
COPY ./.env /app   
COPY ./requirements.txt /app   
COPY ./main.py /app   

RUN pip install -r requirements.txt
EXPOSE 80  
ENTRYPOINT ["streamlit","run"]
CMD ["main.py"]