import psycopg2
from typing import List, Dict, Any

class TaskManager:
  def __init__(self, host="localhost", port=5432, database="task_management", user="admin", password="password123"):
    self.connection_params = {
      'host': host,
      'port': port, 
      'database': database,
      'user': user,
      'password': password
    }
    
  def _get_connection(self):
    return psycopg2.connect(**self.connection_params)
    
  # 1. Отримати всі завдання певного користувача
  def get_all_tasks_by_user(self, user_id: int) -> List[Dict]:
    conn = self._get_connection()
    cur = conn.cursor()
    
    try:
      query1 = """
      SELECT *
      FROM tasks  
      WHERE user_id = %s
      """
      
      query = """
      SELECT t.id, t.title, t.description, s.name as status, t.created_at
      FROM tasks t
      JOIN status s ON t.status_id = s.id  
      WHERE t.user_id = %s
      """
      cur.execute(query, (user_id,))
      columns = [desc[0] for desc in cur.description]
      results = [dict(zip(columns, row)) for row in cur.fetchall()]
      
      return results
    finally:
      cur.close()
      conn.close()
  
  # 2. Вибрати завдання за певним статусом (з підзапитом)
  def get_tasks_by_status(self, status_name: str) -> List[Dict]:
    conn = self._get_connection()
    cur = conn.cursor()
    
    try:
      query1 = '''
        SELECT *
        FROM tasks
        WHERE status_id = (
          SELECT id
          FROM status
          WHERE name = %s
        );
      '''
      
      query = """
      SELECT t.id, t.title, t.description, u.fullname, t.created_at
      FROM tasks t
      JOIN users u ON t.user_id = u.id
      WHERE t.status_id = (SELECT id FROM status WHERE name = %s)
      """
      cur.execute(query, (status_name,))
      columns = [desc[0] for desc in cur.description] 
      results = [dict(zip(columns, row)) for row in cur.fetchall()]
      
      return results
    finally:
      cur.close()
      conn.close()
  
  # 3. Оновити статус конкретного завдання
  def update_task_status(self, task_id: int, new_status: str) -> bool:
    conn = self._get_connection()
    cur = conn.cursor()
    
    try:
      
      query1 = '''
      UPDATE tasks
      SET status_id = (
        SELECT id
        FROM status
        WHERE name = %s
      )
      WHERE id = %s
      '''

      query = """
      UPDATE tasks 
      SET status_id = (SELECT id FROM status WHERE name = %s)
      WHERE id = %s
      """
      cur.execute(query, (new_status, task_id))
      conn.commit()
      return cur.rowcount > 0
    finally:
      cur.close()
      conn.close()
        
  # 4. Отримати список користувачів, які не мають жодного завдання
  def get_users_without_tasks(self) -> List[Dict]:
    conn = self._get_connection()
    cur = conn.cursor()
    
    try:
      query1 = """
      SELECT *
      FROM users
      WHERE id NOT IN (
        SELECT user_id 
        FROM tasks
      )
      """
      
      query = """
      SELECT u.id, u.fullname, u.email
      FROM users u
      WHERE NOT EXISTS (
        SELECT 1 FROM tasks t WHERE t.user_id = u.id
      )
      """
      cur.execute(query, ())
      columns = [desc[0] for desc in cur.description]
      results = [dict(zip(columns, row)) for row in cur.fetchall()]
      
      return results
    finally:
      cur.close()
      conn.close()
  
  # 5. Додати нове завдання для конкретного користувача
  def add_new_task(self, title: str, description: str, status_name: str, user_id: int) -> bool:
    conn = self._get_connection()
    cur = conn.cursor()
    
    try:
      query1 = """
      INSERT INTO tasks (title, description, status_id, user_id)
      VALUES (%s, %s, (SELECT id FROM status WHERE name = %s), %s)
      """
      
      query = """
      INSERT INTO tasks (title, description, status_id, user_id)
      SELECT %s, %s, s.id, %s
      FROM status s
      WHERE s.name = %s
      """
      cur.execute(query, (title, description, user_id, status_name))
      conn.commit()
      return cur.rowcount > 0
    finally:
      cur.close()
      conn.close()
  
  # 6. Отримати всі завдання, які ще не завершено
  def get_incomplete_tasks(self) -> List[Dict]:
    conn = self._get_connection()
    cur = conn.cursor()
    
    try:
      query1 = """
      SELECT *
      FROM tasks
      WHERE status_id != (SELECT id FROM status WHERE name = 'completed')
      """
      
      query = """
      SELECT t.id, t.title, t.description, u.fullname, s.name as status, t.created_at
      FROM tasks t
      JOIN users u ON t.user_id = u.id
      JOIN status s ON t.status_id = s.id
      WHERE s.name != 'completed'
      """
      cur.execute(query, ())
      columns = [desc[0] for desc in cur.description]
      results = [dict(zip(columns, row)) for row in cur.fetchall()]
      
      return results
    finally:
      cur.close()
      conn.close()
  
  # 7. Видалити конкретне завдання
  def delete_task(self, task_id: int) -> bool:
    conn = self._get_connection()
    cur = conn.cursor()
    
    try:
      query1 = """
      DELETE FROM tasks
      WHERE id = %s
      """
      
      query = """
      DELETE FROM tasks
      WHERE id = %s AND EXISTS (SELECT 1 FROM tasks WHERE id = %s)
      """
      cur.execute(query1, (task_id,))  # використовуємо простішу версію
      conn.commit()
      return cur.rowcount > 0
    finally:
      cur.close()
      conn.close()
  
  # 8. Знайти користувачів з певною електронною поштою
  def find_users_by_email(self, email_pattern: str) -> List[Dict]:
    conn = self._get_connection()
    cur = conn.cursor()
    
    try:
      query1 = """
      SELECT *
      FROM users
      WHERE email LIKE %s
      """
      
      query = """
      SELECT u.id, u.fullname, u.email, COUNT(t.id) as task_count
      FROM users u
      LEFT JOIN tasks t ON u.id = t.user_id
      WHERE u.email LIKE %s
      GROUP BY u.id, u.fullname, u.email
      """
      cur.execute(query, (email_pattern,))
      columns = [desc[0] for desc in cur.description]
      results = [dict(zip(columns, row)) for row in cur.fetchall()]
      
      return results
    finally:
      cur.close()
      conn.close()
  
  # 9. Оновити ім'я користувача
  def update_user_name(self, user_id: int, new_fullname: str) -> bool:
    conn = self._get_connection()
    cur = conn.cursor()
    
    try:
      query1 = """
      UPDATE users
      SET fullname = %s
      WHERE id = %s
      """
      
      query = """
      UPDATE users
      SET fullname = %s
      WHERE id = %s AND EXISTS (SELECT 1 FROM users WHERE id = %s)
      """
      cur.execute(query1, (new_fullname, user_id))  # використовуємо простішу версію
      conn.commit()
      return cur.rowcount > 0
    finally:
      cur.close()
      conn.close()
  
  # 10. Отримати кількість завдань для кожного статусу
  def get_task_count_by_status(self) -> List[Dict]:
    conn = self._get_connection()
    cur = conn.cursor()
    
    try:
      query1 = """
      SELECT status_id, COUNT(*) as task_count
      FROM tasks
      GROUP BY status_id
      """
      
      query = """
      SELECT s.name as status, COUNT(t.id) as task_count
      FROM status s
      LEFT JOIN tasks t ON s.id = t.status_id
      GROUP BY s.id, s.name
      ORDER BY task_count DESC
      """
      cur.execute(query, ())
      columns = [desc[0] for desc in cur.description]
      results = [dict(zip(columns, row)) for row in cur.fetchall()]
      
      return results
    finally:
      cur.close()
      conn.close()
  
  # 11. Отримати завдання користувачів з певним доменом пошти
  def get_tasks_by_email_domain(self, domain: str) -> List[Dict]:
    conn = self._get_connection()
    cur = conn.cursor()
    
    try:
      query1 = """
      SELECT t.*
      FROM tasks t
      JOIN users u ON t.user_id = u.id
      WHERE u.email LIKE %s
      """
      
      query = """
      SELECT t.id, t.title, t.description, u.fullname, u.email, s.name as status, t.created_at
      FROM tasks t
      JOIN users u ON t.user_id = u.id
      JOIN status s ON t.status_id = s.id
      WHERE u.email LIKE %s
      ORDER BY t.created_at DESC
      """
      cur.execute(query, (f'%{domain}',))
      columns = [desc[0] for desc in cur.description]
      results = [dict(zip(columns, row)) for row in cur.fetchall()]
      
      return results
    finally:
      cur.close()
      conn.close()
  
  # 12. Отримати список завдань, що не мають опису
  def get_tasks_without_description(self) -> List[Dict]:
    conn = self._get_connection()
    cur = conn.cursor()
    
    try:
      query1 = """
      SELECT *
      FROM tasks
      WHERE description IS NULL OR description = ''
      """
      
      query = """
      SELECT t.id, t.title, u.fullname, s.name as status, t.created_at
      FROM tasks t
      JOIN users u ON t.user_id = u.id
      JOIN status s ON t.status_id = s.id
      WHERE t.description IS NULL OR TRIM(t.description) = ''
      """
      cur.execute(query, ())
      columns = [desc[0] for desc in cur.description]
      results = [dict(zip(columns, row)) for row in cur.fetchall()]
      
      return results
    finally:
      cur.close()
      conn.close()
  
  # 13. Вибрати користувачів та їхні завдання у статусі 'in progress'
  def get_users_with_in_progress_tasks(self) -> List[Dict]:
    conn = self._get_connection()
    cur = conn.cursor()
    
    try:
      query1 = """
      SELECT u.*, t.*
      FROM users u
      INNER JOIN tasks t ON u.id = t.user_id
      WHERE t.status_id = (SELECT id FROM status WHERE name = 'in progress')
      """
      
      query = """
      SELECT u.id as user_id, u.fullname, u.email, 
             t.id as task_id, t.title, t.description, t.created_at
      FROM users u
      INNER JOIN tasks t ON u.id = t.user_id
      INNER JOIN status s ON t.status_id = s.id
      WHERE s.name = 'in progress'
      ORDER BY u.fullname, t.created_at
      """
      cur.execute(query, ())
      columns = [desc[0] for desc in cur.description]
      results = [dict(zip(columns, row)) for row in cur.fetchall()]
      
      return results
    finally:
      cur.close()
      conn.close()
  
  # 14. Отримати користувачів та кількість їхніх завдань
  def get_users_with_task_count(self) -> List[Dict]:
    conn = self._get_connection()
    cur = conn.cursor()
    
    try:
      query1 = """
      SELECT u.*, COUNT(t.id) as task_count
      FROM users u
      LEFT JOIN tasks t ON u.id = t.user_id
      GROUP BY u.id
      """
      
      query = """
      SELECT u.id, u.fullname, u.email, 
             COUNT(t.id) as task_count,
             COUNT(CASE WHEN s.name = 'completed' THEN 1 END) as completed_tasks,
             COUNT(CASE WHEN s.name = 'in progress' THEN 1 END) as in_progress_tasks,
             COUNT(CASE WHEN s.name = 'new' THEN 1 END) as new_tasks
      FROM users u
      LEFT JOIN tasks t ON u.id = t.user_id
      LEFT JOIN status s ON t.status_id = s.id
      GROUP BY u.id, u.fullname, u.email
      ORDER BY task_count DESC
      """
      cur.execute(query, ())
      columns = [desc[0] for desc in cur.description]
      results = [dict(zip(columns, row)) for row in cur.fetchall()]
      
      return results
    finally:
      cur.close()
      conn.close()


if __name__ == "__main__":
    manager = TaskManager()
    
    # Тестування методів
    print("=== 1. Завдання користувача ID=1 ===")
    tasks = manager.get_all_tasks_by_user(1)
    for task in tasks[:3]:  # показати перші 3
        print(f"- {task['title']} ({task['status']})")
    
    print("\n=== 2. Завдання зі статусом 'new' ===")
    new_tasks = manager.get_tasks_by_status('new')
    for task in new_tasks[:3]:
        print(f"- {task['title']} - {task['fullname']}")
    
    print("\n=== 10. Статистика по статусах ===")
    stats = manager.get_task_count_by_status()
    for stat in stats:
        print(f"- {stat['status']}: {stat['task_count']} завдань")