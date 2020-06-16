python manage.py test testapp 2>test_result.log >/dev/null
test_result=$(tail -n 2 test_result.log | head -n 1)
echo "$test_result"
if [ "$test_result" = "FAILED (failures=2, errors=1, skipped=1, expected failures=1, unexpected successes=1)" ]; then
    echo "... PASS"
else
    exit 1
fi

python manage.py test testapp --debug-sql 2>test_debug_sql_result.log >/dev/null
test_result=$(tail -n 2 test_debug_sql_result.log | head -n 1)
echo "$test_result"
if [ "$test_result" = "FAILED (failures=2, errors=1, skipped=1, expected failures=1, unexpected successes=1)" ]; then
    echo "... PASS with --debug-sql"
else
    exit 1
fi
