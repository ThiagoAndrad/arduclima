#!/usr/bin/python 
# -*- coding: utf-8 -*-
import argparse
import serial, redis, time
from elasticsearch import Elasticsearch


def return_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--es_host',help="es_host localhost redis_host localhost")
    parser.add_argument('--redis_host',help="es_host localhost redis_host localhost")
    args = parser.parse_args()
    return args




def get_redis_client():
    args = return_args()
    redis_client = redis.Redis(host=args.redis_host, port=6379, db=0)
    return redis_client

def get_elasticsearch_client():
    args = return_args()
    es_client = Elasticsearch([{'host': args.es_host, 'port': 9200}])
    return es_client


def send_signal_to_arduino():
    serial_port = serial.Serial('/dev/ttyACM0',9600,8,'N')
    time.sleep(10)
    serial_port.write("1")
    return serial_port.readline()

def main():
    # necessario esperar um tempo para acessar o arduino.
    args = return_args()
    if(args.redis_host == None or args.es_host == None):
        print("Você precisa passar o host do es e do redis")
        return False
    string_values = send_signal_to_arduino()
    string_values = string_values.replace("\n", "")
    body = create_object(string_values)
    print(body)
    try:
        send_to_elasticsearch(body)
        get_all_objects()
    except:
        try:
            send_to_redis(body)
        except:
            print("redis nao esta no ar")

def create_object(string):
    # aqui cria o objeto para mandar ao es.
    obj = {}
    obj["luminosity"],obj["soil_moisture"],obj["temperature"],obj["humidity"],obj["latitude"],obj["longitude"],obj["altitude"],obj["pressure"] = string.split(",")
    obj["ts"] = time.time()
    return obj


def send_to_elasticsearch(body):
    # aqui pode especifica o host depois.
    es_client = get_elasticsearch_client()
    es_client.index(index="temp", doc_type='temperatura', body=body)

def send_to_redis(body):
    #aqui seta os dados atuais no redis.
    redis_client = get_redis_client()
    redis_client.set("temperature_"+str(int(round(time.time() * 1000))), body)
   

def get_all_objects():
    # aqui pega todas as chaves do redis e manda para o es, em seguida deleta elas de lá.
    redis_client = get_redis_client()
    for key in redis_client.scan_iter("temperature_*"):
        body = redis_client.get(key)
        send_to_elasticsearch(body)
        redis_client.delete(key)
        
if __name__ == "__main__":
    main()
