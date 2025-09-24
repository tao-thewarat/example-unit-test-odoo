FROM odoo:18

USER root

# Install production dependencies
RUN pip3 install --no-cache-dir pytest pytest-odoo pytest-cov --break-system-packages

USER odoo

# Setup Odoo
ADD --chown=odoo:odoo addons /mnt/imbase/addons
ADD --chown=odoo:odoo odoo.conf /etc/odoo/odoo.conf

USER root
RUN rm -rf /mnt/requirements.txt

USER odoo

EXPOSE 8069

CMD ["/usr/bin/odoo", "-c", "/etc/odoo/odoo.conf"]
