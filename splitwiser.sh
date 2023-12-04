#! /bin/sh
source .env

# Active time stop times (when a script should stop for the [night])
echo ""

echo ""
echo "----------------"
echo "Running SplitWiser!"
echo ""

sleep 1
echo "Pulling latest DB from Google Drive..."

python copier.py

echo "Done."
sleep 3
echo "Starting command-line application...\r\n"

python app.py

sleep 2
echo "Pushing new updates to DB in Google Drive..."

# python copier.py -l

sleep 1
echo "Done."