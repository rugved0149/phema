import { useState } from "react";
import axios from "axios";
import UserResultPanel from "./UserResultPanel";
import { uploadFile } from "../../api/client";

export default function UserScanPanel({ userId, sessionId }) {

  const [url,setUrl]=useState("");
  const [text,setText]=useState("");
  const [file,setFile]=useState(null);
  const [result,setResult]=useState(null);
  const [loading,setLoading]=useState(false);

  const handleFileChange=(e)=>{
    setFile(e.target.files[0]);
  };

const runScan=async()=>{

  if(!sessionId){
    alert("Create session first");
    return;
  }

  if(!url && !text && !file){
    alert("Provide URL, text or file");
    return;
  }

  setLoading(true);

  try{

    let uploadedFilePath=null;

    // --- Upload File First ---

    if(file){

      const uploadRes=await uploadFile(file);

      uploadedFilePath=uploadRes.file_path;

    }

    // --- Build Scan Payload ---

    const payload={

      user_id:userId,
      session_id:sessionId,
      entity_id:sessionId,
      entity_type:"session",

      url:url || null,
      text:text || null,

      file_path:uploadedFilePath,

      session_context:{
        ip:"127.0.0.1"
      }

    };

    const res=await axios.post(
      "http://127.0.0.1:8000/phema/scan",
      payload
    );

    setResult(res.data);

  }catch(err){

    console.error(err.response?.data || err.message);
    alert("Scan failed");

  }finally{

    setLoading(false);

  }

};

  return(

    <div className="bg-gray-900 p-4 rounded-xl shadow-md">

      <h2 className="text-xl font-semibold mb-4 text-white">
        Scan Interface
      </h2>

      <div className="text-green-400 text-sm mb-3">
        Active Session:
        <span className="ml-2 font-mono">
          {sessionId}
        </span>
      </div>

      <input
        type="text"
        placeholder="Enter URL"
        value={url}
        onChange={(e)=>setUrl(e.target.value)}
        className="w-full bg-gray-800 text-white px-3 py-2 rounded mb-3"
      />

      <textarea
        placeholder="Enter Text"
        value={text}
        onChange={(e)=>setText(e.target.value)}
        className="w-full bg-gray-800 text-white px-3 py-2 rounded mb-3"
      />

      <input
        type="file"
        onChange={handleFileChange}
        className="mb-3 text-white"
      />
      {file && (
        <div className="text-sm text-gray-400 mb-2">
          Selected: {file.name}
        </div>
      )}

      <button
        onClick={runScan}
        disabled={loading}
        className="bg-purple-600 px-4 py-2 rounded w-full"
      >
        {loading?"Running Scan...":"Run Scan"}
      </button>

      {result && (
        <div className="mt-4 bg-gray-800 p-3 rounded">
          <div className="text-green-400">
            Scan Executed
          </div>
        </div>
      )}

      {sessionId && (
        <UserResultPanel
          userId={userId}
          sessionId={sessionId}
          entityId={sessionId}
          entityType="session"
        />
      )}

    </div>

  );

}