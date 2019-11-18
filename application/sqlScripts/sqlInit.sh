echo "DROP DATABASE gatorbarter" | sudo mysql -u root 2>/dev/null
sudo mysql -u root < master_script.sql
sudo mysql -u root gatorbarter < makeUsers.sql
sudo mysql -u root gatorbarter < makeCategories.sql
sudo mysql -u root gatorbarter < makeItems.sql
sudo mysql -u root gatorbarter < makeItemImages.sql
sudo mysql -u root gatorbarter < makeAMessage.sql
