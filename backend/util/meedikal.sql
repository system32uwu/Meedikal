CREATE TABLE user (
    ci integer PRIMARY KEY NOT NULL,
    name1 VARCHAR(32) NOT NULL,
    surname1 VARCHAR(32) NOT NULL,
    sex VARCHAR(1) NOT NULL,
    birthdate DATETIME NOT NULL,
    location VARCHAR(256),
    email VARCHAR(256),
    password VARCHAR(128) NOT NULL,
    -- OPTIONAL FIELDS
    name2 VARCHAR(32),
    surname2 VARCHAR(32),
    genre VARCHAR(32),
    active BOOLEAN NOT NULL DEFAULT 1,
    photoUrl TEXT
) WITHOUT ROWID;

CREATE TABLE medicalPersonnel (
    ci integer PRIMARY KEY NOT NULL,
    FOREIGN KEY (ci) REFERENCES user(ci) ON DELETE CASCADE ON UPDATE CASCADE
) WITHOUT ROWID;

CREATE TABLE doctor (
    ci integer PRIMARY KEY NOT NULL,
    FOREIGN KEY (ci) REFERENCES medicalPersonnel(ci) ON DELETE CASCADE ON UPDATE CASCADE
) WITHOUT ROWID;

CREATE TABLE medicalAssistant (
    ci integer PRIMARY KEY NOT NULL,
    FOREIGN KEY (ci) REFERENCES medicalPersonnel(ci) ON DELETE CASCADE ON UPDATE CASCADE
) WITHOUT ROWID;

CREATE TABLE administrative (
    ci integer PRIMARY KEY NOT NULL,
    FOREIGN KEY (ci) REFERENCES user(ci) ON DELETE CASCADE ON UPDATE CASCADE
) WITHOUT ROWID;

CREATE TABLE patient (
    ci integer PRIMARY KEY NOT NULL,
    FOREIGN KEY (ci) REFERENCES user(ci) ON DELETE CASCADE ON UPDATE CASCADE
) WITHOUT ROWID;

CREATE TABLE userPhone (
    ci integer NOT NULL,
    phone VARCHAR(32) NOT NULL,

    PRIMARY KEY(ci,phone),
    FOREIGN KEY (ci) REFERENCES user(ci) ON DELETE CASCADE ON UPDATE CASCADE
) WITHOUT ROWID;

-- Nurses and Doctors might be specialized.
CREATE TABLE specialty (
    id integer PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(64) UNIQUE NOT NULL
);

CREATE TABLE mpHasSpec (
    idSpec integer NOT NULL,
    ciMp integer NOT NULL,
    -- OPTIONAL FIELD
    detail VARCHAR(256),

    PRIMARY KEY (idSpec,ciMp),
    FOREIGN KEY (ciMp) REFERENCES medicalPersonnel(ci) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (idSpec) REFERENCES specialty(id) ON DELETE CASCADE ON UPDATE CASCADE
) WITHOUT ROWID;

CREATE TABLE appointment (
    id integer PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(128) NOT NULL,
    state VARCHAR(36) NOT NULL DEFAULT 'OK',
    date date NOT NULL,
    -- OPTIONAL FIELDS
    startsAt datetime,
    endsAt datetime,
    etpp integer,
    maxTurns integer
); --etpp: estimated time per patient (tiempo estimado por turno de paciente en la consulta)

-- Branch significa sucursal, una cita medica tomara lugar en alguna de las sucursales.
CREATE TABLE branch (
    id integer PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(64) UNIQUE NOT NULL,
    phoneNumber VARCHAR(64) NOT NULL,
    location VARCHAR(64) NOT NULL
);

CREATE TABLE apTakesPlace (
    idAp integer NOT NULL,
    idBranch integer NOT NULL,

    PRIMARY KEY(idAp,idBranch),
    FOREIGN KEY(idAp) REFERENCES appointment(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(idBranch) REFERENCES Branch(id) ON DELETE CASCADE ON UPDATE CASCADE
) WITHOUT ROWID;

CREATE TABLE assignedTo (
    idAp integer NOT NULL,
    ciDoc integer NOT NULL,

    PRIMARY KEY(idAp),
    FOREIGN KEY (ciDoc) REFERENCES doctor(ci) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (idAp) REFERENCES appointment(id) ON DELETE CASCADE ON UPDATE CASCADE
) WITHOUT ROWID;

CREATE TABLE attendsTo (
    idAp integer NOT NULL,
    ciPa integer NOT NULL,
    -- OPTIONAL FIELD
    motive VARCHAR(256),
    number integer UNIQUE, --NULLABLE, but in case it's provided should be UNIQUE.
    time datetime UNIQUE, --NULLABLE, but in case it's provided should be UNIQUE.

    PRIMARY KEY (idAp,ciPa),
    FOREIGN KEY (idAp) REFERENCES appointment(id) ON DELETE CASCADE,
    FOREIGN KEY (ciPa) REFERENCES patient(ci) ON DELETE CASCADE
) WITHOUT ROWID;

CREATE TABLE assistsAp (
    idAp integer NOT NULL,
    ciMa integer NOT NULL,
    time datetime NOT NULL,

    FOREIGN KEY (idAp) REFERENCES assignedTo(idAp) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (ciMa) REFERENCES medicalAssistant(ci) ON DELETE CASCADE ON UPDATE CASCADE
    PRIMARY KEY(idAp,ciMa,time)
) WITHOUT ROWID;

CREATE TABLE clinicalSign (
    id integer PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(128) UNIQUE NOT NULL,
    -- OPTIONAL FIELD
    description VARCHAR(512)
);

CREATE TABLE disease (
    id integer PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(128) UNIQUE NOT NULL,
    -- OPTIONAL FIELD
    description VARCHAR(512)
);

CREATE TABLE symptom (
    id integer PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(128) UNIQUE NOT NULL,
    -- OPTIONAL FIELD
    description VARCHAR(512)
);

CREATE TABLE registersCs (
    idAp integer NOT NULL,
    ciPa integer NOT NULL,
    idCs integer NOT NULL,
    -- OPTIONAL FIELD
    detail VARCHAR(256),

    PRIMARY KEY(idAp,ciPa,idCs),
    FOREIGN KEY (idAp, ciPa) REFERENCES attendsTo(idAp, ciPa) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (idCs) REFERENCES clinicalSign(id) ON DELETE CASCADE ON UPDATE CASCADE
) WITHOUT ROWID;

CREATE TABLE registersSy (
    idAp integer NOT NULL,
    ciPa integer NOT NULL,
    idSy integer NOT NULL,
    -- OPTIONAL FIELD
    detail VARCHAR(256),
    
    PRIMARY KEY(idAp,ciPa,idSy),
    FOREIGN KEY (idAp, ciPa) REFERENCES attendsTo(idAp, ciPa) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (idSy) REFERENCES symptom(id) ON DELETE CASCADE ON UPDATE CASCADE
) WITHOUT ROWID;

CREATE TABLE diagnoses (
    idAp integer NOT NULL,
    ciPa integer NOT NULL,
    idDis integer NOT NULL,
    -- OPTIONAL FIELD
    detail VARCHAR(256),

    PRIMARY KEY(idAp,ciPa,idDis),
    FOREIGN KEY (idAp, ciPa) REFERENCES attendsTo(idAp, ciPa) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (idDis) REFERENCES disease(id) ON DELETE CASCADE ON UPDATE CASCADE
) WITHOUT ROWID;