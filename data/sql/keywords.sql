DROP TABLE IF EXISTS Keywords;

CREATE TABLE Keywords (
   id SERIAL CONSTRAINT PK_Keywords_id PRIMARY KEY,
   word TEXT UNIQUE NOT NULL
);

INSERT INTO Keywords
   (word)
VALUES
   ('Mexican'),
   ('Food'),
   ('FastFood'),
   ('Sandwiches'),
   ('Sandwich'),
   ('Chinese'),
   ('Pizza'),
   ('Burgers'),
   ('Burger'),
   ('Vietnamese'),
   ('American'),
   ('Nightlife'),
   ('Bar'),
   ('Japanese'),
   ('Cafe'),
   ('Indian'),
   ('Deli'),
   ('Italian'),
   ('Sushi'),
   ('Seafood'),
   ('Barbeque'),
   ('Coffee'),
   ('Tea'),
   ('Asian'),
   ('Salad'),
   ('ChickenWings'),
   ('Korean'),
   ('Mediterranean')
;

CREATE INDEX IX_Keywords_word_id ON Keywords (word, id);

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ml242;
