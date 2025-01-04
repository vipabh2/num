import sqlite3

# إنشاء اتصال بقاعدة البيانات أو فتحها إذا كانت موجودة
conn = sqlite3.connect('restricted_users.db')
cursor = conn.cursor()

# إنشاء جدول للمستخدمين المقيدين (إذا لم يكن موجودًا)
cursor.execute('''CREATE TABLE IF NOT EXISTS restricted_users (
                    user_id INTEGER PRIMARY KEY,
                    chat_id INTEGER,
                    username TEXT,
                    first_name TEXT,
                    reason TEXT,
                    restricted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

# إضافة مستخدم مقيد إلى قاعدة البيانات
def add_restricted_user(user_id, chat_id, username, first_name, reason):
    cursor.execute('''INSERT INTO restricted_users (user_id, chat_id, username, first_name, reason) 
                      VALUES (?, ?, ?, ?, ?)''', 
                   (user_id, chat_id, username, first_name, reason))
    conn.commit()

# جلب قائمة المستخدمين المقيدين
def get_restricted_users():
    cursor.execute('''SELECT user_id, username, first_name FROM restricted_users''')
    return cursor.fetchall()

# إغلاق الاتصال بقاعدة البيانات
def close_db():
    conn.close()
