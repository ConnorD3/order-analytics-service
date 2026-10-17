# CST8915-MidtermProject

## Demo Video

🎥 [Watch Demo Video]()

| Member | Role / Responsibility |
| :--- | :--- |
| Andy | Building Order Analytics Service, Overview of order analytics service, demoing order analytics service |
| Eric | A live demo of the application running locally — place orders, then show analytics endpoints |
| Connor | A live demo of the application running on Azure — show all deployed services, place orders, and verify analytics |

## Responsibility  
1. Build the Order Analytics Service
2. A brief overview of your order-analytics-service (language choice, architecture decisions)  
3. The RabbitMQ consumer pattern you chose and why
4. A live demo of the application running locally — place orders, then show analytics endpoints
5. A live demo of the application running on Azure — show all deployed services, place orders, and verify analytics
6. Creating and walkthrough of your architecture diagram

## Source Code
[Python File](./app.py)

[Requirements File](./requirements.txt)

## Configuration (.env file)
```
RABBITMQ_HOST= <IP>
RABBITMQ_PORT= <PORT>
RABBITMQ_USER= <USERNAME>
RABBITMQ_PASS= <PASSWORD>
```

## Running Application
```bash
pip install -r requirements.txt

python app.py
```