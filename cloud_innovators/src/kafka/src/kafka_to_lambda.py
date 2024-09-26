import requests
from kafka import KafkaConsumer
import json

# Kafka Consumer 설정
consumer = KafkaConsumer(
    'merged_topic',  # Kafka 토픽 이름
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group'
)

# API Gateway URL (AWS API Gateway에서 생성된 엔드포인트)
api_gateway_url = "https://398eh901b7.execute-api.us-east-1.amazonaws.com/first_test"

# Kafka에서 메시지를 수신하고, 이를 API Gateway로 전송하는 로직
for message in consumer:
    # Kafka 메시지 수신
    kafka_message = message.value.decode('utf-8')
    print(f"Received Kafka Message: {kafka_message}")

    # API Gateway로 POST 요청 전송
    headers = {'Content-Type': 'application/json'}
    response = requests.post(api_gateway_url, json={'kafka_message': kafka_message}, headers=headers)

    # 결과 출력
    print(f"API Gateway Response: {response.status_code}, {response.text}")
