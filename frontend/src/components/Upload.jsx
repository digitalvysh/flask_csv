import React from 'react'
import { FileUploader } from "react-drag-drop-files";

const Upload = () => {
    const handleChange = async (file) => {
        const formData = new FormData();
        formData.append("file", file);
        const jsonData = await fetch(process.env.REACT_APP_API + "/data", {
            method: "POST",
            body: formData,
        });

        const response = await jsonData.json();
        console.log(response);
    }
    return (
        <div>
            <FileUploader handleChange={handleChange} name="file" types={["CSV"]} />
        </div>
    )
}

export default Upload;