DROP TABLE IF EXISTS HumanEval;

CREATE TABLE HumanEval (
   id SERIAL CONSTRAINT PK_HumanEval_id PRIMARY KEY,
   businessId INT REFERENCES Businesses,
   businessYelpId TEXT -- Will be dropped after the surogate key is populated.
);

INSERT INTO HumanEval
   (businessYelpId)
-- Ground Truth, one from each city.
SELECT yelpId
FROM (
   SELECT
      B.yelpId,
      ROW_NUMBER() OVER (PARTITION BY G.label, B.city ORDER BY B.reviewCount DESC) AS rank
   FROM
      Businesses B
      JOIN GroundTruth G ON G.businessId = B.id
   WHERE
      B.active = true
      AND B.city IN ('Las Vegas', 'Phoenix')
) X
WHERE X.rank = 1

UNION

-- 68 Non-Ground Randoms (34 from each city)
SELECT yelpId
FROM (
   SELECT B.yelpId
   FROM
      Businesses B
      JOIN (
         SELECT DISTINCT businessId
         FROM BusinessCategories BC
         WHERE name IN (
             'Restaurants', 'Food', 'Fast Food', 'Pizza', 'Mexican',
             'Sandwiches', 'American (Traditional)', 'Burgers', 'Italian',
             'Chinese', 'American (New)', 'Breakfast & Brunch', 'Cafes'
         )
      ) Restaurants ON Restaurants.businessId = B.id
   WHERE
      B.active = true
      AND B.city = 'Las Vegas'
      AND NOT EXISTS (SELECT * FROM GroundTruth G WHERE G.businessId = B.id)
      AND B.reviewCount >= 50
   ORDER BY RANDOM()
   LIMIT 34
) X

UNION

SELECT yelpId
FROM (
   SELECT B.yelpId
   FROM
      Businesses B
      JOIN (
         SELECT DISTINCT businessId
         FROM BusinessCategories BC
         WHERE name IN (
             'Restaurants', 'Food', 'Fast Food', 'Pizza', 'Mexican',
             'Sandwiches', 'American (Traditional)', 'Burgers', 'Italian',
             'Chinese', 'American (New)', 'Breakfast & Brunch', 'Cafes'
         )
      ) Restaurants ON Restaurants.businessId = B.id
   WHERE
      B.active = true
      AND B.city = 'Phoenix'
      AND NOT EXISTS (SELECT * FROM GroundTruth G WHERE G.businessId = B.id)
      AND B.reviewCount >= 50
   ORDER BY RANDOM()
   LIMIT 34
) X
;

-- Link up surrogate keys
UPDATE HumanEval H
SET businessId = B.id
FROM Businesses B
WHERE B.yelpId = H.businessYelpId
;

ALTER TABLE HumanEval
DROP COLUMN businessYelpId
;

CREATE INDEX IX_HumanEval_businessId ON HumanEval (businessId);

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ml242;

SELECT
   B.yelpId
FROM
   Businesses B
   JOIN HumanEval HE ON HE.businessId = B.id
