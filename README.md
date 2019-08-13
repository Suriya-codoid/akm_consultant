# akm_consultant

STEP-1: Make sure python has been installed in your system. in this prject am using python version is 2.7.13.

STEP-2: install virtualenv by using pip install virtualenv or easy-install virstualenv

      1.create the virtualenv by using follwong command--->: python -m virtualenv envname
      2.activate the virtual env by using following command--->: source ~/path to the virtualenv/bin/activate
STEP-3: Install the packages from the requirement.txt file by using following command: pip install -r requirement.txt

STEP-4: setup your database credentials in config->settings.py file as below:

      db_uri='mysql+pymysql://username:password@localhost:3306/db_name'
STEP-5: Migrate the database from the below commands: 1.python manage.py db init 2.python manage.py db migrate 3.python manage.py db upgrade

STEP-6: in this project i have created the tech support user. we can define which user should become a tech support. we have to define the user in .env file.

      when the defined user going to signup automatically that user assigned as techsupport.
STEP-7: run the project by following command:

      python manage.py runserver
STEP-8 navigate to your localhost:5000. the project will default running on port 5000. if we want to change the port we can use python manage.py runserver --port=port number
