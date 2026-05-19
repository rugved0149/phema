import { useQuery } from "@tanstack/react-query";
import { api } from "../../api/client";

export default function UserAlertsPanel({

  userId

}){

  const { data,isLoading,error }=useQuery({

    queryKey:["user_alerts",userId],

    queryFn:async()=>{

      const res=await api.get(
        `/user/${userId}/alerts`
      );

      return res.data.alerts;

    },

    enabled:!!userId,

    refetchInterval:5000

  });

  if(!userId) return null;

  if(isLoading){

    return(
      <div className="text-gray-500">
        Loading alerts...
      </div>
    );

  }

  if(error){

    return(
      <div className="text-red-500">
        Failed to load alerts
      </div>
    );

  }

  const alerts=data||[];

  return(

    <div className="bg-yellow-900 border border-yellow-600 p-4 rounded-xl shadow-md mt-6">

      <h2 className="text-xl text-white mb-3">
        Your Alerts
      </h2>

      {alerts.length===0?(
        <div className="text-gray-300">
          No alerts
        </div>
      ):(
        <div className="space-y-2">

          {alerts.map((a,i)=>(

            <div
              key={i}
              className="bg-yellow-800 p-3 rounded"
            >

              <div className="text-sm font-semibold">

                {a.alert_type}

              </div>

              <div className="text-xs">

                {a.message}

              </div>

              <div className="text-xs text-gray-300">

                Session:
                {a.session_id}

              </div>

              <div className="text-xs text-gray-400">

                {new Date(
                  a.timestamp
                ).toLocaleString()}

              </div>

            </div>

          ))}

        </div>
      )}

    </div>

  );

}