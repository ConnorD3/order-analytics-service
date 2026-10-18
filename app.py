import pika
from flask import Flask
import threading
import json
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# product class
class Product:   
    def __init__(self, id, productName, orderCount, totalRevenue):
        self.id = id
        self.productName = productName
        self.orderCount = orderCount
        self.totalRevenue = totalRevenue

# orders class
class Orders:   
    def __init__(self, totalOrders, totalRevenue, averageOrderValue):
        self.totalOrders = totalOrders
        self.totalRevenue = totalRevenue
        self.averageOrderValue = averageOrderValue
        self.totalProducts = []
        self.allProducts = []

# global order object
orders = Orders(0, 0, 0)

# health endpoint
@app.route("/health", methods=["GET"])
def health():
    return {"status": "healthy"}, 200

# get all orders endpoint
@app.route("/orders", methods=["GET"])
def instanceOfOrders():
    products_data = [
        {
            "productName": product.productName,
            "orderCount": product.orderCount,
            "totalRevenue": product.totalRevenue,
        }
        for product in orders.allProducts
    ]
    return json.dumps(products_data)

# summary endpoint
@app.route("/analytics/summary", methods=["GET"])
def summary():

    summary_data = {
        "totalOrders": orders.totalOrders,
        "totalRevenue": orders.totalRevenue,
        "averageOrderValue": orders.averageOrderValue
    }

    return json.dumps(summary_data)

# products endpoint
@app.route("/analytics/products", methods=["GET"])
def products():
    products_data = [
        {
            "productName": product.productName,
            "orderCount": product.orderCount,
            "totalRevenue": product.totalRevenue,
        }
        for product in orders.totalProducts
    ]
    return json.dumps(products_data)

# top products endpoint
@app.route("/analytics/top-products", methods=["GET"])
def topProducts():

    top_products = sorted(orders.totalProducts, key=lambda x: x.orderCount, reverse=True)[:3]

    products_data = [
        {
            "productName": product.productName,
            "totalQuantity": product.orderCount,
        }
        for product in top_products
    ]
    return json.dumps(products_data)

# callback function for RabbitMQ consumer
def callback(ch, method, properties, body):

    order_data = json.loads(body.decode('utf-8'))

    # product details
    id = order_data['product']['id']
    productName = order_data['product']['name']
    orderCount = order_data['quantity']
    totalRevenue = order_data['totalPrice']

    # print(f"Received order: {body}")

    product = Product(id, productName, orderCount, totalRevenue)

    # updating orders with new product information
    orders.totalOrders += product.orderCount
    orders.totalRevenue += product.totalRevenue
    orders.averageOrderValue = orders.totalRevenue / orders.totalOrders
    orders.allProducts.append(product)

    # updating if product exist
    if product.id in [p.id for p in orders.totalProducts]:
        existing_product = next(p for p in orders.totalProducts if p.id == product.id)
        existing_product.orderCount += product.orderCount
        existing_product.totalRevenue += product.totalRevenue
        existing_product.averageOrderValue = existing_product.totalRevenue / existing_product.orderCount
    else:
        orders.totalProducts.append(product)

    ch.basic_ack(delivery_tag=method.delivery_tag)

# function to run the RabbitMQ consumer
def run_consumer():
    # credentials
    host = os.getenv('RABBITMQ_HOST')
    port = int(os.getenv('RABBITMQ_PORT'))
    user = os.getenv('RABBITMQ_USER')
    password = os.getenv('RABBITMQ_PASS')

    # establishing connection to RabbitMQ
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host,
                port=port,
                credentials=pika.PlainCredentials(user, password)
            )
        )
        channel = connection.channel()

        # declaring the queue
        channel.queue_declare(queue='order_queue', durable=True)

        channel.basic_consume(
            queue='order_queue',
            on_message_callback=callback,
            auto_ack=False
        )
        
        channel.start_consuming()
        
    except Exception as e:
        print(f"Consumer crashed with error: {e}")

# start RabbitMQ thread
t1 = threading.Thread(target=run_consumer, daemon=True)
t1.start()

# start Flask app
if __name__ == '__main__':  

    app.run()
    
