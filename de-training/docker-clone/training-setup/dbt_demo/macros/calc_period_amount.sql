{% macro calc_period_amount(debit, credit) %}
    {{ debit }} - {{ credit }}
{% endmacro %}