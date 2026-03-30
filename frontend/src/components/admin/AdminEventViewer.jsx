import { useQuery } from "@tanstack/react-query";
import { api } from "../../api/client";

export default function AdminEventViewer({
  userId,
  sessionId
}) {

  const { data,isLoading }=useQuery({

    queryKey:[
      "events",
      userId,
      sessionId
    ],

    queryFn:async()=>{

      const res=await api.get(

        `correlation/events/${userId}/${sessionId}`

      );

      return res.data.events;

    },

    enabled:
      !!userId &&
      !!sessionId

  });

  if(!userId || !sessionId)
    return null;

  if(isLoading){

    return(

      <div className="text-gray-400">
        Loading events...
      </div>

    );

  }

  const events=data||[];

  return(

    <div className="bg-gray-900 p-4 rounded-xl mt-6">

      <h2 className="text-xl text-white mb-3">

        Event Details

      </h2>

      <div className="max-h-96 overflow-y-auto space-y-2">

        {events.map((e,i)=>(

          <div
            key={i}
            className="bg-gray-800 p-3 rounded"
          >

            <div className="flex justify-between text-sm">

              <span className="text-purple-400">

                {e.module}

              </span>

              <span className="text-gray-400">

                {e.timestamp}

              </span>

            </div>

            <div className="text-white font-medium mt-1">

              {e.signal}

            </div>

            <div className="text-xs text-gray-400 mt-1">

              Severity: {e.severity}

            </div>

            {e.metadata && (

              <pre className="text-xs text-gray-300 mt-2 overflow-x-auto">

                {JSON.stringify(
                  e.metadata,
                  null,
                  2
                )}

              </pre>

            )}

          </div>

        ))}

      </div>

    </div>

  );

}