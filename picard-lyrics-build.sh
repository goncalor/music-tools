PLUGIN_NAME="lazy-lyrics"
TMP=$(mktemp -d -p .)
DIR="$TMP/$PLUGIN_NAME"
mkdir "$DIR"

cp lyrics.py "$DIR"
cp picard-lyrics.py "$DIR/__init__.py"
touch "$DIR/README"

pwd="$PWD"
cd "$TMP"
zip - "$PLUGIN_NAME"/* > "$pwd/$PLUGIN_NAME.zip"

cd "$pwd"
rm -rf "$TMP"
