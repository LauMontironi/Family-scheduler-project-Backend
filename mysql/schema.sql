DROP TABLE IF EXISTS events;

DROP TABLE IF EXISTS children;

DROP TABLE IF EXISTS family_members;

DROP TABLE IF EXISTS families;

DROP TABLE IF EXISTS users;

-- 1. La Familia
CREATE TABLE families (
    id INT AUTO_INCREMENT PRIMARY KEY,
    family_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Miembros (Adultos y Niños en la misma tabla)
CREATE TABLE members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    family_id INT NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE, -- Solo para adultos que hacen login
    password VARCHAR(255), -- Solo para adultos
    relationship VARCHAR(50), -- madre, padre, abuelo, hijo, etc.
    is_child BOOLEAN DEFAULT FALSE, -- CLAVE: TRUE para sección niños, FALSE para adultos
    birthdate DATE,
    gender VARCHAR(20),
    city VARCHAR(100),
    hobbys TEXT,
    is_admin BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (family_id) REFERENCES families (id) ON DELETE CASCADE
);

-- 3. Eventos (Asignables a cualquier miembro)
CREATE TABLE events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    family_id INT NOT NULL,
    member_id INT, -- A quién se le asigna (puede ser NULL si es familiar general)
    title VARCHAR(150) NOT NULL,
    description TEXT,
    location VARCHAR(150),
    type VARCHAR(50), -- medical, school, activity, etc.
    start_at DATETIME NOT NULL,
    end_at DATETIME,
    FOREIGN KEY (family_id) REFERENCES families (id) ON DELETE CASCADE,
    FOREIGN KEY (member_id) REFERENCES members (id) ON DELETE SET NULL
);

INSERT INTO families (family_name) VALUES ('Rivera');
-- Suponiendo que el ID de la familia es 1:
INSERT INTO
    members (
        family_id,
        full_name,
        email,
        is_child,
        is_admin,
        relationship
    )
VALUES (
        1,
        'Ana Rivera',
        'ana@demo.com',
        FALSE,
        TRUE,
        'madre'
    );

--🌳 INSERT DE 5 FAMILIAS + MIEMBROS

START TRANSACTION;

-- =====================================================
-- FAMILIA 1: Rivera
-- =====================================================
INSERT INTO families (family_name) VALUES ('Rivera');

SET @fam1 := LAST_INSERT_ID();

INSERT INTO
    members (
        family_id,
        full_name,
        email,
        password,
        relationship,
        is_child,
        birthdate,
        gender,
        city,
        hobbys,
        is_admin
    )
VALUES (
        @fam1,
        'Ana Rivera',
        'ana.rivera@demo.com',
        'Demo1234!',
        'madre',
        FALSE,
        '1988-04-12',
        'female',
        'Madrid',
        'yoga, lectura, cocina',
        TRUE
    ),
    (
        @fam1,
        'Carlos Rivera',
        'carlos.rivera@demo.com',
        'Demo1234!',
        'padre',
        FALSE,
        '1986-09-03',
        'male',
        'Madrid',
        'running, cine',
        FALSE
    ),
    (
        @fam1,
        'Lucia Rivera',
        'lucia.rivera@demo.com',
        'Demo1234!',
        'default',
        TRUE,
        '2016-02-19',
        'female',
        'Madrid',
        'pintar, baile',
        FALSE
    ),
    (
        @fam1,
        'Mateo Rivera',
        'mateo.rivera@demo.com',
        'Demo1234!',
        'default',
        TRUE,
        '2019-07-22',
        'male',
        'Madrid',
        'lego, futbol',
        FALSE
    ),
    (
        @fam1,
        'Maria Gomez',
        'maria.gomez@demo.com',
        'Demo1234!',
        'abuela',
        FALSE,
        '1959-01-08',
        'female',
        'Madrid',
        'ganchillo, jardineria',
        FALSE
    ),
    (
        @fam1,
        'Jose Rivera',
        'jose.rivera@demo.com',
        'Demo1234!',
        'abuelo',
        FALSE,
        '1956-11-30',
        'male',
        'Madrid',
        'ajedrez, paseo',
        FALSE
    ),
    (
        @fam1,
        'Sofia Rivera',
        'sofia.rivera@demo.com',
        'Demo1234!',
        'tia',
        FALSE,
        '1991-06-15',
        'female',
        'Madrid',
        'fotografia, senderismo',
        FALSE
    ),
    (
        @fam1,
        'Diego Rivera',
        'diego.rivera@demo.com',
        'Demo1234!',
        'tio',
        FALSE,
        '1993-03-10',
        'male',
        'Madrid',
        'guitarra, videojuegos',
        FALSE
    );

-- =====================================================
-- FAMILIA 2: López
-- =====================================================
INSERT INTO families (family_name) VALUES ('Lopez');

SET @fam2 := LAST_INSERT_ID();

INSERT INTO
    members
VALUES (
        NULL,
        @fam2,
        'Laura Lopez',
        'laura.lopez@demo.com',
        'Demo1234!',
        'madre',
        FALSE,
        '1990-10-05',
        'female',
        'Barcelona',
        'pilates, series',
        TRUE
    ),
    (
        NULL,
        @fam2,
        'Javier Lopez',
        'javier.lopez@demo.com',
        'Demo1234!',
        'padre',
        FALSE,
        '1989-12-18',
        'male',
        'Barcelona',
        'cocina, padel',
        FALSE
    ),
    (
        NULL,
        @fam2,
        'Nora Lopez',
        'nora.lopez@demo.com',
        'Demo1234!',
        'default',
        TRUE,
        '2017-05-02',
        'female',
        'Barcelona',
        'manualidades, cuentos',
        FALSE
    ),
    (
        NULL,
        @fam2,
        'Hugo Lopez',
        'hugo.lopez@demo.com',
        'Demo1234!',
        'default',
        TRUE,
        '2021-09-14',
        'male',
        'Barcelona',
        'coches, musica',
        FALSE
    ),
    (
        NULL,
        @fam2,
        'Carmen Lopez',
        'carmen.lopez@demo.com',
        'Demo1234!',
        'abuela',
        FALSE,
        '1961-02-27',
        'female',
        'Barcelona',
        'baile, jardineria',
        FALSE
    ),
    (
        NULL,
        @fam2,
        'Antonio Lopez',
        'antonio.lopez@demo.com',
        'Demo1234!',
        'abuelo',
        FALSE,
        '1958-08-09',
        'male',
        'Barcelona',
        'bicicleta, lectura',
        FALSE
    ),
    (
        NULL,
        @fam2,
        'Marta Lopez',
        'marta.lopez@demo.com',
        'Demo1234!',
        'tia',
        FALSE,
        '1994-04-20',
        'female',
        'Barcelona',
        'viajar, cine',
        FALSE
    );

-- =====================================================
-- FAMILIA 3: Sánchez
-- =====================================================
INSERT INTO families (family_name) VALUES ('Sanchez');

SET @fam3 := LAST_INSERT_ID();

INSERT INTO
    members
VALUES (
        NULL,
        @fam3,
        'Patricia Sanchez',
        'patricia.sanchez@demo.com',
        'Demo1234!',
        'madre',
        FALSE,
        '1987-03-28',
        'female',
        'Valencia',
        'crossfit, lectura',
        TRUE
    ),
    (
        NULL,
        @fam3,
        'Ruben Sanchez',
        'ruben.sanchez@demo.com',
        'Demo1234!',
        'padre',
        FALSE,
        '1985-01-11',
        'male',
        'Valencia',
        'baloncesto, podcasts',
        FALSE
    ),
    (
        NULL,
        @fam3,
        'Irene Sanchez',
        'irene.sanchez@demo.com',
        'Demo1234!',
        'default',
        TRUE,
        '2014-12-01',
        'female',
        'Valencia',
        'patinaje, musica',
        FALSE
    ),
    (
        NULL,
        @fam3,
        'Leo Sanchez',
        'leo.sanchez@demo.com',
        'Demo1234!',
        'default',
        TRUE,
        '2018-06-09',
        'male',
        'Valencia',
        'dinosaurios, puzzles',
        FALSE
    ),
    (
        NULL,
        @fam3,
        'Pilar Sanchez',
        'pilar.sanchez@demo.com',
        'Demo1234!',
        'abuela',
        FALSE,
        '1960-09-21',
        'female',
        'Valencia',
        'cocina, costura',
        FALSE
    ),
    (
        NULL,
        @fam3,
        'Manuel Sanchez',
        'manuel.sanchez@demo.com',
        'Demo1234!',
        'abuelo',
        FALSE,
        '1957-07-04',
        'male',
        'Valencia',
        'huerto, domino',
        FALSE
    ),
    (
        NULL,
        @fam3,
        'Alvaro Sanchez',
        'alvaro.sanchez@demo.com',
        'Demo1234!',
        'tio',
        FALSE,
        '1992-11-17',
        'male',
        'Valencia',
        'senderismo, fotografia',
        FALSE
    );

-- =====================================================
-- FAMILIA 4: Martín
-- =====================================================
INSERT INTO families (family_name) VALUES ('Martin');

SET @fam4 := LAST_INSERT_ID();

INSERT INTO
    members
VALUES (
        NULL,
        @fam4,
        'Elena Martin',
        'elena.martin@demo.com',
        'Demo1234!',
        'madre',
        FALSE,
        '1991-07-13',
        'female',
        'Sevilla',
        'teatro, yoga',
        TRUE
    ),
    (
        NULL,
        @fam4,
        'Sergio Martin',
        'sergio.martin@demo.com',
        'Demo1234!',
        'padre',
        FALSE,
        '1990-02-06',
        'male',
        'Sevilla',
        'correr, musica',
        FALSE
    ),
    (
        NULL,
        @fam4,
        'Claudia Martin',
        'claudia.martin@demo.com',
        'Demo1234!',
        'default',
        TRUE,
        '2015-08-25',
        'female',
        'Sevilla',
        'baile, dibujo',
        FALSE
    ),
    (
        NULL,
        @fam4,
        'Bruno Martin',
        'bruno.martin@demo.com',
        'Demo1234!',
        'default',
        TRUE,
        '2020-01-30',
        'male',
        'Sevilla',
        'bloques, cuentos',
        FALSE
    ),
    (
        NULL,
        @fam4,
        'Rosa Martin',
        'rosa.martin@demo.com',
        'Demo1234!',
        'abuela',
        FALSE,
        '1962-05-16',
        'female',
        'Sevilla',
        'jardineria, cocina',
        FALSE
    ),
    (
        NULL,
        @fam4,
        'Francisco Martin',
        'francisco.martin@demo.com',
        'Demo1234!',
        'abuelo',
        FALSE,
        '1955-10-02',
        'male',
        'Sevilla',
        'pesca, cartas',
        FALSE
    ),
    (
        NULL,
        @fam4,
        'Teresa Martin',
        'teresa.martin@demo.com',
        'Demo1234!',
        'tia',
        FALSE,
        '1988-12-09',
        'female',
        'Sevilla',
        'manualidades, cine',
        FALSE
    ),
    (
        NULL,
        @fam4,
        'Miguel Martin',
        'miguel.martin@demo.com',
        'Demo1234!',
        'tio',
        FALSE,
        '1993-09-23',
        'male',
        'Sevilla',
        'guitarra, padel',
        FALSE
    );

-- =====================================================
-- FAMILIA 5: Fernández
-- =====================================================
INSERT INTO families (family_name) VALUES ('Fernandez');

SET @fam5 := LAST_INSERT_ID();

INSERT INTO
    members
VALUES (
        NULL,
        @fam5,
        'Noelia Fernandez',
        'noelia.fernandez@demo.com',
        'Demo1234!',
        'madre',
        FALSE,
        '1989-11-26',
        'female',
        'Bilbao',
        'senderismo, cocina',
        TRUE
    ),
    (
        NULL,
        @fam5,
        'Ivan Fernandez',
        'ivan.fernandez@demo.com',
        'Demo1234!',
        'padre',
        FALSE,
        '1988-04-01',
        'male',
        'Bilbao',
        'ciclismo, cine',
        FALSE
    ),
    (
        NULL,
        @fam5,
        'Aitana Fernandez',
        'aitana.fernandez@demo.com',
        'Demo1234!',
        'default',
        TRUE,
        '2013-03-03',
        'female',
        'Bilbao',
        'piano, lectura',
        FALSE
    ),
    (
        NULL,
        @fam5,
        'Enzo Fernandez',
        'enzo.fernandez@demo.com',
        'Demo1234!',
        'default',
        TRUE,
        '2017-10-12',
        'male',
        'Bilbao',
        'futbol, lego',
        FALSE
    ),
    (
        NULL,
        @fam5,
        'Amaya Fernandez',
        'amaya.fernandez@demo.com',
        'Demo1234!',
        'abuela',
        FALSE,
        '1963-07-29',
        'female',
        'Bilbao',
        'pintura, jardineria',
        FALSE
    ),
    (
        NULL,
        @fam5,
        'Inaki Fernandez',
        'inaki.fernandez@demo.com',
        'Demo1234!',
        'abuelo',
        FALSE,
        '1959-02-14',
        'male',
        'Bilbao',
        'ajedrez, caminar',
        FALSE
    ),
    (
        NULL,
        @fam5,
        'Lucia Fernandez',
        'lucia.fernandez@demo.com',
        'Demo1234!',
        'tia',
        FALSE,
        '1995-06-06',
        'female',
        'Bilbao',
        'fotografia, baile',
        FALSE
    ),
    (
        NULL,
        @fam5,
        'Unai Fernandez',
        'unai.fernandez@demo.com',
        'Demo1234!',
        'tio',
        FALSE,
        '1992-01-19',
        'male',
        'Bilbao',
        'surf, musica',
        FALSE
    );

COMMIT;

-- =====================================================
-- EVENTS demo (5 familias)
-- =====================================================
START TRANSACTION;

-- ---------- Resolver IDs de familias (por nombre, el último insertado) ----------
SELECT id INTO @fam1
FROM families
WHERE
    family_name = 'Rivera'
ORDER BY id DESC
LIMIT 1;

SELECT id INTO @fam2
FROM families
WHERE
    family_name = 'Lopez'
ORDER BY id DESC
LIMIT 1;

SELECT id INTO @fam3
FROM families
WHERE
    family_name = 'Sanchez'
ORDER BY id DESC
LIMIT 1;

SELECT id INTO @fam4
FROM families
WHERE
    family_name = 'Martin'
ORDER BY id DESC
LIMIT 1;

SELECT id INTO @fam5
FROM families
WHERE
    family_name = 'Fernandez'
ORDER BY id DESC
LIMIT 1;

-- ---------- Resolver IDs de miembros por email ----------
-- Rivera
SELECT id INTO @ana
FROM members
WHERE
    family_id = @fam1
    AND email = 'ana.rivera@demo.com'
LIMIT 1;

SELECT id INTO @carlos
FROM members
WHERE
    family_id = @fam1
    AND email = 'carlos.rivera@demo.com'
LIMIT 1;

SELECT id INTO @lucia_r
FROM members
WHERE
    family_id = @fam1
    AND email = 'lucia.rivera@demo.com'
LIMIT 1;

SELECT id INTO @mateo_r
FROM members
WHERE
    family_id = @fam1
    AND email = 'mateo.rivera@demo.com'
LIMIT 1;

SELECT id INTO @maria_g
FROM members
WHERE
    family_id = @fam1
    AND email = 'maria.gomez@demo.com'
LIMIT 1;

SELECT id INTO @jose_r
FROM members
WHERE
    family_id = @fam1
    AND email = 'jose.rivera@demo.com'
LIMIT 1;

-- Lopez
SELECT id INTO @laura
FROM members
WHERE
    family_id = @fam2
    AND email = 'laura.lopez@demo.com'
LIMIT 1;

SELECT id INTO @javier
FROM members
WHERE
    family_id = @fam2
    AND email = 'javier.lopez@demo.com'
LIMIT 1;

SELECT id INTO @nora_l
FROM members
WHERE
    family_id = @fam2
    AND email = 'nora.lopez@demo.com'
LIMIT 1;

SELECT id INTO @hugo_l
FROM members
WHERE
    family_id = @fam2
    AND email = 'hugo.lopez@demo.com'
LIMIT 1;

SELECT id INTO @carmen_l
FROM members
WHERE
    family_id = @fam2
    AND email = 'carmen.lopez@demo.com'
LIMIT 1;

SELECT id INTO @antonio
FROM members
WHERE
    family_id = @fam2
    AND email = 'antonio.lopez@demo.com'
LIMIT 1;

-- Sanchez
SELECT id INTO @patricia
FROM members
WHERE
    family_id = @fam3
    AND email = 'patricia.sanchez@demo.com'
LIMIT 1;

SELECT id INTO @ruben
FROM members
WHERE
    family_id = @fam3
    AND email = 'ruben.sanchez@demo.com'
LIMIT 1;

SELECT id INTO @irene_s
FROM members
WHERE
    family_id = @fam3
    AND email = 'irene.sanchez@demo.com'
LIMIT 1;

SELECT id INTO @leo_s
FROM members
WHERE
    family_id = @fam3
    AND email = 'leo.sanchez@demo.com'
LIMIT 1;

SELECT id INTO @pilar_s
FROM members
WHERE
    family_id = @fam3
    AND email = 'pilar.sanchez@demo.com'
LIMIT 1;

SELECT id INTO @manuel_s
FROM members
WHERE
    family_id = @fam3
    AND email = 'manuel.sanchez@demo.com'
LIMIT 1;

-- Martin
SELECT id INTO @elena
FROM members
WHERE
    family_id = @fam4
    AND email = 'elena.martin@demo.com'
LIMIT 1;

SELECT id INTO @sergio
FROM members
WHERE
    family_id = @fam4
    AND email = 'sergio.martin@demo.com'
LIMIT 1;

SELECT id INTO @claudia
FROM members
WHERE
    family_id = @fam4
    AND email = 'claudia.martin@demo.com'
LIMIT 1;

SELECT id INTO @bruno
FROM members
WHERE
    family_id = @fam4
    AND email = 'bruno.martin@demo.com'
LIMIT 1;

SELECT id INTO @rosa_m
FROM members
WHERE
    family_id = @fam4
    AND email = 'rosa.martin@demo.com'
LIMIT 1;

SELECT id INTO @fran_m
FROM members
WHERE
    family_id = @fam4
    AND email = 'francisco.martin@demo.com'
LIMIT 1;

-- Fernandez
SELECT id INTO @noelia
FROM members
WHERE
    family_id = @fam5
    AND email = 'noelia.fernandez@demo.com'
LIMIT 1;

SELECT id INTO @ivan_f
FROM members
WHERE
    family_id = @fam5
    AND email = 'ivan.fernandez@demo.com'
LIMIT 1;

SELECT id INTO @aitana
FROM members
WHERE
    family_id = @fam5
    AND email = 'aitana.fernandez@demo.com'
LIMIT 1;

SELECT id INTO @enzo_f
FROM members
WHERE
    family_id = @fam5
    AND email = 'enzo.fernandez@demo.com'
LIMIT 1;

SELECT id INTO @amaya
FROM members
WHERE
    family_id = @fam5
    AND email = 'amaya.fernandez@demo.com'
LIMIT 1;

SELECT id INTO @inaki
FROM members
WHERE
    family_id = @fam5
    AND email = 'inaki.fernandez@demo.com'
LIMIT 1;

-- =====================================================
-- INSERT EVENTS (8 por familia aprox)
-- member_id puede ser NULL para eventos “familia general”
-- =====================================================

-- ---------- Rivera ----------
INSERT INTO
    events (
        family_id,
        member_id,
        title,
        description,
        location,
        type,
        start_at,
        end_at
    )
VALUES (
        @fam1,
        NULL,
        'Plan semanal familiar',
        'Revisar agenda de la semana y repartir tareas.',
        'Casa',
        'family',
        '2026-02-02 20:30:00',
        '2026-02-02 21:15:00'
    ),
    (
        @fam1,
        @lucia_r,
        'Reunion con tutora (Lucia)',
        'Seguimiento del trimestre.',
        'Colegio',
        'school',
        '2026-02-05 16:30:00',
        '2026-02-05 17:00:00'
    ),
    (
        @fam1,
        @mateo_r,
        'Futbol - entrenamiento',
        'Llevar botella de agua.',
        'Polideportivo',
        'activity',
        '2026-02-06 18:00:00',
        '2026-02-06 19:15:00'
    ),
    (
        @fam1,
        @ana,
        'Revision dental (Ana)',
        'Limpieza anual.',
        'Clinica Dental Sol',
        'medical',
        '2026-02-10 09:30:00',
        '2026-02-10 10:15:00'
    ),
    (
        @fam1,
        @carlos,
        'ITV coche (Carlos)',
        'Llevar papeles del seguro.',
        'ITV Vallecas',
        'errand',
        '2026-02-12 08:30:00',
        '2026-02-12 09:30:00'
    ),
    (
        @fam1,
        @jose_r,
        'Comida con abuelo Jose',
        'Comida en familia.',
        'Restaurante Centro',
        'family',
        '2026-02-15 14:00:00',
        '2026-02-15 16:00:00'
    ),
    (
        @fam1,
        NULL,
        'Cumple de Ana',
        'Tarta y cena con familia.',
        'Casa',
        'birthday',
        '2026-04-12 19:30:00',
        '2026-04-12 22:30:00'
    ),
    (
        @fam1,
        @maria_g,
        'Control tension (Maria)',
        'Llevar registro de medicacion.',
        'Centro de Salud',
        'medical',
        '2026-02-20 11:00:00',
        '2026-02-20 11:30:00'
    );

-- ---------- Lopez ----------
INSERT INTO
    events (
        family_id,
        member_id,
        title,
        description,
        location,
        type,
        start_at,
        end_at
    )
VALUES (
        @fam2,
        NULL,
        'Plan familiar mensual',
        'Revisar eventos del mes.',
        'Casa',
        'family',
        '2026-02-01 20:00:00',
        '2026-02-01 20:45:00'
    ),
    (
        @fam2,
        @nora_l,
        'Pediatra (Nora)',
        'Revision general.',
        'CAP Eixample',
        'medical',
        '2026-02-04 10:20:00',
        '2026-02-04 11:00:00'
    ),
    (
        @fam2,
        @hugo_l,
        'Guarderia - festival',
        'Actuacion de canciones.',
        'Guarderia',
        'school',
        '2026-02-07 11:00:00',
        '2026-02-07 12:00:00'
    ),
    (
        @fam2,
        @laura,
        'Clase de pilates',
        'Traer esterilla.',
        'Studio Pilates',
        'activity',
        '2026-02-09 19:00:00',
        '2026-02-09 20:00:00'
    ),
    (
        @fam2,
        @javier,
        'Partido padel',
        'Reservado pista 3.',
        'Club Padel BCN',
        'activity',
        '2026-02-11 21:00:00',
        '2026-02-11 22:30:00'
    ),
    (
        @fam2,
        @antonio,
        'Revision oftalmologo (Antonio)',
        'Control de graduacion.',
        'Clinica Ocular',
        'medical',
        '2026-02-18 12:10:00',
        '2026-02-18 12:40:00'
    ),
    (
        @fam2,
        NULL,
        'Cumple de Laura',
        'Cena familiar.',
        'Casa',
        'birthday',
        '2026-10-05 20:30:00',
        '2026-10-05 23:00:00'
    ),
    (
        @fam2,
        @carmen_l,
        'Clase de baile (Carmen)',
        'Zumba suave.',
        'Centro Civico',
        'activity',
        '2026-02-22 18:00:00',
        '2026-02-22 19:00:00'
    );

-- ---------- Sanchez ----------
INSERT INTO
    events (
        family_id,
        member_id,
        title,
        description,
        location,
        type,
        start_at,
        end_at
    )
VALUES (
        @fam3,
        NULL,
        'Cena familiar',
        'Cena tranquila sin pantallas.',
        'Casa',
        'family',
        '2026-02-03 20:45:00',
        '2026-02-03 22:00:00'
    ),
    (
        @fam3,
        @irene_s,
        'Patinaje - entrenamiento',
        'Llevar protecciones.',
        'Pista Norte',
        'activity',
        '2026-02-06 17:30:00',
        '2026-02-06 18:30:00'
    ),
    (
        @fam3,
        @leo_s,
        'Excursion cole (Leo)',
        'Mochila pequeña + agua.',
        'Parque Natural',
        'school',
        '2026-02-09 09:00:00',
        '2026-02-09 13:30:00'
    ),
    (
        @fam3,
        @patricia,
        'Revision ginecologa (Patricia)',
        'Chequeo anual.',
        'Clinica Central',
        'medical',
        '2026-02-12 08:50:00',
        '2026-02-12 09:30:00'
    ),
    (
        @fam3,
        @ruben,
        'Revision coche - taller',
        'Cambio de aceite.',
        'Taller R&R',
        'errand',
        '2026-02-13 18:00:00',
        '2026-02-13 19:00:00'
    ),
    (
        @fam3,
        @pilar_s,
        'Comida con abuela Pilar',
        'Paella en casa de Pilar.',
        'Casa Pilar',
        'family',
        '2026-02-16 14:30:00',
        '2026-02-16 17:00:00'
    ),
    (
        @fam3,
        NULL,
        'Cumple de Ruben',
        'Sorpresa y tarta.',
        'Casa',
        'birthday',
        '2026-01-11 19:00:00',
        '2026-01-11 22:00:00'
    ),
    (
        @fam3,
        @manuel_s,
        'Cita medico (Manuel)',
        'Revisar analitica.',
        'Centro de Salud',
        'medical',
        '2026-02-25 10:00:00',
        '2026-02-25 10:25:00'
    );

-- ---------- Martin ----------
INSERT INTO
    events (
        family_id,
        member_id,
        title,
        description,
        location,
        type,
        start_at,
        end_at
    )
VALUES (
        @fam4,
        NULL,
        'Organizar semana',
        'Reparto de tareas y compras.',
        'Casa',
        'family',
        '2026-02-02 21:00:00',
        '2026-02-02 21:30:00'
    ),
    (
        @fam4,
        @claudia,
        'Baile - clase',
        'Llevar zapatillas.',
        'Academia Danza',
        'activity',
        '2026-02-04 18:00:00',
        '2026-02-04 19:00:00'
    ),
    (
        @fam4,
        @bruno,
        'Vacuna (Bruno)',
        'Cartilla de vacunas.',
        'Centro de Salud',
        'medical',
        '2026-02-05 09:10:00',
        '2026-02-05 09:40:00'
    ),
    (
        @fam4,
        @elena,
        'Reunion trabajo (Elena)',
        'Reunion de proyecto.',
        'Oficina',
        'work',
        '2026-02-10 11:00:00',
        '2026-02-10 12:00:00'
    ),
    (
        @fam4,
        @sergio,
        'Gimnasio',
        'Entreno de fuerza.',
        'Gym Sur',
        'activity',
        '2026-02-12 20:00:00',
        '2026-02-12 21:15:00'
    ),
    (
        @fam4,
        @fran_m,
        'Visita medico (Francisco)',
        'Control de rutina.',
        'Clinica',
        'medical',
        '2026-02-17 13:20:00',
        '2026-02-17 13:45:00'
    ),
    (
        @fam4,
        NULL,
        'Cumple de Elena',
        'Cena especial.',
        'Casa',
        'birthday',
        '2026-07-13 20:30:00',
        '2026-07-13 23:00:00'
    ),
    (
        @fam4,
        @rosa_m,
        'Taller jardineria (Rosa)',
        'Traer guantes.',
        'Centro Civico',
        'activity',
        '2026-02-21 10:00:00',
        '2026-02-21 11:30:00'
    );

-- ---------- Fernandez ----------
INSERT INTO
    events (
        family_id,
        member_id,
        title,
        description,
        location,
        type,
        start_at,
        end_at
    )
VALUES (
        @fam5,
        NULL,
        'Menu semanal',
        'Planificar comidas y lista de compra.',
        'Casa',
        'family',
        '2026-02-01 19:30:00',
        '2026-02-01 20:00:00'
    ),
    (
        @fam5,
        @aitana,
        'Clase de piano (Aitana)',
        'Practicar escala do mayor.',
        'Conservatorio',
        'activity',
        '2026-02-03 17:00:00',
        '2026-02-03 18:00:00'
    ),
    (
        @fam5,
        @enzo_f,
        'Futbol - partido',
        'Llevar equipacion completa.',
        'Campo Municipal',
        'activity',
        '2026-02-07 10:30:00',
        '2026-02-07 11:45:00'
    ),
    (
        @fam5,
        @noelia,
        'Revision medica (Noelia)',
        'Analitica anual.',
        'Clinica Norte',
        'medical',
        '2026-02-09 08:15:00',
        '2026-02-09 09:00:00'
    ),
    (
        @fam5,
        @ivan_f,
        'Cita banco (Ivan)',
        'Hipoteca / revision condiciones.',
        'Banco Centro',
        'errand',
        '2026-02-12 16:00:00',
        '2026-02-12 16:45:00'
    ),
    (
        @fam5,
        @amaya,
        'Centro mayores (Amaya)',
        'Actividad de pintura.',
        'Centro Mayores',
        'activity',
        '2026-02-18 11:00:00',
        '2026-02-18 12:30:00'
    ),
    (
        @fam5,
        NULL,
        'Cumple de Ivan',
        'Cena familiar.',
        'Casa',
        'birthday',
        '2026-04-01 20:30:00',
        '2026-04-01 23:00:00'
    ),
    (
        @fam5,
        @inaki,
        'Consulta cardiologia (Inaki)',
        'Llevar resultados previos.',
        'Hospital',
        'medical',
        '2026-02-26 09:40:00',
        '2026-02-26 10:20:00'
    );

COMMIT;