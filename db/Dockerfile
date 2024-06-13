FROM mongo:latest

WORKDIR /data

COPY dump /data/dump

CMD mongod --fork --logpath /var/log/mongodb.log && \
  mongorestore --drop --db sampleDB /data/dump/sampleDB && \
  mongod --shutdown && \
  mongod --bind_ip_all
