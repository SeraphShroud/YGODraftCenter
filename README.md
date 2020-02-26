## Dependencies
First install the following:
1) node.js        https://nodejs.org/en/
2) Python 3.7.6   https://www.python.org/downloads/
3) MongoDB 4.2.3  https://www.mongodb.com/download-center/community

Then in the directory you want the project in, `git clone https://github.com/SeraphShroud/ygodraftcenter.git`

Please install the dependencies in the requirements.txt before running
### `pip3 install -r requirements.txt`


## How to run

Currently there are 3 executable parts of this codebase.

# Front-end React API Retrieval Demo

Go to the src/client/ directory then run `npm start`
* Currently not working! You will need to remove the client/ directory and move all the files up to src/ as a workaround.

# Server-Client Python Demo

Go to src/server/ and run `python3 server.py`
Then on another terminal go to src/client/ and run `python3 client.py`

3 Clients will join a room that the server can show via `list` and `room #`

# API-Server Pytests

Go to src/server/tests and run `pytest`

This will run all the unit tests for the server side backend. It is recommeneded to install MongoDB Compass Community for a GUI of the database.
https://www.mongodb.com/download-center/compass

Once installed, enter `mongodb://localhost:27017` into the URL and you'll be able to see the databases and collections.


## npm Scripts Below

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.<br />
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.<br />
You will also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.<br />
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.<br />
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.<br />
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: https://facebook.github.io/create-react-app/docs/code-splitting

### Analyzing the Bundle Size

This section has moved here: https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size

### Making a Progressive Web App

This section has moved here: https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app

### Advanced Configuration

This section has moved here: https://facebook.github.io/create-react-app/docs/advanced-configuration

### Deployment

This section has moved here: https://facebook.github.io/create-react-app/docs/deployment

### `npm run build` fails to minify

This section has moved here: https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify
