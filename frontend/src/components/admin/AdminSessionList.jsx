import { useQuery } from "@tanstack/react-query";
import { api } from "../../api/client";
import RiskBadge from "../common/RiskBadge";

export default function AdminSessionList({
  userId,
  onSelectSession
}){

  const { data,isLoading,error }=useQuery({

    queryKey:["sessions",userId],

    queryFn:async()=>{

      const res=await api.get(
        `/admin/user/${userId}/sessions`
      );

      return res.data.sessions;

    },

    enabled:!!userId,

    refetchInterval:5000

  });

  if(!userId) return null;

  if(isLoading){
    return(
      <div className="text-gray-500">
        Loading sessions...
      </div>
    );
  }

  if(error){
    return(
      <div className="text-red-500">
        Failed to load sessions
      </div>
    );
  }

  const sessions=data||[];

  return(

    <div className="bg-white border p-4 rounded-xl shadow-sm">

      <h2 className="text-xl text-gray-800 mb-3">
        Sessions
      </h2>

      {sessions.length===0?(
        <div className="text-gray-500">
          No sessions found
        </div>
      ):(
        <div className="space-y-2">

          {sessions.map((s)=>(

            <div
              key={s.session_id}
              className="bg-gray-100 p-3 rounded cursor-pointer hover:bg-gray-200"
              onClick={()=>onSelectSession(
                s.session_id
              )}
            >

              <div className="flex justify-between items-center">

                <span className="text-gray-700 font-mono">
                  {s.session_id}
                </span>

                <div className="flex items-center gap-3">

                  <span className="text-gray-600 text-sm w-[48px] text-right font-mono">
                    {s.last_risk_score ?? 0}
                  </span>

                  <RiskBadge level={s.peak_risk_level ?? "LOW"}/>

                </div>

              </div>

              <div className="mt-2 text-xs text-gray-600 flex flex-wrap gap-4">

                <span>
                  Peak:
                  <span className="ml-1 font-mono text-yellow-600">
                    {s.peak_risk_score ?? 0}
                  </span>
                </span>

                <span>
                  Level:
                  <span className="ml-1 font-semibold text-red-600">
                    {s.peak_risk_level ?? "LOW"}
                  </span>
                </span>

                <span>
                  Time:
                  <span className="ml-1 font-mono">
                    {s.peak_risk_timestamp
                      ? new Date(
                          s.peak_risk_timestamp
                        ).toLocaleString()
                      : "N/A"}
                  </span>
                </span>

                <span>
                  Trend:
                  <span className="ml-1 font-semibold text-blue-600">
                    {s.risk_trend ?? "STABLE"}
                  </span>
                </span>

              </div>

            </div>

          ))}

        </div>
      )}

    </div>

  );

}