PRAGMA foreign_keys=ON;

CREATE TABLE user (
    ci integer PRIMARY KEY,
    name1 VARCHAR(32) NOT NULL,
    name2 VARCHAR(32),
    surname1 VARCHAR(32) NOT NULL,
    surname2 VARCHAR(32),
    sex VARCHAR(1) NOT NULL,
    genre VARCHAR(32),
    birthdate DATETIME NOT NULL,
    location VARCHAR(256),
    email VARCHAR(256),
    active BOOLEAN NOT NULL,
    password VARCHAR(128) NOT NULL
);

CREATE TABLE medicalPersonnel (
    ci integer PRIMARY KEY,
    FOREIGN KEY (ci) REFERENCES user(ci) ON DELETE CASCADE
);

CREATE TABLE doctor (
    ci integer PRIMARY KEY,
    FOREIGN KEY (ci) REFERENCES medicalPersonnel(ci) ON DELETE CASCADE
);

CREATE TABLE medicalAssistant (
    ci integer PRIMARY KEY,
    FOREIGN KEY (ci) REFERENCES medicalPersonnel(ci) ON DELETE CASCADE
);

CREATE TABLE administrative (
    ci integer PRIMARY KEY,
    FOREIGN KEY (ci) REFERENCES user(ci) ON DELETE CASCADE
);

CREATE TABLE patient (
    ci integer PRIMARY KEY,
    FOREIGN KEY (ci) REFERENCES user(ci) ON DELETE CASCADE
);

CREATE TABLE userPhone (
    ci integer,
    phone VARCHAR(32),

    PRIMARY KEY(ci,phone),
    FOREIGN KEY (ci) REFERENCES user(ci) ON DELETE CASCADE
);

-- Nurses and Doctors might be specialized.
CREATE TABLE specialty (
    id integer PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(64) UNIQUE NOT NULL
);

CREATE TABLE mpHasSpec (
    idSpec integer,
    ciMp integer,

    PRIMARY KEY (idSpec,ciMp),
    FOREIGN KEY (ciMp) REFERENCES medicalPersonnel(ci) ON DELETE CASCADE,
    FOREIGN KEY (idSpec) REFERENCES specialty(id) ON DELETE CASCADE
);

CREATE TABLE appointment (
    id integer PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(128) NOT NULL,
    date date NOT NULL,
    state VARCHAR(36) NOT NULL,
    timeBegins time,
    timeEnds time,
    etpp integer,
    maxTurns integer
); --etpp: estimated time per patient (tiempo estimado por turno de paciente en la consulta)

-- Branch significa sucursal, una cita medica tomara lugar en alguna de las sucursales.
CREATE TABLE branch (
    id integer PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(64) NOT NULL,
    phoneNumber VARCHAR(64) NOT NULL,
    location VARCHAR(64) NOT NULL
);

CREATE TABLE apTakesPlace (
    idAp integer,
    idBranch integer,

    PRIMARY KEY(idAp,idBranch)
);

CREATE TABLE assignedTo (
    idAp integer,
    ciDoc integer,

    PRIMARY KEY(idAp, ciDoc),
    FOREIGN KEY (ciDoc) REFERENCES doctor(ci) ON DELETE CASCADE,
    FOREIGN KEY (idAp) REFERENCES appointment(id) ON DELETE CASCADE
);

CREATE TABLE assistsAp (
    idAp integer,
    ciMa integer,
    time time,

    PRIMARY KEY(idAp,ciMa,time)
);

CREATE TABLE attendsTo (
    idAp integer,
    ciPa integer,
    motive VARCHAR(256),
    number integer,
    time time,

    PRIMARY KEY (idAp,ciPa),
    FOREIGN KEY (idAp) REFERENCES appointment(id) ON DELETE CASCADE,
    FOREIGN KEY (ciPa) REFERENCES patient(ci) ON DELETE CASCADE
);

CREATE TABLE clinicalSign (
    id integer PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(128) UNIQUE NOT NULL,
    description VARCHAR(512)
);

CREATE TABLE disease (
    id integer PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(128) UNIQUE NOT NULL,
    description VARCHAR(512)
);

CREATE TABLE symptom (
    id integer PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(128) UNIQUE NOT NULL,
    description VARCHAR(512)
);

CREATE TABLE registersCs (
    idAp integer,
    ciPa integer,
    idCs integer,
    detail VARCHAR(256),

    PRIMARY KEY(idAp,ciPa,idCs),
    FOREIGN KEY (idAp, ciPa) REFERENCES attendsTo(idAp, ciPa) ON DELETE CASCADE,
    FOREIGN KEY (idCs) REFERENCES clinicalSign(id) ON DELETE CASCADE
);

CREATE TABLE registersSy (
    idAp integer,
    ciPa integer,
    idSy integer,
    detail VARCHAR(256),
    
    PRIMARY KEY(idAp,ciPa,idSy),
    FOREIGN KEY (idAp, ciPa) REFERENCES attendsTo(idAp, ciPa) ON DELETE CASCADE,
    FOREIGN KEY (idSy) REFERENCES symptom(id) ON DELETE CASCADE
);

CREATE TABLE diagnoses (
    idAp integer,
    ciPa integer,
    idDis integer,
    detail VARCHAR(256),

    PRIMARY KEY(idAp,ciPa,idDis),
    FOREIGN KEY (idAp, ciPa) REFERENCES attendsTo(idAp, ciPa) ON DELETE CASCADE,
    FOREIGN KEY (idDis) REFERENCES disease(id) ON DELETE CASCADE
);