import { useQuery } from "@tanstack/react-query";
import { api } from "../../api/client";
import RiskBadge from "../common/RiskBadge";

export default function UserSessionHistory({
  userId,
  onSelectSession
}){

  const { data,isLoading,error }=useQuery({

    queryKey:["user_sessions",userId],

    queryFn:async()=>{

      const res=await api.get(
        `/user/${userId}/sessions`
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
        Failed to load session history
      </div>
    );
  }

  const sessions=data||[];

  return(

    <div className="bg-white border p-4 rounded-xl shadow-sm">

      <h2 className="text-xl text-gray-800 mb-3">
        Session History
      </h2>

      {sessions.length===0?(
        <div className="text-gray-500">
          No previous sessions found
        </div>
      ):(
        <div className="space-y-2">

          {sessions.map((s)=>(

            <div
              key={s.session_id}
              className="bg-gray-100 p-3 rounded cursor-pointer hover:bg-gray-200 flex justify-between items-center"
              onClick={()=>onSelectSession(
                s.session_id
              )}
            >

              <span className="text-gray-700 font-mono">
                {s.session_id}
              </span>

              <div className="flex items-center gap-3">

                <span className="text-gray-600 text-sm w-[48px] text-right font-mono">
                  {s.risk_score}
                </span>

                <RiskBadge level={s.risk_level}/>

              </div>

            </div>

          ))}

        </div>
      )}

    </div>

  );

}