from __future__ import with_statement
from fabric.api import settings, env, prefix
from fabric.contrib.console import confirm
from fabric.operations import sudo, run, local, put
from fabric.context_managers import cd
import os

env.hosts = [os.environ.get('CPIMS_APP_HOST')]
env.user = os.environ.get('CPIMS_APP_USER')
env.key_filename = os.environ.get('CPIMS_KEY_FILENAME')
src_dir = os.environ.get('CPIMS_SRC_DIR')
deploy_dir = os.environ.get('CPIMS_DEPLOY_DIR')
target_dir = os.environ.get('CPIMS_TARGET_DIR')
cpims_venv = os.environ.get('CPIMS_VENV')
cpims_host = os.environ.get('CPIMS_DB_HOST')
cpims_password = os.environ.get('CPIMS_DB_PASSWORD')
cpims_db = os.environ.get('CPIMS_DB')
cpims_port = os.environ.get('CPIMS_DB_PORT')
cpims_dbuser = os.environ.get('CPIMS_DB_USER')
cpims_debug = os.environ.get('CPIMS_DEBUG')

def install_pg_bdr():
    "setting up postgres-bdr as the default postgres db"
    run("sudo yum install -y epel-release")
    run("sudo yum install -y https://download.postgresql.org/pub/repos/yum/9.4/redhat/rhel-7-x86_64/pgdg-centos94-9.4-3.noarch.rpm")
    run("sudo yum install -y --nogpgcheck http://packages.2ndquadrant.com/postgresql-bdr94-2ndquadrant/yum-repo-rpms/postgresql-bdr94-2ndquadrant-redhat-latest.noarch.rpm")
    with settings(warn_only=True):
        result = run("sudo yum -t check-update")
        if result.return_code ==  100:
            run('sudo yum update -y')
    run("sudo yum install -y --nogpgcheck postgresql-bdr94-bdr postgresql-bdr94-devel")
    run("sudo /usr/pgsql-9.4/bin/postgresql94-setup initdb")
    run("sudo systemctl start postgresql-9.4.service")
    run("sudo systemctl enable postgresql-9.4.service")
    source = "%s/configs/postgresql/*" %(os.environ.get('PWD'),)
    put(local_path = source, remote_path ='/tmp/')
    run("sudo -u postgres cp /tmp/pg_hba.conf /var/lib/pgsql/9.4-bdr/data/")
    run("rm /tmp/pg_hba.conf")
    run("sudo -u postgres cp /tmp/postgresql.conf /var/lib/pgsql/9.4-bdr/data/")
    run("rm /tmp/postgresql.conf")
    run("sudo systemctl restart postgresql-9.4.service")


def install_virtualenv():
    run("sudo yum install -y epel-release")
    run('sudo yum update -y')
    run("sudo yum install -y gcc python2-pip python-devel python-setuptools memcached")
    run("sudo pip install --upgrade pip")
    run("sudo pip install virtualenv virtualenvwrapper uwsgi")
    run("/usr/bin/echo 'export WORKON_HOME=~/.envs' >> /home/vagrant/.bash_profile")
    #run("source /home/vagrant/.bash_profile")
    run("/usr/bin/echo 'source /usr/bin/virtualenvwrapper.sh' >> /home/vagrant/.bash_profile")
    run("mkvirtualenv %s" %(cpims_venv))

def install_cpims():
    print "creating archive ..."
    if os.path.isdir(deploy_dir):
        local('rm -rf %s' %deploy_dir)
    local('mkdir %s' %deploy_dir)
    local('tar --exclude=cpims/configs --exclude=cpims/.git --exclude=.gitignore --exclude=*pyc --exclude=fabfile.py* -C %s -czvf %s/cpims.tar.gz cpims' %(src_dir,deploy_dir,))
    put('%s/cpims.tar.gz' %(deploy_dir,), target_dir)
    run('rm -rf %s/cpims' %(target_dir,))
    run('tar -xzvf cpims.tar.gz')
    run('rm cpims.tar.gz')
    local('rm -rf %s' %deploy_dir)
    with cd('/home/vagrant/cpims'), prefix('workon %s' %(cpims_venv)):
        run('pip install -r requirements.txt')


def install_pg_configuration():
    "install the pg connection details"
    with cd("/home/vagrant"):
        run("/usr/bin/echo 'CPIMS_HOST=%s' >> .bash_profile" %(cpims_host))
        run("/usr/bin/echo 'CPIMS_PASSWORD=%s' >> .bash_profile" %(cpims_password))
        run("/usr/bin/echo 'CPIMS_DB=%s' >> .bash_profile" %(cpims_db))
        run("/usr/bin/echo 'CPIMS_PORT=%s' >> .bash_profile" %(cpims_port))
        run("/usr/bin/echo 'CPIMS_DBUSER=%s' >> .bash_profile" %(cpims_dbuser))
        run("/usr/bin/echo 'CPIMS_DEBUG=%s' >> .bash_profile" %(cpims_debug))
        run("/usr/bin/echo 'export CPIMS_HOST' >> .bash_profile")
        run("/usr/bin/echo 'export CPIMS_PASSWORD' >> .bash_profile")
        run("/usr/bin/echo 'export CPIMS_DB' >> .bash_profile")
        run("/usr/bin/echo 'export CPIMS_PORT' >> .bash_profile")
        run("/usr/bin/echo 'export CPIMS_DBUSER' >> .bash_profile")
        run("/usr/bin/echo 'export CPIMS_DEBUG' >> .bash_profile")

def setup_pg():
    "install the pg users"
    with settings(sudo_user='postgres') and cd('/var/lib/pgsql'):
        sudo("psql -c \"create user %s with encrypted password '%s'\"" %(cpims_dbuser, cpims_password), user='postgres')
        sudo("psql -c \"create database %s owner %s\"" %(cpims_db, cpims_dbuser), user='postgres')


def install_fixtures():
    "installing basic fixtures for cpims"
    with cd('%s/cpims' %(target_dir)), prefix('workon %s' %(cpims_venv)):
        run("python manage.py makemigrations")
        run("python manage.py migrate cpovc_auth")
        run("python manage.py migrate")
        run("python manage.py loaddata cpovc_auth/fixtures/initial_data.json")
        run("python manage.py loaddata cpovc_main/fixtures/initial_user.json")
        run("python manage.py loaddata cpovc_main/fixtures/initial_geo.json")
        run("python manage.py loaddata cpovc_main/fixtures/list_general.csv.json")
        run("python manage.py loaddata cpovc_main/fixtures/initial_facility1.csv.json")
        run("python manage.py loaddata cpovc_main/fixtures/initial_facility2.csv.json")
        run("python manage.py loaddata cpovc_main/fixtures/olmis_forms.csv.json")
        run("python manage.py loaddata cpovc_main/fixtures/olmis_assessment.csv.json")
        run("python manage.py loaddata cpovc_main/fixtures/olmis_household_assessment_3.json")
        run("python manage.py loaddata cpovc_main/fixtures/olmis_registry.json")
        run("python manage.py loaddata cpovc_main/fixtures/eligibility.json")
        run("python manage.py loaddata cpovc_main/fixtures/olmis_services.csv.json")
        run("python manage.py loaddata cpovc_main/fixtures/ovc_form_type_id.json")
        run("python manage.py loaddata cpovc_main/fixtures/olmis_services.csv.json")
        run("python manage.py loaddata cpovc_main/fixtures/ovc_form_type_id.json")
        run("python manage.py createsuperuser")
        run("python manage.py loaddata cpovc_main/fixtures/initial_org_unit.csv.json")
        run("python manage.py loaddata cpovc_main/fixtures/initial_org_unit_contact.csv.json")
        run("python manage.py loaddata cpovc_main/fixtures/initial_org_unit_geo.csv.json")
        run("python manage.py loaddata cpovc_main/fixtures/initial_persons.csv.json")
        run("python manage.py loaddata cpovc_main/fixtures/initial_person_type.csv.json")
        run("python manage.py loaddata cpovc_main/fixtures/initial_persons_externalids.csv.json")
        run("python manage.py loaddata cpovc_main/fixtures/initial_persons_geo.csv.json")
        run("python manage.py loaddata cpovc_main/fixtures/initial_persons_org_units.csv.json")

def create_super_user():
    with cd('%s/cpims' %(target_dir)), prefix('workon %s' %(cpims_venv)):
        #run("python manage.py createsuperuser")
        run("python manage.py loaddata cpovc_main/fixtures/initial_org_unit.csv.json")
        run("python manage.py loaddata cpovc_main/fixtures/initial_org_unit_contact.csv.json")
        run("python manage.py loaddata cpovc_main/fixtures/initial_org_unit_geo.csv.json")
        run("python manage.py loaddata cpovc_main/fixtures/initial_persons.csv.json")
        run("python manage.py loaddata cpovc_main/fixtures/initial_person_type.csv.json")
        run("python manage.py loaddata cpovc_main/fixtures/initial_persons_externalids.csv.json")
        run("python manage.py loaddata cpovc_main/fixtures/initial_persons_geo.csv.json")
        run("python manage.py loaddata cpovc_main/fixtures/initial_persons_org_units.csv.json")


def configure_uwsgi():
    handle = open('%s/configs/uwsgi/cpims.ini' %(os.environ.get('PWD')), 'w')
    handle.write('[uwsgi]\n')
    handle.write('project = cpims\n')
    handle.write('username = %s\n' %(env.user,))
    handle.write('base = /home/%(username)\n')
    handle.write('chdir = %(base)/%(project)\n')
    handle.write('home = %%(base)/.envs/%s\n' %(cpims_venv,))
    handle.write('module = %(project).wsgi:application\n')
    handle.write('master = true\n')
    handle.write('processes = 5\n')
    handle.write('uid = %(username)\n')
    handle.write('socket = /run/uwsgi/%(project).sock\n')
    handle.write('chown-socket = %(username):nginx\n')
    handle.write('chmod-socket = 660\n')
    handle.write('vacuum = true\n')
    handle.write('env = CPIMS_HOST=%s\n' %(cpims_host,))
    handle.write('env = CPIMS_DB=%s\n' %(cpims_db,))
    handle.write('env = CPIMS_DEBUG=%s\n' %(cpims_debug,))
    handle.write('env = CPIMS_PORT=%s\n' %(cpims_port,))
    handle.write('env = CPIMS_DBUSER=%s\n' %(cpims_dbuser,))
    handle.write('env = CPIMS_PASSWORD=%s\n' %(cpims_password,))
    handle.close()

def install_uwsgi():
    run("sudo mkdir /etc/uwsgi")
    run("sudo mkdir /etc/uwsgi/sites")
    source = "%s/configs/uwsgi/cpims.ini" %(os.environ.get('PWD'),)
    put(local_path = source, remote_path ='/tmp/')
    run("sudo cp /tmp/cpims.ini /etc/uwsgi/sites/")
    run("rm /tmp/cpims.ini")
    source = "%s/scripts/uwsgi/uwsgi.service" %(os.environ.get('PWD'),)
    put(local_path = source, remote_path ='/tmp/')
    run("sudo cp /tmp/uwsgi.service /etc/systemd/system/")
    run("rm /tmp/uwsgi.service")
    run("sudo systemctl restart uwsgi")
    run("sudo systemctl enable uwsgi")

def install_nginx():
    run("sudo yum install -y nginx")
    source = "%s/configs/nginx/nginx.conf" %(os.environ.get('PWD'),)
    put(local_path = source, remote_path ='/tmp/')
    run("sudo cp /tmp/nginx.conf /etc/nginx/")
    run("rm /tmp/nginx.conf")
   
    run("sudo chmod 750 /home/%s" %(env.user,))
    run("sudo groupmems -a nginx -g %s" %(env.user,))
    run("sudo systemctl restart nginx")
    run("sudo systemctl enable nginx")

def configure_se_linux():
    run("sudo setenforce 0")
    source = "%s/configs/selinux/config" %(os.environ.get('PWD'),)
    put(local_path = source, remote_path ='/tmp/')
    run("sudo cp /tmp/config /etc/selinux/config")
    run("rm /tmp/config")


def deploy():
    install_pg_bdr()
    setup_pg()
    install_pg_configuration()
    install_virtualenv()
    install_cpims()
    install_fixtures()
    configure_uwsgi()
    configure_se_linux()
    install_nginx()
    install_uwsgi()
    
