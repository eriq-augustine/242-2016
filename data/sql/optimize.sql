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
CREATE INDEX IX_BusinessCategories_businessId ON BusinessCategories (businessId);
CREATE INDEX IX_BusinessAttributes_businessId ON BusinessAttributes (businessId);
