sudo mysql -u root < master_script.sql
sudo mysql -u root gatorbarter < makeUsers.sql
sudo mysql -u root gatorbarter < makeCategories.sql
sudo mysql -u root gatorbarter < makeItems.sql
sudo mysql -u root gatorbarter < makeItemImages.sql