#!/bin/zsh
# only works on my environment. If there is interest, I can work on making it universal

start_loc=$(yq ".Settings.location" $HOME/.config/zman/config.yaml)

yq ".Settings.location = 'New York, NY'"

termshot -c "zman"
mv out.png images/zman.png

termshot -c "zman -d '06/08/2025'"
mv out.png images/date.png

termshot -c "zman -l 'Boston, MA'"
mv out.png images/location.png

yq ".Settings.location = '${start_loc}'"
