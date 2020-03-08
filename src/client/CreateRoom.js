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

    fileUploadHandler = event => {
        console.log(event.target.files[0])
        this.setState({
            ydkFile: event.target.files[0]
        })
    }

    onClickHandler = async () => {
        const data = new FormData()
        data.append('file', this.state.ydkFile)
        const resp = await axios.post("http://localhost:9000/upload", data);
        const respData = await resp.data
        console.log(respData)
    }

    render() {
        return (
            <div class="upload-container">
                <input type="file" name="file" onChange={this.fileUploadHandler} />
                <button type="button" class="btn btn-success btn-block" onClick={this.onClickHandler}>Upload</button>
            </div>

        )
    }
}


export default CreateRoom
