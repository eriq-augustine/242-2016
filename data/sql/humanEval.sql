DROP TABLE IF EXISTS HumanEval;

CREATE TABLE HumanEval (
   id SERIAL CONSTRAINT PK_HumanEval_id PRIMARY KEY,
   businessId INT REFERENCES Businesses,
   businessYelpId TEXT -- Will be dropped after the surogate key is populated.
);

INSERT INTO HumanEval
   (businessYelpId)
VALUES
   ('Vvh2Hd4SsZjEEfKLNKAEWw'),
   ('yQONzVpX-DEpGSuKMIov6A'),
   ('24qSrF_XOrvaHDBy-gLIQg'),
   ('4rySWsfL5enT7t4XuVNJuQ'),
   ('K2_Hmmo5crTYWiT_1sWnfQ'),
   ('jHte0SjUldZeDDZ5py0ZhA'),
   ('_BU867oRCLZnDIRmg7S6Wg'),
   ('1OigyqVxIfE6AGKNGWZjnw'),
   ('hgy8A1Wnqyi4M-HJIFLpyQ'),
   ('EfmR4e1tmjC5_ZQOgfnYrg'),
   ('Cm1jT60fxb1DjwpqjWJ8EA'),
   ('aidjBZ-cLeRmrsAPM6ZkcA'),
   ('tJhh6NDsNIwWMpxlP-0F7g'),
   ('-1bOb2izeJBZjHC7NWxiPA'),
   ('VlfBIVmtmGYkTq1xbdBIDw'),
   ('scr5gHaPC_36GtaCxmJEHA'),
   ('9Y5kXneSwv-l-8TODZWQAQ'),
   ('fm4X0SV2Kofj-57ZfHiZ_A'),
   ('6VaAYF0Pu1O3d-yrQSwk5w'),
   ('YHGpemLe7cbnPSubG-cRRg'),
   ('xjFGpzNg3FJuqpS-_B4ceg'),
   ('JkuXXDySMl5fF0hwmLxNCA'),
   ('Ug97walz3YLxPMrpkktsFg'),
   ('LxxmtHFNZ5S-MyhykoE4Sg'),
   ('nxflzDedizEvyvxqhz1ghw'),
   ('H6CJflwclNpttYrtsBMsVg'),
   ('0_LZEAYsexEZS-OFTjdjNQ'),
   ('IWA1J9m0rzU8AgXRjXJUoQ'),
   ('qyNtVViurIcChc35mfYIEw'),
   ('ar90fbRbQtiyZLtwjwwXUg'),
   ('dPg69r5nLzEmug0OvNfkmQ'),
   ('GN72XbUh61J5wWQyW2oZsQ'),
   ('yXMvhCmUADlaHabo-DiUYw'),
   ('59U8McUEjsRC_7h4ALk12Q'),
   ('DoiIvRASpaPw6z0wveDAJw'),
   ('MnoF8A3UAghzXKSunNSn2Q'),
   ('jOgSvW9VNw0Cw9p8w5A2JQ'),
   ('_ibKsVEx2LMobFd52D0NZg'),
   ('-ftQeUsqwDkExRg6IYrubQ'),
   ('NNGJQF3WeIHzGzweCpZ-VA'),
   ('dzSPa5kkpQIRjMOHvDUF_Q'),
   ('glLo_FNtgQ7OmAR8hUrDqQ'),
   ('XkNQVTkCEzBrq7OlRHI11Q'),
   ('DcrM4hwDcU2G6vuh2cnaYQ'),
   ('4sW8Z6NLXLRkruSKSKUEUw'),
   ('r6UzCUbllqkkc9BSV7Vodg'),
   ('dF-u2E0ZFAZMlAlsTjHz2A'),
   ('YzE9DAJDb5fqGa8WTZgBjg'),
   ('ZOa7CkROQBhLuATpNHcHgg'),
   ('qr1u2QOYqR_53oUJQWgftQ'),
   ('_aRnypLaHgZ7E9wZqHilOg'),
   ('IRBkVErlqhKMeNCxRgjRQw'),
   ('-sC66z4SO3tR7nFCjfQwuQ'),
   ('px45x27eir8RyN6YjX-VWQ'),
   ('zAoFrUwRVdSrvYWNB5e5Jw'),
   ('-JpZiiGPKOuCEiODGNyovw'),
   ('EUmfOpiQxJ5yaEMypI30gQ'),
   ('PfJ17JQJKsX9KHHEkkr6iQ'),
   ('2yBk6SvYQPnickE_QJrlaA'),
   ('K9hZAkRFuyfmLwceX8K4wg'),
   ('VAwTkxl4EV7MoGFpI_xcXQ'),
   ('kEaQt6G55MvXh1OW-1VCzQ'),
   ('w8sRfLP8U7uX4OktcSbb_w'),
   ('eX_f1ZzrpejCp6xJpfLmDQ'),
   ('IALApn21BROm-knJfH96eA'),
   ('7q1FpSXbE6XtLNg518pxDA'),
   ('VP8w1WNZKP-CObuhsMi7RQ'),
   ('3OadREi9_BfBz5EmwoqQcw'),
   ('bzQPFOLLxuwx7K7dw8j7Zw'),
   ('0hej0FRXraL5BNUKWhY_8w'),
   ('dHgoX3L2AKYixgH8hmJjfA'),
   ('ZRJwVLyzEJq1VAihDhYiow'),
   ('zjQxaHZSb47p7l-b7Nhzgg'),
   ('EolW2H_wkpYwWbBURN_4gQ'),
   ('u-VxYYupPzLHJph6XNUe2A'),
   ('sY7OAhyojv3YI0EUUW_gUQ'),
   ('qlgAl9biUkK1wvmJ4ggDFg'),
   ('mDdqifuTrfXAOfxiLMGu5Q'),
   ('jKLR4wAywvVcGtQnCLzoRw'),
   ('Gly54cM3avJg9n2F0l8V-g'),
   ('-4mNZfAXMd2mxEsD2YRcaQ'),
   ('eZXAQxBXReD78AWWf0_4ZA'),
   ('awM0p144EFHee9BdD4rw9Q'),
   ('vPDeCSYSD0XOD7r6XwU6wA'),
   ('8jTAfGcJMLs9VNcG4dndNQ'),
   ('5Rtds_pTigLiIEOm5KSAPA'),
   ('l-npaoUMhCy8HocKsuI-GQ'),
   ('8860WNIW_oiLU6XZkGgklg'),
   ('jS1niU6w9hSWxdH7wg1iTg'),
   ('GmzpzmxinfLMw5OXQKFEBQ'),
   ('-hWBlyI2k95yjU-cgwCKJg'),
   ('-wvryBujtHabx4jCW98eqQ'),
   ('kT_7_6nj39hV7o98c8WLbA'),
   ('U4HVQcnsWnChm9ssOb_CPA'),
   ('6MC-Ojl29-8N0Cg7ybAIPA'),
   ('0JUcQpKWku8D86TVY6cTgA'),
   ('JLTFO7WY88XaWbxQY4VgxA'),
   ('VMF64L6p5WeX9Se_GAvu-g'),
   ('mtYDfc-XhixQLGNjmjxC_g'),
   ('nbu8ikob1xlhhr38durIXw')
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
