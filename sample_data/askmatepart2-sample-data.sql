--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

ALTER TABLE IF EXISTS ONLY public.question DROP CONSTRAINT IF EXISTS pk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS pk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS pk_comment_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS pk_question_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.tag DROP CONSTRAINT IF EXISTS pk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_tag_id CASCADE;

DROP TABLE IF EXISTS public.question;
CREATE TABLE question (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    view_number integer,
    vote_number integer,
    title text,
    message text,
    image text,
    user_id integer
);

DROP TABLE IF EXISTS public.answer;
CREATE TABLE answer (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    vote_number integer,
    question_id integer,
    message text,
    image text,
    user_id integer
);

DROP TABLE IF EXISTS public.comment;
CREATE TABLE comment (
    id serial NOT NULL,
    question_id integer,
    answer_id integer,
    message text,
    submission_time timestamp without time zone,
    edited_count integer,
    user_id integer
);


DROP TABLE IF EXISTS public.question_tag;
CREATE TABLE question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);

DROP TABLE IF EXISTS public.tag;
CREATE TABLE tag (
    id serial NOT NULL,
    name text
);

DROP TABLE IF EXISTS public.users;
CREATE TABLE public.users (
    id serial NOT NULL,
    user_name text,
    password text,
    email text
);

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pk_id PRIMARY KEY (id);

ALTER TABLE ONLY answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);

ALTER TABLE ONLY question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);

ALTER TABLE ONLY tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);

ALTER TABLE ONLY answer
    ADD CONSTRAINT answer___fk_user_id FOREIGN KEY (user_id) REFERENCES users(id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id);

ALTER TABLE ONLY question
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES answer(id);

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES tag(id);

ALTER TABLE answer
	ADD accepted BOOL DEFAULT FALSE;

INSERT INTO question VALUES (0, '2021-04-29 09:19:00', 32, 0, 'How to treat toenail fungus?', 'I''m looking for natural solutions!', 'toenail_fungus.jpeg');
INSERT INTO question VALUES (1, '2021-05-09 21:24:00', 26, 2, 'I have acne, help!', 'I''ve been struggling with acne since my teens. I tried all the creams but nothing seems to help!', 'acne.jpeg');
INSERT INTO question VALUES (2, '2021-05-12 18:04:04', 36, 2, 'How to treat warts?', 'I developed warts after swimming in a public pool. They cover the sole of my foot. :(', 'warts.jpeg');
INSERT INTO question VALUES (3, '2021-05-21 12:01:34', 16, 4, 'I might have intestinal parasites?', 'I think something is moving inside of me, help!!!', 'tummyache.jpg');
SELECT pg_catalog.setval('question_id_seq', 2, true);

INSERT INTO answer VALUES (0, '2021-06-01 09:19:00', 1, 0, 'I swear by Vicks VapoRub! I applied a small amount to the affected area at least once a day. It worked wonders.', 'wick.jpeg');
INSERT INTO answer VALUES (1, '2021-06-02 10:19:00', 0, 0, 'Snakeroot extract worked for me. A 2008 study showed that snakeroot extract is as effective against toenail fungus as the prescription antifungal medicine ciclopirox. Apply it to the affected area every third day for the first month, twice a week for the second month, and once a week for the third month.', 'snakeroot.jpg');
INSERT INTO answer VALUES (2, '2021-06-03 11:19:00', 1, 0, 'Try tea tree oil. Paint the tea tree oil directly onto the affected nail twice daily with a cotton swab.', 'teatreeoil.jpeg');
INSERT INTO answer VALUES (3, '2021-06-04 12:19:00', 0, 0, 'Oregano oil contains thymol. According to a 2016 review, thymol has antifungal and antibacterial properties. Treatment: apply oregano oil to the nail twice daily with a cotton swab.', 'oreganooil.jpeg');
INSERT INTO answer VALUES (4, '2021-06-05 13:19:00', 2, 0, 'My aunt used vinegar for her toenail fungus. She soaked her foot in one part vinegar to two parts warm water for 20 minutes daily and it worked for her.', 'vinegar.jpg');
INSERT INTO answer VALUES (5, '2021-06-06 09:19:00', -2, 1, 'Try antibiotics, talk with a dermatologist.', NULL);
INSERT INTO answer VALUES (6, '2021-06-06 10:19:00', 10, 1, 'DO NOT use antibiotics! It will ruin your gut flora. Talk with a holistic practitioner and heal your gut and gut flora. It will cure your acne.', NULL);
INSERT INTO answer VALUES (7, '2021-06-06 11:19:00', 100, 1, 'Look for food allergens, do an elimination diet. For many people eating common allergens like dairy, soy or gluten causes their acne problems.', NULL);
INSERT INTO answer VALUES (8, '2021-06-06 12:19:00', -1, 2, 'Stop going to swim!', NULL);
INSERT INTO answer VALUES (9, '2021-06-06 13:19:00', 15, 2, 'Fürgyé'' le!', NULL);
INSERT INTO answer VALUES (10, '2021-06-06 14:19:00', 1, 2, 'Better see a dermatologist.', NULL);
INSERT INTO answer VALUES (11, '2021-06-06 15:19:00', 17, 2, 'Duct tape is one of the most popular home remedies for warts. It''s inexpensive and easy to find. Duct tape is said to remove the infected skin over time.', 'ducttape.jpeg');
INSERT INTO answer VALUES (12, '2021-06-06 16:19:00', 0, 3, 'Call the ambulance!', 'gyorfipal.jpg');
INSERT INTO answer VALUES (13, '2021-06-06 17:19:00', 1, 3, 'Take some laxatives. Maybe see a doctor?', 'toilet.jpeg');
SELECT pg_catalog.setval('answer_id_seq', 2, true);

INSERT INTO comment VALUES (0, 0, NULL, 'Please, upload a picture with a better resolution!', '2021-06-07 05:49:00');
INSERT INTO comment VALUES (1, NULL, 1, 'I''m afraid of snakes! :OOO', '2021-06-07 16:55:00');
SELECT pg_catalog.setval('comment_id_seq', 2, true);

INSERT INTO tag VALUES (1, 'python');
INSERT INTO tag VALUES (2, 'health');
INSERT INTO tag VALUES (3, 'skin');
SELECT pg_catalog.setval('tag_id_seq', 3, true);

INSERT INTO question_tag VALUES (0, 1);
INSERT INTO question_tag VALUES (1, 3);
INSERT INTO question_tag VALUES (2, 3);
