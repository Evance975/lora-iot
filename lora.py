import time
import socket
import subprocess
import paho.mqtt.client as mqtt


# MQTT SETTINGS

MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_TOPIC = "IP Address request"


# getting local IP addresses

def get_ip_address():
    try:
        # Using socket to get the local IP address

        skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Connect to Google's DNS server to get local IP address
        skt.connect(("8.8.8.8", 80))
        ip_address = skt.getsockname()[0]
        skt.close()
        return ip_address
    except Exception as e:
        print(f"Error obtaining IP address: {e}")
        return None


# Function connecting to the MQTT broker
def connect_to_mqtt():
    client = mqtt.Client()

    while True:
        try:
            print("Connecting to MQTT broker...")
            client.connect(MQTT_BROKER, MQTT_PORT, 60)
            print("Successfully connected to MQTT broker.")
            return client
        except Exception as e:
            print(f"Connection to broker failed. Retrying again in 5 seconds... ({e})")
            time.sleep(5)


# Function to publish the IP address to the specified topic
def publish_ip_address(client, ip_address):
    try:
        print(f"Publishing IP address ({ip_address}) to topic: {MQTT_TOPIC}")
        client.publish(MQTT_TOPIC, ip_address)
    except Exception as e:
        print(f"Error publishing IP address: {e}")


def main():
    mqtt_client = connect_to_mqtt()

    while True:
        try:
            # Reading the local IP address

            ip_address = get_ip_address()

            if ip_address:
                # Publish the IP address to the MQTT topic
                publish_ip_address(mqtt_client, ip_address)

            # Wait for some time before checking again
            time.sleep(60)
        except KeyboardInterrupt:
            print("Exiting...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
