import { useQuery } from "@tanstack/react-query";
import { api } from "../../api/client";

export default function UserAdvicePanel({
  userId,
  sessionId
}) {

  const { data } = useQuery({

    queryKey: [

      "advice",
      userId,
      sessionId

    ],

    queryFn: async () => {

      const res=await api.get(

        `/advice/${userId}/${sessionId}`

      );

      return res.data;

    },

    enabled:
      !!userId &&
      !!sessionId,

    refetchInterval:5000

  });

  if(!data) return null;

  return (

    <div className="bg-gray-900 p-4 rounded-xl mt-4">

      <h2 className="text-xl text-white mb-3">
        Security Advice
      </h2>

      <div className="text-yellow-400 mb-2">

        Risk Level:
        <span className="ml-2">
          {data.risk_level}
        </span>

      </div>

      <ul className="list-disc ml-5 text-gray-300">

        {data.advice.map((a,i)=>(

          <li key={i}>
            {a}
          </li>

        ))}

      </ul>

    </div>

  );

}