CREATE TABLE IF NOT EXISTS ClubeAstronomia (
    id_clube INT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cidade VARCHAR(100),
    fundacao DATE
);

CREATE TABLE IF NOT EXISTS Membro (
    id_membro INT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    id_clube INT,
    FOREIGN KEY (id_clube) REFERENCES ClubeAstronomia(id_clube)
);

CREATE TABLE IF NOT EXISTS CorpoCeleste (
    id_corpo INT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(50),
    constelacao VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Equipamento (
    id_equipamento INT PRIMARY KEY,
    modelo VARCHAR(100) NOT NULL,
    tipo VARCHAR(50),
    fabricante VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS LocalObservacao (
    id_local INT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    altitude_m INT
);

CREATE TABLE IF NOT EXISTS EventoObservacao (
    id_evento INT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    data_evento DATE,
    id_local INT,
    FOREIGN KEY (id_local) REFERENCES LocalObservacao(id_local)
);

CREATE TABLE IF NOT EXISTS OrganizacaoEvento (
    id_evento INT,
    id_clube INT,
    PRIMARY KEY (id_evento, id_clube),
    FOREIGN KEY (id_evento) REFERENCES EventoObservacao(id_evento),
    FOREIGN KEY (id_clube) REFERENCES ClubeAstronomia(id_clube)
);

CREATE TABLE IF NOT EXISTS Observacao (
    id_obs INT PRIMARY KEY,
    id_membro INT,
    id_evento INT,
    id_corpo INT,
    id_equipamento INT,
    horario TIMESTAMP,
    condicoes_climaticas VARCHAR(100),
    anotacoes TEXT,
    FOREIGN KEY (id_membro) REFERENCES Membro(id_membro),
    FOREIGN KEY (id_evento) REFERENCES EventoObservacao(id_evento),
    FOREIGN KEY (id_corpo) REFERENCES CorpoCeleste(id_corpo),
    FOREIGN KEY (id_equipamento) REFERENCES Equipamento(id_equipamento)
);
