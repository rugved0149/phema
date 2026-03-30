import { api } from "./client";

export const getUserSessions=async(userId)=>{

  const res=await api.get(
    `/user/${userId}/sessions`
  );

  return res.data;

};