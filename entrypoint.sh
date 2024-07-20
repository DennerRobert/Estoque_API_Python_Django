#!/usr/bin/env bash
# wait-for-it.sh

until pg_isready -h "$POSTGRES_HOST"; do
	echo "Esperando o Postgres iniciar..."
	sleep 1
done

echo "Postgres iniciado - executando comandos..."

echo "Criando migrações..."
python manage.py makemigrations

echo "Aplicando migrações..."
python manage.py migrate

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "Criando superusuário..."
python manage.py shell <<EOF
from django.contrib.auth.models import User
from django.core.management import CommandError

username = 'admin'
email = 'admin@example.com'
password = 'adminpass'

try:
    User.objects.get(username=username)
except User.DoesNotExist:
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superusuário criado com sucesso.")
else:
    print("Superusuário já existe.")
EOF

if [ "$DEBUG" = "False" ]; then
	echo "Iniciando: Modo de produção"
	gunicorn --bind 0.0.0.0:8000 estoque.wsgi:application
else
	echo "Iniciando: Modo de desenvolvimento"
	python manage.py runserver 0.0.0.0:8000
fi


