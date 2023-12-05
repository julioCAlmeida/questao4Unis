CREATE DATABASE imc_db;
USE imc_db;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    altura FLOAT NOT NULL,
    peso FLOAT NOT NULL,
    data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);