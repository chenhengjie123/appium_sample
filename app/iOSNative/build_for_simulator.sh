echo "remove build folder"
rm -rf ./build

echo "begin build .app for simulator"
xcodebuild -target ToDoList -sdk iphonesimulator -configuration Release

