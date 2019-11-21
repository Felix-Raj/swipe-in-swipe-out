### Swipe In Swipe Out
Find your expected Swipe Out time. Default time expected in office is 8 hours.

### How to use

```bash
chmod +x siso.py
mv siso.py siso
# add (copy or move ) siso to a location which is already in PATH
# see PATH by executing echo $PATH
siso --si 09:40  # swipe in time
siso --ext 1:30  # extend out time by 1 hour 30 minutes
siso -o  # show me my expected out time

# if the script is being used to run some test on new features, supply the 
# -t flag with any command

# to change the hours working in office use option --iot
siso --iot 6:30 --si 09:30
# iot is only useful with si

siso -v
# show as much as details as possible
```
