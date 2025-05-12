import psycopg2
from psycopg2 import sql




def connect():
    """ Connect to the PostgreSQL database server """
    conn = None

    try:
        
        #establishing the connection
        conn = psycopg2.connect(
            database="tatai", user='postgres', password='root@123', host='127.0.0.1', port='5432'
        )

        # create a cursor
        cur = conn.cursor()
        
        
        sql4 = '''SELECT json_agg(row) FROM (select "instrument","symbol","expiry_dt","strike_pr","option_typ","OPEN","HIGH","LOW","CLOSE","SETTLE_PR","contracts","val_inlakh","open_int","chg_in_oi","TIMESTAMP" from bandel.sharemarket_e limit 4) row;'''
        
        sql5 = '''SELECT array( select row_to_json(row) FROM (select "instrument","symbol","expiry_dt","strike_pr","option_typ","OPEN","HIGH","LOW","CLOSE","SETTLE_PR","contracts","val_inlakh","open_int","chg_in_oi","TIMESTAMP" from bandel.sharemarket_e limit 5) row);'''
        sql6 = '''SELECT row_to_json(row) FROM (select "instrument","symbol","expiry_dt","strike_pr","option_typ","OPEN","HIGH","LOW","CLOSE","SETTLE_PR","contracts","val_inlakh","open_int","chg_in_oi","TIMESTAMP" from bandel.sharemarket_e limit 10) row ;'''
        cur.execute(sql4)

        
        results = cur.fetchone()
        
        cur.close()
        print(type(results))
        
        print(results[0])
        return (results)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    jsonStr = connect()
    print("bivas ball")
    print(jsonStr)
