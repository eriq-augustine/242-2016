-- Link with surrogate keys, drop old keys, build indexes.

-- Link surrogate keys.

UPDATE Photos P
SET businessId = B.id
FROM Businesses B
WHERE B.yelpId = P.businessYelpId
;

UPDATE UserEliteYears UE
SET userId = U.id
FROM Users U
WHERE U.yelpId = UE.userYelpId
;

UPDATE Tips T
SET
   userId = U.id,
   businessId = B.id
FROM
   Users U,
   Businesses B
WHERE
   U.yelpId = T.userYelpId
   AND B.yelpId = T.businessYelpId
;

UPDATE Reviews R
SET
   userId = U.id,
   businessId = B.id
FROM
   Users U,
   Businesses B
WHERE
   U.yelpId = R.userYelpId
   AND B.yelpId = R.businessYelpId
;

UPDATE Friendships F
SET
   sourceUser = SU.id,
   targetUser = TU.id
FROM
   Users SU,
   Users TU
WHERE
   SU.yelpId = F.sourceUserYelpId
   AND TU.yelpId = F.targetUserYelpId
;

UPDATE CheckIns C
SET businessId = B.id
FROM Businesses B
WHERE B.yelpId = C.businessYelpId
;

UPDATE BusinessNeighborhoods BN
SET businessId = B.id
FROM Businesses B
WHERE B.yelpId = BN.businessYelpId
;

UPDATE BusinessHours BH
SET businessId = B.id
FROM Businesses B
WHERE B.yelpId = BH.businessYelpId
;

UPDATE BusinessCategories BC
SET businessId = B.id
FROM Businesses B
WHERE B.yelpId = BC.businessYelpId
;

UPDATE BusinessAttributes BA
SET businessId = B.id
FROM Businesses B
WHERE B.yelpId = BA.businessYelpId
;

-- Drop redundant Yelp keys

ALTER TABLE Photos
DROP COLUMN businessYelpId
;

ALTER TABLE UserEliteYears
DROP COLUMN userYelpId
;

ALTER TABLE Tips
DROP COLUMN businessYelpId,
DROP COLUMN userYelpId
;

ALTER TABLE Reviews
DROP COLUMN businessYelpId,
DROP COLUMN userYelpId
;

ALTER TABLE Friendships
DROP COLUMN sourceUserYelpId,
DROP COLUMN targetUserYelpId
;

ALTER TABLE CheckIns
DROP COLUMN businessYelpId
;

ALTER TABLE BusinessNeighborhoods
DROP COLUMN businessYelpId
;

ALTER TABLE BusinessHours
DROP COLUMN businessYelpId
;

ALTER TABLE BusinessCategories
DROP COLUMN businessYelpId
;

ALTER TABLE BusinessAttributes
DROP COLUMN businessYelpId
;

-- Support tables

DROP TABLE IF EXISTS BusinessAttributesAggregate;
CREATE TABLE BusinessAttributesAggregate (
   id SERIAL CONSTRAINT PK_BusinessAttributesAggregate_id PRIMARY KEY,
   businessId INT REFERENCES Businesses,
   value TEXT NOT NULL
);

INSERT INTO BusinessAttributesAggregate
   (businessId, value)
SELECT
   businessId,
   STRING_AGG(CONCAT(name, '::', value), ';;') AS attributes
FROM BusinessAttributes
GROUP BY businessId
;

DROP TABLE IF EXISTS BusinessCategoriesAggregate;
CREATE TABLE BusinessCategoriesAggregate (
   id SERIAL CONSTRAINT PK_BusinessCategoriesAggregate_id PRIMARY KEY,
   businessId INT REFERENCES Businesses,
   value TEXT NOT NULL
);

INSERT INTO BusinessCategoriesAggregate
   (businessId, value)
SELECT
   businessId,
   STRING_AGG(name, ';;') AS categories
FROM BusinessCategories
GROUP BY businessId
;

DROP TABLE IF EXISTS ReviewWords;
CREATE TABLE ReviewWords (
   id SERIAL CONSTRAINT PK_ReviewWords_id PRIMARY KEY,
   businessId INT REFERENCES Businesses,
   reviewId INT REFERENCES Reviews,
   word TEXT NOT NULL,
   wordCount INT NOT NULL
);

INSERT INTO ReviewWords
   (businessId, reviewId, word, wordCount)
SELECT
  X.businessId,
  X.reviewId,
  X.word,
  X.wordCount
FROM (
      SELECT
        businessId,
        id AS reviewId,
        LOWER(REGEXP_REPLACE(
          REGEXP_SPLIT_TO_TABLE(text, E'\\s+'),
          E'\\W+',
          '',
          'g'
        )) AS word,
        COUNT(*) AS wordCount
      FROM Reviews
      GROUP BY
        businessId,
        id,
        word
) X
WHERE
  X.word IS NOT NULL
  AND X.word <> ''
;

DROP TABLE IF EXISTS ReviewWordsAggregate;
CREATE TABLE ReviewWordsAggregate (
   id SERIAL CONSTRAINT PK_ReviewWordsAggregate_id PRIMARY KEY,
   businessId INT REFERENCES Businesses,
   word TEXT NOT NULL,
   wordCount INT NOT NULL
);

INSERT INTO ReviewWordsAggregate
   (businessId, word, wordCount)
SELECT
  businessId,
  word,
  SUM(wordCount)
FROM ReviewWords
GROUP BY
   businessId,
   word
;

DROP TABLE IF EXISTS ReviewStats;
CREATE TABLE ReviewStats (
   id SERIAL CONSTRAINT PK_ReviewStats_id PRIMARY KEY,
   businessId INT REFERENCES Businesses,
   meanReviewLen FLOAT NOT NULL,
   availableReviewCount INT NOT NULL
);

INSERT INTO ReviewStats
   (businessId, meanReviewLen, availableReviewCount)
SELECT
   businessId,
   AVG(CHAR_LENGTH(REGEXP_REPLACE(text, E'\\s+', '', 'g'))) AS meanReviewLen,
   COUNT(*) AS availableReviewCount
FROM Reviews
GROUP BY businessId
;

DROP TABLE IF EXISTS ReviewSpecialWords;
CREATE TABLE ReviewSpecialWords (
   id SERIAL CONSTRAINT PK_ReviewTopWords_id PRIMARY KEY,
   businessId INT REFERENCES Businesses,
   topWords TEXT,
   keyWords TEXT
);

INSERT INTO ReviewSpecialWords
   (businessId, topWords, keyWords)
SELECT
   COALESCE(T.businessId, K.businessId),
   T.topWords,
   K.keyWords
FROM
   (
      SELECT
         businessId,
         STRING_AGG(X.word, ';;') AS topWords
      FROM (
         SELECT
            W.businessId,
            W.word,
            ROW_NUMBER() OVER (PARTITION BY W.businessId ORDER BY W.wordCount DESC) AS wordRank
         FROM
            ReviewWordsAggregate W
            LEFT JOIN Stopwords S ON S.word = W.word
         WHERE
            S.word IS NULL
            AND CHAR_LENGTH(W.word) >= 4
      ) X
      WHERE X.wordRank <= 10
      GROUP BY X.businessId
   ) T
   FULL OUTER JOIN (
      SELECT
         W.businessId,
         STRING_AGG(K.word, ';;') AS keyWords
      FROM
         ReviewWordsAggregate W
         JOIN Keywords K ON W.word = K.word
      GROUP BY W.businessId
   ) K ON K.businessId = T.businessId
;

-- Indexes

-- Key up the foreign keys.
CREATE INDEX IX_Photos_businessId ON Photos (businessId);
CREATE INDEX IX_UserEliteYears_userId ON UserEliteYears (userId);
CREATE INDEX IX_Tips_businessId_userId ON Tips (businessId, userId);
CREATE INDEX IX_Reviews_businessId_userId ON Reviews (businessId, userId);
CREATE INDEX IX_Friendships_sourceUser_targetUser ON Friendships (sourceUser, targetUser);
CREATE INDEX IX_CheckIns_businessId ON CheckIns (businessId);
CREATE INDEX IX_BusinessNeighborhoods_businessId ON BusinessNeighborhoods (businessId);
CREATE INDEX IX_BusinessHours_businessId ON BusinessHours (businessId);
CREATE INDEX IX_BusinessAttributes_businessId ON BusinessAttributes (businessId);
CREATE INDEX IX_BusinessCategories_businessId ON BusinessCategories (businessId);

-- Supports
CREATE INDEX IX_BusinessAttributesAggregate_businessId ON BusinessAttributesAggregate (businessId, value);
CREATE INDEX IX_BusinessCategoriesAggregate_businessId ON BusinessCategoriesAggregate (businessId, value);
CREATE INDEX IX_ReviewWords_businessId ON ReviewWords (businessId);
CREATE INDEX IX_ReviewWordsAggregate_businessId ON ReviewWordsAggregate (businessId);
CREATE INDEX IX_ReviewStats_businessId ON ReviewStats (businessId, meanReviewLen, availableReviewCount);
CREATE INDEX IX_ReviewSpecialWords_businessId_topWords_keyWords ON ReviewSpecialWords (businessId, topWords, keyWords);

-- Performance indexes.
CREATE INDEX IX_BusinessCategories_name_businessId ON BusinessCategories (name, businessId);
CREATE INDEX IX_ReviewWords_word_wordCount_businessId ON ReviewWords (word, wordCount, businessId);
CREATE INDEX IX_ReviewWordsAggregate_word_wordCount_businessId ON ReviewWordsAggregate (word, wordCount, businessId);
CREATE INDEX IX_BusinessHours_open_close_businessId ON BusinessHours (open, close, businessId);

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ml242;
