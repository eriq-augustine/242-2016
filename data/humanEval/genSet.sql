-- Ground Truth, one from each city.

SELECT id
FROM (
   SELECT
      B.id,
      ROW_NUMBER() OVER (PARTITION BY G.label, B.city ORDER BY B.reviewCount DESC) AS rank
   FROM
      Businesses B
      JOIN GroundTruth G ON G.businessId = B.id
   WHERE B.city IN ('Las Vegas', 'Phoenix')
) X
WHERE X.rank = 1

UNION

-- 68 Non-Ground Randoms (34 from each city)
SELECT id
FROM (
   SELECT B.id
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
      B.city = 'Las Vegas'
      AND NOT EXISTS (SELECT * FROM GroundTruth G WHERE G.businessId = B.id)
      AND B.reviewCount >= 50
   ORDER BY RANDOM()
   LIMIT 34
) X

UNION

SELECT id
FROM (
   SELECT B.id
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
      B.city = 'Phoenix'
      AND NOT EXISTS (SELECT * FROM GroundTruth G WHERE G.businessId = B.id)
      AND B.reviewCount >= 50
   ORDER BY RANDOM()
   LIMIT 34
) X

;
