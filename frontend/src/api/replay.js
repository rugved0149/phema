import { api } from "./client";

export const getTimeline = async (entityType, entityId) => {
  const res = await api.get(
    `/correlation/replay/${entityType}/${entityId}`
  );
  return res.data;
};