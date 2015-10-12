cd /c/root/intersect/datamanager
echo "Updating data..."
doit
echo "Copying data..."
cp -ruv /c/root/data/master/* /c/GDrive/NWU/data/
cp -ruv /c/root/data/master/* /c/root/workspace/data

cd /c/root/intersect/quantstrategies
echo "Creating Portfolios..."
doit
echo "Copying Portfolio data..."
cp -ruv /c/root/data/models/* /c/GDrive/NWU/Portfolio

echo "Archiving data..."
tar -cvzf /c/root/backup/`date +%Y-%m-%d`.tar.gz /c/root/data/

echo "Copying backup to NAS"
cp -ruv /c/root/backup/`date +%Y-%m-%d`.tar.gz /z/backup/data/`date +%Y-%m-%d`.tar.gz 