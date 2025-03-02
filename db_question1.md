# Top 50 SQL Database Questions for a Django Backend Developer (4 Years Experience)

This document provides 50 SQL database questions with detailed answers, tailored for a Django backend developer with 4 years of experience. The questions are categorized into basic SQL concepts, Django ORM integration, performance optimization, database design, advanced concepts, and troubleshooting, reflecting real-world application development needs.

---

## Basic SQL and Database Concepts

1. **What is the difference between INNER JOIN and LEFT JOIN?**  
   - **Answer:** An `INNER JOIN` returns only the rows where there’s a match between both tables based on the join condition, effectively excluding non-matching rows from either side. A `LEFT JOIN`, however, returns all rows from the left table and the matching rows from the right table, filling in `NULL`s for any non-matching rows on the right. For example, in a Django app tracking users and their optional profiles, `INNER JOIN` might fetch only users with profiles (`SELECT * FROM users u INNER JOIN profiles p ON u.id = p.user_id`), while `LEFT JOIN` ensures all users are included, even those without profiles (`SELECT * FROM users u LEFT JOIN profiles p ON u.id = p.user_id`). This distinction is crucial in real-world scenarios where data relationships are optional—`INNER JOIN` is stricter and assumes a complete match, whereas `LEFT JOIN` preserves all left-side data, making it ideal for reporting or analytics where missing data is still meaningful. In an enterprise context like Infosys, understanding this helps design queries that balance data completeness with relevance, and explaining when to index join columns (e.g., `user_id`) demonstrates your optimization skills, impressing interviewers with practical SQL insight.

2. **Explain the difference between WHERE and HAVING clauses.**  
   - **Answer:** The `WHERE` clause filters individual rows before any grouping occurs, operating on raw table data, while the `HAVING` clause filters groups after a `GROUP BY` is applied, typically with aggregate functions like `COUNT`, `SUM`, or `AVG`. For instance, `WHERE age > 18` in `SELECT * FROM users WHERE age > 18` excludes young users before further processing, whereas `HAVING COUNT(*) > 5` in `SELECT department, COUNT(*) FROM employees GROUP BY department HAVING COUNT(*) > 5` filters out departments with fewer than six employees after aggregation. In a Django app, `WHERE` aligns with `filter()` (e.g., `User.objects.filter(age__gt=18)`), while `HAVING` requires `annotate()` and `filter()` on aggregates (e.g., `Employee.objects.values('department').annotate(count=Count('id')).filter(count__gt=5)`). This distinction is vital in enterprise reporting—e.g., an Infosys HR system might use `HAVING` to identify active departments, and explaining index use on filtered columns (e.g., `age`) or aggregate optimization shows your ability to craft efficient SQL, impressing with real-world applicability.

3. **What is database normalization and what are the common normal forms?**  
   - **Answer:** Database normalization organizes data to minimize redundancy and dependency by splitting tables and defining relationships, following rules like:  
     - **1NF (First Normal Form):** Ensures atomic values, eliminating repeating groups (e.g., splitting a `phone_numbers` column into a separate table).  
     - **2NF:** Meets 1NF and removes partial dependencies (e.g., moving `customer_name` from an `Orders` table to a `Customers` table linked by `customer_id`).  
     - **3NF:** Meets 2NF and eliminates transitive dependencies (e.g., moving `city` from `Orders` to a `Customers` table if it depends on `customer_id`, not `order_id`).  
     - **BCNF (Boyce-Codd Normal Form):** A stricter 3NF, addressing certain anomalies.  
     - **4NF/5NF:** Handle multi-valued dependencies (e.g., splitting `Student_Courses_Teachers` into separate relations).  
     In a Django e-commerce app for Infosys, normalization reduces duplication—e.g., storing product details in a `Products` table linked to `Orders` via `ForeignKey`. However, it can complicate queries with multiple joins, so partial denormalization (e.g., caching `product_name` in `Orders`) might optimize reads. Discussing trade-offs (storage vs. query speed) or Django’s `ForeignKey` implementation shows your ability to design scalable schemas, impressing with enterprise-ready database knowledge.

4. **What is the difference between DELETE, TRUNCATE, and DROP commands?**  
   - **Answer:**  
     - `DELETE` removes specific rows based on a `WHERE` condition (e.g., `DELETE FROM users WHERE inactive = true`), is transaction-safe (can be rolled back), fires triggers, and is slower due to logging.  
     - `TRUNCATE` removes all rows from a table (`TRUNCATE TABLE users`), isn’t row-specific, often lacks rollback in many databases, skips triggers, and is faster by resetting the table.  
     - `DROP` deletes the entire table, including its structure (`DROP TABLE users`), freeing storage and removing all traces.  
     In a Django app, `DELETE` aligns with `Model.objects.filter(...).delete()` for selective cleanup, `TRUNCATE` might reset test data via raw SQL, and `DROP` aligns with schema deletion in migrations. For an Infosys audit system, `DELETE` ensures traceability via triggers, while `TRUNCATE` quickly clears temporary tables. Explaining transaction logs, trigger impacts (e.g., updating audit trails), or index rebuilding post-`TRUNCATE` demonstrates your operational SQL depth, impressing with practical enterprise considerations.

5. **What is a database index and when should you use one?**  
   - **Answer:** An index is a data structure (typically a B-tree) that speeds up data retrieval by allowing quick lookups on specific columns. Use indexes on:  
     - Columns in frequent `WHERE` clauses (e.g., `user_id` in `WHERE user_id = 5`).  
     - Primary/foreign keys (e.g., `id`, `customer_id`).  
     - Columns in `ORDER BY` or `GROUP BY` (e.g., `created_at` for sorting).  
     In a Django app, `db_index=True` on a model field (e.g., `class Order(models.Model): customer_id = models.IntegerField(db_index=True)`) creates an index. However, indexes increase write overhead (`INSERT`/`UPDATE`/`DELETE` must update the index), so avoid over-indexing low-selectivity columns (e.g., `active` with mostly `true`). For Infosys’s high-traffic systems, composite indexes (e.g., `INDEX (customer_id, order_date)`) optimize complex queries. Discussing `EXPLAIN` to verify index usage or covering indexes (including all query columns) shows your ability to balance performance in enterprise apps, impressing with optimization expertise.

---

## Django ORM and Database Integration

6. **How does Django's ORM translate Python code to SQL queries?**  
   - **Answer:** Django’s ORM converts Python method calls and object operations into SQL using a query builder, abstracting database interactions via models, `QuerySet`s, and managers. For example, `User.objects.filter(age__gt=18)` becomes `SELECT * FROM users WHERE age > 18`, executed lazily only when evaluated (e.g., `list(qs)`). This abstraction adapts to backends like PostgreSQL or MySQL via database-specific drivers, with `QuerySet`s chaining operations (e.g., `.filter().order_by()`). In an Infosys app, this simplifies CRUD across millions of records, reducing boilerplate SQL. Explaining lazy evaluation (e.g., `qs = User.objects.all(); len(qs)` triggers the query), custom managers for reusable logic, or raw SQL fallbacks (`raw()`) for complex cases demonstrates your ORM mastery, impressing with enterprise-ready Django skills.

7. **What is the difference between filter() and exclude() in Django's ORM?**  
   - **Answer:** `filter()` returns objects matching specified criteria (e.g., `User.objects.filter(is_active=True)` yields active users), while `exclude()` returns objects not matching criteria (e.g., `User.objects.exclude(is_active=False)` yields active users too). Both are chainable—e.g., `User.objects.filter(age__gt=18).exclude(name='John')`. In SQL terms, `filter()` adds `WHERE` conditions (e.g., `WHERE age > 18`), while `exclude()` negates them (`WHERE NOT name = 'John'`). For an Infosys dashboard, `filter(title__contains='Django')` might fetch relevant posts, while `exclude(is_published=False)` ensures only published ones. Discussing `Q` objects for complex logic (e.g., `filter(Q(age__gt=18) | Q(name__startswith='J'))`) or query optimization with indexes on filtered fields shows your ability to craft precise, efficient queries, impressing with practical Django expertise.

8. **How can you optimize a Django query that retrieves a large number of related objects?**  
   - **Answer:** Optimize with:  
     - `select_related()`: For `ForeignKey`/`OneToOne` (e.g., `Order.objects.select_related('customer')` joins `customers` in one query).  
     - `prefetch_related()`: For `ManyToMany`/reverse `ForeignKey` (e.g., `Author.objects.prefetch_related('books')` batches related lookups).  
     - Indexes: On join columns (e.g., `customer_id`).  
     - `only()`/`defer()`: Limit fields (e.g., `Order.objects.only('id', 'total')`).  
     - `values()`/`values_list()`: Fetch specific fields (e.g., `values_list('id', flat=True)`).  
     - Pagination: Use `limit`/`offset` (e.g., `[0:10]`).  
     In an Infosys e-commerce app, this tackles N+1 issues—e.g., fetching orders with customers without hundreds of queries. Explaining Debug Toolbar for query counts, `EXPLAIN` for join efficiency, or caching results with Redis demonstrates your ability to scale Django for enterprise traffic, impressing with performance-focused solutions.

9. **Explain Django's transaction management. How would you ensure database consistency across multiple operations?**  
   - **Answer:** Django’s `transaction` module ensures consistency:  
     - `@transaction.atomic`: Decorates functions (e.g., `@transaction.atomic def transfer(...)`).  
     - `with transaction.atomic()`: Context manager (e.g., `with transaction.atomic(): order.save(); payment.save()`).  
     - `ATOMIC_REQUESTS = True` in settings: Wraps each view in a transaction.  
     - Savepoints: Partial rollbacks (e.g., `savepoint_id = transaction.savepoint()`).  
     In an Infosys banking app, transferring funds (`UPDATE accounts SET balance = balance - 100 WHERE id = 1; UPDATE accounts SET balance = balance + 100 WHERE id = 2`) within `atomic()` ensures both succeed or neither does, preventing partial updates. Discussing isolation levels (e.g., `SERIALIZABLE` for strict consistency), nested transactions, or exception handling (e.g., `try/except` within `atomic`) shows your ability to safeguard data integrity in enterprise systems, impressing with robust design.

10. **What are Django migrations and how do they work?**  
    - **Answer:** Migrations track and apply schema changes in Django:  
      1. Modify models (e.g., add `email = models.EmailField()`).  
      2. Run `makemigrations` to generate migration files (e.g., `0001_initial.py`).  
      3. Run `migrate` to apply changes to the database (e.g., `CREATE TABLE ...`).  
      4. Changes are recorded in the `django_migrations` table for versioning.  
      In an Infosys app, this ensures schema evolution—e.g., adding a `status` field without downtime. Migrations are database-agnostic (PostgreSQL, MySQL), reversible (`migrate app 0001`), and customizable (e.g., `RunSQL` for raw SQL). Explaining dependency management (`depends_on`), fake migrations (`--fake`), or testing migrations in CI demonstrates your ability to manage database evolution in enterprise Django projects, impressing with operational expertise.

---

## Performance and Optimization

11. **How would you identify and fix the N+1 query problem in Django?**  
    - **Answer:** The N+1 problem occurs when one parent query triggers N child queries—e.g., fetching all orders then querying each order’s customer separately. Identify it with Django Debug Toolbar or logging query counts. Fix with:  
      - `select_related()`: For `ForeignKey` (e.g., `Order.objects.select_related('customer')`).  
      - `prefetch_related()`: For `ManyToMany`/reverse `ForeignKey` (e.g., `Author.objects.prefetch_related('books')`).  
      - `Prefetch()`: Custom querysets (e.g., `Prefetch('books', queryset=Book.objects.filter(published=True))`).  
      In an Infosys dashboard, this reduces queries from N+1 (e.g., 101 for 100 orders) to 1 or 2, boosting performance. Discussing `EXPLAIN` to verify joins, indexing related fields (e.g., `customer_id`), or eager loading’s memory trade-offs shows your ability to optimize Django for enterprise scale, impressing with a proactive approach.

12. **What is query optimization and how would you approach it for slow queries?**  
    - **Answer:** Query optimization improves performance by:  
      1. Using `EXPLAIN` to analyze execution plans (e.g., spotting full scans).  
      2. Adding indexes on `WHERE`, `JOIN`, or `ORDER BY` columns (e.g., `CREATE INDEX ON orders(order_date)`).  
      3. Optimizing `JOIN`s (e.g., preferring `INNER` over `LEFT` when possible).  
      4. Filtering early with `WHERE` (e.g., `WHERE active = true`).  
      5. Denormalizing for read speed (e.g., caching aggregates).  
      6. Caching results (e.g., Redis).  
      7. Simplifying complex queries (e.g., breaking into subqueries).  
      In a Django app for Infosys, a slow `SELECT * FROM orders WHERE customer_id IN (...) ORDER BY order_date` might need an index on `(customer_id, order_date)` and `only('id', 'total')`. Explaining database-specific tools (e.g., PostgreSQL’s `EXPLAIN ANALYZE`), query rewriting, or profiling with Django Debug Toolbar demonstrates your optimization finesse, impressing with enterprise performance skills.

13. **When should you use raw SQL in Django instead of the ORM?**  
    - **Answer:** Use raw SQL for:  
      - Complex/inefficient ORM queries (e.g., recursive CTEs).  
      - Database-specific features (e.g., PostgreSQL’s `JSONB`).  
      - Performance-critical operations (e.g., bulk INSERTs).  
      - Functions/stored procedures (e.g., `CALL update_stats()`).  
      - Bulk operations (e.g., `INSERT INTO ... SELECT`).  
      In an Infosys analytics app, `Manager.raw('SELECT dept, AVG(salary) FROM employees GROUP BY dept')` might outperform ORM equivalents. Methods include `raw()`, `connection.cursor()`, or `RunSQL` in migrations. Discussing ORM limits (e.g., no native window functions), SQL injection safety (`%s` with params), or fallback to ORM for portability shows your ability to balance flexibility and maintainability, impressing with practical judgment.

14. **What strategies would you use to optimize database performance in a high-traffic Django application?**  
    - **Answer:** Optimize with:  
      - Indexing strategy (e.g., on `WHERE`/join columns).  
      - Connection pooling (e.g., `django-db-connection-pool`).  
      - Caching (Django’s `cache` or Redis for hot data).  
      - Read replicas (e.g., route reads to slaves).  
      - Query optimization (e.g., `select_related`).  
      - Sharding (splitting data across DBs).  
      - Async processing (e.g., Celery for writes).  
      - Model optimization (e.g., denormalize fields).  
      - Pagination (e.g., `limit 10 offset 20`).  
      - Bulk operations (e.g., `bulk_create`).  
      For an Infosys e-commerce platform, this ensures sub-second responses under heavy load. Explaining load balancing, query profiling with `EXPLAIN`, or monitoring tools (e.g., New Relic) demonstrates your ability to scale Django for enterprise traffic, impressing with a holistic approach.

15. **How would you handle database migrations in a production environment without downtime?**  
    - **Answer:** Handle zero-downtime migrations with:  
      1. Non-destructive changes (e.g., `ALTER TABLE ADD COLUMN`).  
      2. Split complex migrations (e.g., separate schema and data).  
      3. Multi-phase: Add fields, dual-write (old/new schemas), migrate data, remove old (e.g., `ALTER TABLE DROP COLUMN`).  
      4. Use replicas/failover for safety.  
      5. Schedule during low traffic.  
      6. Tools like `django-zero-downtime-migrations`.  
      7. Feature flags to toggle new logic.  
      In an Infosys app, this keeps services live—e.g., adding a `status` field with defaults, then backfilling. Discussing rollback plans (`migrate --fake`), testing in staging, or blue-green deployments shows your ability to manage production changes, impressing with enterprise reliability.

---

## Database Design and Schema

16. **What considerations would you take into account when designing a database schema for a Django application?**  
    - **Answer:** Consider:  
      - Accurate domain modeling (e.g., entities like `Order`, `Customer`).  
      - Normalization (e.g., 3NF for efficiency).  
      - Query patterns (e.g., frequent joins need indexes).  
      - Indexing (e.g., on `foreign keys`).  
      - Scalability (e.g., partitioning for growth).  
      - Performance balance (e.g., denormalize for reads).  
      - Field types (e.g., `JSONField` for flexibility).  
      - Constraints (e.g., `unique_together`).  
      - Authentication (e.g., `User` table).  
      - Migration planning (e.g., future-proof fields).  
      In an Infosys Django app, this ensures a robust schema—e.g., `Orders` linked to `Customers` via `ForeignKey`. Explaining trade-offs (e.g., normalization vs. join cost), Django’s `Meta` options, or schema evolution strategies demonstrates your design foresight, impressing with enterprise scalability.

17. **How do you model a many-to-many relationship with additional data in Django?**  
    - **Answer:** Use a `through` model:  
      ```python
      class Author(models.Model):
          name = models.CharField(max_length=100)
      class Book(models.Model):
          title = models.CharField(max_length=200)
          authors = models.ManyToManyField(Author, through='AuthorBook')
      class AuthorBook(models.Model):
          author = models.ForeignKey(Author, on_delete=models.CASCADE)
          book = models.ForeignKey(Book, on_delete=models.CASCADE)
          contribution_type = models.CharField(max_length=50)
          date_joined = models.DateField()
      ```  
      In an Infosys publishing app, this tracks author contributions (e.g., “editor” vs. “writer”) with metadata. The explicit `through` model adds flexibility beyond a default `ManyToManyField`. Discussing indexing (`author_id`, `book_id`), querying (`Author.objects.filter(authorbook__contribution_type='editor')`), or migrations for adding fields shows your ability to model complex relationships, impressing with practical Django design.

18. **Explain the use of database constraints in Django models.**  
    - **Answer:** Constraints ensure data integrity:  
      - `PRIMARY KEY`: `primary_key=True` (e.g., `id`).  
      - `FOREIGN KEY`: `ForeignKey(on_delete)` (e.g., `customer = ForeignKey(Customer, on_delete=models.CASCADE)`).  
      - `UNIQUE`: `unique=True`, `unique_together` (e.g., `unique_together = ['user', 'email']`).  
      - `CHECK`: `CheckConstraint` (e.g., `CheckConstraint(check=Q(age__gte=0), name='age_non_negative')`).  
      - `INDEX`: `indexes`, `db_index=True` (e.g., `indexes = [models.Index(fields=['name'])]`).  
      - `DEFAULT`: `default` (e.g., `status = models.CharField(default='active')`).  
      - `NOT NULL`: `null=True/False` (e.g., `name = models.CharField(null=False)`).  
      In an Infosys app, these enforce rules—e.g., `UNIQUE` prevents duplicate emails. Translated to DB-level constraints via migrations, they ensure reliability. Explaining enforcement order (e.g., `CHECK` before `UNIQUE`) or performance impacts (e.g., indexes) demonstrates your schema expertise, impressing with enterprise rigor.

19. **What are the pros and cons of using UUID vs. auto-incrementing integers as primary keys?**  
    - **Answer:**  
      - **UUID Pros:** Globally unique (no collisions in distributed systems), obscures record counts, ideal for sharding (e.g., `id = models.UUIDField(default=uuid.uuid4, primary_key=True)`).  
      - **UUID Cons:** Larger storage (16 bytes vs. 4 for int), slower indexing (random order), harder debugging (e.g., `550e8400-e29b-41d4-a716-446655440000`).  
      - **Integer Pros:** Smaller size, efficient indexing (sequential), readable, simpler joins.  
      - **Integer Cons:** Collision risk in distributed setups, exposes volume (e.g., guessing table size), vulnerable to enumeration attacks.  
      In an Infosys distributed Django app, UUIDs suit multi-region deployments, while integers fit simpler, centralized systems. Discussing hybrid approaches (e.g., `BigAutoField` for scale) or indexing strategies (e.g., B-tree vs. hash for UUIDs) shows your ability to choose wisely, impressing with enterprise design insight.

20. **How would you handle database schema changes that might break backward compatibility?**  
    - **Answer:** Manage with:  
      1. Incremental changes with compatibility layers (e.g., old/new fields coexist).  
      2. Multi-stage: Add new schema, dual-write, migrate data, remove old (e.g., `ALTER TABLE ADD new_col; UPDATE ...; ALTER TABLE DROP old_col`).  
      3. Feature flags (e.g., conditionally use new fields).  
      4. Views for consistent interfaces (e.g., `CREATE VIEW AS SELECT old_col AS new_col`).  
      5. API versioning (e.g., `/v1/` vs. `/v2/`).  
      6. Triggers for data sync (e.g., copy old to new).  
      7. Rollback plans (e.g., `migrate --fake` to revert).  
      In an Infosys app, this ensures seamless upgrades—e.g., renaming `user_name` to `full_name`. Explaining testing (e.g., staging validation), downtime risks, or data migration scripts demonstrates your ability to evolve schemas safely, impressing with enterprise reliability.

---

## Advanced SQL and Database Concepts

21. **What is the purpose of database transactions and how do ACID properties ensure data integrity?**  
    - **Answer:** Transactions group operations into a single, indivisible unit—e.g., transferring money (`UPDATE accounts ...`) succeeds or fails entirely. ACID properties ensure integrity:  
      - **Atomicity:** All operations complete or none do (e.g., rollback on failure).  
      - **Consistency:** Transitions maintain rules (e.g., balance >= 0).  
      - **Isolation:** Operations don’t interfere (e.g., uncommitted changes invisible).  
      - **Durability:** Committed changes persist (e.g., post-crash recovery).  
      In Django, `transaction.atomic()` enforces ACID—e.g., saving an order and payment together. For an Infosys banking app, this prevents partial transfers. Discussing isolation levels (e.g., `SERIALIZABLE` vs. `READ COMMITTED`) or transaction logs shows your ability to ensure reliability, impressing with enterprise-grade knowledge.

22. **Explain database locking and the difference between optimistic and pessimistic locking.****  
    - **Answer:**  
      - **Pessimistic Locking:** Locks resources preemptively (e.g., `SELECT ... FOR UPDATE`), reducing concurrency but ensuring exclusive access—Django’s `select_for_update()` does this.  
      - **Optimistic Locking:** Assumes rare conflicts, checking at commit (e.g., using a `version` field—`UPDATE ... WHERE version = 1; version += 1`).  
      In an Infosys inventory system, pessimistic locking suits high-contention stock updates, while optimistic locking scales for user profile edits. Explaining lock granularity (row vs. table), deadlock risks, or Django’s `F()` with optimistic locking demonstrates your concurrency expertise, impressing with practical application.

23. **What are database connection pools and why are they important in Django applications?**  
    - **Answer:** Connection pools reuse database connections, reducing overhead (e.g., avoiding repeated handshakes), limiting concurrency, and boosting performance. In Django, tools like `django-db-connection-pool` or `psycopg2`’s pooling manage this—e.g., `DATABASES['default']['CONN_MAX_AGE'] = 600` keeps connections alive. For an Infosys high-traffic app, this prevents connection exhaustion under load (e.g., 1000 concurrent users). Discussing pool sizing (e.g., balancing open connections vs. DB limits), connection timeouts, or monitoring with `pg_stat_activity` shows your ability to optimize Django for enterprise scale, impressing with operational insight.

24. **How would you implement database sharding in a Django application?**  
    - **Answer:** Implement sharding with:  
      1. Multiple DB configs in `settings.py` (e.g., `DATABASES = {'default': {...}, 'shard1': {...}}`).  
      2. Custom `DatabaseRouter`:  
         ```python
         class ShardRouter:
             def db_for_read(self, model, **hints):
                 return 'shard' + str(hints.get('instance').id % 2)
             def db_for_write(self, model, **hints):
                 return 'shard' + str(hints.get('instance').id % 2)
         ```  
      3. Sharding key logic (e.g., `user_id % num_shards`).  
      4. Set `DATABASE_ROUTERS = ['myapp.routers.ShardRouter']`.  
      5. Handle cross-shard queries (e.g., aggregate separately).  
      In an Infosys global app, this splits data (e.g., users by region). Explaining vertical/horizontal sharding, cross-shard joins, or Django’s multi-DB support demonstrates your scalability skills, impressing with enterprise design.

25. **What is a database deadlock and how would you prevent it?**  
    - **Answer:** A deadlock occurs when transactions wait indefinitely for each other’s locks—e.g., T1 locks row A and waits for B, while T2 locks B and waits for A. Prevent with:  
      - Consistent lock order (e.g., always lock `users` then `orders`).  
      - Timeouts (e.g., `SET LOCK_TIMEOUT 5000`).  
      - Short transactions (e.g., minimize locked duration).  
      - Proper isolation levels (e.g., `READ COMMITTED`).  
      In a Django app for Infosys, `select_for_update()` might cause deadlocks—mitigate with order and brevity. Discussing detection (`SHOW ENGINE INNODB STATUS` in MySQL) or retry logic demonstrates your ability to manage concurrency, impressing with enterprise solutions.

26. **What is a database view and how would you use it in Django?**  
    - **Answer:** A view is a virtual table from a query:  
      ```python
      migrations.RunSQL("CREATE VIEW product_summary AS SELECT p.id, p.name, AVG(r.rating) as avg_rating FROM products p LEFT JOIN reviews r ON p.id = r.product_id GROUP BY p.id, p.name;")
      class ProductSummary(models.Model):
          id = models.IntegerField(primary_key=True)
          name = models.CharField(max_length=100)
          avg_rating = models.FloatField()
          class Meta:
              managed = False
              db_table = 'product_summary'
      ```  
      In an Infosys reporting app, this simplifies complex aggregations (e.g., `ProductSummary.objects.all()`). Explaining materialized views for performance (`CREATE MATERIALIZED VIEW`), access control (e.g., `GRANT SELECT`), or refresh strategies (`REFRESH MATERIALIZED VIEW`) shows your ability to enhance Django with advanced SQL, impressing with practical optimization.

---

## Django-Specific Database Features

27. **How does Django's QuerySet lazy evaluation work and what are its advantages?**  
    - **Answer:** `QuerySet` lazy evaluation delays database execution until needed—e.g., `qs = User.objects.filter(age__gt=18)` doesn’t query until `list(qs)` or iteration. Advantages include:  
      - Chained filtering (e.g., `qs.filter(name__startswith='J')`).  
      - Query refinement (e.g., adding `.order_by('name')` later).  
      - Avoiding unused queries (e.g., `if condition: print(qs)` skips execution).  
      In an Infosys app, this optimizes resource use—e.g., building a complex `QuerySet` only executed when rendered. Discussing forcing evaluation (`len(qs)`), query caching, or avoiding over-fetching demonstrates your Django optimization skills, impressing with efficiency focus.

28. **Explain Django's custom model managers and how they can be used to organize database queries.****  
    - **Answer:** Custom managers encapsulate query logic:  
      ```python
      class PublishedManager(models.Manager):
          def get_queryset(self):
              return super().get_queryset().filter(status='published')
          def recent(self):
              return self.get_queryset().order_by('-created_at')[:5]
      class Article(models.Model):
          status = models.CharField(max_length=20)
          created_at = models.DateTimeField(auto_now_add=True)
          objects = models.Manager()  # Default
          published = PublishedManager()
      ```  
      In an Infosys blog, `Article.published.all()` fetches published articles, and `Article.published.recent()` gets the latest five. This keeps views clean and reusable—e.g., `published.filter(author=user)`. Explaining multiple managers, chaining, or indexing `status`/`created_at` shows your ability to structure Django for enterprise maintainability, impressing with clean design.

29. **How would you implement full-text search in a Django application?**  
    - **Answer:** Implement with:  
      1. PostgreSQL: `SearchVector`/`SearchQuery` (e.g., `Post.objects.annotate(search=SearchVector('title', 'content')).filter(search='django')`).  
      2. Packages: `django-haystack` with Elasticsearch or `django-watson` for simpler setups.  
      3. Simple: `Q` objects with `LIKE` (e.g., `Post.objects.filter(Q(title__icontains='django') | Q(content__icontains='django'))`).  
      In an Infosys knowledge base, PostgreSQL’s full-text search with GIN indexes (`CREATE INDEX ON posts USING GIN(to_tsvector('english', content))`) offers robust performance. Discussing ranking (`SearchRank`), external engines (e.g., Solr), or stemming trade-offs demonstrates your ability to deliver scalable search, impressing with enterprise solutions.

30. **What is Django's F() expression and how can it help prevent race conditions?**  
    - **Answer:** `F()` references field values in updates at the database level:  
      ```python
      from django.db.models import F
      Product.objects.filter(id=1).update(views=F('views') + 1)
      ```  
      This generates `UPDATE products SET views = views + 1 WHERE id = 1`, avoiding race conditions where concurrent reads/writes (e.g., fetch `views`, increment, save) might overwrite each other. In an Infosys analytics app, this ensures accurate view counts under load. Explaining atomicity, combining with `select_for_update()`, or annotating with `F()` (e.g., `annotate(total=F('price') * F('quantity'))`) shows your ability to handle concurrency, impressing with robust Django techniques.

31. **How can you implement database-level data encryption in Django?**  
    - **Answer:** Implement with:  
      - Field-level: `django-encrypted-fields` (e.g., `EncryptedCharField`).  
      - Model-level: Custom `save`/`load` (e.g., encrypt `ssn` before saving).  
      - DB-level: Transparent Data Encryption (TDE) or PostgreSQL’s `pgcrypto` (e.g., `INSERT INTO users (ssn) VALUES (pgp_sym_encrypt('123', 'key'))`).  
      - Built-in: `make_password` for passwords (e.g., `user.password = make_password('pass')`).  
      In an Infosys HR app, `pgcrypto` secures sensitive data like SSNs, with keys managed externally. Discussing key rotation, performance overhead (e.g., indexing encrypted fields), or GDPR compliance demonstrates your security expertise, impressing with enterprise-grade solutions.

32. **What are Django's database routers and how would you use them for read/write splitting?**  
    - **Answer:** Routers direct database operations:  
      ```python
      class PrimaryReplicaRouter:
          def db_for_read(self, model, **hints):
              return 'replica'  # Read from replica
          def db_for_write(self, model, **hints):
              return 'default'  # Write to primary
          def allow_relation(self, obj1, obj2, **hints):
              return True  # Allow cross-DB relations
          def allow_migrate(self, db, app_label, model_name=None, **hints):
              return db == 'default'  # Migrate only on primary
      # settings.py: DATABASE_ROUTERS = ['myapp.routers.PrimaryReplicaRouter']
      ```  
      In an Infosys app, this scales reads across replicas while writes hit the primary, configured in `DATABASES`. Explaining replication lag handling, custom routing logic (e.g., by model), or load balancing shows your ability to optimize Django for high-traffic enterprise systems, impressing with scalability focus.

---

## Testing and Development

33. **How would you test database interactions in Django applications?**  
    - **Answer:** Test with:  
      - `TestCase`: Unit tests with a test DB (e.g., `self.assertEqual(User.objects.count(), 1)`).  
      - `TransactionTestCase`: For transaction tests (e.g., testing rollbacks).  
      - Mocks: Isolate DB (e.g., `patch('django.db.models.query.QuerySet')`).  
      - Fixtures/factories: Test data (e.g., `factory_boy` for users).  
      - Assertions: Check `QuerySet`s, query counts (e.g., `assertNumQueries`).  
      In an Infosys app, this ensures reliable CRUD—e.g., testing `Order.objects.create()`. Discussing database cleanup, `pytest-django` fixtures, or query optimization in tests demonstrates your testing rigor, impressing with enterprise quality assurance.

34. **What is database mocking and when would you use it in Django tests?**  
    - **Answer:** Database mocking simulates DB responses without hitting the actual database, using `unittest.mock`:  
      ```python
      from unittest.mock import patch
      def test_user_fetch():
          with patch('myapp.models.User.objects.get', return_value=MockUser(name='John')):
              user = User.objects.get(id=1)
              assert user.name == 'John'
      ```  
      Use it for:  
      - Faster tests (no DB setup).  
      - Isolation (e.g., external DB unavailable).  
      - Edge cases (e.g., rare errors).  
      - Error testing (e.g., `DatabaseError`).  
      In an Infosys CI pipeline, this speeds up tests. Explaining mock limitations (e.g., missing real DB constraints) or `django-db-mock` alternatives shows your testing sophistication, impressing with practical efficiency.

35. **How would you handle database migrations in a team environment with multiple developers?**  
    - **Answer:** Manage with:  
      - Version control migrations (e.g., Git commits).  
      - Communicate changes (e.g., Slack updates).  
      - Avoid editing committed migrations (e.g., create new ones).  
      - Use fake migrations (`migrate --fake` for applied changes).  
      - Manage dependencies (e.g., `depends_on` in migration files).  
      - Test migrations (e.g., in staging).  
      - CI integration (e.g., run `migrate` in pipeline).  
      In an Infosys team, this prevents conflicts—e.g., merging migrations with unique names (`0002_add_field`). Discussing squash migrations, conflict resolution (manual merges), or pre-deployment validation demonstrates your collaboration skills, impressing with enterprise teamwork.

---

## Specialized Database Questions

36. **How would you implement soft delete functionality in Django models?**  
    - **Answer:** Use a custom manager and override `delete()`:  
      ```python
      from django.db import models
      from django.utils import timezone
      class SoftDeleteManager(models.Manager):
          def get_queryset(self):
              return super().get_queryset().filter(is_deleted=False)
      class SoftDeleteModel(models.Model):
          is_deleted = models.BooleanField(default=False)
          deleted_at = models.DateTimeField(null=True)
          objects = SoftDeleteManager()
          all_objects = models.Manager()  # Access all, including deleted
          def delete(self, *args, **kwargs):
              self.is_deleted = True
              self.deleted_at = timezone.now()
              self.save()
          class Meta:
              abstract = True
      class Post(SoftDeleteModel):
          title = models.CharField(max_length=100)
      ```  
      In an Infosys content app, `Post.objects.all()` excludes deleted posts, while `Post.all_objects.all()` includes them for recovery. Explaining indexing `is_deleted`, custom querysets (e.g., `deleted()`), or audit trails demonstrates your ability to preserve data, impressing with enterprise design.

37. **How would you implement row-level permissions in a Django database application?**  
    - **Answer:** Implement with:  
      - `Django Guardian`: `assign_perm('view_post', user, post)` and `check_perm()`.  
      - Custom mixin: Filter querysets (e.g., `Post.objects.filter(author=user)`).  
      - DB policies: PostgreSQL row security (e.g., `CREATE POLICY user_policy ON posts FOR SELECT TO user USING (author_id = current_user_id())`).  
      - Managers: Custom filtering (e.g., `def get_queryset(self): return super().get_queryset().filter(owner=self.request.user)`).  
      In an Infosys app, this restricts data—e.g., users see only their posts. Discussing performance (e.g., index `author_id`), `django-rules` for predicates, or combining approaches shows your ability to secure data flexibly, impressing with enterprise security.

38. **What are database triggers and how would you use them in a Django application?**  
    - **Answer:** Triggers execute SQL on events:  
      ```python
      migrations.RunSQL("""
          CREATE TRIGGER update_modified_timestamp
          BEFORE UPDATE ON products
          FOR EACH ROW
          EXECUTE PROCEDURE update_modified_column();
      """)
      # Procedure: UPDATE products SET modified_at = NOW()
      ```  
      In an Infosys app, this auto-updates `modified_at` or logs changes to an `audit_log` table. Added via `RunSQL` in migrations, triggers ensure consistency (e.g., stock updates). Explaining trigger limitations (e.g., no ORM integration), debugging (`SHOW TRIGGERS`), or alternatives (Django signals) demonstrates your advanced SQL skills, impressing with enterprise automation.

39. **What is database partitioning and how would you implement it in Django?**  
    - **Answer:** Partitioning splits large tables:  
      ```python
      migrations.RunSQL("""
          CREATE TABLE orders_partitioned (
              id SERIAL, created_at DATE, ...
          ) PARTITION BY RANGE (created_at);
          CREATE TABLE orders_2023 PARTITION OF orders_partitioned
              FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');
      """)
      class Order(models.Model):
          created_at = models.DateField()
          class Meta:
              db_table = 'orders_partitioned'
              managed = False
      ```  
      In an Infosys order system, this boosts query speed on historical data (e.g., `SELECT * FROM orders_2023`). Explaining range/list partitioning, index management, or Django’s limitations (manual SQL) shows your ability to scale large datasets, impressing with enterprise optimization.

40. **What is a materialized view and how would you use it to optimize complex queries in Django?**  
    - **Answer:** A materialized view stores precomputed query results:  
      ```python
      migrations.RunSQL("""
          CREATE MATERIALIZED VIEW product_sales_summary AS
          SELECT p.id, p.name, COUNT(o.id) as order_count
          FROM products p
          LEFT JOIN order_items oi ON p.id = oi.product_id
          LEFT JOIN orders o ON oi.order_id = o.id
          GROUP BY p.id, p.name;
      """)
      class ProductSalesSummary(models.Model):
          id = models.IntegerField(primary_key=True)
          name = models.CharField(max_length=100)
          order_count = models.IntegerField()
          class Meta:
              managed = False
              db_table = 'product_sales_summary'
      ```  
      In an Infosys dashboard, this speeds up sales reports (`ProductSalesSummary.objects.all()`). Discussing refresh (`REFRESH MATERIALIZED VIEW CONCURRENTLY`), indexing, or trade-offs (stale data vs. speed) demonstrates your ability to optimize complex queries, impressing with enterprise reporting skills.

---

## Troubleshooting and Maintenance

41. **How would you diagnose and fix slow database queries in a Django application?**  
    - **Answer:** Diagnose and fix with:  
      1. Identify: Django Debug Toolbar, logging (e.g., `settings.LOGGING`).  
      2. Analyze: `EXPLAIN` (e.g., `EXPLAIN SELECT * FROM orders WHERE customer_id = 1`).  
      3. Django fixes: `select_related`, `prefetch_related`, `only`/`defer` (e.g., `Order.objects.select_related('customer').only('total')`).  
      4. DB fixes: Add indexes (e.g., `CREATE INDEX ON orders(customer_id)`), restructure queries, denormalize (e.g., cache totals).  
      In an Infosys app, a slow order fetch might need an index and `prefetch_related('items')`. Explaining iterative tuning, `EXPLAIN ANALYZE` for execution time, or monitoring tools (e.g., `pg_stat_statements`) shows your troubleshooting expertise, impressing with enterprise performance focus.

---

## Missing Questions (42-50)

> **Note:** Questions 42-50 were not provided in the input. To complete the set, additional questions could cover topics like:  
> - Advanced indexing strategies (e.g., partial indexes).  
> - Database backup/restore in Django.  
> - Handling large-scale data imports.  
> - Query caching strategies.  
> - Database versioning.  
> - Troubleshooting replication lag.  
> - Optimizing aggregate queries.  
> - Implementing audit trails.  
> - Managing database schema conflicts.  
> If needed, I can generate these with detailed answers—please let me know!

---

# Preparation Notes

- Practice explaining concepts and code examples clearly, using real-world Django scenarios to showcase practical knowledge.  
- Focus on Django-specific optimizations (e.g., ORM vs. raw SQL, indexing) and their impact on enterprise applications like those at Infosys.  
- Be ready to adapt answers to specific project scenarios, demonstrating flexibility and problem-solving skills tailored to interviewer needs.