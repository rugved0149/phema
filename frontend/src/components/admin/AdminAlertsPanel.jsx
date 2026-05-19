import { useQuery } from "@tanstack/react-query";
import { api } from "../../api/client";

export default function AdminAlertsPanel(){

  const { data,isLoading,error }=useQuery({

    queryKey:["admin_alerts"],

    queryFn:async()=>{

      const res=await api.get(
        "/admin/alerts"
      );

      return res.data.alerts;

    },

    refetchInterval:5000

  });

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

    <div className="bg-red-900 border border-red-600 p-4 rounded-xl shadow-md">

      <h2 className="text-xl text-white mb-3">
        High Risk Alerts
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
              className="bg-red-800 p-3 rounded"
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