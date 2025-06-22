 #🍕 Pizza Restaurant API Challenge

This is a RESTful API for a Pizza Restaurant built using **Flask**, **SQLAlchemy**, and **PostgresSQL**. The API manages restaurants, pizzas, and the many-to-many relationship between them using a join table (`RestaurantPizza`). This project follows the **MVC pattern**.

---

## 📁 Project Structure
├── server/
│ ├── init.py
  | ---database.py
│ ├── app.py
│ ├── config.py
│ ├── models/
│ │ ├── init.py
│ │ ├── restaurant.py
│ │ ├── pizza.py
│ │ └── restaurant_pizza.py
│ ├── controllers/
│ │ ├── init.py
│ │ ├── restaurant_controller.py
│ │ ├── pizza_controller.py
│ │ └── restaurant_pizza_controller.py
│ ├── seed.py
├
├── challenge-1-pizzas.postman_collection.json
└── README.md




## ⚙️ Setup Instructions

### 1. Clone the repository


git clone https://github.com/yourusername/pizza-api-challenge.git
cd pizza-api-challenge

### 2. Create virtual environment and install dependencies
pipenv install flask flask_sqlalchemy flask_migrate psycopg2-binary
pipenv shell


3. Configure PostgresSQL
Update server/config.py to match your PostgresSQL credentials:
SQLALCHEMY_DATABASE_URI = "postgresql://username:password@localhost:5432/pizza_api"


4. Initialize the database
export FLASK_APP=server/app.py

flask db init
flask db migrate -m "Initial migration"
flask db upgrade


5. Seed the database
Add initial data in server/seed.py and run:
python server/seed.py


🧩 Models
#Restaurant
id: integer, primary key

name: string

address: string

Relationships:

has many RestaurantPizzas

#Pizza
id: integer, primary key

name: string

ingredients: string

Relationships:

has many RestaurantPizzas

#RestaurantPizza (Join Table)
id: integer, primary key

price: integer (validation: must be between 1 and 30)

restaurant_id: FK

pizza_id: FK

Relationships:

belongs to Restaurant

belongs to Pizza

✅ Cascading delete: When a Restaurant is deleted, its associated RestaurantPizzas are also deleted.

🔁 API Endpoints
📍 GET /restaurants
Returns: List of all restaurants


📍 GET /restaurants/int:id
Returns: Details of a restaurant and its pizzas

📍 DELETE /restaurants/int:id
Deletes: A restaurant and its RestaurantPizzas

Success: 204 No Content

Not Found:


📍 GET /pizzas
Returns: List of all pizzas

📍 POST /restaurant_pizzas
Creates: A new RestaurantPizza entry

✅ Validation Rules
Field	Rule
price	Must be between 1 and 30
pizza_id	Must reference a valid Pizza
restaurant_id	Must reference a valid Restaurant



🧪 Postman Collection
Steps:
Open Postman

Click Import

Upload challenge-1-pizzas.postman_collection.json

Test each route (GET, POST, DELETE)


🙌 Credits
Built with Flask, SQLAlchemy, and PostgresSQL. Structured using the MVC architecture.



📝 License
This project is open-source and available under the MIT License.






