VERSION_INFO_LOCATION="muutils/__init__.py"
PUBLISH_BRANCH="main"
PYPI_TOKEN_FILE=".pypi-token"
LAST_VERSION_FILE=".lastversion"

# get version from init file
VERSION=$(grep -oP '__version__ = "\K.*?(?=")' $VERSION_INFO_LOCATION)
# get contents of $LAST_VERSION_FILE
LAST_VERSION=$(cat $LAST_VERSION_FILE)

# run tests, build everything
set -x
set -e

make check-format

make test

rm -rf build/
rm -rf dist/
rm -rf muutils.egg-info/

poetry build

# py -m build --wheel

# twine check dist/*

set +x

echo "done building!"
echo "pypi username: __token__"
echo "pypi token from '$PYPI_TOKEN_FILE' :"
cat $PYPI_TOKEN_FILE

echo ""
echo "current version is $VERSION, last auto-uploaded version is $LAST_VERSION"

# test that the version has been changed (make portable)
if [ "$VERSION" = "$LAST_VERSION" ]; then
	echo "python package $VERSION is the same as last published version $LAST_VERSION, exiting!"
	exit 1
fi

echo "enter the new version number if you want to upload to pypi and create a new tag"

read -p "confirm: " NEW_VERSION

# test that NEW_VERSION is the same as VERSION
if [ "$NEW_VERSION" != "$VERSION" ]; then
	echo "confirmation failed, exiting!"
	exit 1
fi

# assert that git is on the correct branch
if [ "$(git branch --show-current)" != $PUBLISH_BRANCH ]; then
	echo "git is not on the $PUBLISH_BRANCH branch, exiting!"
	exit 1
fi

# assert that git is clean
if [ -n "$(git status --porcelain)" ]; then
	echo "git is not clean, exiting!"
	exit 1
fi


set -x

echo "uploading!"

echo $NEW_VERSION > .lastversion
git add .lastversion
git commit -m "auto update to $NEW_VERSION"
git tag $NEW_VERSION
git push origin $NEW_VERSION
twine upload dist/*


