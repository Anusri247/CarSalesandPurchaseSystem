use carsalespurchasedb;

CREATE TABLE car_inventory (
    car_id INT AUTO_INCREMENT PRIMARY KEY,
    brand VARCHAR(50),
    model VARCHAR(50),
    year INT,
    color VARCHAR(30),
    price DECIMAL(10, 2)
);

CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(15),
    email VARCHAR(100) DEFAULT NULL,
    car_id INT,  -- This column stores the ID of the purchased car
    transaction_type VARCHAR(15)  -- This column stores 'purchase' or 'sale'
);
ALTER TABLE customers
ADD COLUMN car_id INT,
ADD COLUMN transaction_type VARCHAR(15);

ALTER TABLE customers DROP COLUMN email;




