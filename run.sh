cd /c/root/intersect/datamanager
echo "Running data tasks"
doit
echo "Copying data..."
cp -ruv /c/root/data/master/* /c/Users/Niel/Google\ Drive/NWU/data/
cp -ruv /c/root/data/master/* /c/root/workspace/data
echo "archiving data"
tar -cvzf /c/root/backup/`date +%Y-%m-%d`.tar.gz /c/root/data/
