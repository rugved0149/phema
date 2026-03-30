import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { getRisk } from "../../api/risk";

export default function EntityInvestigation({
  userId,
  sessionId
}){

  const [entityId,setEntityId]=useState("");
  const [entityType,setEntityType]=useState("session");

  const { data,isLoading,error,refetch }=useQuery({

    queryKey:[
      "risk",
      userId,
      sessionId,
      entityType,
      entityId
    ],

    queryFn:()=>getRisk(
      userId,
      sessionId,
      entityType,
      entityId
    ),

    enabled:false

  });

  const handleSearch=()=>{

    if(!entityId||!userId||!sessionId)
      return;

    refetch();

  };

  return(

    <div className="bg-gray-900 p-4 rounded-xl shadow-md">

      <h2 className="text-xl font-semibold mb-4 text-white">
        Entity Investigation
      </h2>

      <div className="flex gap-2 mb-4">

        <select
          value={entityType}
          onChange={(e)=>
            setEntityType(e.target.value)
          }
          className="bg-gray-800 text-white px-2 py-1 rounded"
        >

          <option value="session">Session</option>
          <option value="user">User</option>
          <option value="ip">IP</option>
          <option value="file">File</option>

        </select>

        <input
          type="text"
          placeholder="Enter entity ID"
          value={entityId}
          onChange={(e)=>
            setEntityId(e.target.value)
          }
          className="flex-1 bg-gray-800 text-white px-3 py-1 rounded"
        />

        <button
          onClick={handleSearch}
          className="bg-blue-600 px-4 py-1 rounded"
        >
          Analyze
        </button>

      </div>

      {isLoading&&(
        <div className="text-gray-400">
          Analyzing...
        </div>
      )}

      {error&&(
        <div className="text-red-500">
          Failed to fetch risk data
        </div>
      )}

      {data&&(

        <div className="space-y-4">

          <div>
            <span className="text-gray-400">
              Risk Score:
            </span>

            <span className="text-white font-bold ml-2">
              {data.risk_score}
            </span>
          </div>

          <div>
            <span className="text-gray-400">
              Risk Level:
            </span>

            <span
              className={`font-bold ml-2 ${
                data.risk_level==="HIGH"
                  ?"text-red-500"
                  :data.risk_level==="MEDIUM"
                  ?"text-yellow-400"
                  :"text-green-400"
              }`}
            >
              {data.risk_level}
            </span>
          </div>

        </div>

      )}

    </div>

  );

}