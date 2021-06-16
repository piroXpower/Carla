FROM pypy:3

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "pypy3", "-?m", "Evelyn" ] 
