#!/bin/bash

set -e

/opt/kafka/bin/kafka-storage.sh format -t $CLUSTER_ID -c /opt/kafka/config/kraft/server.properties --ignore-formatted
/opt/kafka/bin/kafka-server-start.sh /opt/kafka/config/kraft/server.properties &

sleep 5

/init-users.sh

wait