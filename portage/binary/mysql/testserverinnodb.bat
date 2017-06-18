echo "opening server database"
echo "#######################"

mysqld --defaults-file=C:/kde/download/svn/trunk/kdesupport/akonadi/server/src/storage/mysql-global.conf --datadir=C:/Users/p/data --shared-memory

echo "server should have been started!"