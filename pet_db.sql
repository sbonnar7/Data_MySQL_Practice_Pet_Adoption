CREATE DATABASE petadoption;
USE petadoption;

CREATE TABLE pets(
	id INT auto_increment PRIMARY KEY,
    name VARCHAR(24) NOT NULL,
    species VARCHAR(24) NOT NULL,
    age INT NOT NULL,
    adopted BOOLEAN DEFAULT FALSE
);

INSERT INTO pets
(name, species, age)
VALUES
('Biscuits', 'Dog', 5),
('Lucky', 'Dog', 7),
('Felix', 'Cat', 12),
('Fluffy', 'Cat', 2),
('Snappy', 'Crocodile', 5);

