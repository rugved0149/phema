import { useQuery } from "@tanstack/react-query";
import { api } from "../../api/client";

export default function UserSessionSummary({
  userId,
  sessionId
}) {

  const { data } = useQuery({

    queryKey:[
      "summary",
      userId,
      sessionId
    ],

    queryFn:async()=>{

      const res=await api.get(

        `/correlation/risk/${userId}/${sessionId}/session/${sessionId}`

      );

      return res.data;

    },

    enabled:
      !!userId &&
      !!sessionId

  });

  if(!data) return null;

  return(

    <div className="bg-gray-900 p-4 rounded-xl mt-4">

      <h2 className="text-xl text-white mb-3">
        Session Summary
      </h2>

      <div className="text-gray-300">

        Risk Score:
        <span className="ml-2 text-white font-bold">
          {data.risk_score}
        </span>

      </div>

      <div className="text-gray-300 mt-1">

        Attack Type:
        <span className="ml-2 text-purple-400">
          {data.attack_type}
        </span>

      </div>

      <div className="mt-3">

        <div className="text-gray-400">
          Reasons:
        </div>

        <ul className="list-disc ml-5 text-sm text-gray-300">

          {data.reasons?.map((r,i)=>(

            <li key={i}>
              {r}
            </li>

          ))}

        </ul>

      </div>

    </div>

  );

}