import React from "react"
import axios from 'axios'
import { Link } from "react-router-dom";

class CreateRoom extends React.Component {
    constructor() {
        super()
        this.state = {
            userId: "testuser",
            ydkFile: null
        }
    }

    fileSelectedHandler = event => {
        this.setState({
            ydkFile: event.target.files[0]
        })
    }

    fileUploadHandler = async () => {
        console.log(this.state);
        var sendData = {
            userId: this.state.userId,
            ydkFile: this.state.ydkFile
        }
        const resp = await axios.post("http://localhost:9000/upload", sendData);
        const data = await resp.data
        console.log("Response: " + data);
        this.setState({
            cardInfoList: data
        })
    }

    render() {
        return (
            <div className="upload-container">
                <input type="file" onChange={this.fileSelectedHandler} />
                <button onClick={this.fileUploadHandler}>Upload</button>
            </div>

        )
    }
}


export default CreateRoom
