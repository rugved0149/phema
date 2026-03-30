import { useQuery } from "@tanstack/react-query";
import { api } from "../../api/client";

export default function AdminCampaignPanel(){

  const { data,isLoading }=useQuery({

    queryKey:["campaigns"],

    queryFn:async()=>{

      const res=await api.get(
        "/campaign/active"
      );

      return res.data;

    },

    refetchInterval:5000

  });

  if(isLoading){

    return(

      <div className="text-gray-400">
        Loading campaigns...
      </div>

    );

  }

  return(

    <div className="bg-gray-900 p-4 rounded-xl mt-6">

      <h2 className="text-xl text-white mb-3">

        Active Campaigns

      </h2>

      <div className="mb-4">

        <h3 className="text-purple-400">

          Phishing Campaigns

        </h3>

        {data.phishing_campaigns.map((c,i)=>(

          <div
            key={i}
            className="bg-gray-800 p-2 rounded mt-2"
          >

            <div className="text-yellow-400">

              {c.signal}

            </div>

            <div className="text-sm text-gray-400">

              Users affected:
              {c.users_affected}

            </div>

          </div>

        ))}

      </div>

      <div>

        <h3 className="text-red-400">

          File Campaigns

        </h3>

        {data.file_campaigns.map((c,i)=>(

          <div
            key={i}
            className="bg-gray-800 p-2 rounded mt-2"
          >

            <div className="text-yellow-400">

              {c.signal}

            </div>

            <div className="text-sm text-gray-400">

              Users affected:
              {c.users_affected}

            </div>

          </div>

        ))}

      </div>

    </div>

  );

}