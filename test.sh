
echo forth_primitive.py:
echo -n "testing forth_primitive.py... "
python forth_primitive.py > forth_primitive.s
gcc -o forth_primitive forth_primitive.s
./forth_primitive
rm forth_primitive forth_primitive.s
echo " -> 77777"
echo done.

echo test.fth:
python forth.py test.fth > test.s
gcc test.s -o test
./test
rm test test.s

echo test2.fth:
python forth.py test2.fth > test2.s
gcc -c f.c
gcc f.o test2.s -o test2
./test2
rm test2 test2.s f.o

