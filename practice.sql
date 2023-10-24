SELECT 
    PIN_NO,
    TAX_PAYER_ID,
    STATION_ID,
    EFFECTIVE_DATE,
    CREATED_DATE,
    EMAIL_ID,
    'CONSISTENCY' AS Standard,
    CONSISTENCY AS Score
FROM 
(
    SELECT 
        PIN_NO,
        TAX_PAYER_ID,
        STATION_ID,
        EMAIL_ID,
        EFFECTIVE_DATE, 
        TO_CHAR(CREATED_DT, 'yyyymmdd') AS CREATED_DATE, 
        CASE 
            WHEN C.EMAIL_ID IS NOT NULL THEN 1 
            ELSE 0 
        END AS CONSISTENCY
) CONSISTENCY_METRIC
UNION ALL
SELECT 
    PIN_NO,
    TAX_PAYER_ID,
    STATION_ID,
    EMAIL_ID,
    EFFECTIVE_DATE, 
    TO_CHAR(CREATED_DT, 'yyyymmdd') AS CREATED_DATE, 
    CASE 
        WHEN ROW_NUM = 1 THEN 1 
        ELSE 0 
    END AS UNIQUENESS
FROM 
(
    SELECT 
        B.PIN_NO,
        B.TAX_PAYER_ID,
        B.STATION_ID,
        TRIM(A.EMAIL_ID) AS EMAIL_ID,
        B.EFFECTIVE_DATE,
        B.CREATED_DT,
        ROW_NUMBER () OVER (
            PARTITION BY TRIM(A.EMAIL_ID)
            ORDER BY B.PIN_NO
        ) AS ROW_NUM
    FROM 
        KRA_INT.I_TRE_COMMON_CONTACT_DTL A
    JOIN 
        KRA_INT.I_TRE_TAX_PAYER_MST B
    ON 
        A.TAX_PAYER_ID = B.TAX_PAYER_ID
) C2
UNION ALL
SELECT 
    PIN_NO,
    TAX_PAYER_ID,
    STATION_ID,
    EMAIL_ID,
    EFFECTIVE_DATE, 
    TO_CHAR(CREATED_DT, 'yyyymmdd') AS CREATED_DATE, 
    CASE 
        WHEN C.IPAGE_PROCESSED = 'Y' OR C.ACTIVE_FLAG = 'Y' THEN 1 
        ELSE 0 
    END AS TIMELINESS
FROM 
(
    SELECT 
        B.PIN_NO,
        B.TAX_PAYER_ID,
        B.STATION_ID,
        TRIM(A.EMAIL_ID) AS EMAIL_ID,
        B.EFFECTIVE_DATE,
        B.CREATED_DT,
        ROW_NUMBER () OVER (
            PARTITION BY TRIM(A.EMAIL_ID)
            ORDER BY B.PIN_NO
        ) AS ROW_NUM
    FROM 
        KRA_INT.I_TRE_COMMON_CONTACT_DTL A
    JOIN 
        KRA_INT.I_TRE_TAX_PAYER_MST B
    ON 
        A.TAX_PAYER_ID = B.TAX_PAYER_ID
) C2;

UNION ALL
SELECT 
    PIN_NO,
    TAX_PAYER_ID,
    STATION_ID,
    EFFECTIVE_DATE,
    CREATED_DATE,
    EMAIL_ID,
    'VALIDITY' AS Standard,
    VALIDITY AS Score
FROM 
(
    SELECT 
        PIN_NO,
        TAX_PAYER_ID,
        STATION_ID,
        EMAIL_ID,
        EFFECTIVE_DATE, 
        TO_CHAR(CREATED_DT, 'yyyymmdd') AS CREATED_DATE, 
        CASE 
        -- CHECKING FOR VALIDITY BASED ON EMAIL RULES
        WHEN (
            -- if the email format follows the pattern: username@domain
            REGEXP_LIKE(C.EMAIL_ID, '^[A-Za-z0-9._]+@[A-Za-z]+\.[A-Za-z]+$')
            -- if the length of the username is within the specified range for each domain
            AND (
                (UPPER(REGEXP_SUBSTR(C.EMAIL_ID, '@[A-Za-z]+\.[A-Za-z]+$')) = '@GMAIL.COM' AND LENGTH(REGEXP_SUBSTR(C.EMAIL_ID, '^[A-Za-z0-9._]+')) BETWEEN 6 AND 30)
                OR (UPPER(REGEXP_SUBSTR(C.EMAIL_ID, '@[A-Za-z]+\.[A-Za-z]+$')) IN ('@YAHOO.COM', '@HOTMAIL.COM', '@OUTLOOK.COM') AND LENGTH(REGEXP_SUBSTR(C.EMAIL_ID, '^[A-Za-z0-9._]+')) >= 4)
            )
            -- Adding a catch-all condition for "other" domains (valid)
            OR (
                UPPER(REGEXP_SUBSTR(C.EMAIL_ID, '@[A-Za-z]+\.[A-Za-z]+$')) NOT IN ('@GMAIL.COM', '@YAHOO.COM', '@HOTMAIL.COM', '@OUTLOOK.COM')
            --            AND LENGTH(REGEXP_SUBSTR(C.EMAIL_ID, '^[A-Za-z0-9._]+')) >= 4
            )
        ) THEN '1'
        ELSE '0'
        END AS VALIDITY,
) VALIDITY_METRIC
UNION ALL
SELECT 
    PIN_NO,
    TAX_PAYER_ID,
    STATION_ID,
    EFFECTIVE_DATE,
    CREATED_DATE,
    EMAIL_ID,
    'COMPLETENESS' AS Standard,
    COMPLETENESS AS Score
FROM 
(
    SELECT 
        PIN_NO,
        TAX_PAYER_ID,
        STATION_ID,
        EMAIL_ID,
        EFFECTIVE_DATE, 
        TO_CHAR(CREATED_DT, 'yyyymmdd') AS CREATED_DATE, 
        CASE 
            WHEN C.EMAIL_ID LIKE '%@%.%' AND C.EMAIL_ID IS NOT NULL THEN '1' ELSE '0'
        END AS COMPLETENESS
) COMPLETENESS_METRIC
UNION ALL
SELECT 
    PIN_NO,
    TAX_PAYER_ID,
    STATION_ID,
    EFFECTIVE_DATE,
    CREATED_DATE,
    EMAIL_ID,
    'ACCURACY' AS Standard,
    CASE 
        WHEN CONSISTENCY || UNIQUENESS || TIMELINESS || COMPLETENESS || VALIDITY = '11111' THEN 1 
        ELSE 0 
    END AS Score
FROM 
(
    SELECT 
        PIN_NO,
        TAX_PAYER_ID,
        STATION_ID,
        EMAIL_ID,
        EFFECTIVE_DATE, 
        TO_CHAR(CREATED_DT, 'yyyymmdd') AS CREATED_DATE, 
        CASE 
            WHEN CONSISTENCY || UNIQUENESS || TIMELINESS || COMPLETENESS || VALIDITY = '11111' THEN 1 
            ELSE 0 
        END AS ACCURACY
) ACCURACY_METRIC;

SELECT 
    PIN_NO,
    TAX_PAYER_ID,
    STATION_ID,
    EMAIL_ID,
    EFFECTIVE_DATE, 
    TO_CHAR(CREATED_DT, 'yyyymmdd') AS CREATED_DATE, 
    FROM 
    (
        SELECT 
            B.PIN_NO,
            B.TAX_PAYER_ID,
            B.STATION_ID,
            TRIM(A.EMAIL_ID) AS EMAIL_ID,
            B.IPAGE_PROCESSED,
            B.ACTIVE_FLAG,
            B.EFFECTIVE_DATE,
            B.CREATED_DT,
            ROW_NUMBER () OVER (
                PARTITION BY A.EMAIL_ID
                ORDER BY PIN_NO
            ) ROW_NUM
        FROM 
            KRA_INT.I_TRE_COMMON_CONTACT_DTL A,
            KRA_INT.I_TRE_TAX_PAYER_MST B
        WHERE 
            A.TAX_PAYER_ID = B.TAX_PAYER_ID
    ) C
)



SELECT 
    PIN_NO,
    TAX_PAYER_ID,
    STATION_ID,
    EFFECTIVE_DATE,
    CREATED_DATE,
    EMAIL_ID,
    'CONSISTENCY' AS Standard, CONSISTENCY AS SCORE
    FROM 
        ( CASE 
            WHEN C.EMAIL_ID IS NOT NULL THEN 1 
            ELSE 0 
        END AS CONSISTENCY
        
----    CONSISTENCY, 
----    UNIQUENESS, 
----    TIMELINESS, 
----    VALIDITY,
----    COMPLETENESS,   
--    /* Accuracy is the average of other standards */
--    CASE 
--        WHEN CONSISTENCY || UNIQUENESS || TIMELINESS || COMPLETENESS || VALIDITY = '11111' THEN 1 
--        ELSE 0 
--    END AS ACCURACY
FROM 
(
    SELECT 
        PIN_NO,
        TAX_PAYER_ID,
        STATION_ID,
        EMAIL_ID,
        EFFECTIVE_DATE, 
        TO_CHAR(CREATED_DT, 'yyyymmdd') AS CREATED_DATE, 
        CASE 
            WHEN C.EMAIL_ID IS NOT NULL THEN 1 
            ELSE 0 
        END AS CONSISTENCY,
        
     -- UNIQUENESS = 1 IF ROW_NUM IS 1 
        CASE 
            WHEN C.ROW_NUM = 1 THEN 1 
            ELSE 0 
        END AS UNIQUENESS,
        
     -- TIMELINESS = 1 IF IPAGE_PROCESSED IS 'Y' OR ACTIVE_FLAG IS 'Y'
        CASE 
            WHEN C.IPAGE_PROCESSED = 'Y' OR C.ACTIVE_FLAG = 'Y' THEN 1 
            ELSE 0 
        END AS TIMELINESS,
        
    CASE 
    -- CHECKING FOR VALIDITY BASED ON EMAIL RULES
    WHEN (
        -- if the email format follows the pattern: username@domain
        REGEXP_LIKE(C.EMAIL_ID, '^[A-Za-z0-9._]+@[A-Za-z]+\.[A-Za-z]+$')
        -- if the length of the username is within the specified range for each domain
        AND (
            (UPPER(REGEXP_SUBSTR(C.EMAIL_ID, '@[A-Za-z]+\.[A-Za-z]+$')) = '@GMAIL.COM' AND LENGTH(REGEXP_SUBSTR(C.EMAIL_ID, '^[A-Za-z0-9._]+')) BETWEEN 6 AND 30)
            OR (UPPER(REGEXP_SUBSTR(C.EMAIL_ID, '@[A-Za-z]+\.[A-Za-z]+$')) IN ('@YAHOO.COM', '@HOTMAIL.COM', '@OUTLOOK.COM') AND LENGTH(REGEXP_SUBSTR(C.EMAIL_ID, '^[A-Za-z0-9._]+')) >= 4)
        )
        -- Adding a catch-all condition for "other" domains (valid)
        OR (
            UPPER(REGEXP_SUBSTR(C.EMAIL_ID, '@[A-Za-z]+\.[A-Za-z]+$')) NOT IN ('@GMAIL.COM', '@YAHOO.COM', '@HOTMAIL.COM', '@OUTLOOK.COM')
--            AND LENGTH(REGEXP_SUBSTR(C.EMAIL_ID, '^[A-Za-z0-9._]+')) >= 4
        )
    ) THEN '1'
    ELSE '0'
    END AS VALIDITY,
   
    CASE 
        -- CHECKING FOR COMPLETENESS: PRESENCE OF USERNAME, "@" SYMBOL, AND DOMAIN, AND NOT NULL
        WHEN C.EMAIL_ID LIKE '%@%.%' AND C.EMAIL_ID IS NOT NULL THEN '1' ELSE '0'
        END AS COMPLETENESS
    FROM 
    (
        SELECT 
            B.PIN_NO,
            B.TAX_PAYER_ID,
            B.STATION_ID,
            TRIM(A.EMAIL_ID) AS EMAIL_ID,
            B.IPAGE_PROCESSED,
            B.ACTIVE_FLAG,
            B.EFFECTIVE_DATE,
            B.CREATED_DT,
            ROW_NUMBER () OVER (
                PARTITION BY A.EMAIL_ID
                ORDER BY PIN_NO
            ) ROW_NUM
        FROM 
            KRA_INT.I_TRE_COMMON_CONTACT_DTL A,
            KRA_INT.I_TRE_TAX_PAYER_MST B
        WHERE 
            A.TAX_PAYER_ID = B.TAX_PAYER_ID
    ) C
)