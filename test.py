import os

# open a pipe to "df ...", read from its stdout,
# strip the trailing \n, split it into a list on
# every \n, and put the results in 'data'
pipe = os.popen("df -Ph | " + "grep --color=never -E '^/dev' | " + "awk '{print $1, $2, $3, $4, $5, $6}'")
data = pipe.read().strip().split('/n')
pipe.close()

print data
