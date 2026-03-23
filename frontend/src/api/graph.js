import { api } from "./client";

export const getGraph = async (entityType, entityId) => {
  const res = await api.get(
    `/correlation/graph/${entityType}/${entityId}`
  );
  return res.data;
};