import { useQuery } from "@tanstack/react-query";
import { getUserSessions } from "../../api/user";

export default function UserHistoryPanel({
  userId,
  onSelectSession
}){

  const {data,isLoading,error}=useQuery({

    queryKey:["user-sessions",userId],

    queryFn:()=>getUserSessions(userId),

    enabled:!!userId

  });

  if(!userId) return null;

  if(isLoading)
    return(
      <div className="text-gray-400">
        Loading session history...
      </div>
    );

  if(error)
    return(
      <div className="text-red-500">
        Failed to load sessions
      </div>
    );

  const sessions=data?.sessions || [];

  return(

    <div className="bg-gray-900 p-4 rounded-xl shadow-md mt-4">

      <h2 className="text-white text-lg mb-3">
        Session History
      </h2>

      {sessions.length===0 && (

        <div className="text-gray-400 text-sm">
          No sessions found
        </div>

      )}

      {sessions.map((session)=> (

        <div
          key={session.session_id}
          onClick={()=>onSelectSession(session.session_id)}
          className="bg-gray-800 p-2 rounded mb-2 cursor-pointer hover:bg-gray-700"
        >

          <div className="text-green-400 text-sm">
            {session.session_id}
          </div>

          <div className="text-gray-400 text-xs">
            {session.created_at}
          </div>

        </div>

      ))}

    </div>

  );

}