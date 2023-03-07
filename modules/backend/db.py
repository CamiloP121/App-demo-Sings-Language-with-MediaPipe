import sqlite3
import pandas as pd

def create_db():
    '''
    Create a database
    '''
    conn = sqlite3.connect('modules/db/test_database.db') 
    c = conn.cursor()

    c.execute('''
            CREATE TABLE IF NOT EXISTS mp_result
            ([id_image] TEXT PRIMARY KEY,
            [image] TEXT, 
            [WRIST] TEXT,
            [THUMB_CMC] TEXT,
            [THUMB_MCP] TEXT,
            [THUMB_IP] TEXT,
            [THUMB_TIP] TEXT,
            [INDEX_FINGER_MCP] TEXT,
            [INDEX_FINGER_PIP] TEXT,
            [INDEX_FINGER_DIP] TEXT,
            [INDEX_FINGER_TIP] TEXT,
            [MIDDLE_FINGER_MCP] TEXT,
            [MIDDLE_FINGER_PIP] TEXT,
            [MIDDLE_FINGER_DIP] TEXT,
            [MIDDLE_FINGER_TIP] TEXT,
            [RING_FINGER_MCP] TEXT,
            [RING_FINGER_PIP] TEXT,
            [RING_FINGER_DIP] TEXT,
            [RING_FINGER_TIP] TEXT,
            [PINKY_MCP] TEXT,
            [PINKY_PIP] TEXT,
            [PINKY_DIP] TEXT,
            [PINKY_TIP] TEXT,
            [score] TEXT,
            [orentation_hands] TEXT) 
            ''')
    
    conn.commit()
    conn.close()


def insert_db(dictionary_result:dict):
    '''
    Function to insert data into database
    ----------------------------------------------------------------
    Args:
    dictionary_result (dict): dictionary
    '''
    # Select ID
    _,len = download_db()
    dictionary_result['id_image'] = '_'.join(['id',str(len),dictionary_result['orentation_hands']])

    for i, (key, value) in enumerate(dictionary_result.items()):
        dictionary_result[key] = str(value)
        


    conn = sqlite3.connect('modules/db/test_database.db')
    c = conn.cursor()
    c.execute("INSERT INTO mp_result VALUES (:id_image,:image,:WRIST,:THUMB_CMC,:THUMB_MCP,:THUMB_IP,:THUMB_TIP,:INDEX_FINGER_MCP,:INDEX_FINGER_PIP,:INDEX_FINGER_DIP,:INDEX_FINGER_TIP,:MIDDLE_FINGER_MCP,:MIDDLE_FINGER_PIP,:MIDDLE_FINGER_DIP,:MIDDLE_FINGER_TIP,:RING_FINGER_MCP,:RING_FINGER_PIP,:RING_FINGER_DIP,:RING_FINGER_TIP,:PINKY_MCP,:PINKY_PIP,:PINKY_DIP,:PINKY_TIP,:score,:orentation_hands)", dictionary_result)
    conn.commit()
    conn.close()

def download_db():
    ''''
    Download database
    ----------------------------------------------------------------
    Returns:
    database
    Length of the database
    '''
    conn = sqlite3.connect('modules/db/test_database.db', isolation_level=None,
                        detect_types=sqlite3.PARSE_COLNAMES)
    #conn.close()
    db_df = pd.read_sql_query("SELECT * FROM mp_result", conn)
    return db_df, len(db_df)
    #db_df.to_csv('database.csv', index=False)
    

if __name__=='__main__':
    print('Si')
    
    import json
    with open('test/mp_results.json', 'r') as file:
        mp_results = json.load(file)
    #insert_db(6,'prueba',str(mp_results['WRIST']))
    print(mp_results)
    insert_db(mp_results)
    #[print(f':{key},') for key in mp_results.keys()]