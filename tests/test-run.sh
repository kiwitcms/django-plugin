python manage.py test testapp 2>test_result.log >/dev/null
test_result=$(tail -n 1 test_result.log)
echo "$test_result"
if [ "$test_result" = "FAILED (failures=2, errors=1, skipped=1, expected failures=1, unexpected successes=1)" ]; then
    echo "... PASS"
else
    exit 1
fi
