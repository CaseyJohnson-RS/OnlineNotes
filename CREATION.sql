
CREATE TABLE IF NOT EXISTS public."Users"
(
    id bigserial NOT NULL,
    email character varying(256) NOT NULL,
    nickname character varying(64) DEFAULT 'John Doe',
    password_hash character varying(64) NOT NULL,
    active boolean NOT NULL DEFAULT TRUE,
    role_id smallint NOT NULL DEFAULT 1,
    PRIMARY KEY (id),
    CONSTRAINT "User email must be unique" UNIQUE (email)
);

CREATE TABLE IF NOT EXISTS public."Roles"
(
    id smallserial NOT NULL,
    role_name character varying(16),
    PRIMARY KEY (id),
    CONSTRAINT "Role names must be unique" UNIQUE (role_name)
);

CREATE TABLE IF NOT EXISTS public."Error_messages"
(
    id serial NOT NULL,
    email character varying(256) NOT NULL,
    text character varying(10000),
    PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS public."Reviews"
(
    id serial NOT NULL,
    email character varying(256),
    rating smallint DEFAULT 10,
    text character varying(500),
    PRIMARY KEY (id),
	CONSTRAINT "Rating wrong value" CHECK(rating > 0 AND rating < 11)
);

CREATE TABLE IF NOT EXISTS public."User_note_labels"
(
    user_id bigint,
    label character varying(16),
    PRIMARY KEY (user_id, label)
);

CREATE TABLE IF NOT EXISTS public."Notes"
(
    user_id bigint NOT NULL,
    note_id integer NOT NULL,
    header character varying(128),
    text character varying(20000),
    hex_color character varying(6),
    status smallint NOT NULL DEFAULT 1,
    PRIMARY KEY (user_id, note_id)
);

CREATE TABLE IF NOT EXISTS public."Note_status"
(
    id smallserial,
    title character varying(16) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (title)
);

CREATE TABLE IF NOT EXISTS public."Note_assigned_labels"
(
    user_id bigint,
    note_id integer,
    label character varying(16),
    PRIMARY KEY (user_id, note_id, label)
);


ALTER TABLE IF EXISTS public."Users"
    ADD FOREIGN KEY (role_id)
    REFERENCES public."Roles" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."User_note_labels"
    ADD FOREIGN KEY (user_id)
    REFERENCES public."Users" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."Notes"
    ADD FOREIGN KEY (status)
    REFERENCES public."Note_status" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."Notes"
    ADD FOREIGN KEY (user_id)
    REFERENCES public."Users" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE IF EXISTS public."Note_assigned_labels"
    ADD FOREIGN KEY (user_id, note_id)
    REFERENCES public."Notes" (user_id, note_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE IF EXISTS public."Note_assigned_labels"
    ADD FOREIGN KEY (user_id, label)
    REFERENCES public."User_note_labels" (user_id, label) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;
 
CREATE OR REPLACE FUNCTION set_note_id()
RETURNS TRIGGER AS
$$
BEGIN
IF NEW .note_id IS NULL THEN
	if (SELECT COUNT(*) FROM "Notes" WHERE user_id = NEW .user_id) = 0 THEN
		SELECT 0 INTO NEW .note_id;
	ELSE
		SELECT (SELECT MAX(note_id) FROM "Notes" WHERE user_id = NEW .user_id) + 1 into NEW .note_id;
	END IF;
END IF;
RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_note_id_trigger
BEFORE INSERT ON "Notes"
FOR EACH ROW EXECUTE FUNCTION set_note_id();

CREATE UNIQUE INDEX email_idx ON "Users" (email);

INSERT INTO "Roles" (role_name) VALUES ('user');
INSERT INTO "Roles" (role_name) VALUES ('admin');

INSERT INTO "Note_status" (title) VALUES ('active');
INSERT INTO "Note_status" (title) VALUES ('archived');
INSERT INTO "Note_status" (title) VALUES ('deleted');

