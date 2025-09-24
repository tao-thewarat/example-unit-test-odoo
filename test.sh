 OPTIONS="bash -lc 'odoo -c /etc/odoo/odoo.conf -d odoo_test -i account_ext --stop-after-init && pytest --odoo-database=odoo_test --odoo-addons-path=/mnt/addons --cov=/mnt/addons/account_ext --cov-config=/mnt/.coveragerc --cov-report=term-missing /mnt/addons/account_ext/tests -v'" \
docker compose -f docker-compose.test.yml up --build --abort-on-container-exit tests
