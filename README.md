# drama-db

<h2>INSTALLATION INSTRUCTIONS</h2>
<h3>Installing GULP</h3>
<ul>
	<li>Create gulpfile.js according to <a href="https://stackoverflow.com/questions/38937095/no-gulpfile-found">these</a> instructions.</li>
	<li>npm install gulp</li>
	<li>pip install django-gulp</li>
	<li>npm install all of the requirements in the gulpfile.js file like <a href="https://stackoverflow.com/questions/43586635/how-to-install-all-required-modules-from-gulpfile-js">this</a>.</li>
</ul>
<p>Please note, gulp must be version 4.x or it won't work! Follow instructions <a href="https://github.com/pattern-lab/edition-node-gulp/wiki/Updating-to-Gulp-4">here</a> to uninstall previous version and install new version.</p>
<h3>Beautiful Soup</h3>
<ul>
	<li>pip install requests</li>
	<li>pip install beautifulsoup4</li>
</ul>
<h2>RUNNING ENVIRONMENT</h2> 
<h3>Run Website</h3>
<ul>
	<li>source env/bin/activate</li>
	<li>python manage.py runserver</li>
	<li>navigate to 127.0.0.1:8000</li>
</ul>
<h3>Make Migrations</h3>
<ul>
	<li>python manage.py makemigrations</li>
	<li>python manage.py migrate</li>
</ul>
<h3>Cron Jobs</h3>
<ul>
	<li>https://stackoverflow.com/questions/15395479/why-ive-got-no-crontab-entry-on-os-x-when-using-vim</li>
	<li>https://django-cron.readthedocs.io/en/latest/installation.html</li>
</ul>

<h2>RESOURCES</h2>
<p>Setting up the <a href="https://virtualenv.pypa.io/en/latest/userguide/">virtual environment</a>
	<p>Postgres app <a href="https://postgresapp.com/">here</a></p>
	<p>Setting up Postgres and making migrations <a href="https://medium.com/agatha-codes/painless-postgresql-django-d4f03364989">here</a></p>
	<p>Setting up BeautifulSoup in order to scrape web pages <a href="https://www.digitalocean.com/community/tutorials/how-to-work-with-web-data-using-requests-and-beautiful-soup-with-python-3">here</a></p>
