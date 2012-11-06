VERSION="$(cat version.txt)"
TMP_DIR=$(mktemp -d jenkins.XXX)
mkdir $TMP_DIR/pypimirror-$VERSION
cp -r * $TMP_DIR/pypimirror-$VERSION
mkdir -p SOURCES
tar czvf SOURCES/pypimirror-$VERSION.tar.gz \
    --exclude=jenkins-rpm \
    --exclude=SOURCES \
    --exclude=SPECS \
    --exclude=RPMS \
    --exclude=SRPMS \
    --exclude=BUILD \
    --exclude=BUILDROOT \
    --exclude="*.rpm" \
    --exclude=pypimirror.spec \
    -C $TMP_DIR pypimirror-$VERSION
rm -rf $TMP_DIR
if [ -z "${BUILD_NUMBER}" ]; then BUILD_NUMBER='1'; fi
rpmbuild -ba --define="_topdir $PWD" --define="name pypimirror" --define="_tmppath $PWD/tmp" --define="ver $VERSION" --define "rel $BUILD_NUMBER" pypimirror.spec
