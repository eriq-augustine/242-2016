DROP TABLE IF EXISTS BusinessAttributes;
DROP TABLE IF EXISTS BusinessCategories;
DROP TABLE IF EXISTS BusinessHours;
DROP TABLE IF EXISTS BusinessNeighborhoods;
DROP TABLE IF EXISTS CheckIns;
DROP TABLE IF EXISTS Friendships;
DROP TABLE IF EXISTS Reviews;
DROP TABLE IF EXISTS Tips;
DROP TABLE IF EXISTS UserEliteYears;

DROP TABLE IF EXISTS Photos;
DROP TABLE IF EXISTS Businesses;
DROP TABLE IF EXISTS Users;

--

CREATE TABLE Users (
   id SERIAL CONSTRAINT PK_Users_id PRIMARY KEY,
   yelpId TEXT NOT NULL UNIQUE,
   firstName TEXT,
   reviewCount INT, -- Total number of reviews?
   averageStars DECIMAL(3, 2), -- Among sample reviews?
   votesFunny INT,
   votesUseful INT,
   votesCool INT,
   yelpingSinceYear INT,
   yelpingSinceMonth INT,
   fans INT NOT NULL DEFAULT 0,
   complimentCool INT NOT NULL DEFAULT 0,
   complimentCute INT NOT NULL DEFAULT 0,
   complimentFunny INT NOT NULL DEFAULT 0,
   complimentHot INT NOT NULL DEFAULT 0,
   complimentList INT NOT NULL DEFAULT 0,
   complimentMore INT NOT NULL DEFAULT 0,
   complimentNote INT NOT NULL DEFAULT 0,
   complimentPhotos INT NOT NULL DEFAULT 0,
   complimentPlain INT NOT NULL DEFAULT 0,
   complimentProfile INT NOT NULL DEFAULT 0,
   complimentWriter INT NOT NULL DEFAULT 0
);

CREATE TABLE Businesses (
   id SERIAL CONSTRAINT PK_Businesses_id PRIMARY KEY,
   yelpId TEXT NOT NULL UNIQUE,
   name TEXT NOT NULL,
   address TEXT,
   city TEXT,
   state TEXT,
   latitude TEXT,
   longitude TEXT,
   stars DECIMAL(2, 1),
   reviewCount INT, -- Total number of reviews?
   active BOOLEAN -- Called "open" in the file desctiption.
);

CREATE TABLE Photos (
   id SERIAL CONSTRAINT PK_Photos_id PRIMARY KEY,
   yelpId TEXT,
   businessId INT REFERENCES Businesses,
   businessYelpId TEXT, -- Will be dropped after the surogate key is populated.
   caption TEXT,
   label TEXT
);

CREATE TABLE UserEliteYears (
   id SERIAL CONSTRAINT PK_UserEliteYears_id PRIMARY KEY,
   userId INT REFERENCES Users,
   userYelpId TEXT, -- Will be dropped after the surogate key is populated.
   year int NOT NULL
);

CREATE TABLE Tips (
   id SERIAL CONSTRAINT PK_Tips_id PRIMARY KEY,
   businessId INT REFERENCES Businesses,
   businessYelpId TEXT, -- Will be dropped after the surogate key is populated.
   userId INT REFERENCES Users,
   userYelpId TEXT, -- Will be dropped after the surogate key is populated.
   text TEXT,
   date DATE,
   likes INT
);

CREATE TABLE Reviews (
   id SERIAL CONSTRAINT PK_Reviews_id PRIMARY KEY,
   yelpId TEXT,
   businessId INT REFERENCES Businesses,
   businessYelpId TEXT, -- Will be dropped after the surogate key is populated.
   userId INT REFERENCES Users,
   userYelpId TEXT, -- Will be dropped after the surogate key is populated.
   stars INT NOT NULL,
   text TEXT,
   date DATE NOT NULL,
   votesFunny INT,
   votesUseful INT,
   votesCool INT
);

CREATE TABLE Friendships (
   id SERIAL CONSTRAINT PK_Friendships_id PRIMARY KEY,
   sourceUser INT REFERENCES Users,
   targetUser INT REFERENCES Users,
   sourceUserYelpId TEXT, -- Will be dropped after sourceUser is populated.
   targetUserYelpId TEXT  -- Will be dropped after targetUser is populated.
);

CREATE TABLE CheckIns (
   id SERIAL CONSTRAINT PK_CheckIns_id PRIMARY KEY,
   businessId INT REFERENCES Businesses,
   businessYelpId TEXT, -- Will be dropped after the surogate key is populated.
   day INT NOT NULL,
   time INT NOT NULL,
   count INT
);

CREATE TABLE BusinessNeighborhoods (
   id SERIAL CONSTRAINT PK_BusinessNeighborhoods_id PRIMARY KEY,
   businessId INT REFERENCES Businesses,
   businessYelpId TEXT, -- Will be dropped after the surogate key is populated.
   name TEXT NOT NULL
);

CREATE TABLE BusinessHours (
   id SERIAL CONSTRAINT PK_BusinessHours_id PRIMARY KEY,
   businessId INT REFERENCES Businesses,
   businessYelpId TEXT, -- Will be dropped after the surogate key is populated.
   day INT, -- Same as CheckIns (0 - Sunday, 1 - Monday, ... etc)
   open INT, -- Minutes from midnight.
   close INT
);

CREATE TABLE BusinessCategories (
   id SERIAL CONSTRAINT PK_BusinessCategories_id PRIMARY KEY,
   businessId INT REFERENCES Businesses,
   businessYelpId TEXT, -- Will be dropped after the surogate key is populated.
   name TEXT NOT NULL
);

CREATE TABLE BusinessAttributes (
   id SERIAL CONSTRAINT PK_BusinessAttributes_id PRIMARY KEY,
   businessId INT REFERENCES Businesses,
   businessYelpId TEXT, -- Will be dropped after the surogate key is populated.
   name TEXT NOT NULL,
   value TEXT NOT NULL
);

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ml242;
