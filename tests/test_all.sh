# Comprehensive test script for Stages 1-3
echo "Testing env var expansion:"
echo $HOME
echo "Testing stub commands:"
ls -la /var/log
cd ../tmp
echo "Testing error handling:"
invalid_command --flag
echo "Testing VFS navigation:"
ls /
cd /dir1
ls
echo "Exiting emulator..."
exit
