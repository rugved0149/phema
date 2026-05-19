import { api } from "./client";

export const getUserSessions=async(userId)=>{

  const res=await api.get(

    `/user/${userId}/sessions`

  );

  return res.data;

};


export const createUserSession=async(
  userId,
  sessionId
)=>{

  const res=await api.post(

    `/user/${userId}/session`,

    null,

    {

      params:{
        session_id:sessionId
      }

    }

  );

  return res.data;

};