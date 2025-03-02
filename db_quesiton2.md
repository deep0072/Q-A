# SQL Interview Questions and Answers for Infosys Backend Developer Role (4+ Years Experience, Django Backend Focus)

This document contains 50 SQL questions with detailed answers, tailored for a backend developer preparing for an Infosys interview. The questions cover basic concepts, intermediate and advanced queries, database design, performance optimization, and transactions, aligned with enterprise-level expectations.

---

## Basic Concepts (Foundational Knowledge with Practical Insights)

1. **What is a primary key, and how does it differ from a unique key in a real-world application?**  
   - **Answer:** A primary key uniquely identifies each record in a table, enforcing both uniqueness and non-NULL constraints—e.g., in a Django `User` model, `id` is typically the primary key (`id = models.AutoField(primary_key=True)`). A unique key ensures uniqueness but allows NULL values, suitable for fields like `email` (`email = models.EmailField(unique=True, null=True)`). In Infosys projects, primary keys often use auto-incrementing integers for simplicity or UUIDs (`id = models.UUIDField(default=uuid.uuid4, primary_key=True)`) for scalability in distributed systems, avoiding collisions across regions—e.g., a global customer database. Unique keys fit optional fields like `username`, where NULLs might be permitted pre-verification. Performance-wise, primary keys create clustered indexes in databases like MySQL InnoDB or SQL Server, physically ordering data for efficient range queries (e.g., `SELECT * FROM users WHERE id BETWEEN 100 AND 200`), while unique keys create non-clustered indexes, acting as separate pointers optimized for lookups (e.g., `SELECT * FROM users WHERE username = 'john'`). In an Infosys banking app, `id` as a primary key ensures fast joins, while a unique `account_number` supports optional uniqueness. Explaining Django’s ORM mapping, security (UUIDs obscure counts), or index impacts demonstrates your enterprise design skills, impressing with practical insight.

2. **What is normalization, and how would you apply it in a Django project?**  
   - **Answer:** Normalization reduces data redundancy via rules like 1NF (atomic values, no repeating groups), 2NF (no partial dependencies), and 3NF (no transitive dependencies). For example, instead of a `Customer` table with redundant addresses, split into `Customer` (id, name) and `Address` (customer_id, street), linked by `ForeignKey`. In a Django project for Infosys’s e-commerce platform, this saves storage and simplifies updates—e.g., changing a customer’s street in `Address` once rather than across all `Orders`. Implement with models: `class Customer(models.Model): name = models.CharField(); class Address(models.Model): customer = models.ForeignKey(Customer, on_delete=models.CASCADE), street = models.CharField()`. However, for faster reads in a high-traffic app, denormalize by adding `city` to `Orders` (`city = models.CharField()`), avoiding joins for `SELECT order_id, city FROM orders`. Use Django’s `ForeignKey` for relationships, with raw SQL (`connection.cursor()`) for complex joins (e.g., multi-table aggregates) the ORM can’t optimize. Discussing trade-offs (storage vs. query speed), indexing `customer_id`, or sync with signals (`@receiver(post_save)`) showcases your ability to balance efficiency and scalability, impressing with enterprise-level design.

3. **Explain indexing and its impact on a high-traffic Django application.**  
   - **Answer:** Indexing creates a B-tree to speed up retrieval—e.g., indexing `created_at` in `Orders` accelerates `SELECT * FROM orders WHERE created_at > '2024-01-01'`. In an Infosys banking app handling thousands of transactions per second, indexing `account_number` (`CREATE INDEX idx_account ON accounts(account_number)`) ensures sub-second lookups (e.g., `SELECT balance FROM accounts WHERE account_number = '12345'`). In Django, use `db_index=True` (`account_number = models.CharField(db_index=True)`) or `Meta.indexes` for composite indexes (e.g., `indexes = [models.Index(fields=['customer_id', 'order_date'])]`) to optimize `SELECT * FROM orders WHERE customer_id = 1 ORDER BY order_date`. However, over-indexing slows writes—`INSERT`, `UPDATE`, and `DELETE` update indexes, critical in write-heavy systems like audit logs. Use `EXPLAIN` to verify index usage (e.g., avoiding full scans), tailoring to patterns from Django Debug Toolbar. For Infosys’s high traffic, composite indexes (e.g., `(customer_id, order_date)`) reduce sort times, and covering indexes (e.g., including `total`) avoid table access. Explaining selectivity (e.g., avoiding low-variety fields like `status`) or maintenance costs demonstrates your optimization expertise, impressing with enterprise performance focus.

---

## Intermediate SQL Queries (Practical Scenarios for Backend Development)

4. **Write a query to find the top 5 employees with the highest salary, handling ties appropriately.**  
   - **Answer:**  
     ```sql
     SELECT emp_id, full_name, salary
     FROM employee
     WHERE salary IN (
         SELECT salary
         FROM employee
         ORDER BY salary DESC
         LIMIT 5
     )
     ORDER BY salary DESC, emp_id;
     ```  
     This ensures fairness in an Infosys HR system by including ties—e.g., if multiple employees share the 5th highest salary ($100,000), all are returned, not just the first five. The subquery selects the top 5 salary values, and the outer query fetches all matches, with `emp_id` as a tiebreaker for deterministic output, vital for audit trails. For a million-row table, indexing `salary` (`CREATE INDEX idx_salary ON employee(salary)`) reduces sorting from O(n log n) to O(log n), critical for performance. In Django, `Employee.objects.order_by('-salary')[:5]` doesn’t handle ties naturally—raw SQL or `annotate()` with `Rank()` might be needed. For Infosys’s global payroll, `PARTITION BY country` could rank regionally, and a composite index on `(salary, emp_id)` optimizes retrieval. Explaining edge cases (e.g., fewer than 5 employees) or optimization strategies impresses with practical SQL depth.

5. **Write a query to calculate the average salary per department, excluding departments with fewer than 3 employees.**  
   - **Answer:**  
     ```sql
     SELECT department, AVG(salary) as avg_salary
     FROM employee
     GROUP BY department
     HAVING COUNT(emp_id) >= 3
     ORDER BY avg_salary DESC;
     ```  
     This provides meaningful analytics for Infosys by filtering out small departments (e.g., a two-person team) where averages might mislead—`HAVING` applies post-aggregation, ensuring only sizable groups remain. Indexing `department` (`CREATE INDEX idx_dept ON employee(department)`) speeds up `GROUP BY`, crucial for millions of records. In Django, `Employee.objects.values('department').annotate(avg_salary=Avg('salary')).filter(count__gte=3)` mirrors this, but raw SQL allows precision (e.g., `ROUND(AVG(salary), 2)`). A composite index on `(department, salary)` optimizes grouping and averaging, and a materialized view (`CREATE MATERIALIZED VIEW dept_stats AS ...`) precomputes stats for dashboards, refreshed nightly. Discussing NULL handling (`COALESCE(salary, 0)`) or `EXPLAIN` analysis demonstrates your enterprise analytics skills, impressing with precision.

6. **Write a query to find employees with salaries above their department’s average.**  
   - **Answer:**  
     ```sql
     SELECT e.emp_id, e.full_name, e.salary, e.department
     FROM employee e
     WHERE e.salary > (
         SELECT AVG(salary)
         FROM employee e2
         WHERE e2.department = e.department
     );
     ```  
     This correlated subquery identifies top earners per department for Infosys performance reviews—comparing each salary to its department’s average. For large datasets, it recalculates averages per row, so optimize with a CTE:  
     ```sql
     WITH dept_avg AS (
         SELECT department, AVG(salary) as avg_salary
         FROM employee
         GROUP BY department
     )
     SELECT e.emp_id, e.full_name, e.salary, e.department
     FROM employee e
     JOIN dept_avg da ON e.department = da.department
     WHERE e.salary > da.avg_salary;
     ```  
     This aggregates once, boosting efficiency—a key for Infosys’s scalable systems. In Django, `Employee.objects.annotate(dept_avg=Avg('salary', filter=Q(department=F('department')))).filter(salary__gt=F('dept_avg'))` approximates this, but raw SQL leverages database features (e.g., PostgreSQL’s `FILTER`). Indexing `department` and `salary` enhances performance, and suggesting a denormalized `dept_avg_salary` with triggers shows your enterprise optimization prowess, impressing with practical solutions.

7. **Write a query to find the number of orders placed per customer in the last 30 days.**  
   - **Answer:**  
     ```sql
     SELECT c.customer_id, c.name, COUNT(o.order_id) as order_count
     FROM customers c
     LEFT JOIN orders o ON c.customer_id = o.customer_id
     WHERE o.order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
     GROUP BY c.customer_id, c.name
     ORDER BY order_count DESC;
     ```  
     Using `LEFT JOIN` ensures all customers appear, even with zero orders, ideal for an Infosys sales dashboard—`COUNT(o.order_id)` defaults to 0 for non-ordering customers. Indexing `order_date` and `customer_id` (`CREATE INDEX idx_orders ON orders(customer_id, order_date)`) prevents full scans, vital for millions of orders. In Django, `Customer.objects.annotate(order_count=Count('orders', filter=Q(orders__order_date__gte=timezone.now() - timedelta(days=30))))` replicates this, but raw SQL handles timezone nuances (e.g., `UTC_TIMESTAMP()`). For Infosys’s real-time needs, partitioning `orders` by `order_date` or caching in Redis optimizes performance. Explaining NULL handling or covering indexes (e.g., including `order_id`) impresses with enterprise scalability.

8. **Write a query to find employees who joined in the last quarter of 2024.**  
   - **Answer:**  
     ```sql
     SELECT emp_id, full_name, date_of_joining
     FROM employee
     WHERE date_of_joining BETWEEN '2024-10-01' AND '2024-12-31';
     ```  
     This suits Infosys’s HR onboarding reports, filtering hires efficiently. For flexibility, use `QUARTER(date_of_joining) = 4 AND YEAR(date_of_joining) = 2024`, parameterizable in a stored procedure (`CREATE PROCEDURE get_q4_hires(year INT)`). Indexing `date_of_joining` (`CREATE INDEX idx_join_date ON employee(date_of_joining)`) ensures quick filtering over historical data, critical for millions of employees. In Django, `Employee.objects.filter(date_of_joining__range=['2024-10-01', '2024-12-31'])` works, but raw SQL supports database-specific functions (e.g., MySQL’s `EXTRACT`). Suggesting a covering index on `(date_of_joining, emp_id, full_name)` or archiving to `retired_employees` demonstrates your enterprise optimization skills, impressing with scalability.

9. **Write a query to find duplicate email addresses in the employee table.**  
   - **Answer:**  
     ```sql
     SELECT email, COUNT(*) as count
     FROM employee
     GROUP BY email
     HAVING count > 1;
     ```  
     This detects data quality issues in Infosys’s employee database—e.g., duplicate `john.doe@infosys.com` entries—crucial for compliance and communication. Indexing `email` (`CREATE INDEX idx_email ON employee(email)`) speeds grouping, and a `UNIQUE` constraint (`ALTER TABLE employee ADD UNIQUE (email)`) prevents future duplicates. In Django, `unique=True` (`email = models.EmailField(unique=True)`) enforces this via migrations. A cleanup script might merge duplicates (e.g., latest `updated_at`), and a trigger could log to `audit_log`. Handling case-insensitive duplicates (`LOWER(email)` with a functional index) or validation during insertion (Django validators) shows your proactive enterprise approach, impressing with data integrity focus.

10. **Write a query to find employees reporting to a specific manager (e.g., manager_id = 100).**  
    - **Answer:**  
      ```sql
      SELECT emp_id, full_name, department
      FROM employee
      WHERE manager_id = 100;
      ```  
      This suits Infosys’s org lookups, but for multi-level hierarchies, a recursive CTE is powerful:  
      ```sql
      WITH RECURSIVE hierarchy AS (
          SELECT emp_id, full_name, manager_id, 1 AS level
          FROM employee
          WHERE manager_id = 100
          UNION ALL
          SELECT e.emp_id, e.full_name, e.manager_id, h.level + 1
          FROM employee e
          JOIN hierarchy h ON e.manager_id = h.emp_id
      )
      SELECT * FROM hierarchy;
      ```  
      This traces all subordinates under manager 100, vital for Infosys’s global teams. Indexing `manager_id` (`CREATE INDEX idx_mgr ON employee(manager_id)`) ensures efficient joins. In Django, `Employee.objects.filter(manager_id=100)` handles the basic case, but recursive queries need raw SQL. Suggesting a materialized view or cycle prevention (`WHERE e.emp_id != h.emp_id`) demonstrates your hierarchical data expertise, impressing with enterprise scalability.

---

## Advanced SQL Queries (Complex Scenarios for Scalability)

11. **Write a query to find the second highest salary without using LIMIT.**  
    - **Answer:**  
      ```sql
      SELECT MAX(salary)
      FROM employee
      WHERE salary < (SELECT MAX(salary) FROM employee);
      ```  
      This works across databases without `LIMIT`, finding the highest salary below the maximum—e.g., if salaries are 100k, 90k, 90k, it returns 90k—fitting Infosys’s diverse tech stack. For ties, use:  
      ```sql
      SELECT salary
      FROM (SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) as rnk FROM employee) t
      WHERE rnk = 2;
      ```  
      `DENSE_RANK()` ensures all tied second-highest salaries are returned, crucial for payroll fairness. Indexing `salary` optimizes both, and in Django, raw SQL is needed (ORM lacks window support). Discussing edge cases (e.g., fewer than two salaries) or a stored procedure for nth-highest salary impresses with advanced SQL skills.

12. **Write a query to find employees who are also managers (self-join).**  
    - **Answer:**  
      ```sql
      SELECT DISTINCT e.emp_id, e.full_name
      FROM employee e
      JOIN employee m ON e.emp_id = m.manager_id;
      ```  
      This identifies managers in Infosys’s org chart—`DISTINCT` avoids duplicates if one manages multiple subordinates. Indexing `manager_id` (`CREATE INDEX idx_mgr ON employee(manager_id)`) speeds joins, vital for large datasets. In Django, `Employee.objects.filter(id__in=Employee.objects.values('manager_id'))` replicates this, but raw SQL allows conditions (e.g., `m.status = 'active'`). Counting subordinates (`COUNT(m.emp_id) GROUP BY e.emp_id`) or using a CTE for multi-level analysis demonstrates adaptability for Infosys’s leadership dashboards, impressing with practical design.

13. **Write a query to find the department with the highest total salary expenditure.**  
    - **Answer:**  
      ```sql
      SELECT department, SUM(salary) as total_salary
      FROM employee
      GROUP BY department
      ORDER BY total_salary DESC
      LIMIT 1;
      ```  
      Essential for Infosys budgeting, this aggregates salaries—indexing `department` and `salary` (`CREATE INDEX idx_dept_salary ON employee(department, salary)`) optimizes grouping. For ties, use:  
      ```sql
      WITH ranked_depts AS (
          SELECT department, SUM(salary) as total_salary,
                 RANK() OVER (ORDER BY SUM(salary) DESC) as rnk
          FROM employee
          GROUP BY department
      )
      SELECT department, total_salary
      FROM ranked_depts
      WHERE rnk = 1;
      ```  
      This ensures all top spenders are returned. In Django, `Employee.objects.values('department').annotate(total=Sum('salary')).order_by('-total')[:1]` works, but raw SQL offers precision (e.g., `ROUND`). Suggesting a scheduled job for precomputed stats impresses with enterprise foresight.

14. **Write a query to find employees who have worked on more than 3 projects.**  
    - **Answer:**  
      ```sql
      SELECT e.emp_id, e.full_name, COUNT(pa.project_id) as project_count
      FROM employee e
      JOIN project_assignments pa ON e.emp_id = pa.emp_id
      GROUP BY e.emp_id, e.full_name
      HAVING project_count > 3;
      ```  
      This tracks workload in Infosys’s PM systems—`HAVING` filters post-aggregation for multi-project employees. Indexing `emp_id` in `project_assignments` (`CREATE INDEX idx_pa_emp ON project_assignments(emp_id)`) speeds joins, crucial for millions of assignments. In Django, `Employee.objects.annotate(project_count=Count('project_assignments')).filter(project_count__gt=3)` mirrors this. Adding `WHERE pa.status = 'completed'` refines it, and partitioning by year enhances scalability—impressing with enterprise optimization.

15. **Write a query to rank employees by salary within each department.**  
    - **Answer:**  
      ```sql
      SELECT emp_id, full_name, department, salary,
             RANK() OVER (PARTITION BY department ORDER BY salary DESC) as salary_rank
      FROM employee;
      ```  
      This ranks employees per department for Infosys evaluations—`RANK()` assigns gaps for ties (e.g., 1, 1, 3), while `DENSE_RANK()` (1, 1, 2) avoids them, offering flexibility. Indexing `department` and `salary` (`CREATE INDEX idx_dept_salary ON employee(department, salary)`) optimizes `PARTITION BY` and `ORDER BY`. In Django, raw SQL is needed (ORM lacks window support). Suggesting a materialized view or tie-breaking with `emp_id` demonstrates advanced SQL skills, impressing with enterprise reporting.

16. **Write a query to find the most frequent order amount in the last year.**  
    - **Answer:**  
      ```sql
      SELECT order_amount, COUNT(*) as frequency
      FROM orders
      WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
      GROUP BY order_amount
      ORDER BY frequency DESC
      LIMIT 1;
      ```  
      This identifies trends in Infosys’s e-commerce—e.g., $50 orders most common. Indexing `order_date` and `order_amount` (`CREATE INDEX idx_orders_date_amt ON orders(order_date, order_amount)`) speeds filtering and grouping. In Django, `Order.objects.filter(order_date__gte=timezone.now() - timedelta(days=365)).values('order_amount').annotate(freq=Count('id')).order_by('-freq')[:1]` works, but raw SQL ensures ties are handled. Partitioning by `order_date` or caching optimizes this—impressing with enterprise analytics.

17. **Write a query to find customers who haven’t placed an order in the last 6 months.**  
    - **Answer:**  
      ```sql
      SELECT c.customer_id, c.name
      FROM customers c
      LEFT JOIN orders o ON c.customer_id = o.customer_id
      AND o.order_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
      WHERE o.order_id IS NULL;
      ```  
      This finds inactive customers for Infosys’s CRM—`LEFT JOIN` with a date filter ensures only recent orders count, and `IS NULL` selects non-orderers. Indexing `customer_id` and `order_date` (`CREATE INDEX idx_orders_cust_date ON orders(customer_id, order_date)`) boosts performance. In Django, `Customer.objects.filter(orders__order_date__lt=timezone.now() - timedelta(days=180)).distinct()` approximates this. Partitioning or periodic cleanup impresses with scalability focus.

18. **Write a query to find overlapping project assignments for employees.**  
    - **Answer:**  
      ```sql
      SELECT pa1.emp_id, pa1.project_id as project1, pa2.project_id as project2,
             pa1.start_date, pa1.end_date, pa2.start_date, pa2.end_date
      FROM project_assignments pa1
      JOIN project_assignments pa2 ON pa1.emp_id = pa2.emp_id
      AND pa1.project_id < pa2.project_id
      WHERE pa1.start_date <= pa2.end_date AND pa2.start_date <= pa1.end_date;
      ```  
      This detects conflicts in Infosys’s PM tools—e.g., overlapping project dates. Indexing `emp_id`, `start_date`, and `end_date` (`CREATE INDEX idx_pa_emp_dates ON project_assignments(emp_id, start_date, end_date)`) optimizes joins. In Django, raw SQL is needed. Suggesting constraints or Gantt views impresses with enterprise utility.

19. **Write a query to pivot order counts by month for the current year.**  
    - **Answer:**  
      ```sql
      SELECT customer_id,
             SUM(CASE WHEN MONTH(order_date) = 1 THEN 1 ELSE 0 END) as Jan,
             SUM(CASE WHEN MONTH(order_date) = 2 THEN 1 ELSE 0 END) as Feb,
             SUM(CASE WHEN MONTH(order_date) = 3 THEN 1 ELSE 0 END) as Mar
      FROM orders
      WHERE YEAR(order_date) = YEAR(CURDATE())
      GROUP BY customer_id;
      ```  
      This pivots monthly order counts for Infosys dashboards—indexing `order_date` (`CREATE INDEX idx_order_date ON orders(order_date)`) speeds filtering. In Django, `annotate()` with `ExtractMonth` could work, but raw SQL supports `PIVOT` (if available). Extending to 12 months or caching impresses with enterprise reporting.

20. **Write a query to find employees whose salary increased by more than 10% in the last year.**  
    - **Answer:**  
      ```sql
      SELECT e.emp_id, e.full_name, e.salary as current_salary, sh.salary as previous_salary
      FROM employee e
      JOIN salary_history sh ON e.emp_id = sh.emp_id
      WHERE sh.change_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
      AND e.salary > sh.salary * 1.10;
      ```  
      This tracks raises in Infosys HR—indexing `emp_id` and `change_date` (`CREATE INDEX idx_sh_emp_date ON salary_history(emp_id, change_date)`) optimizes joins. In Django, raw SQL is ideal. Suggesting triggers for history or handling multiple changes (`MAX(change_date)`) impresses with enterprise focus.

---

## Database Design and Normalization (Scalable Design for Enterprise)

21. **How would you design a database schema for an e-commerce system at Infosys?**  
    - **Answer:** Tables: `Customers` (id, name, email), `Orders` (id, customer_id, order_date, total), `Products` (id, name, price), `Order_Items` (order_id, product_id, quantity), with `ForeignKey`s (`customer_id = models.ForeignKey(Customers, on_delete=models.CASCADE)`) and indexes on `customer_id`, `order_date`. Normalize to 3NF—`Order_Items` links `Orders` and `Products`, avoiding duplication—but denormalize `total` in `Orders` (`total = models.DecimalField()`) for quick reads, synced via signals or triggers. Use UUIDs (`id = models.UUIDField(primary_key=True)`) for distributed scalability and partitioning by `order_date` (`PARTITION BY RANGE`) for millions of orders. In an Infosys global platform, this balances integrity and performance—explaining constraints (e.g., `CHECK (quantity > 0)`), migrations, or sharding strategies impresses with enterprise design foresight.

22. **What is the difference between a clustered and non-clustered index, and when to use each?**  
    - **Answer:** Clustered indexes order data physically (e.g., `order_date` in `CREATE CLUSTERED INDEX idx_date ON orders(order_date)`), while non-clustered indexes are separate pointers (e.g., `customer_id` in `CREATE INDEX idx_cust ON orders(customer_id)`). Use clustered for range queries (e.g., `SELECT * FROM orders WHERE order_date BETWEEN '2024-01-01' AND '2024-12-31'`)—common in Infosys order tracking—as data is sequential. Use non-clustered for lookups (e.g., `SELECT * FROM orders WHERE customer_id = 123`), efficient for random access. In Django, `db_index=True` creates non-clustered indexes, while clustered behavior ties to primary keys in InnoDB. Discussing one-per-table limits or write overhead impresses with enterprise optimization.

23. **What is denormalization, and when would you use it in a Django project?**  
    - **Answer:** Denormalization adds redundancy—e.g., `customer_name` in `Orders` (`customer_name = models.CharField()`)—to boost read performance. Use it in read-heavy Django apps like Infosys analytics, where joins (e.g., `Orders JOIN Customers`) slow queries—`SELECT customer_name, SUM(total) FROM orders GROUP BY customer_name` becomes faster. Sync with triggers (`CREATE TRIGGER sync_name AFTER UPDATE ON customers ...`) or Django signals (`@receiver(post_save, sender=Customer)`). Risks include inconsistency—e.g., `customer_name` updates in `Customers` but not `Orders`. Explaining profiling with Django Debug Toolbar, caching alternatives, or gradual denormalization (e.g., hot data) demonstrates your enterprise performance focus, impressing with practical judgment.

24. **How do you handle many-to-many relationships in a database?**  
    - **Answer:** Use a junction table—e.g., `Employee_Projects` (emp_id, project_id)—linked via `ForeignKey`s. In Django, `ManyToManyField` (`projects = models.ManyToManyField(Project)`) auto-creates this. For Infosys PM tools, add fields like `role` (`role = models.CharField()`)—e.g., `class Employee_Projects(models.Model): emp = models.ForeignKey(Employee), project = models.ForeignKey(Project), role = models.CharField()`. Indexing `emp_id` and `project_id` (`CREATE INDEX idx_emp_proj ON employee_projects(emp_id, project_id)`) speeds queries (e.g., `SELECT * FROM employee_projects WHERE emp_id = 1`). Explaining `through` models, query optimization, or additional constraints impresses with enterprise design flexibility.

25. **What is a composite key, and when would you use it?**  
    - **Answer:** A composite key combines columns for uniqueness—e.g., `order_id, product_id` in `Order_Items` (`primary_key = (order_id, product_id)`). Use it when no single column suffices—common in Infosys junction tables (e.g., `Employee_Projects`) or natural keys (e.g., `department_code + employee_number`). In Django, `unique_together` (`class Meta: unique_together = ['order_id', 'product_id']`) enforces this. Discussing indexing (automatic with primary keys) or preferring surrogate keys for simplicity impresses with enterprise design nuance.

26. **What is a surrogate key, and why might Infosys prefer it?**  
    - **Answer:** A surrogate key is an artificial identifier—e.g., auto-incremented ID (`id = models.AutoField(primary_key=True)`) or UUID. Infosys might prefer it for simplicity (e.g., consistent joins), scalability (no collisions in distributed systems—`id = models.UUIDField()`), and decoupling data from business logic (e.g., `customer_id` vs. `email`). It prevents issues like natural key changes (e.g., `email` updates) and enumeration vulnerabilities. Explaining storage trade-offs (UUIDs larger) or hybrid approaches (e.g., `BigAutoField`) impresses with enterprise scalability focus.

27. **What is a view, and how would you use it in a Django project?**  
    - **Answer:** A view is a virtual table from a query—e.g., `CREATE VIEW active_users AS SELECT * FROM users WHERE last_login > NOW() - INTERVAL '30 days'`. In Django, use via raw SQL:  
      ```python
      class ActiveUsers(models.Model):
          class Meta:
              managed = False
              db_table = 'active_users'
      ```  
      For Infosys reporting, this simplifies queries (`ActiveUsers.objects.all()`). Materialized views (`CREATE MATERIALIZED VIEW`) enhance performance—e.g., precomputing sales stats. Discussing refresh strategies (`REFRESH MATERIALIZED VIEW CONCURRENTLY`) or access control (`GRANT SELECT`) impresses with enterprise utility.

28. **What is the difference between a schema and a database?**  
    - **Answer:** A database is the container (e.g., `infosys_db`), while a schema is the structure within it—tables, views, etc. In Infosys multi-tenant apps, separate schemas per tenant (e.g., `tenant1`, `tenant2` in `DATABASES['default']`) isolate data. In Django, `schema_name` or multi-DB configs manage this. Explaining logical vs. physical separation or schema migrations impresses with enterprise design clarity.

29. **How do you ensure data integrity in a database?**  
    - **Answer:** Use constraints—primary keys (`id = models.AutoField(primary_key=True)`), foreign keys (`customer = models.ForeignKey(Customer)`), triggers (`CREATE TRIGGER log_changes ...`), and transactions (`with transaction.atomic():`). In Django, validators (`email = models.EmailField(validators=[validate_email])`) add logic. For Infosys, foreign keys prevent orphans (e.g., orders without customers), and triggers log changes to `audit_log`. Discussing `CHECK` constraints or cascading deletes impresses with enterprise integrity focus.

30. **What is a stored procedure, and how might it benefit an Infosys application?**  
    - **Answer:** A stored procedure is precompiled SQL—e.g., `CREATE PROCEDURE update_salary(emp_id INT, new_salary DECIMAL) AS BEGIN UPDATE employee SET salary = new_salary WHERE id = emp_id; END;`. It reduces network calls, enhancing performance—call in Django via `cursor.execute('CALL update_salary(%s, %s)', [1, 50000])`. For Infosys HR, this batches salary updates efficiently. Explaining parameterization for security, transaction wrapping, or ORM limitations (raw SQL needed) impresses with enterprise optimization.

---

## Performance Optimization (Critical for Scalable Systems)

31. **How do you optimize a slow-running query in a production environment?**  
    - **Answer:** Use `EXPLAIN` to analyze plans (e.g., `EXPLAIN SELECT * FROM orders WHERE customer_id = 123`), add indexes (e.g., `CREATE INDEX idx_cust ON orders(customer_id)`), rewrite with CTEs/joins (e.g., `WITH avg AS ...`), or partition tables (`PARTITION BY RANGE(order_date)`). In an Infosys app, a slow customer order query benefits from indexing `customer_id`. Discussing profiling (Django Debug Toolbar), testing with `EXPLAIN ANALYZE`, or rollback plans impresses with enterprise caution.

32. **What are common database performance bottlenecks, and how do you address them?**  
    - **Answer:** Unindexed queries (add `CREATE INDEX`), table scans (optimize `WHERE`), lock contention (use row-level locks, short transactions). For Infosys apps, read replicas offload reads (`DATABASES['replica']`), and isolation levels (e.g., `READ COMMITTED`) balance consistency/performance. Explaining connection pooling, query tuning with `EXPLAIN`, or monitoring impresses with enterprise scalability.

33. **How does caching improve database performance, and how would you implement it in Django?**  
    - **Answer:** Caching stores results in memory (e.g., Redis), reducing DB load—e.g., caching user profiles. In Django, use `django-redis` (`CACHES = {'default': {'BACKEND': 'django_redis.cache.RedisCache'}}`) or `@cache_page(60)` for views. For Infosys, signals invalidate cache (`@receiver(post_save)`). Discussing cache eviction (LRU), consistency, or `memcached` alternatives impresses with enterprise performance focus.

34. **What is query execution plan, and how do you use it?**  
    - **Answer:** An execution plan shows query steps (e.g., index scan)—use `EXPLAIN` or `EXPLAIN ANALYZE` (e.g., `EXPLAIN SELECT * FROM orders WHERE order_date > '2024-01-01'`). In Infosys apps, fix table scans with indexes (`CREATE INDEX idx_date ON orders(order_date)`). Explaining cost analysis, `ANALYZE` for stats, or Django Debug Toolbar integration impresses with enterprise optimization.

35. **How do you handle large datasets in a Django app for reporting?**  
    - **Answer:** Paginate (`LIMIT`, `OFFSET`—e.g., `Order.objects.all()[0:10]`), index key fields, use materialized views (`CREATE MATERIALIZED VIEW sales_summary AS ...`), or aggregates (`annotate(sum=Sum('total'))`). For Infosys dashboards, Django’s `Paginator` or a data warehouse (e.g., Snowflake) scales reporting. Discussing chunked querysets (`iterator()`) or partitioning impresses with enterprise data handling.

36. **What is partitioning, and when would you use it?**  
    - **Answer:** Partitioning splits tables (e.g., by date—`CREATE TABLE orders PARTITION BY RANGE (order_date)`). Use for large tables like `Orders` in Infosys—e.g., `orders_2023` for faster queries (`SELECT * FROM orders_2023`). Explaining range/list partitioning, index management, or Django integration (`managed = False`) impresses with scalability focus.

37. **How do you reduce lock contention in a multi-user system?**  
    - **Answer:** Use row-level locking (`SELECT ... FOR UPDATE`), short transactions (`with transaction.atomic():`), and appropriate isolation levels (e.g., `READ COMMITTED`). In Infosys banking apps, minimize locked scope and retry on deadlocks (`try/except DatabaseError`). Discussing timeouts or monitoring impresses with enterprise concurrency skills.

38. **What is the difference between a B-tree and a bitmap index?**  
    - **Answer:** B-tree indexes suit range queries (e.g., `order_date`—`CREATE INDEX idx_date ON orders(order_date)`), while bitmap indexes fit low-cardinality fields (e.g., `status`—`CREATE BITMAP INDEX idx_status ON orders(status)`). For Infosys, use B-tree for `Orders.order_date`, bitmap for `Orders.status`. Explaining cardinality or write overhead impresses with enterprise optimization.

39. **How do you handle slow writes in a database?**  
    - **Answer:** Reduce indexes (e.g., drop unused), batch inserts (`INSERT INTO ... VALUES (...), (...);`), use async writes (e.g., Celery—`task.delay()`). In Infosys systems, bulk insert logs efficiently. Discussing `bulk_create` in Django or deferred constraints impresses with enterprise performance focus.

40. **What is connection pooling, and why is it important?**  
    - **Answer:** Connection pooling reuses connections, reducing overhead—e.g., `django-db-connection-pool` (`DATABASES['default']['CONN_MAX_AGE'] = 600`). Vital for Infosys’s high concurrency, preventing exhaustion (e.g., 1000 users). Explaining pool sizing or monitoring (`pg_stat_activity`) impresses with enterprise scalability.

---

## Transactions and Concurrency (Ensuring Data Integrity)

41. **What are ACID properties, and how do they apply to a banking application?**  
    - **Answer:** ACID ensures integrity: Atomicity (all steps complete), Consistency (rules maintained), Isolation (no interference), Durability (changes saved). In an Infosys banking app, a transfer (`UPDATE accounts ...`) relies on ACID—`SERIALIZABLE` isolation prevents conflicts. Explaining transaction logs or rollback impresses with enterprise reliability.

42. **How do you handle concurrency in SQL to prevent data inconsistencies?**  
    - **Answer:** Use locking (`SELECT ... FOR UPDATE`), optimistic locking (version fields—`UPDATE ... WHERE version = 1`), or isolation levels (`SET TRANSACTION ISOLATION LEVEL READ COMMITTED`). In Django, `select_for_update()` secures Infosys inventory updates. Discussing `F()` expressions or retry logic impresses with enterprise concurrency skills.

43. **What is a deadlock, and how do you prevent it?**  
    - **Answer:** A deadlock occurs when transactions wait for each other’s resources—prevent with consistent lock order (e.g., `customer` then `order`), timeouts (`SET LOCK_TIMEOUT 5000`), or short transactions. In Infosys apps, order locks systematically. Explaining detection (`SHOW ENGINE INNODB STATUS`) impresses with enterprise troubleshooting.

44. **What is the difference between READ COMMITTED and SERIALIZABLE isolation levels?**  
    - **Answer:** `READ COMMITTED` prevents dirty reads (uncommitted data), while `SERIALIZABLE` ensures full isolation (no phantom reads). Use `READ COMMITTED` for Infosys reports, `SERIALIZABLE` for transactions. Explaining performance trade-offs or Django settings (`DATABASES['default']['OPTIONS']`) impresses with enterprise knowledge.

45. **Write a transaction to transfer money between two accounts safely.**  
    - **Answer:**  
      ```sql
      BEGIN TRANSACTION;
      UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
      UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;
      IF @@ERROR = 0
          COMMIT;
      ELSE
          ROLLBACK;
      ```  
      This ensures atomicity in Infosys banking—locking rows with `FOR UPDATE` (`SELECT ... FOR UPDATE`) prevents conflicts. In Django, `with transaction.atomic():` wraps this. Discussing error handling or logging impresses with enterprise safety.

46. **What is a savepoint, and how would you use it?**  
    - **Answer:** A savepoint marks a rollback point—e.g., `SAVEPOINT sp1; ROLLBACK TO sp1;`. In Infosys batch processing, use for partial rollbacks—e.g., `with transaction.atomic(): savepoint_id = transaction.savepoint(); ...; transaction.savepoint_rollback(savepoint_id)`. Explaining nested transactions impresses with enterprise granularity.

47. **How do you implement optimistic locking in a Django app?**  
    - **Answer:** Add a `version` field (`version = models.IntegerField(default=0)`), check before updates—e.g., `UPDATE ... WHERE version = old_version`. In Django: `Model.objects.filter(id=1, version=old_v).update(version=F('version')+1, data=new_data)`. For Infosys apps, this scales low-contention updates. Discussing conflict retries impresses with enterprise concurrency.

48. **What is two-phase commit, and when might Infosys use it?**  
    - **Answer:** Two-phase commit ensures distributed transactions—prepare (all nodes agree), then commit. Infosys might use it in payment systems syncing `accounts` and `audit` databases—e.g., via a transaction coordinator. Explaining coordinator failure or alternatives (e.g., saga pattern) impresses with enterprise distributed systems knowledge.

49. **How do you log database changes for auditing?**  
    - **Answer:** Use triggers—e.g., `CREATE TRIGGER log_update AFTER UPDATE ON employee FOR EACH ROW INSERT INTO audit_log (emp_id, old_salary, new_salary, timestamp) VALUES (OLD.id, OLD.salary, NEW.salary, NOW());`. In Infosys, log `old`/`new` values, indexing `timestamp`, `emp_id`. Discussing Django signals or GDPR compliance impresses with enterprise auditing.

50. **What is the difference between a pessimistic and optimistic locking strategy?**  
    - **Answer:** Pessimistic locking locks upfront (e.g., `FOR UPDATE`—`select_for_update()` in Django), while optimistic locking checks at commit (e.g., version fields). Use pessimistic for high-contention Infosys auctions, optimistic for low-contention profiles. Explaining contention trade-offs or hybrid approaches impresses with enterprise concurrency expertise.

---

# Preparation Notes

- Focus on practical SQL skills, scalability, and optimization for Infosys’s enterprise projects—e.g., banking, e-commerce examples.  
- Practice explaining queries and optimizations (e.g., indexing, CTEs) to showcase problem-solving, tying to Django where relevant.  
- Highlight Django integration (e.g., raw SQL vs. ORM, `F()` expressions) and real-world applications to demonstrate enterprise readiness.