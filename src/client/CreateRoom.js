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

    checkFileType = (event) => {
        let files = event.target.files 
        let err = ''
        const types = ['.ydk']
        if (types.every(type => files[0].type !== type)) {
            err += files[0].type + ' is not a supported format. Please upload a .ydk file.\n';
        }
      
        if (err !== '') {
            event.target.value = null
            console.log(err)
            return false; 
        }
        return true;
    }

    fileUploadHandler = event => {
        console.log(event.target.files[0])
        console.log(event.target.files[0].type)
        // Need to figure out how to check if extension is .ydk for validation
        // This does not work yet.
        // if (this.checkFileType(event)){
        //     this.setState({
        //         ydkFile: event.target.files[0]
        //     })
        // }
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
