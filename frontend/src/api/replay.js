import { api } from "./client";

export const getTimeline = async (userId, sessionId, entityType, entityId) => {
  const res = await api.get(
    `/correlation/replay/${userId}/${sessionId}/${entityType}/${entityId}`
  );
  return res.data;
};