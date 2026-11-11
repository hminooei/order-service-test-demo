# Order Service Style & Safety Guide

1. **Parameterized SQL Only**: Always pass query values via parameter tuples (`cursor.execute("SELECT ... WHERE col = ?", (val,))`). Never interpolate variables into SQL strings with f-strings or `%`.
2. **Explicit Outbound Timeouts**: Every `requests.get` or `requests.post` call MUST pass an explicit `timeout=` argument (for example, `timeout=5.0`).
3. **Guard Empty Collections**: Check for empty sequences before computing averages or ratios to avoid `ZeroDivisionError`.
