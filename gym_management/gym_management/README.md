Gym Management (Frappe / ERPNext)
A custom Frappe app that manages gym members, membership plans, class sessions, bookings, waitlists and check-ins. Billing is delegated to ERPNext (Customer, Item, Sales Invoice,Payment Entry) instead of being re-implemented.

Requirements
Python 3.10+
Frappe Framework v15.122.0
ERPNext v15.122.0 
bench CLI

Installation that i follow
bench init my-bench
cd my-bench
bench new-site gym.localhost --install-app erpnext
bench --site gym.localhost install-app gym_management
sudo service redis-server start
sudo service mariadb start
bench --site gym.localhost set-config developer_mode 1
bench start 

for anyone to intall it:
bench new-site gym.localhost
bench --site gym.localhost install-app erpnext
bench get-app https://github.com/zainabmarzoukibrahim/gym_management.git
bench --site gym.localhost install-app gym_management
bench start

How to run tests:
bench --site gym.localhost run-tests --app gym_management
OR
bench --site gym.localhost run-tests --module "مسار الملف"