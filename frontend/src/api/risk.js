import { api } from "./client";

export const getRisk=async(
  userId,
  sessionId,
  entityType,
  entityId
)=>{

  const res=await api.get(

    `/correlation/risk/${userId}/${sessionId}/${entityType}/${entityId}`

  );

  return res.data;

};