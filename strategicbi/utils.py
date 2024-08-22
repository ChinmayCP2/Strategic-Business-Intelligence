from django.db import connection

def custom_sql_for_default_display():
    '''Query to get State district names with a inner join and thier codes'''
    cursor = connection.cursor()
    cursor.execute("""
        WITH distinct_locations AS (
        SELECT 
            "stateCode",
            "districtCode",
            MAX(created_at) AS created_at
        FROM 
            public.strategicbi_datamodel
        GROUP BY 
            "stateCode", 
            "districtCode"
        )
        SELECT 
        dl."stateCode" AS stateCode,
        s."stateNameEnglish" AS stateNameEnglish,
        dl."districtCode" AS districtCode,
        d."districtNameEnglish" AS districtNameEnglish,
        dl.created_at
        FROM 
        distinct_locations dl
        INNER JOIN public.lgd_statemodel s ON dl."stateCode" = s.id
        INNER JOIN public.lgd_districtmodel d ON dl."districtCode" = d.id
        ORDER BY 
        dl.created_at DESC;
    """)
    rows = cursor.fetchall()
    return rows

def get_distinct_locations(state):
    '''sql for get district location'''
    with connection.cursor() as cursor:
        cursor.execute("""
            WITH distinct_locations AS (
                SELECT 
                    "stateCode",
                    "districtCode",
                    MAX(created_at) AS created_at
                FROM 
                    public.strategicbi_datamodel
                GROUP BY 
                    "stateCode", 
                    "districtCode"
            )
            SELECT 
                dl."stateCode" AS stateCode,
                s."stateNameEnglish" AS stateNameEnglish,
                dl."districtCode" AS districtCode,
                d."districtNameEnglish" AS districtNameEnglish,
                dl.created_at
            FROM 
                distinct_locations dl
            INNER JOIN public.lgd_statemodel s ON dl."stateCode" = s.id
            INNER JOIN public.lgd_districtmodel d ON dl."districtCode" = d.id
            WHERE 
                s.id = %s
            ORDER BY 
                dl.created_at DESC
        """, [state])
        rows = cursor.fetchall()
    return rows