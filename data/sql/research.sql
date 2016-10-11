-- Q: Does Users.review cound match the actual number of reviews in this dataset?
-- A: No.
SELECT
   U.id,
   U.firstName,
   U.reviewCount AS total,
   R.reviewCount AS given
FROM
   Users U
   JOIN (
      SELECT
         userId,
         COUNT(*) AS reviewCount
      FROM Reviews
      GROUP BY userId
   ) R ON R.userId = U.id
WHERE U.reviewCount != R.reviewCount
LIMIT 1
;

-- Q: Are all review users present?
-- A: Yes
SELECT id
FROM Reviews
WHERE userId IS NULL
;

-- Q: Are all review businesses present?
-- A: Yes
SELECT id
FROM Reviews
WHERE businessId IS NULL
;

-- Q: How many photos are there without captions?
-- A: 112947 / 200000
SELECT COUNT(*)
FROM Photos
WHERE caption IS NOT NULL
;

-- Q: What is the label distribution like?
-- A: Even distribution (where present): [menu, inside, outside, drink, food] all 16000.
SELECT
   label,
   COUNT(*)
FROM Photos
GROUP BY label
ORDER BY COUNT(*) DESC
;

-- Q: What is the rough language distribution like?
-- A: EN: 2670679, FR: 11338, DE: 3049
SELECT
   lang,
   COUNT(*)
FROM (
   SELECT
      CASE
         WHEN text ~* '\m(nous|vous|je|alors|avec|fait|faites|très)\M' THEN 'FR'
         WHEN text ~* '\m(ich|jeder|ein)\M' THEN 'DE'
         ELSE 'EN'
      END AS lang
   FROM Reviews
) X
GROUP BY lang
ORDER BY COUNT(*) DESC
;

-- Q: How many businesses are currently active?
-- A: 73211 active, 12690 inactive.
SELECT
   active,
   COUNT(*)
FROM Businesses
GROUP BY active
ORDER BY COUNT(*) DESC
;

-- Q: What is the average review length?
-- A:
/*
  min | max  |         mean         |      stddev
 -----+------+----------------------+------------------
    1 | 5000 | 621.0787820485604451 | 589.135003974604
*/
SELECT
   MIN(len) AS min,
   MAX(len) AS max,
   AVG(len) AS mean,
   STDDEV(len) AS stddev
FROM (
   SELECT CHAR_LENGTH(text) AS len
   FROM Reviews
) X
;
