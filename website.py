import requests
import os

os.system("sudo apt-get install apache2")

os.system("sudo service apache2 status")

while True:
    url = input("Введите доменную ссылку, которую хотите создать, например site.com: ")
    try:
        site = requests.get(url)
        print("Сайт уже существует!")
    except:
        os.system(f"sudo mkdir /var/www/{url}")
        os.system(f"sudo chown -R $USER:$USER /var/www/{url}")
        os.system(f"sudo chmod -R 755 /var/www/{url}")
        os.system(f"echo 'Привет, доменный сайт!' | sudo tee /var/www/{url}/index.html")
        apache_config = f"""
<VirtualHost *:80>
    ServerAdmin admin@{url}
    ServerName {url}
    ServerAlias www.{url}
    DocumentRoot /var/www/{url}

    ErrorLog ${{APACHE_LOG_DIR}}/error.log
    CustomLog ${{APACHE_LOG_DIR}}/access.log combined
</VirtualHost>
        """
        with open(f"/etc/apache2/sites-available/{url}.conf", "w") as conf_file:
            conf_file.write(apache_config)
        os.system(f"sudo a2ensite {url}.conf")
        os.system("sudo service apache2 restart")
        print("Доменный сайт успешно создан!")
        break
