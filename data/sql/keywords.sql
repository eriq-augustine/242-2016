DROP TABLE IF EXISTS Keywords;

CREATE TABLE Keywords (
   id SERIAL CONSTRAINT PK_Keywords_id PRIMARY KEY,
   word TEXT UNIQUE NOT NULL
);

INSERT INTO Keywords
   (word)
VALUES
   ('mexican'),
   ('fastfood'),
   ('sandwiches'),
   ('sandwich'),
   ('chinese'),
   ('pizza'),
   ('burgers'),
   ('burger'),
   ('vietnamese'),
   ('american'),
   ('nightlife'),
   ('bar'),
   ('japanese'),
   ('cafe'),
   ('indian'),
   ('deli'),
   ('italian'),
   ('sushi'),
   ('seafood'),
   ('barbeque'),
   ('coffee'),
   ('tea'),
   ('asian'),
   ('salad'),
   ('chickenwings'),
   ('korean'),
   ('mediterranean')
;

CREATE INDEX IX_Keywords_word_id ON Keywords (word, id);

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ml242;
