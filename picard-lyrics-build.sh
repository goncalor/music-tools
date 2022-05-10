TMP=$(mktemp -d -p .)
DIR="$TMP/lyrics"
mkdir "$DIR"

cp lyrics.py "$DIR"
cp picard-lyrics.py "$DIR/__init__.py"
touch "$DIR/README"

pwd="$PWD"
cd "$TMP"
zip - lyrics/* > "$pwd/lyrics.zip"

cd "$pwd"
rm -rf "$TMP"
