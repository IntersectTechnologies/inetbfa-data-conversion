cd /c/root/intersect/datamanager
echo "Running data tasks"
doit
echo "Copying data..."
cp -ruv /c/root/data/master/* /c/GDrive/NWU/data/
cp -ruv /c/root/data/master/* /c/root/workspace/data
echo "archiving data"
tar -cvzf /c/root/backup/`date +%Y-%m-%d`.tar.gz /c/root/data/

cp -ruv /c/root/data/models/* /c/GDrive/NWU/Portfolio