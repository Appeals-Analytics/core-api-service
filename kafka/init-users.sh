#!/bin/bash

set -e

BOOTSTRAP="localhost:9092"

echo "Ожидание доступности Kafka API..."

for i in {1..30}; do
  if /opt/kafka/bin/kafka-broker-api-versions.sh --bootstrap-server "$BOOTSTRAP" >/dev/null 2>&1; then
    echo "Kafka готова."
    break
  fi
  echo "Kafka ещё не готова... ($i/30)"
  sleep 5
done

echo "Начинаем создание/обновление пользователей SCRAM..."

/opt/kafka/bin/kafka-configs.sh --bootstrap-server "$BOOTSTRAP" \
  --alter \
  --add-config "SCRAM-SHA-256=[password=$KAFKA_ADMIN_PASSWORD]" \
  --entity-type users \
  --entity-name "$KAFKA_ADMIN_USER"

/opt/kafka/bin/kafka-configs.sh --bootstrap-server "$BOOTSTRAP" \
  --alter \
  --add-config "SCRAM-SHA-256=[password=$KAFKA_APP_PASSWORD]" \
  --entity-type users \
  --entity-name "$KAFKA_APP_USER"

echo "Пользователи SCRAM успешно настроены."