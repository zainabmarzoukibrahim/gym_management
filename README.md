### Gym Management

Gym Management System

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app gym_management
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/gym_management
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### CI

This app can use GitHub Actions for CI. The following workflows are configured:

- CI: Installs this app and runs unit tests on every push to `develop` branch.
- Linters: Runs [Frappe Semgrep Rules](https://github.com/frappe/semgrep-rules) and [pip-audit](https://pypi.org/project/pip-audit/) on every pull request.

##how to open app folder:
gym_management.gym_management

Gym Management (Frappe / ERPNext) A custom Frappe app that manages gym members, membership plans, class sessions, bookings, waitlists and check-ins. Billing is delegated to ERPNext (Customer, Item, Sales Invoice,Payment Entry) instead of being re-implemented.

Requirements Python 3.10+ Frappe Framework v15.122.0 ERPNext v15.122.0 bench CLI

Installation that i follow 
bench init my-bench 
cd my-bench bench new-site gym.localhost --install-app erpnext 
bench --site gym.localhost install-app gym_management 
sudo service redis-server start 
sudo service mariadb start 
bench --site gym.localhost set-config developer_mode 1
bench start

for anyone to intall it: bench new-site gym.localhost bench --site gym.localhost install-app erpnext bench get-app https://github.com/zainabmarzoukibrahim/gym_management.git bench --site gym.localhost install-app gym_management bench start

How to run tests: bench --site gym.localhost run-tests --app gym_management OR bench --site gym.localhost run-tests --module "مسار الملف"

###assumptions 

1. Membership Freeze and End Date
Decision: Frozen days will be added to the membership's end_date.
Reason: Freezing a membership pauses its validity period, so the member does not lose the frozen days from their active membership duration.
2. Conditional Display of Membership Fields
Decision: The "freeze button" and "sales_invoice" are displayed only when the document is submitted ("docstatus == 1").
Reason: because thise should relevant only after the membership document has been submitted

3. Email and Phone Number Validation
Decision: Used Frappe's built-in field options to validate email addresses and phone numbers instead of implementing custom validation code.
Reason: This reduces redundant code and relies on Frappe's built-in validation features.
4. Membership Expiry Reminder
Decision: Set the membership expiry reminder to be sent 3days before the membership's end date.
Reason: This gives members enough time to renew their memberships before they expire.
Trainer Specialities
5- Create "Gym Speciality" as the main DocType and "Trainer Speciality" as a Child DocType linked to "Gym Speciality", because the "specialties" field in "Gym Trainer" is a Table MultiSelect field, which requires a Child DocType.

### License

mit
