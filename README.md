# drama-db

<h2>INSTALLATION INSTRUCTIONS</h2>
<h4>Installing GULP</h4>
<ul>
	<li>Create gulpfile.js according to <a href="https://stackoverflow.com/questions/38937095/no-gulpfile-found">these</a> instructions.</li>
	<li>npm install gulp</li>
	<li>pip install django-gulp</li>
	<li>npm install all of the requirements in the gulpfile.js file like <a href="https://stackoverflow.com/questions/43586635/how-to-install-all-required-modules-from-gulpfile-js">this</a>.</li>
</ul>
<p>Please note, gulp must be version 4.x or it won't work! Follow instructions <a href="https://github.com/pattern-lab/edition-node-gulp/wiki/Updating-to-Gulp-4">here</a> to uninstall previous version and install new version.</p>
<h3>Beautiful Soup</h3>
<code>pip install requests</code>
<code>pip install beautifulsoup4</code>
<h2>RUNNING ENVIRONMENT AND COMMANDS</h2> 
<h4>Run Website</h4>
<code>source env/bin/activate</code><br>
<code>python manage.py runserver</code><br>
<code>navigate to 127.0.0.1:8000</code>
<h4>Make Migrations</h4>
<code>python manage.py makemigrations</code><br>
<code>python manage.py migrate</code>
<h4>Run Cron Jobs</h4>
	<code>python manage.py runcrons --force</code>	
<h4>Load Fixtures</h4>
	<code>python manage.py loaddata fixture_name</code></code>
<h4>Reference</h4>
	<li>https://stackoverflow.com/questions/15395479/why-ive-got-no-crontab-entry-on-os-x-when-using-vim</li>
	<li>https://django-cron.readthedocs.io/en/latest/installation.html</li>

<h2>RESOURCES</h2>
<p>Setting up the <a href="https://virtualenv.pypa.io/en/latest/userguide/">virtual environment</a>
	<p>Postgres app <a href="https://postgresapp.com/">here</a></p>
	<p>Setting up Postgres and making migrations <a href="https://medium.com/agatha-codes/painless-postgresql-django-d4f03364989">here</a></p>
	<p>Setting up BeautifulSoup in order to scrape web pages <a href="https://www.digitalocean.com/community/tutorials/how-to-work-with-web-data-using-requests-and-beautiful-soup-with-python-3">here</a></p>
