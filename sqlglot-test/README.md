# Find source tables (simple)

```python
# bi.mt5_deal AS d
# bi.mt5_user AS u
for table in parse_one("""
    INSERT INTO bi.trades
    SELECT d.dt
         , d.login
         , SUM(d.profit) AS profit
      FROM bi.mt5_deal d
      JOIN bi.mt5_user u
        ON d.login = u.login
     GROUP BY 1,2
    """,
    dialect="bigquery").find(exp.Select).find_all(exp.Table):
    print(table)
```
# Find source tables (using scope)

```py
from sqlglot.optimizer.scope import build_scope

ast = parse_one("""
WITH x AS (
  SELECT a FROM y
)
SELECT a FROM x
""")

root = build_scope(ast)
for scope in root.traverse():
    print(scope)

# Scope<SELECT a FROM y>
# Scope<WITH x AS (SELECT a FROM y) SELECT a FROM x>

tables = [
    source

    # Traverse the Scope tree, not the AST
    for scope in root.traverse()

    # `selected_sources` contains sources that have been selected in this scope, e.g. in a FROM or JOIN clause.
    # `alias` is the name of this source in this particular scope.
    # `node` is the AST node instance
    # if the selected source is a subquery (including common table expressions),
    #     then `source` will be the Scope instance for that subquery.
    # if the selected source is a table,
    #     then `source` will be a Table instance.
    for alias, (node, source) in scope.selected_sources.items()
    if isinstance(source, exp.Table)
]

for table in tables:
    print(table)

# y  -- Success!
```

```py
from sqlglot.optimizer.scope import build_scope

ast = parse_one("""
WITH x AS (
  SELECT d.deal
    FROM bi.mt5_deal AS d
)
SELECT a FROM x
""")

root = build_scope(ast)
for scope in root.traverse():
    print(scope)

# Scope<SELECT a FROM y>
# Scope<WITH x AS (SELECT a FROM y) SELECT a FROM x>

tables = [
    source

    # Traverse the Scope tree, not the AST
    for scope in root.traverse()

    # `selected_sources` contains sources that have been selected in this scope, e.g. in a FROM or JOIN clause.
    # `alias` is the name of this source in this particular scope.
    # `node` is the AST node instance
    # if the selected source is a subquery (including common table expressions),
    #     then `source` will be the Scope instance for that subquery.
    # if the selected source is a table,
    #     then `source` will be a Table instance.
    for alias, (node, source) in scope.selected_sources.items()
    if isinstance(source, exp.Table)
]

for table in tables:
    print(table)
# bi.mt5_deal AS d
```


# Find target table

```python



```


# Parsing .sql file

```python


```
