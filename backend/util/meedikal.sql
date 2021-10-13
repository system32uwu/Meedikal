CREATE TABLE user (
    ci INTEGER PRIMARY KEY NOT NULL,
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
    ci INTEGER PRIMARY KEY NOT NULL,
    FOREIGN KEY (ci) REFERENCES user(ci) ON DELETE CASCADE ON UPDATE CASCADE
) WITHOUT ROWID;

CREATE TABLE doctor (
    ci INTEGER PRIMARY KEY NOT NULL,
    FOREIGN KEY (ci) REFERENCES medicalPersonnel(ci) ON DELETE CASCADE ON UPDATE CASCADE
) WITHOUT ROWID;

CREATE TABLE medicalAssistant (
    ci INTEGER PRIMARY KEY NOT NULL,
    FOREIGN KEY (ci) REFERENCES medicalPersonnel(ci) ON DELETE CASCADE ON UPDATE CASCADE
) WITHOUT ROWID;

CREATE TABLE administrative (
    ci INTEGER PRIMARY KEY NOT NULL,
    FOREIGN KEY (ci) REFERENCES user(ci) ON DELETE CASCADE ON UPDATE CASCADE
) WITHOUT ROWID;

CREATE TABLE patient (
    ci INTEGER PRIMARY KEY NOT NULL,
    FOREIGN KEY (ci) REFERENCES user(ci) ON DELETE CASCADE ON UPDATE CASCADE
) WITHOUT ROWID;

CREATE TABLE userPhone (
    ci INTEGER NOT NULL,
    phone VARCHAR(32) NOT NULL,

    PRIMARY KEY(ci,phone),
    FOREIGN KEY (ci) REFERENCES user(ci) ON DELETE CASCADE ON UPDATE CASCADE
) WITHOUT ROWID;

-- Nurses and Doctors might be specialized.
CREATE TABLE specialty (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(64) UNIQUE NOT NULL
);

CREATE TABLE mpHasSpec (
    idSpec INTEGER NOT NULL,
    ciMp INTEGER NOT NULL,
    -- OPTIONAL FIELD
    detail VARCHAR(256),

    PRIMARY KEY (idSpec,ciMp),
    FOREIGN KEY (ciMp) REFERENCES medicalPersonnel(ci) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (idSpec) REFERENCES specialty(id) ON DELETE CASCADE ON UPDATE CASCADE
) WITHOUT ROWID;

CREATE TABLE appointment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(128) NOT NULL,
    state VARCHAR(36) NOT NULL DEFAULT 'OK',
    date date NOT NULL,
    -- OPTIONAL FIELDS
    startsAt datetime,
    endsAt datetime,
    etpp INTEGER,
    maxTurns INTEGER
); --etpp: estimated time per patient (tiempo estimado por turno de paciente en la consulta)

-- Branch significa sucursal, una cita medica tomara lugar en alguna de las sucursales.
CREATE TABLE branch (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(64) UNIQUE NOT NULL,
    phoneNumber VARCHAR(64) NOT NULL,
    location VARCHAR(64) NOT NULL
);

CREATE TABLE apTakesPlace (
    idAp INTEGER NOT NULL,
    idBranch INTEGER NOT NULL,

    PRIMARY KEY(idAp,idBranch),
    FOREIGN KEY(idAp) REFERENCES appointment(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(idBranch) REFERENCES Branch(id) ON DELETE CASCADE ON UPDATE CASCADE
) WITHOUT ROWID;

CREATE TABLE assignedTo (
    idAp INTEGER NOT NULL,
    ciDoc INTEGER NOT NULL,

    PRIMARY KEY(idAp),
    FOREIGN KEY (ciDoc) REFERENCES doctor(ci) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (idAp) REFERENCES appointment(id) ON DELETE CASCADE ON UPDATE CASCADE
) WITHOUT ROWID;

CREATE TABLE attendsTo (
    idAp INTEGER NOT NULL,
    ciPa INTEGER NOT NULL,
    -- OPTIONAL FIELD
    motive VARCHAR(256),
    time DATETIME, --NULLABLE, but in case it's provided it should be unique with both idAp and ciPa
    number INTEGER, --NULLABLE, but in case it's provided it should be unique with both idAp and ciPa
    
    UNIQUE (idAp, ciPa),
    FOREIGN KEY (idAp) REFERENCES appointment(id) ON DELETE CASCADE,
    FOREIGN KEY (ciPa) REFERENCES patient(ci) ON DELETE CASCADE
);

-- If a number is already picked, or is not in range of (0, maxTurns) raise an error
-- If a time is already picked, or is not in range of (startsAt, endsAt) raise an error
-- If the appointment does not have maxTurns, but a number for a turn is trying to be inserted in attendsTo, raise an error 
-- If the appointment does not have startsAt and endsAt setted, but a time for a turn is trying to be inserted in attendsTo, raise an error
CREATE TRIGGER assign_to_attendsTo 
    BEFORE INSERT ON attendsTo
BEGIN
    SELECT CASE WHEN new.number IS NOT NULL THEN
        CASE
            WHEN NOT EXISTS (SELECT 1 FROM appointment WHERE appointment.id = new.idAp AND appointment.maxTurns IS NOT NULL)
                THEN RAISE(ABORT, 'number of turns is not setted yet')

            WHEN EXISTS(SELECT 1 FROM attendsTo WHERE number = new.number AND idAp = new.idAp)
                THEN RAISE(ABORT, 'number is already picked')
            
            WHEN NOT EXISTS(SELECT 1 FROM appointment WHERE appointment.id = new.idAp AND (new.number > 0 and new.number <= appointment.maxTurns)) 
                THEN RAISE(ABORT, 'number is not in the range of 0 and maximum turns')
        
        END
    END;

    SELECT CASE WHEN new.time IS NOT NULL THEN
        CASE
            WHEN EXISTS (SELECT 1 FROM appointment WHERE appointment.id = new.idAp AND (appointment.startsAt IS NULL OR appointment.startsAt IS NULL))
                THEN RAISE(ABORT, 'start and end time for this appointment are not setted yet')

            WHEN EXISTS(SELECT 1 FROM attendsTo WHERE time = new.time AND idAp = new.idAp)
                THEN RAISE(ABORT, 'time is already picked')
            
            WHEN NOT EXISTS(SELECT 1 FROM appointment WHERE appointment.id = new.idAp AND (new.time >= appointment.startsAt AND new.time <= appointment.endsAt)) 
                THEN RAISE(ABORT, 'time is not in the range of start and end time for this appointment')
        
        END
    END;
    
END;

CREATE TABLE assistsAp (
    idAp INTEGER NOT NULL,
    ciMa INTEGER NOT NULL,
    time datetime NOT NULL,

    FOREIGN KEY (idAp) REFERENCES assignedTo(idAp) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (ciMa) REFERENCES medicalAssistant(ci) ON DELETE CASCADE ON UPDATE CASCADE
    PRIMARY KEY(idAp,ciMa,time)
) WITHOUT ROWID;

CREATE TABLE clinicalSign (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(128) UNIQUE NOT NULL,
    -- OPTIONAL FIELD
    description VARCHAR(512)
);

CREATE TABLE disease (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(128) UNIQUE NOT NULL,
    -- OPTIONAL FIELD
    description VARCHAR(512)
);

CREATE TABLE symptom (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(128) UNIQUE NOT NULL,
    -- OPTIONAL FIELD
    description VARCHAR(512)
);

CREATE TABLE registersCs (
    idAp INTEGER NOT NULL,
    ciPa INTEGER NOT NULL,
    idCs INTEGER NOT NULL,
    -- OPTIONAL FIELD
    detail VARCHAR(256),

    PRIMARY KEY(idAp,ciPa,idCs),
    FOREIGN KEY (idAp, ciPa) REFERENCES attendsTo(idAp, ciPa) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (idCs) REFERENCES clinicalSign(id) ON DELETE CASCADE ON UPDATE CASCADE
) WITHOUT ROWID;

CREATE TABLE registersSy (
    idAp INTEGER NOT NULL,
    ciPa INTEGER NOT NULL,
    idSy INTEGER NOT NULL,
    -- OPTIONAL FIELD
    detail VARCHAR(256),
    
    PRIMARY KEY(idAp,ciPa,idSy),
    FOREIGN KEY (idAp, ciPa) REFERENCES attendsTo(idAp, ciPa) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (idSy) REFERENCES symptom(id) ON DELETE CASCADE ON UPDATE CASCADE
) WITHOUT ROWID;

CREATE TABLE diagnoses (
    idAp INTEGER NOT NULL,
    ciPa INTEGER NOT NULL,
    idDis INTEGER NOT NULL,
    -- OPTIONAL FIELD
    detail VARCHAR(256),

    PRIMARY KEY(idAp,ciPa,idDis),
    FOREIGN KEY (idAp, ciPa) REFERENCES attendsTo(idAp, ciPa) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (idDis) REFERENCES disease(id) ON DELETE CASCADE ON UPDATE CASCADE
) WITHOUT ROWID;