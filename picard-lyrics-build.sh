PLUGIN_NAME="lazy-lyrics"
TMP=$(mktemp -d -p .)
DIR="$TMP/$PLUGIN_NAME"
mkdir "$DIR"

cp -v lyrics.py "$DIR"
cp -vr picard-lyrics/{__init__.py,MANIFEST.toml} "$DIR"
cp -v README.md "$DIR"

pwd="$PWD"
cd "$TMP"
zip - "$PLUGIN_NAME"/* > "$pwd/$PLUGIN_NAME.zip"

cd "$pwd"
rm -rf "$TMP"
