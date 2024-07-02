CREATE DATABASE zoo;
USE zoo;

-- Let's make some habitats for the animals to live in
CREATE TABLE habitats(
	habitat_id INT PRIMARY KEY AUTO_INCREMENT,
	habitat_name VARCHAR(20),
    capacity INT,
    current_population INT
);

INSERT INTO habitats (habitat_name, capacity, current_population)
VALUES
('Plains', 10, 0),
('Jungle', 20, 0),
('Aquarium', 20, 0);

-- We'll also need some supplies to help us look after the animals
CREATE TABLE supplies(
	supply_id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(20),
	type VARCHAR(20),
	quantity INT,
	min_quantity INT
);

INSERT INTO supplies (name, type, quantity, min_quantity)
VALUES
('Fruits', 'Food', 100, 20),
('Meat', 'Food', 150, 30),
('Fish', 'Food', 50, 10),
('First aid kits', 'Medical', 20, 5),
('Medicines', 'Medical', 100, 20),
('Disinfectants', 'Cleaning', 50, 10),
('Brooms', 'Cleaning', 10, 2),
('Water bottles', 'General', 200, 50),
('Feeding bowls', 'General', 50, 10);


-- Let's now hire some staff to help look after the animals
CREATE TABLE staff(
	staff_id INT PRIMARY KEY AUTO_INCREMENT,
	first_name VARCHAR(20),
	last_name VARCHAR(20),
	role VARCHAR(20),
	email VARCHAR(30),
	phone_number VARCHAR(20)
);

INSERT INTO staff (first_name, last_name, role, email, phone_number)
VALUES
('John', 'Doe', 'Zookeeper', 'jd@gmail.com', '01122334455'),
('Sarah', 'Smith', 'Zookeeper', 'sarahxx@gmail.com', '06677889911'),
('Fiona', 'Farbles', 'Zookeeper', 'fionaf@gmail.com', '012121212'),
('Laura', 'Oranges', 'Zookeeper', 'laurao@gmail.com', '012341234'),
('Dave', 'Davidson', 'Vet', 'vetdave@gmail.com', '012345678'),
('Rupert', 'Robertson', 'Vet', 'vetrupert@gmail.com', '0987654321'),
('Lara', 'Laurencekirk', 'Office Worker', 'laural@gmail.com', NULL),
('Frank', 'Frankerson', 'Office Worker', 'ffrankerson@gmail.com', '0234567891')
;


-- All set! Let's get some animals into our zoo
CREATE TABLE animals(
	animal_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
	name CHAR(20) UNIQUE,
	species VARCHAR(20),
	age INT,
	health_status VARCHAR(20),
    CONSTRAINT check_health_status CHECK (health_status IN ('Healthy', 'Needs Attention')),
    habitat_id INT,
	FOREIGN KEY (habitat_id) REFERENCES habitats(habitat_id)
);

INSERT INTO animals (name, species, age, health_status, habitat_id)
VALUES
('Leo', 'Lion', 4, 'Healthy', 1),
('Leona', 'Lion', 6, 'Healthy', 1),
('Maurice', 'Monkey', 12, 'Healthy', 2),
('Caeser', 'Monkey', 11, 'Healthy', 2),
('Doug', 'Monkey', 7, 'Needs Attention', 2),
('Penelope', 'Monkey', 5, 'Healthy', 2),
('Shimmer', 'Seal', 2, 'Healthy', 2),
('Shimmy', 'Seal', 4, 'Healthy', 2);

-- Oops I've put the Seals in the wrong enclosure! Let's quickly get them in the right home...
UPDATE animals
SET habitat_id=3
WHERE name='Shimmer'; 

UPDATE animals
SET habitat_id=3
WHERE name='Shimmy';

-- Let's also make a logbook for staff to log care incidents with the animals
CREATE TABLE care(
	care_id INT PRIMARY KEY AUTO_INCREMENT,
	care_date DATE,
	notes TEXT,
    animal_id INT,
    staff_id INT,
    FOREIGN KEY (animal_id) REFERENCES animals(animal_id),
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
);

-- Let's also convert the paper log books from each vet
-- Rupert first
INSERT INTO care (care_date, notes, animal_id, staff_id)
VALUES
('2023-02-12', 'Leo had a cut, Ive disinfected it', 1, 5),
('2023-04-01', 'Gave Maurice a flea treatment', 3, 5),
('2023-08-14', 'Checked Shimmers weight', 7, 5),
('2024-01-02', 'Gave Leona a haircut', 2, 5);

-- Now vet Dave
INSERT INTO care (care_date, notes, animal_id, staff_id)
VALUES
('2023-01-26', 'Trimmed Caesers fingernails', 4, 4),
('2023-05-12', 'Leo needed some dewormer', 1, 4),
('2023-07-05', 'Doug had an eye infection now treated', 5, 4),
('2024-03-02', 'Doug had an upset tummy', 5, 4);


-- This collated care log is out of order, let's view in order to get a better view
SELECT * FROM care
ORDER BY care_date;


-- Let's find if there is any animals in need of medical attention
SELECT * FROM animals
WHERE health_status = 'Needs Attention';
-- Should return a table showing that monkey Doug needs attention.
-- Let's use a medical kit to solve his issue
SET SQL_SAFE_UPDATES = 0;
UPDATE supplies
SET quantity = quantity - 1
WHERE name = 'First aid kits';
SET SQL_SAFE_UPDATES = 1;
-- And then update to show he's healthy again
UPDATE animals
SET health_status = 'Healthy'
WHERE animal_id = 5;


-- As part of an exchange program, Penelope the monkey is being sent to another zoo and we are recieving a new monkey Molly
-- Safe travels, Penelope!
DELETE FROM animals WHERE animal_id = 6;
-- Welcome to your new home, Molly!
INSERT INTO animals (name, species, age, health_status, habitat_id)
VALUES
('Molly', 'Monkey', '4', 'Healthy', 2);

-- One of our visitors has asked us how many animals we have in total and what the average age is
SELECT 
    COUNT(*) AS total_animals,
    AVG(age) AS average_age
FROM animals;

-- The visitor is now asking us what animals are in what enclosures, let's use an INNER JOIN to make a guidebook
SELECT a.name, h.habitat_name, a.species
FROM animals a 
JOIN habitats h ON a.habitat_id = h.habitat_id;

-- We now need to find what treatments have been done on Leo and call each of the vets to confirm details. Let's do a join to find who we need to call.
SELECT c.care_date, c.notes, s.first_name, s.last_name, s.phone_number
FROM care c
JOIN staff s ON c.staff_id = s.staff_id
WHERE c.animal_id=1;

-- We need to print name badges, let's use a function to get staff full name
SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM staff;

-- Let's create a procedure to help the zookeepers keep stock after a morning routine
-- If I have time I'll figure out how to tell SQL to calculate the SET quantity based on lion count
-- I have since had time and changed it to automatically count the lions

DELIMITER //

CREATE PROCEDURE lion_morning_routine()
BEGIN

DECLARE lion_count INT;
    SELECT COUNT(*) INTO lion_count
    FROM animals
    WHERE species = 'Lion';

    UPDATE supplies
    SET quantity = quantity - 2
    WHERE name IN ('Meat', 'Brooms', 'Feeding bowls', 'Water bottles');
END //

DELIMITER ;

SET SQL_SAFE_UPDATES = 0;
CALL lion_morning_routine();
SET SQL_SAFE_UPDATES = 1;

