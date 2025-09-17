#!/bin/zsh

termshot -c "zman"
mv out.png images/zman.png

termshot -c "zman -d '2025-08-06'"
mv out.png images/date.png

termshot -c "zman -l 'Boston, MA'"
mv out.png images/location.png

