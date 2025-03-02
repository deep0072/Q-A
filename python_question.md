# Top 50 Python Questions for a Python Developer (4 Years Experience)

This document provides 50 Python-related questions with detailed answers, tailored for a developer with 4+ years of experience, such as a Django backend developer preparing for an interview (e.g., Infosys). The questions cover core Python, advanced concepts, Django-specific usage, performance optimization, and practical application scenarios.

---

## Core Python Concepts

1. **What is the difference between `__str__` and `__repr__` in Python?**  
   - **Answer:** `__str__` provides a readable, informal string representation of an object for end-users, while `__repr__` offers a formal, unambiguous representation for developers, ideally allowing the object to be recreated via `eval()`. If `__str__` isn’t defined, Python falls back to `__repr__`. For example:  
     ```python
     class Point:
         def __init__(self, x, y):
             self.x, self.y = x, y
         def __str__(self):
             return f"({self.x}, {self.y})"
         def __repr__(self):
             return f"Point({self.x}, {self.y})"
     p = Point(1, 2)
     print(str(p))  # Outputs: (1, 2)
     print(repr(p))  # Outputs: Point(1, 2)
     ```  
     In a Django model, `__str__` is commonly overridden (e.g., `return self.name`) for readable admin displays, while `__repr__` aids debugging in logs or the shell. In an Infosys context, understanding this ensures user-friendly outputs in customer-facing apps and precise diagnostics in backend systems. Explaining edge cases (e.g., `__str__` returning non-strings raises `TypeError`) or suggesting `__repr__` for serialization highlights your depth, impressing interviewers with your grasp of Python’s object representation nuances.

2. **How does Python's Global Interpreter Lock (GIL) affect multi-threading?**  
   - **Answer:** The GIL in CPython ensures only one thread executes Python bytecode at a time, preventing true parallelism for CPU-bound tasks but benefiting I/O-bound tasks where threads wait for external operations. For instance, in a Django app serving HTTP requests (I/O-bound), `threading.Thread` improves concurrency as threads yield during network delays. However, for CPU-intensive tasks like computing `sum(x**2 for x in range(10**7))`, the GIL serializes execution across threads, negating multi-core benefits. To overcome this, use `multiprocessing`:  
     ```python
     from multiprocessing import Process
     def compute(n): print(sum(x**2 for x in range(n)))
     processes = [Process(target=compute, args=(10**6,)) for _ in range(4)]
     for p in processes: p.start()
     for p in processes: p.join()
     ```  
     This spawns separate interpreters, leveraging all cores—crucial for Infosys’s data-intensive Django tasks (e.g., report generation). Discussing alternatives like `asyncio` for I/O or `numba` for JIT compilation shows your optimization skills, aligning with enterprise performance needs.

3. **What are Python decorators, and how do you create one?**  
   - **Answer:** Decorators are higher-order functions that modify or enhance other functions or classes, applied with the `@` syntax, commonly used for logging, authentication, or caching. Here’s an example:  
     ```python
     def log(func):
         def wrapper(*args, **kwargs):
             print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
             result = func(*args, **kwargs)
             print(f"Result: {result}")
             return result
         return wrapper
     @log
     def add(a, b):
         return a + b
     add(2, 3)  # Outputs: Calling add with args=(2, 3), kwargs={}; Result: 5
     ```  
     In Django, decorators like `@login_required` or `@cache_page` wrap views, leveraging Python’s dynamic nature. To preserve metadata, use `@functools.wraps(func)` in the wrapper, retaining `__name__` and docstrings—e.g., without it, `add.__name__` would be `wrapper`. Suggesting a class-based decorator for stateful behavior (e.g., counting calls) or discussing parameter passing (`@decorator(arg)`) demonstrates your mastery of this feature, impressing with its application in enterprise Django development.

4. **Explain the difference between `deepcopy` and `copy` in Python.**  
   - **Answer:** `copy.copy()` creates a shallow copy, duplicating the top-level object but sharing references to nested objects, while `copy.deepcopy()` creates a fully independent copy, recursively duplicating all nested structures. For example:  
     ```python
     import copy
     a = [[1, 2], 3]
     b = copy.copy(a)      # Shallow copy
     c = copy.deepcopy(a)  # Deep copy
     b[0][0] = 99
     print(a)  # [[99, 2], 3] (a affected)
     print(b)  # [[99, 2], 3]
     print(c)  # [[1, 2], 3]  (c independent)
     ```  
     Shallow copies are faster but risky for mutable nested data, while deep copies ensure isolation at a higher memory and time cost. In Django, `copy.copy()` might clone a form’s data for simple operations, but `deepcopy()` is safer for complex configs or nested querysets to avoid side effects. Discussing memory overhead (deepcopy’s recursion scales poorly with depth) or custom `__copy__` methods for specific classes shows your ability to optimize Python for Infosys’s enterprise apps, balancing performance and safety.

5. **What are Python’s `*args` and `**kwargs`, and when would you use them?**  
   - **Answer:** `*args` collects extra positional arguments into a tuple, and `**kwargs` gathers extra keyword arguments into a dictionary, enabling flexible function signatures. For example:  
     ```python
     def func(a, *args, **kwargs):
         print(f"a={a}, args={args}, kwargs={kwargs}")
     func(1, 2, 3, x=4, y=5)  # Outputs: a=1, args=(2, 3), kwargs={'x': 4, 'y': 5}
     ```  
     In Django, they’re prevalent in view functions (`def view(request, *args, **kwargs)`), model `__init__`, or signal receivers, allowing extensibility without breaking existing code. They’re perfect for utilities like logging wrappers or generic APIs in Infosys projects. Explaining unpacking (`func(*[1, 2], **{'x': 3})`), performance considerations (e.g., `*args` creates a new tuple each call), or their use in decorators (passing arguments through) demonstrates your practical expertise, impressing with Python’s flexibility in enterprise contexts.

---

## Advanced Python Features

6. **What are context managers, and how do you implement one?**  
   - **Answer:** Context managers manage resources like files or database connections using the `with` statement, ensuring proper setup and cleanup even if exceptions occur. You can implement them with `__enter__` and `__exit__` or `@contextmanager`:  
     ```python
     from contextlib import contextmanager
     import time
     @contextmanager
     def timer():
         start = time.time()
         try:
             yield
         finally:
             print(f"Elapsed: {time.time() - start:.2f}s")
     with timer():
         time.sleep(1)  # Outputs: Elapsed: 1.00s
     ```  
     In Django, `with transaction.atomic():` ensures database consistency, while `with open('file.txt'):` safely handles files. The `@contextmanager` approach simplifies code with `yield`, while `__enter__/__exit__` offers control (e.g., `__exit__` handling exceptions with `exc_type`). Suggesting a custom context manager for Django DB pooling or discussing `__exit__` returning `True` to suppress errors shows your ability to leverage Python for robust Infosys applications, blending theory with practical enterprise use.

7. **How do generators work in Python, and why are they memory-efficient?**  
   - **Answer:** Generators yield values one at a time using `yield`, pausing execution between calls, unlike lists that store all values in memory. For example:  
     ```python
     def fibonacci(n):
         a, b = 0, 1
         for _ in range(n):
             yield a
             a, b = b, a + b
     fib = fibonacci(5)
     print(list(fib))  # [0, 1, 1, 2, 3]
     ```  
     This is memory-efficient because only one value is held at a time, perfect for large datasets (e.g., streaming logs in Django) or infinite sequences. Compared to `[x for x in range(10**9)]`, which could crash, `(x for x in range(10**9))` scales effortlessly. In Django, `Model.objects.iterator()` uses generators for bulk queries, minimizing memory use. Explaining their stateful nature (via `next()`), or suggesting a generator-based CSV parser for Infosys’s data pipelines, demonstrates your optimization skills, impressing with enterprise-ready solutions.

8. **What is the difference between `list comprehension` and `generator expression`?**  
   - **Answer:** A list comprehension `[x for x in range(10)]` builds a complete list in memory, while a generator expression `(x for x in range(10))` yields values lazily, conserving memory. For example:  
     ```python
     import sys
     lst = [x*2 for x in range(1000)]
     gen = (x*2 for x in range(1000))
     print(sys.getsizeof(lst))  # ~9000 bytes (varies)
     print(sys.getsizeof(gen))  # ~100 bytes
     ```  
     Use list comprehensions for small, immediate results (e.g., `[user.name for user in users]` in Django), and generator expressions for iteration over large ranges (e.g., `sum(x for x in range(10**6))`). In an Infosys data processing task, generators prevent memory crashes with million-row datasets. Discussing conversion (`list(gen)`), chaining (`(x for x in gen if x > 0)`), or memory profiling with `tracemalloc` shows your ability to optimize Python for enterprise scalability, making your answer stand out.

9. **Explain Python’s `property` decorator and its use cases.**  
   - **Answer:** The `@property` decorator turns methods into getter-like attributes, with `@setter` for controlled assignment, encapsulating data access. Example:  
     ```python
     class Circle:
         def __init__(self, radius):
             self._radius = radius
         @property
         def radius(self):
             return self._radius
         @radius.setter
         def radius(self, value):
             if value >= 0:
                 self._radius = value
             else:
                 raise ValueError("Radius must be non-negative")
     c = Circle(5)
     print(c.radius)  # 5
     c.radius = 10    # Sets _radius to 10
     ```  
     In Django models, `@property` computes derived fields (e.g., `full_name` from `first_name` and `last_name`) without DB storage, ideal for admin displays or APIs. It’s great for validation, lazy computation, or read-only attributes. Suggesting `@cached_property` for expensive operations (e.g., aggregating related objects) or exploring descriptors (`__get__/__set__`) demonstrates your OOP depth, aligning with Infosys’s need for clean, maintainable codebases.

10. **What are metaclasses in Python, and when would you use them?**  
    - **Answer:** Metaclasses define how classes are created, with `type` as the default metaclass, allowing customization of class behavior. Example:  
      ```python
      import time
      class Meta(type):
          def __new__(cls, name, bases, attrs):
              attrs['created'] = time.time()
              return super().__new__(cls, name, bases, attrs)
      class MyClass(metaclass=Meta):
          pass
      print(MyClass.created)  # Timestamp of class creation
      ```  
      In Django, metaclasses like `ModelBase` dynamically map model fields to database columns. Use them in Infosys projects for framework-level tasks—e.g., auto-registering plugins or enforcing coding standards (adding required methods). Explaining their rarity in application code (favoring simpler solutions), or diving into `__prepare__` for ordered attribute dictionaries, shows your advanced Python knowledge, impressing with your understanding of under-the-hood mechanics critical for enterprise frameworks.

---

## Django-Specific Python Questions

11. **How does Django use Python’s dynamic nature in its ORM?**  
    - **Answer:** Django’s ORM exploits Python’s dynamic attributes to map model fields to database columns, enabling runtime query construction with `QuerySet`s. For example, `User.objects.filter(name='John')` translates to `SELECT * FROM users WHERE name = 'John'`, using `__getattr__` and descriptors dynamically. Define a model:  
      ```python
      from django.db import models
      class User(models.Model):
          name = models.CharField(max_length=100)
          age = models.IntegerField()
      ```  
      This adapts to backends like PostgreSQL or MySQL without static SQL. In an Infosys app, this scales CRUD operations across millions of records efficiently. Discussing lazy evaluation (`QuerySet`s execute only when evaluated, e.g., `list(qs)`), custom `Manager`s (e.g., `objects = ActiveManager()`), or raw SQL fallbacks for complex queries shows your ability to harness Python’s dynamism for enterprise Django solutions, impressing with practical insight.

12. **What are Django signals, and how are they implemented in Python?**  
    - **Answer:** Signals provide a pub/sub system for event handling, decoupling actions in Django apps. Example:  
      ```python
      from django.db.models.signals import post_save
      from django.dispatch import receiver
      from django.contrib.auth.models import User
      @receiver(post_save, sender=User)
      def user_saved(sender, instance, created, **kwargs):
          if created:
              print(f"New user created: {instance.username}")
      ```  
      `post_save` triggers after a `User` save, running `user_saved` if `created` is `True`. In an Infosys app, this might create profiles or log audits. Signals use Python’s dynamic dispatch for runtime listener registration, enhancing modularity. Suggesting custom signals (`Signal(providing_args=['user'])`), discussing performance (synchronous execution can slow requests), or proposing async signal handling with Celery demonstrates your expertise in building scalable, maintainable Django systems, aligning with enterprise needs.

13. **How does Django’s middleware system leverage Python’s function wrapping?**  
    - **Answer:** Middleware are callable classes that wrap request/response processing, using Python’s function wrapping for extensibility. Example:  
      ```python
      class CustomMiddleware:
          def __init__(self, get_response):
              self.get_response = get_response
          def __call__(self, request):
              print("Before view execution")
              response = self.get_response(request)
              print("After view execution")
              return response
      ```  
      Added to `MIDDLEWARE` in `settings.py`, this logs request phases. In Infosys Django apps, middleware might enforce authentication, rate limiting, or logging. Explaining async middleware (`async def __call__`), exception handling (`process_exception`), or request modification (e.g., adding headers) shows your ability to enhance the request lifecycle, impressing with your grasp of Django’s Pythonic architecture for enterprise use.

14. **How do you implement custom template tags in Django using Python?**  
    - **Answer:** Custom template tags extend Django’s templating, defined in a `templatetags` module:  
      ```python
      from django import template
      register = template.Library()
      @register.filter
      def add_prefix(value, prefix):
          return f"{prefix}{value}"
      # In template: {{ "hello"|add_prefix:"prefix_" }} -> "prefix_hello"
      ```  
      In an Infosys app, this might format data (e.g., currency prefixes) or create reusable UI logic. You can also write inclusion tags or simple tags with `@register.simple_tag`. Discussing tag compilation (e.g., `Node` subclasses for complex rendering), caching results, or ensuring security (escaping output with `mark_safe`) demonstrates your ability to extend Django’s frontend capabilities, impressing with practical Python application in enterprise contexts.

15. **What is the purpose of Django’s `manage.py` file, and how is it structured in Python?**  
    - **Answer:** `manage.py` is a command-line utility for Django projects, leveraging `django.core.management` to execute tasks like `runserver` or `migrate`. Its structure:  
      ```python
      import os
      import sys
      if __name__ == "__main__":
          os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
          from django.core.management import execute_from_command_line
          execute_from_command_line(sys.argv)
      ```  
      In Infosys projects, it’s the entry point for deployment scripts, migrations, or custom commands (e.g., `python manage.py my_command`). Explaining custom command creation (`BaseCommand` subclass), environment variable handling, or its role in CI/CD pipelines shows your understanding of Django’s operational backbone, impressing with enterprise-ready insights.

---

## Performance and Optimization

16. **How would you profile a Python application to identify bottlenecks?**  
    - **Answer:** Use `cProfile` or `line_profiler` to pinpoint slow code:  
      ```python
      import cProfile
      def slow_function():
          time.sleep(1)
          return sum(range(1000000))
      cProfile.run('slow_function()')  # Outputs call counts, times
      ```  
      In Django, integrate Django Debug Toolbar to profile views and queries, identifying N+1 issues or slow templates. For Infosys’s high-traffic apps, `line_profiler` (via `@profile` decorator) offers line-by-line granularity for CPU-bound tasks. Discussing visualization (e.g., `snakeviz`), sampling profilers (e.g., `py-spy`) for production, or combining with `tracemalloc` for memory leaks demonstrates your ability to optimize Python at scale, impressing with a systematic approach.

17. **What are Python’s `asyncio` and `async/await`, and how do they improve performance?**  
    - **Answer:** `asyncio` enables asynchronous programming for I/O-bound tasks, using `async def` and `await` for non-blocking execution:  
      ```python
      import asyncio
      async def fetch_data():
          await asyncio.sleep(1)  # Simulates I/O
          return "data"
      async def main():
          result = await fetch_data()
          print(result)
      asyncio.run(main())  # Outputs: data
      ```  
      In Django, `asgiref.sync` bridges sync and async code, enabling async views for concurrency (e.g., handling multiple API calls). For Infosys’s real-time systems, this boosts throughput without threading overhead. Explaining event loops, task scheduling (`asyncio.gather`), or pitfalls (e.g., blocking calls like `time.sleep`) shows your ability to leverage Python’s modern features for enterprise performance, impressing with practical application.

18. **How do you optimize Python code for memory usage?**  
    - **Answer:** Optimize memory by:  
      - Using generators instead of lists (e.g., `(x for x in range(10**6))`)  
      - Employing `__slots__` in classes to reduce instance overhead:  
        ```python
        class Point:
            __slots__ = ['x', 'y']
            def __init__(self, x, y):
                self.x, self.y = x, y
        ```  
      - Avoiding unnecessary copies with `copy` (use references)  
      - Leveraging built-ins (e.g., `set` for lookups vs. lists)  
      In Django, this minimizes footprint for large querysets or data imports. Discussing `tracemalloc` profiling, `array` module for numeric data, or `weakref` for temporary references demonstrates your ability to manage memory in Infosys’s resource-intensive apps, impressing with optimization depth.

19. **What is memoization in Python, and how would you implement it?**  
    - **Answer:** Memoization caches function results for repeated inputs, speeding up expensive computations:  
      ```python
      from functools import lru_cache
      @lru_cache(maxsize=128)
      def fibonacci(n):
          if n < 2:
              return n
          return fibonacci(n-1) + fibonacci(n-2)
      print(fibonacci(50))  # Fast due to caching
      ```  
      In Django, this optimizes recursive utilities or view calculations (e.g., cached category trees). Manual implementation with a dict (`cache = {}; return cache.setdefault(n, compute(n))`) offers flexibility. Discussing `lru_cache`’s LRU eviction, thread safety, or alternatives like Redis for distributed caching shows your ability to enhance performance in enterprise Python, impressing with practical optimization strategies.

20. **How do you handle large datasets in Python efficiently?**  
    - **Answer:** Handle large datasets with:  
      - Generators for streaming (e.g., `(line for line in file)`)  
      - `pandas` chunks for CSV processing:  
        ```python
        import pandas as pd
        for chunk in pd.read_csv('large.csv', chunksize=10000):
            process_chunk(chunk)
        ```  
      - `mmap` for memory-mapped files  
      - Django’s `iterator()` for querysets (`Model.objects.iterator()`)  
      In Infosys’s data pipelines, this prevents memory overload during imports or analytics. Explaining chunk sizing, database cursors (`server-side cursors` in PostgreSQL), or `numpy` for numeric efficiency demonstrates your ability to scale Python for enterprise data tasks, impressing with real-world solutions.

---

## Error Handling and Debugging

21. **How do you implement custom exceptions in Python?**  
    - **Answer:** Custom exceptions extend `Exception`, adding context:  
      ```python
      class CustomError(Exception):
          def __init__(self, message, code):
              super().__init__(message)
              self.code = code
      try:
          raise CustomError("Invalid input", 400)
      except CustomError as e:
          print(f"Error {e.code}: {e}")  # Error 400: Invalid input
      ```  
      In Django APIs, this enhances error responses (e.g., returning HTTP status codes). Discussing inheritance (`ValueError` for specific cases), logging integration, or exception chaining (`raise NewError from e`) shows your ability to build robust error handling for Infosys’s production systems, impressing with enterprise-ready design.

22. **What is the difference between `try/except` and `try/finally`?**  
    - **Answer:** `try/except` catches and handles exceptions, while `try/finally` ensures cleanup regardless of exceptions:  
      ```python
      try:
          file = open("data.txt")
          data = file.read()
      except FileNotFoundError:
          print("File not found")
      finally:
          file.close()  # Runs even if exception occurs
      ```  
      In Django, `finally` ensures resources (e.g., DB connections) are released. Combining them (`try/except/finally`) is common—e.g., logging errors then cleaning up. Explaining `else` (runs if no exception) or context managers as alternatives (`with`) demonstrates your error-handling sophistication, impressing with practical Python application.

23. **How does Python’s `logging` module compare to `print()` for debugging?**  
    - **Answer:** `logging` offers levels (DEBUG, INFO), formatting, and handlers, unlike `print()`’s simplicity:  
      ```python
      import logging
      logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")
      logging.debug("Debug message")  # DEBUG: Debug message
      ```  
      In Django production apps, `logging` to files or external services (e.g., Sentry) ensures traceability, while `print()` is ephemeral. Discussing handlers (`FileHandler`), log rotation, or `logging.getLogger(__name__)` for module-specific logs shows your ability to implement enterprise-grade debugging for Infosys, impressing with professional practices.

24. **What is the purpose of Python’s `pdb` debugger?**  
    - **Answer:** `pdb` provides interactive debugging with breakpoints:  
      ```python
      import pdb
      def func():
          x = 1
          pdb.set_trace()  # Breakpoint
          y = x + 2
          return y
      func()  # Use n (next), s (step), c (continue)
      ```  
      In Django, `pdb` debugs views or management commands interactively. Suggesting `ipdb` (enhanced with IPython) or post-mortem debugging (`pdb.post_mortem()`) for exceptions demonstrates your debugging prowess, impressing with hands-on problem-solving skills for enterprise development.

25. **How do you handle race conditions in Python multi-threading?**  
    - **Answer:** Use `threading.Lock` to ensure thread safety:  
      ```python
      from threading import Lock, Thread
      counter = 0
      lock = Lock()
      def safe_update():
          global counter
          with lock:
              temp = counter
              time.sleep(0.01)  # Simulate work
              counter = temp + 1
      threads = [Thread(target=safe_update) for _ in range(10)]
      for t in threads: t.start()
      for t in threads: t.join()
      print(counter)  # 10 (consistent)
      ```  
      In Django’s I/O-bound apps, this prevents data corruption. Discussing `RLock` for reentrancy, `multiprocessing` for CPU tasks (bypassing GIL), or `queue.Queue` for thread-safe data sharing shows your ability to manage concurrency in Infosys’s multi-user systems, impressing with robust solutions.

---

## Object-Oriented Programming (OOP) in Python

26. **What is the difference between classmethod and staticmethod in Python?**  
    - **Answer:** `@classmethod` takes `cls` as the first argument, accessing class state, while `@staticmethod` takes no implicit arguments, acting like a regular function:  
      ```python
      class MyClass:
          class_var = "shared"
          @classmethod
          def from_cls(cls, x):
              return cls(x)
          @staticmethod
          def util(x):
              return x * 2
      obj = MyClass.from_cls(5)
      print(MyClass.util(3))  # 6
      ```  
      In Django, `@classmethod` creates factory methods (e.g., `Model.from_json()`), while `@staticmethod` handles utilities (e.g., string formatting). Explaining their use in inheritance (`cls` adapts to subclasses) or avoiding instance creation for utilities shows your OOP finesse, impressing with practical application.

27. **How does Python implement inheritance, and what is method resolution order (MRO)?**  
    - **Answer:** Inheritance lets subclasses inherit parent attributes/methods, with MRO determining lookup order via C3 linearization:  
      ```python
      class A:
          def method(self): return "A"
      class B(A): pass
      class C(B): pass
      print(C.__mro__)  # (<class 'C'>, <class 'B'>, <class 'A'>, <class 'object'>)
      print(C().method())  # "A"
      ```  
      In Django, models inherit from `models.Model`, using MRO for field resolution. Discussing multiple inheritance (`class D(A, B)`), `super()`, or debugging with `mro()` shows your ability to manage complex OOP in Infosys’s Django projects, impressing with technical rigor.

28. **What are abstract base classes (ABCs) in Python?**  
    - **Answer:** ABCs enforce method implementation in subclasses using the `abc` module:  
      ```python
      from abc import ABC, abstractmethod
      class Shape(ABC):
          @abstractmethod
          def area(self):
              pass
      class Circle(Shape):
          def __init__(self, radius):
              self.radius = radius
          def area(self):
              return 3.14 * self.radius ** 2
      # Shape()  # TypeError: Can't instantiate abstract class
      ```  
      In Django plugins for Infosys, ABCs ensure interface compliance (e.g., a payment gateway base class). Explaining `@abstractmethod` with properties or concrete methods in ABCs shows your ability to design robust OOP systems, impressing with enterprise-grade structuring.

29. **How does Python handle multiple inheritance?**  
    - **Answer:** Python supports multiple inheritance, resolving conflicts via MRO:  
      ```python
      class A:
          def method(self): return "A"
      class B:
          def method(self): return "B"
      class C(A, B):
          pass
      print(C().method())  # "A" (A before B in MRO)
      print(C.__mro__)  # (<class 'C'>, <class 'A'>, <class 'B'>, <class 'object'>)
      ```  
      In Django, this might combine mixins (e.g., `LoginRequiredMixin`, `PermissionMixin`). Discussing `super()` for cooperative inheritance or diamond problem resolution (C3 ensures predictable order) demonstrates your OOP expertise, impressing with its relevance to complex Infosys frameworks.

30. **What is duck typing in Python?**  
    - **Answer:** Duck typing focuses on object behavior over type (“If it walks like a duck…”):  
      ```python
      def call_quack(obj):
          return obj.quack()
      class Duck:
          def quack(self): return "Quack"
      class Person:
          def quack(self): return "Mimic Quack"
      print(call_quack(Duck()))    # Quack
      print(call_quack(Person()))  # Mimic Quack
      ```  
      In Django, this enables flexible APIs (e.g., accepting any object with a `save()` method). Explaining its contrast with static typing or use in dynamic plugins for Infosys apps shows your ability to leverage Python’s flexibility, impressing with practical design insight.

---

## Functional Programming in Python

31. **What are lambda functions, and how are they used in Python?**  
    - **Answer:** Lambda functions are anonymous, single-expression functions:  
      ```python
      square = lambda x: x * x
      print(square(5))  # 25
      print(list(map(lambda x: x + 1, [1, 2, 3])))  # [2, 3, 4]
      ```  
      In Django, they’re used in querysets (`order_by(lambda x: x.name)`), `map()`, or `filter()`. Their brevity aids inline logic, but overuse can reduce readability—favor named functions for complex cases. Discussing scope (capturing outer variables) or alternatives like `partial` shows your functional programming finesse, impressing with concise yet practical applications.

32. **How do `map()`, `filter()`, and `reduce()` work in Python?**  
    - **Answer:** These functions enable functional transformations:  
      - `map()`: Applies a function to each item  
      - `filter()`: Selects items by condition  
      - `reduce()`: Combines items via a function  
      ```python
      from functools import reduce
      nums = [1, 2, 3]
      print(list(map(lambda x: x*2, nums)))      # [2, 4, 6]
      print(list(filter(lambda x: x > 1, nums)))  # [2, 3]
      print(reduce(lambda x, y: x + y, nums))     # 6
      ```  
      In Infosys’s Django apps, they process data (e.g., mapping user data to JSON). Explaining lazy evaluation with `map` (Python 3 returns iterators) or `reduce`’s initial value option enhances your answer, impressing with functional efficiency.

33. **What is a closure in Python, and how does it work?**  
    - **Answer:** A closure is a nested function retaining access to its outer scope after the outer function finishes:  
      ```python
      def outer(x):
          def inner(y):
              return x + y
          return inner
      add_five = outer(5)
      print(add_five(3))  # 8
      ```  
      In Django, closures create stateful callbacks (e.g., counters in middleware). Discussing nonlocal variables (`nonlocal x` to modify `x`) or their use in decorators shows your functional programming depth, impressing with practical enterprise applications.

34. **How does Python handle immutability in functional programming?**  
    - **Answer:** Immutable types like `tuple` and `str` can’t be changed, supporting functional purity by avoiding side effects:  
      ```python
      x = (1, 2)
      # x[0] = 3  # TypeError: 'tuple' object does not support item assignment
      y = x + (3,)  # New tuple: (1, 2, 3)
      ```  
      In Django, this ensures data consistency (e.g., immutable query params). Explaining frozen dataclasses or avoiding mutable defaults (`def func(x=[]):`) demonstrates your ability to apply functional principles in Infosys’s robust systems, impressing with clean design.

35. **What are Python’s `functools` and `itertools` modules?**  
    - **Answer:** `functools` and `itertools` enhance functional programming:  
      - `functools`: Offers `lru_cache`, `partial`  
      - `itertools`: Provides efficient iteration (e.g., `chain`, `combinations`)  
      ```python
      from functools import partial
      from itertools import chain
      add = partial(lambda x, y: x + y, 5)
      print(add(3))           # 8
      print(list(chain([1, 2], [3])))  # [1, 2, 3]
      ```  
      In Django utilities for Infosys, `partial` preconfigures functions, and `chain` merges querysets. Discussing `itertools.islice` for pagination or `functools.reduce` for aggregation shows your ability to optimize Python, impressing with enterprise tools.

---

## Testing and Development

36. **How do you write unit tests in Python using `unittest`?**  
    - **Answer:** Use `unittest` for structured testing:  
      ```python
      import unittest
      class TestMath(unittest.TestCase):
          def test_add(self):
              self.assertEqual(1 + 1, 2)
          def test_sub(self):
              self.assertEqual(3 - 1, 2)
      if __name__ == '__main__':
          unittest.main()
      ```  
      In Django, `TestCase` extends this with database support for model tests. Discussing setup/teardown (`setUp`, `tearDown`), assertions (`assertRaises`), or test discovery (`unittest discover`) shows your testing rigor, impressing with enterprise-quality assurance for Infosys.

37. **What is the difference between `unittest` and `pytest`?**  
    - **Answer:** `unittest` is built-in, requiring subclassing and explicit assertions, while `pytest` is a third-party tool with simpler syntax and auto-discovery:  
      ```python
      # unittest
      import unittest
      class Test(unittest.TestCase):
          def test_add(self):
              self.assertEqual(1 + 1, 2)
      # pytest
      def test_add():
          assert 1 + 1 == 2
      ```  
      In Django, `pytest` with `pytest-django` simplifies testing views/models. Explaining fixtures, parametrized tests (`@pytest.mark.parametrize`), or `pytest`’s plugin ecosystem (e.g., coverage) demonstrates your modern testing approach, impressing with efficiency for Infosys projects.

38. **How do you mock objects in Python tests?**  
    - **Answer:** Use `unittest.mock` to isolate dependencies:  
      ```python
      from unittest.mock import patch
      import module
      def test_function():
          with patch('module.function', return_value=42):
              assert module.function() == 42
      ```  
      In Django, mock API calls or querysets (e.g., `patch('app.models.Model.objects.get')`). Discussing `MagicMock`, side effects (`side_effect`), or `patch.object` for instance methods shows your ability to test robustly in Infosys’s complex systems, impressing with isolation techniques.

39. **What is Python’s `doctest` module, and when would you use it?**  
    - **Answer:** `doctest` tests code in docstrings:  
      ```python
      def add(a, b):
          """
          >>> add(2, 3)
          5
          """
          return a + b
      import doctest
      doctest.testmod()
      ```  
      It’s useful for simple examples or inline documentation but less common in Django (favoring `unittest`/`pytest`). Explaining its limitations (no setup/teardown) or use in tutorials for Infosys’s training materials shows your testing versatility, impressing with niche knowledge.

40. **How do you ensure code quality in a Python project?**  
    - **Answer:** Ensure quality with:  
      - Linters: `flake8`, `pylint` for style  
      - Formatters: `black`, `isort` for consistency  
      - Type checking: `mypy` for static analysis  
      - Tests: Unit/integration with `pytest`  
      - CI/CD: Automated checks (e.g., GitHub Actions)  
      In Django projects for Infosys, this maintains scalability and readability. Discussing pre-commit hooks, coverage tools (`coverage.py`), or code review processes demonstrates your commitment to enterprise-grade code, impressing with professional standards.

---

## Practical Application and Real-World Scenarios

41. **How would you implement a singleton pattern in Python?**  
    - **Answer:** A singleton ensures one instance:  
      ```python
      class Singleton:
          _instance = None
          def __new__(cls):
              if cls._instance is None:
                  cls._instance = super().__new__(cls)
              return cls._instance
      s1 = Singleton()
      s2 = Singleton()
      print(s1 is s2)  # True
      ```  
      In Django, this might manage a global config or connection pool for Infosys apps. Discussing metaclass alternatives (`class SingletonMeta(type)`), thread safety (`threading.Lock`), or `__init__` pitfalls (called multiple times) shows your design pattern expertise, impressing with enterprise applicability.

42. **How do you process a large CSV file in Python efficiently?**  
    - **Answer:** Process large CSVs with `pandas` chunks:  
      ```python
      import pandas as pd
      for chunk in pd.read_csv('large.csv', chunksize=10000):
          process_chunk(chunk)  # e.g., save to Django model
      ```  
      In Infosys’s data imports, this avoids memory overload. Alternatives include `csv` module with generators or `mmap` for memory mapping. Explaining chunk optimization (balancing I/O and processing), `dask` for parallelism, or database bulk inserts (`bulk_create`) demonstrates your ability to handle enterprise data tasks, impressing with scalability.

43. **What is Python’s `pickle` module, and when should you avoid it?**  
    - **Answer:** `pickle` serializes Python objects:  
      ```python
      import pickle
      data = {'a': 1}
      with open('data.pkl', 'wb') as f:
          pickle.dump(data, f)
      with open('data.pkl', 'rb') as f:
          loaded = pickle.load(f)  # {'a': 1}
      ```  
      In Django, it’s used for caching or session data, but avoid with untrusted sources (security risks—arbitrary code execution). Prefer JSON for interoperability. Discussing `dill` for complex objects or security mitigations (e.g., validating input) shows your practical caution, impressing with enterprise safety.

44. **How would you implement a simple caching system in Python?**  
    - **Answer:** Implement a basic cache with TTL:  
      ```python
      import time
      class Cache:
          def __init__(self):
              self.storage = {}
          def set(self, key, value, ttl=None):
              self.storage[key] = (value, time.time() + (ttl or 3600))
          def get(self, key):
              val, exp = self.storage.get(key, (None, 0))
              if time.time() > exp:
                  del self.storage[key]
                  return None
              return val
      cache = Cache()
      cache.set("key", "value", ttl=2)
      print(cache.get("key"))  # "value"
      time.sleep(2)
      print(cache.get("key"))  # None
      ```  
      In Django, use `django.core.cache` for production. Discussing thread safety (`threading.Lock`), LRU eviction (`collections.OrderedDict`), or Redis integration shows your ability to build performant Infosys systems, impressing with practical design.

45. **How do you handle configuration in a Python/Django application?**  
    - **Answer:** Use `settings.py` in Django and `python-decouple` for environment variables:  
      ```python
      from decouple import config
      API_KEY = config('API_KEY', default='default_key')
      # .env file: API_KEY=secret
      ```  
      In Infosys apps, this secures sensitive data (e.g., DB credentials). Discussing `os.environ`, 12-factor app principles, or secrets management (e.g., AWS Secrets Manager) demonstrates your enterprise configuration skills, impressing with security and scalability focus.

---

## Python Ecosystem and Tools

46. **What is `virtualenv`, and why is it important?**  
    - **Answer:** `virtualenv` creates isolated Python environments:  
      ```bash
      virtualenv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate
      pip install django
      ```  
      In Django projects for Infosys, it prevents dependency conflicts (e.g., different Django versions). Explaining `venv` (built-in alternative), `virtualenvwrapper`, or `pipenv` for dependency management shows your ecosystem mastery, impressing with development best practices.

47. **How does `pip` work, and what is `requirements.txt`?**  
    - **Answer:** `pip` installs Python packages, and `requirements.txt` lists dependencies:  
      ```bash
      pip install -r requirements.txt  # Installs listed packages
      pip freeze > requirements.txt    # Exports current environment
      # requirements.txt: django==4.2.7
      ```  
      In Django projects for Infosys, this ensures reproducibility across dev, test, and prod. Discussing version pinning, `pip install --upgrade`, or `poetry` for modern dependency management demonstrates your tooling expertise, impressing with enterprise deployment readiness.

48. **What is Python’s `asyncio` library used for in Django?**  
    - **Answer:** `asyncio` enables async views/tasks in Django via `asgiref.sync`:  
      ```python
      from django.http import HttpResponse
      import asyncio
      async def async_view(request):
          await asyncio.sleep(1)  # Simulates async I/O
          return HttpResponse("Done")
      ```  
      In Infosys’s real-time APIs, this improves I/O-bound performance (e.g., fetching external data). Explaining `async_to_sync` for legacy code, `asyncio.gather` for parallel tasks, or channels for WebSockets shows your ability to modernize Django, impressing with cutting-edge skills.

49. **How do you use Python’s `collections` module in real-world applications?**  
    - **Answer:** `collections` provides specialized data structures:  
      - `Counter`: Counts occurrences  
      - `defaultdict`: Default values  
      - `namedtuple`: Lightweight classes  
      ```python
      from collections import Counter, defaultdict
      print(Counter(['a', 'a', 'b']))  # Counter({'a': 2, 'b': 1})
      d = defaultdict(int)
      d['key'] += 1  # No KeyError
      ```  
      In Django for Infosys, `Counter` analyzes logs, `defaultdict` simplifies aggregations. Discussing `deque` for queues or `OrderedDict` for order preservation shows your ability to optimize data handling, impressing with practical utility.

50. **What are Python type hints, and how do you use them?**  
    - **Answer:** Type hints improve readability and tooling support:  
      ```python
      def add(a: int, b: int) -> int:
          return a + b
      # With mypy: mypy script.py checks types
      ```  
      In Django for Infosys, they enhance model or view code (e.g., `def get_user(id: int) -> User`). Explaining `Union`, `Optional`, or IDE integration (e.g., PyCharm) with `mypy` shows your commitment to maintainable, enterprise-grade Python, impressing with modern practices.

---

# Preparation Notes

- Focus on practical Python usage in Django backend development.  
- Be ready to explain code examples and their optimizations.  
- Highlight experience with performance, testing, and real-world scenarios.  
- Tailor answers to enterprise needs (e.g., scalability, maintainability).