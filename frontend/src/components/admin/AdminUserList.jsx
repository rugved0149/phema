import { useQuery } from "@tanstack/react-query";
import { api } from "../../api/client";

export default function AdminUserList({
  onSelectUser
}){

  const { data,isLoading,error }=useQuery({

    queryKey:["users"],

    queryFn:async()=>{

      const res=await api.get(
        "/admin/users"
      );

      return res.data.users;

    },

    refetchInterval:5000

  });

  if(isLoading){

    return(
      <div className="text-gray-400">
        Loading users...
      </div>
    );

  }

  if(error){

    return(
      <div className="text-red-500">
        Failed to load users
      </div>
    );

  }

  const users=data||[];

  return(

    <div className="bg-gray-900 p-4 rounded-xl">

      <h2 className="text-xl text-white mb-3">
        Users
      </h2>

      {users.length===0?(
        <div className="text-gray-400">
          No users found
        </div>
      ):(
        <div className="space-y-2">

          {users.map((u,i)=>(

            <div
              key={i}
              className="bg-gray-800 p-3 rounded cursor-pointer hover:bg-gray-700"
              onClick={()=>onSelectUser(u)}
            >

              <span className="text-green-400 font-mono">

                {u}

              </span>

            </div>

          ))}

        </div>
      )}

    </div>

  );

}