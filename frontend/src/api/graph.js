import { api } from "./client";

export const getGraph = async (userId, sessionId, entityType, entityId) => {
  const res = await api.get(
    `/correlation/graph/${userId}/${sessionId}/${entityType}/${entityId}`
  );
  return res.data;
};