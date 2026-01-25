CREATE SCHEMA `family_schedule` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- USERS
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE = InnoDB;

-- FAMILIES
CREATE TABLE IF NOT EXISTS families (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE = InnoDB;

-- FAMILY MEMBERS (bridge users <-> families)
CREATE TABLE IF NOT EXISTS family_members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    family_id INT NOT NULL,
    user_id INT NOT NULL,
    role ENUM('admin', 'parent') NOT NULL DEFAULT 'parent',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_family_user (family_id, user_id),
    CONSTRAINT fk_fm_family FOREIGN KEY (family_id) REFERENCES families (id) ON DELETE CASCADE,
    CONSTRAINT fk_fm_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
) ENGINE = InnoDB;

-- CHILDREN
CREATE TABLE IF NOT EXISTS children (
    id INT AUTO_INCREMENT PRIMARY KEY,
    family_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    birthdate DATE NULL,
    notes TEXT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_children_family FOREIGN KEY (family_id) REFERENCES families (id) ON DELETE CASCADE
) ENGINE = InnoDB;

-- EVENTS
CREATE TABLE IF NOT EXISTS events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    family_id INT NOT NULL,
    child_id INT NULL,
    created_by INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    type ENUM(
        'activity',
        'medical',
        'birthday',
        'reminder',
        'school',
        'other'
    ) NOT NULL DEFAULT 'other',
    start_at DATETIME NOT NULL,
    end_at DATETIME NULL,
    location VARCHAR(255) NULL,
    notes TEXT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_events_family_start (family_id, start_at),
    INDEX idx_events_child_start (child_id, start_at),
    CONSTRAINT fk_events_family FOREIGN KEY (family_id) REFERENCES families (id) ON DELETE CASCADE,
    CONSTRAINT fk_events_child FOREIGN KEY (child_id) REFERENCES children (id) ON DELETE SET NULL,
    CONSTRAINT fk_events_user FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE RESTRICT
) ENGINE = InnoDB;

ALTER TABLE users
CHANGE COLUMN password_hash password VARCHAR(255) NOT NULL;

--- insercion de datos de pruebas para establecer la conexion y verificar el correcto funcionamiento -
INSERT INTO
    users (email, password, full_name)
VALUES (
        'madre@example.com',
        '$2b$12$hash_fake_madre',
        'Laura Montironi'
    ),
    (
        'padre@example.com',
        '$2b$12$hash_fake_padre',
        'Marco Rossi'
    );

INSERT INTO
    family_schedule.family_members (family_id, user_id, role)
VALUES (1, 1, 'admin'),
    (1, 2, 'parent');

INSERT INTO
    family_schedule.children (
        family_id,
        name,
        birthdate,
        notes
    )
VALUES (
        1,
        'Emma',
        '2016-05-12',
        'Le gusta danza y dibujo'
    ),
    (
        1,
        'Lucas',
        '2019-09-03',
        'Alergia leve al polen'
    );

INSERT INTO
    family_schedule.events (
        family_id,
        child_id,
        created_by,
        title,
        type,
        start_at,
        end_at,
        location,
        notes,
        created_at
    )
VALUES (
        1,
        1,
        1,
        'Clase de danza',
        'activity',
        '2026-02-03 17:00:00',
        '2026-02-03 18:00:00',
        'Academia Central',
        'Llevar zapatillas',
        NOW()
    );

INSERT INTO
    family_schedule.events (
        family_id,
        child_id,
        created_by,
        title,
        type,
        start_at,
        location,
        notes,
        created_at
    )
VALUES (
        1,
        2,
        1,
        'Pediatra',
        'medical',
        '2026-02-05 10:30:00',
        'Centro Médico Norte',
        'Control anual',
        NOW()
    );

INSERT INTO
    family_schedule.events (
        family_id,
        child_id,
        created_by,
        title,
        type,
        start_at,
        notes,
        created_at
    )
VALUES (
        1,
        1,
        1,
        'Cumpleaños Emma',
        'birthday',
        '2026-05-12 00:00:00',
        'Recordatorio de cumpleaños',
        NOW()
    );

INSERT INTO
    users (email, password, full_name)
VALUES (
        'abuela@example.com',
        '$fake_hash_abuela',
        'Ana Belmaña'
    ),
    (
        'tio@example.com',
        '$fake_hash_tio',
        'Carlos Montironi'
    );

INSERT INTO
    family_members (family_id, user_id, role)
VALUES (2, 3, 'admin'), -- abuela en familia 2
    (1, 4, 'parent');
-- tio en familia 1

INSERT INTO
    children (
        family_id,
        name,
        birthdate,
        notes
    )
VALUES (
        2,
        'Sofía',
        '2014-11-20',
        'Le encanta leer'
    ),
    (
        2,
        'Mateo',
        NULL,
        'Aún no registrada la fecha'
    );

INSERT INTO
    events (
        family_id,
        child_id,
        created_by,
        title,
        type,
        start_at,
        end_at,
        location,
        notes
    )
VALUES (
        2,
        NULL,
        3,
        'Reunión familiar',
        'reminder',
        '2026-02-01 19:00:00',
        '2026-02-01 21:00:00',
        'Casa Belmaña',
        'Traer postre'
    ),
    (
        2,
        4,
        3,
        'Fútbol',
        'activity',
        '2026-02-02 18:00:00',
        '2026-02-02 19:30:00',
        'Polideportivo',
        NULL
    );

INSERT INTO
    events (
        family_id,
        child_id,
        created_by,
        title,
        type,
        start_at,
        end_at,
        location,
        notes
    )
VALUES (
        2,
        NULL,
        3,
        'Reunión familiar',
        'reminder',
        '2026-02-01 19:00:00',
        '2026-02-01 21:00:00',
        'Casa Belmaña',
        'Traer postre'
    ),
    (
        2,
        4,
        3,
        'Fútbol',
        'activity',
        '2026-02-02 18:00:00',
        '2026-02-02 19:30:00',
        'Polideportivo',
        NULL
    );

INSERT INTO
    events (
        family_id,
        child_id,
        created_by,
        title,
        type,
        start_at,
        notes
    )
VALUES (
        1,
        3,
        1,
        'Parque con Lucio',
        'activity',
        '2026-02-06 16:00:00',
        'Llevar agua'
    );

INSERT INTO children (family_id, name) VALUES (999, 'ErrorKid');

INSERT INTO
    events (
        family_id,
        child_id,
        created_by,
        title,
        type,
        start_at
    )
VALUES (
        1,
        1,
        999,
        'Error Event',
        'other',
        '2026-02-10 10:00:00'
    );

ALTER TABLE family_members
ADD COLUMN relationship_label VARCHAR(50) NULL,
ADD COLUMN avatar_url VARCHAR(500) NULL;